"""
App routes
"""

from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import APP #pylint: disable=cyclic-import
from app import DB
from app.forms import LoginForm, RegistrationForm, EditProfileForm
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

@APP.before_request
def before_request():
    """
    stuff to do before request
    :return:
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        DB.session.commit()

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

@APP.route('/user/<username>')
@login_required
def user(username):
    """
    user
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@APP.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    edit profile
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        DB.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
