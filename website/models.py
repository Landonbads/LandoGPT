from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000))
    email = db.Column(db.String(1000),unique=True)
    messages = db.Column(JSON)
    conversation_context = db.Column(JSON)
    password = db.Column(db.Text)
    credits = db.relationship('Credits')

class Credits(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))