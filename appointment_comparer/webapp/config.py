from os import environ
from os.path import join, dirname

from dotenv import load_dotenv

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'change_this_in_env_file'


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class ProductionConfig(Config):
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECRET_KEY = environ["SECRET_KEY"]
