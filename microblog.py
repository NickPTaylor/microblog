"""
Micro-blog App
"""

from app import app, db # pylint: disable=unused-import
from app.models import User, Post
from app import cli

@app.shell_context_processor
def make_shell_context():
    """
    make shell context
    """
    return {'DB': db, 'User': User, 'Post': Post}
