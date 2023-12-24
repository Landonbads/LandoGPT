# imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# constant for database name
DB_NAME = 'database.db'
# declare database name
db = SQLAlchemy()

# create login manager via flask_login
login_manager = LoginManager()

# initialize secret key and create flask application
def create_app():
    app = Flask(__name__)
    # config for flask app using sqlite.
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///.{DB_NAME}'
    app.config['SECRET_KEY'] = 'mele kalikimaka'

    # initialize database
    db.init_app(app)


    login_manager.init_app(app)

    #need to import and register blueprints
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    # import User model from models.py
    from .models import User
    with app.app_context():
        db.create_all()


    return app