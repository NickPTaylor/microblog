"""
Microblog App
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from flask import Flask
from config import Config

APP = Flask(__name__)
APP.config.from_object(Config)
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)
LOGIN = LoginManager(APP)
LOGIN.login_view = 'login'

from app import routes, models  #pylint: disable=wrong-import-position
