"""
Micro-blog App
"""

from app import create_app, db, cli # pylint: disable=unused-import
from app.models import User, Post

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    """
    make shell context
    """
    return {'DB': db, 'User': User, 'Post': Post}
