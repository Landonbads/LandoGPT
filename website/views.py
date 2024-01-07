from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from flask_login import current_user, login_required
from openai import OpenAI
from .models import Credits, User
from .models import db
import stripe

views = Blueprint('views',__name__)

client = OpenAI()

def get_response(conversation_context, prompt):
    user = User.query.get(current_user.id) # fetch current user
    user_credits = Credits.query.filter_by(user_id=current_user.id).first() # fetch user credits
    TOKEN_COST_PER_1K = .06
    client.api_key = current_app.config['OPEN_API_KEY'] # configure OpenAI
    
    user.messages = [] 

    for prompt_and_response in conversation_context: # loop through previous questions and answers and add the context
        user.messages.append({"role": "user", "content": prompt_and_response["prompt"]})
        user.messages.append({"role": "assistant", "content": prompt_and_response["response"]})
    
    user.messages.append({"role": "user", "content": prompt}) # append new prompt/question
    db.session.commit()

    response = client.chat.completions.create(
        model='gpt-4-1106-preview',
        messages=user.messages,
    )

    token_usage = response.usage.total_tokens # total tokens used, including both prompt and response
    user_credits.amount -= (token_usage / 1000) * TOKEN_COST_PER_1K # calculate and deduct cost of prompt+response
    db.session.commit() # commit changes to database

    return response.choices[0].message.content # returns content of response


@views.route('/',methods=['POST','GET'])
def home():
    if not current_user.is_authenticated: # if user is not authenticated redirect to sign up page
        return redirect(url_for('auth.sign_up'))
    else: # if user is authenticated redirect to user dashboard
        return redirect(url_for('views.dashboard')) 


# dashboard route for logged in users
@views.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    user = User.query.get(current_user.id) # fetch current user
    load_credits = Credits.query.filter_by(user_id=current_user.id).first() # load credits from user
    if request.method == 'POST' and len(request.form) == 1: # check if message or clear
        if load_credits.amount > 0: # check if user has enough credits
            prompt = request.form.get('prompt')
            response = get_response(user.conversation_context, prompt)
            user.messages.append({"role": "assistant", "content": response})
            user.conversation_context.append({"prompt":prompt, "response":response}) # add question and response to context
            db.session.commit()
            print("test1")
            print(user.messages)
        else:
            flash('Not enough credits!', 'danger') # flash error message if user doesn't have enough credits
    elif request.method == 'POST' and len(request.form) > 1: # when clear conversation button is clicked
        user.messages = []
        user.conversation_context = []
        db.session.commit()

    print("test2")
    print(user.messages)
    return render_template("dashboard.html",messages=user.messages,credits=load_credits.amount)


@views.route('/stripe_pay')
@login_required
def stripe_pay():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1OTTkxBwvJKEtU3uyxm4mpyp',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('views.thankyou', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('views.dashboard', _external=True),
        metadata={'user_id': current_user.id}
    )
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': current_app.config['STRIPE_PUBLIC_KEY']
    }

@views.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = current_app.config['ENDPOINT_SECRET']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        amount_total = session['amount_total']
        conversion_rate = 100.0  # stripe returns amount in cents, need to convert
        credits_purchased = amount_total / conversion_rate

        # update user credits
        user_credits = Credits.query.filter_by(user_id=user_id).first()
        if user_credits:
            user_credits.amount += credits_purchased
        db.session.commit()

    return {}

@views.route('/thankyou',methods=['GET'])
@login_required
def thankyou():
    load_credits = Credits.query.filter_by(user_id=current_user.id).first()
    return render_template("thankyou.html",credits = load_credits.amount)