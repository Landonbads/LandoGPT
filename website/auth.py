from flask import Blueprint, render_template


auth = Blueprint("auth",__name__)


@auth.route('/sign-up')
def sign_up():
    return "<h1>sign-up</h1>"

@auth.route('/login')
def login():
    return "<h1>login</h1>"

@auth.route('/logout')
def logout():
    return "<h1>logout</h1>"
