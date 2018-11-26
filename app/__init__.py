"""
Microblog App
"""

from flask import Flask

APP = Flask(__name__)

from app import routes  #pylint: disable=wrong-import-position
