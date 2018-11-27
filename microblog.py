"""
Micro-blog App
"""

from app import APP, DB # pylint: disable=unused-import
from app.models import User, Post

@APP.shell_context_processor
def make_shell_context():
    return {'DB': DB, 'User': User, 'Post': Post}
