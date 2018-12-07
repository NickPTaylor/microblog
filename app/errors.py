"""
Module for handling error.
"""

from flask import render_template
from app import APP, DB

@APP.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@APP.errorhandler(500)
def internal_error(error):
    DB.session.rollback()
    return render_template('500.html'), 500
