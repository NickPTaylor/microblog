"""
models module
"""
from datetime import datetime
from app import DB


class User(DB.Model):
    """
    user model
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), index=True, unique=True)
    email = DB.Column(DB.String(120), index=True, unique=True)
    password_hash = DB.Column(DB.String(128))
    posts = DB.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(DB.Model):
    """
    post model
    """
    id = DB.Column(DB.Integer, primary_key=True)
    body = DB.Column(DB.String(140))
    timestamp = DB.Column(DB.DateTime, index=True, default=datetime.utcnow)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
