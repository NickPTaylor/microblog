"""
models module
"""
from datetime import datetime
from time import time
from hashlib import md5

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt

from app import APP, DB, LOGIN

@LOGIN.user_loader
def load_user(id):
    """
    load user
    """
    return User.query.get(int(id))

followers = DB.Table('followers',\
    DB.Column('follower_id', DB.Integer, DB.ForeignKey('user.id')),
    DB.Column('followed_id', DB.Integer, DB.ForeignKey('user.id')),
)

class User(UserMixin, DB.Model):
    """
    user model
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(64), index=True, unique=True)
    email = DB.Column(DB.String(120), index=True, unique=True)
    password_hash = DB.Column(DB.String(128))
    posts = DB.relationship('Post', backref='author', lazy='dynamic')
    about_me = DB.Column(DB.String(140))
    last_seen = DB.Column(DB.DateTime, default=datetime.utcnow)
    followed = DB.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=DB.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

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

    def avatar(self, size):
        """
        get avatar
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        url_fmt = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'
        return url_fmt.format(digest, size)

    def follow(self, user):
        """
        follow user
        """
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        """
        unfollow user
        """
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        """
        is this user following user
        """
        return self.followed.\
            filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            APP.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, APP.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


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
