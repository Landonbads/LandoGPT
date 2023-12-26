# routes for authentication

from flask import Blueprint, render_template,request,flash, redirect, url_for
from .models import User
from .models import db
from sqlalchemy.exc import IntegrityError
import bcrypt
from flask_login import login_user, logout_user, login_required
from website import login_manager


# create blueprint for login/signup authentication
auth = Blueprint("auth",__name__)

# configure where unauthenticated user should be redirected if trying to access dashboard
login_manager.login_view = '/login'

# sign up route, allows for post and get requests
@auth.route('/sign-up',methods=['POST','GET'])
def sign_up():
    # retrive data from post request
    if request.method=='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        # hash password before storing in database
        hashed_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        
        # flash an error if email or password aren't formatted correctly
        if len(email) < 7:
            flash('Email not formatted correctly!', 'danger')
        elif len(password) < 7:
            flash('Password should be at least 7 characters!', 'danger')
        elif len(username) < 2:
            flash('First name should be at least 1 character!','danger')
        else:
            # try catch to handle integrity error (if email already exists in database)
            try:
                # create user with username,email, and hashed password given via request
                user = User(
                    username=username,
                    email=email,
                    password=hashed_password
                )  
                
                # add user to database
                db.session.add(user)
                # commit changes
                db.session.commit()
                # flash a message to notify user of successful account creation
                flash('Account successfully created!','success')
            except IntegrityError:
                flash('Email already signed up!', 'danger')


    return render_template("signup.html")

@login_manager.user_loader
def load_user(user_id):
    # Fetch user object from database via user ID
    return User.query.get(user_id)


# login route, allows for post and get requests
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # fetch email and password of form input
        email = request.form.get('email')
        password = request.form.get('password')

        # check if email is in database
        user = User.query.filter_by(email=email).first() # returns user

        # check if user found and if password matches
        if user and bcrypt.checkpw(password.encode(),user.password):
            # login the user and redirect to user dashboard
            login_user(user,remember=True)
            return redirect(url_for('views.dashboard'))
        else:
            flash("Incorrect email or password!")
            return render_template("login.html")
    else:
        # get request, re-render page
        return render_template("login.html")

# simple logout route. 
@auth.route('/logout')
@login_required # only can access if logged in
def logout():
    logout_user() # logout user with flask_login
    flash('Successfully logged out.')
    return redirect(url_for('auth.login')) # redirect to login page
