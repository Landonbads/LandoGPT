# routes for authentication

from flask import Blueprint, render_template,request,flash, redirect, url_for
from .models import User
from .models import db

# create blueprint for login/signup authentication
auth = Blueprint("auth",__name__)

# sign up route, allows for post and get requests
@auth.route('/sign-up',methods=['POST','GET'])
def sign_up():
    # retrive data from post request
    if request.method=='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # flash an error if email or password aren't formatted correctly
        if len(email) < 7:
            flash('Email not formatted correctly!', 'danger')
        elif len(password) < 7:
            flash('Password should be at least 7 characters!', 'danger')
        elif len(username) < 2:
            flash('First name should be at least 1 character!','danger')
        else:
            # create user with username,email, and password given via request
            user = User(
                username=username,
                email=email,
                password=password
            )   
            # add user to database
            db.session.add(user)
            # commit changes
            db.session.commit()
            return redirect(url_for('mel'))
    # if not registering user, just reload page
    else:
        return render_template("signup.html")

@auth.route("/users",)
def user_list():
    users = db.session.execute(db.select(User.email)).scalars().all()
    return render_template("home.html",emails=users)


# login route, allows for post and get requests
@auth.route('/login')
def login():
    return render_template("login.html")

# simple logout route
@auth.route('/logout')
def logout():
    return render_template("logout.html")
