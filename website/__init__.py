# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import path
import os

load_dotenv() # load .env variables
DB_NAME = 'database.db' # constant for database name
db = SQLAlchemy() # declare database name
login_manager = LoginManager() # create login manager via flask_login

def create_app(): # initialize secret key and create flask application

    app = Flask(__name__)
    # config for flask app using sqlite.
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')
    app.config['STRIPE_PUBLIC_KEY'] = os.environ.get('STRIPE_PUBLIC_KEY')
    app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')
    app.config['OPEN_API_KEY'] = os.environ.get('OPENAI_API_KEY')
    app.config['ENDPOINT_SECRET'] = os.environ.get('ENDPOINT_SECRET')
    db.init_app(app)# initialize database

    login_manager.init_app(app)

    # need to import and register blueprints
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')