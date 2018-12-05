"""
App routes
"""

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import APP #pylint: disable=cyclic-import
from app import DB
from app.forms import LoginForm, RegistrationForm
from app.models import User

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
@login_required
def index():
    """
    index
    """
    return render_template('index.html', title="Home", posts=POSTS)

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """
    login
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title="Sign in", form=form)

@APP.route('/logout')
def logout():
    """
    log out
    """
    logout_user()
    return redirect(url_for('index'))

@APP.route('/register', methods=['GET', 'POST'])
def register():
    """
    register
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        DB.session.add(user)
        DB.session.commit()
        flash('Congratulations, your are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

