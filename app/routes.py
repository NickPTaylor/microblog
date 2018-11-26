"""
App routes
"""

from flask import render_template, flash, redirect, url_for
from app import APP #pylint: disable=cyclic-import
from app.forms import LoginForm

USER = {'username': "Nick"}

POSTS = [
    {
        'author': {'username': "Laura"},
        'body': "Beautiful day in Crawley"
    },
    {
        'author': {'username': "Nick"},
        'body' : "Work is a den of cunts..."
    },
    {
        'author': {'username': "Laura"},
        'body': "Why?"
    },
    {
        'author': {'username': "Nick"},
        'body' : "Coz I said so."
    }
]

@APP.route('/')
@APP.route('/index')
def index():
    """
    index
    """
    return render_template('index.html', title="Home", user=USER, posts=POSTS)

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    login
    """
    form = LoginForm()
    if form.validate_on_submit():
        msg = 'Login requested for user {}, remember_me={}'
        flash(msg.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign in", form=form)
