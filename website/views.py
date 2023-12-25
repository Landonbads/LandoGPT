from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from openai import OpenAI
import os
import requests
import json

views = Blueprint('views',__name__)

client = OpenAI() # create openai client
headers = {'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}'} # grab api key from .env file


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
        data = {
            "model": "gpt-4-1106-preview",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions",headers=headers,json=data)
        if response.status_code==200:
            print(response.json()['choices'][0]['message']['content']) # print out content of gpt response
    return render_template("dashboard.html")
