"""
App routes
"""

from flask import render_template
from app import APP #pylint: disable=cyclic-import

USER={'username': 'Nick'}

POSTS=[
    {
        'author': {'username': 'Laura'},
        'body': 'Beautiful day in Crawley'
    },
    {
        'author': {'username': 'Nick'},
        'body' : 'Work is a den of cunts...'
    },
    {
        'author': {'username': 'Laura'},
        'body': 'Why?'
    },
    {
        'author': {'username': 'Nick'},
        'body' : 'Coz I said so.'
    }
]

@APP.route('/')
@APP.route('/index')


def index():
    """
    index
    """
    return render_template('index.html', title='Home', user=USER, posts=POSTS)
