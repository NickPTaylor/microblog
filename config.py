"""
Configuration
"""
import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
    config
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Data base settings.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail server settings.
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # Pagination
    POSTS_PER_PAGE = 3

    # Languages
    LANGUAGES = ['en', 'es']

    # Services.
    YANDEX_TRANSLATOR_KEY = os.environ.get('YANDEX_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # Worker server.
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
