from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from openai import OpenAI
import os
import json

views = Blueprint('views',__name__)


client = OpenAI()
client.api_key = os.environ.get('OPENAI_API_KEY') # configure OpenAI
conversation_context = [] # history of questions and answers of chat

def get_response(conversation_context, prompt):
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
        return redirect(url_for('auth.dashboard')) 


# dashboard route for logged in users
@views.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        response = get_response(conversation_context, prompt)
        conversation_context.append((prompt, response)) # add question and response to context

    return render_template("dashboard.html")

@views.route('/delete-conversation',methods=['POST'])
@login_required
def delete_conversation():
    global conversation_context
    conversation_context = []
