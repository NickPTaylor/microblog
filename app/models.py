"""
models module
"""
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import DB, LOGIN

@LOGIN.user_loader
def load_user(id):
    """
    load user
    """
    return User.query.get(int(id))

class User(UserMixin, DB.Model):
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

    def set_password(self, password):
        """
        set password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        check password
        """
        return check_password_hash(self.password_hash, password)

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
