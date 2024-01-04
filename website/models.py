from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(250),unique=True)
    password = db.Column(db.String(255))
    credits = db.relationship('Credits')

class Credits(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

# tbd MessageHistory object