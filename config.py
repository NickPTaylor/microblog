"""
Configuration
"""
import os


class Config():
    """
    config
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
