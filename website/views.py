from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

views = Blueprint('views',__name__)

@views.route('/',methods=['POST','GET'])
def home():
    # if user is not authenticated redirect to sign up page
    if not current_user.is_authenticated:
        return redirect(url_for('auth.sign_up'))
    # if user is authenticated redirect to user dashboard
    else:
        return redirect(url_for('auth.dashboard'))
