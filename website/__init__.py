from flask import Flask

# initialize secret key and create flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mele kalikimaka'

    #need to import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    return app