"""
Microblog App
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

APP = Flask(__name__)
APP.config.from_object(Config)
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)

from app import routes, models  #pylint: disable=wrong-import-position
