from flask import Blueprint, render_template, request,flash

# create blueprint for login/signup authentication
auth = Blueprint("auth",__name__)

# sign up route, allows for post and get requests
@auth.route('/sign-up',methods=['POST','GET'])
def sign_up():
    # retrive data from post request
    if request.method=='POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password = request.form.get('password')
        
        # flash an error if email or password aren't formatted correctly
        if len(email) < 7:
            flash('Email not formatted correctly!', 'danger')
        elif len(password) < 7:
            flash('Password should be at least 7 characters!', 'danger')
        elif len(firstname) < 2:
            flash('First name should be at least 1 character!','danger')
        else:
            flash('Sser account created!', 'success')

    return render_template("signup.html")

# login route, allows for post and get requests
@auth.route('/login')
def login():
    return render_template("login.html")

# simple logout route
@auth.route('/logout')
def logout():
    return render_template("logout.html")
