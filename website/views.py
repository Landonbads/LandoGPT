from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from openai import OpenAI
from .models import Credits
import stripe

views = Blueprint('views',__name__)

client = OpenAI()
conversation_context = [] # history of questions and answers of chat
messages = []

def get_response(conversation_context, prompt):
    global messages
    client.api_key = current_app.config['OPEN_API_KEY'] # configure OpenAI
    messages = [] # messages list to send in openai api post request 

    for question, answer in conversation_context: # loop through previous questions and answers and add the context
        messages.append({"role": "user", "content": question})
        messages.append({"role": "assistant", "content": answer})
    
    messages.append({"role": "user", "content": prompt}) # append new prompt/question

    response = client.chat.completions.create(
        model='gpt-4-1106-preview',
        messages=messages,
    )

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
    global messages
    global conversation_context
    load_credits = Credits.query.filter_by(user_id=current_user.id).first() # load credits from user
    if request.method == 'POST' and len(request.form) == 1: # check length to make sure it's the send message button
        prompt = request.form.get('prompt')
        response = get_response(conversation_context, prompt)
        messages.append({"role": "assistant", "content": response})
        conversation_context.append((prompt, response)) # add question and response to context
    
    elif request.method == 'POST' and len(request.form) > 1: # when clear conversation button is clicked
        messages = []
        conversation_context = []
    
    return render_template("dashboard.html",messages=messages,credits=load_credits.amount)


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
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

@views.route('/thankyou',methods=['GET'])
@login_required
def thankyou():
    load_credits = Credits.query.filter_by(user_id=current_user.id).first() # load credits from user
    return render_template("thankyou.html",credits = load_credits.amount)