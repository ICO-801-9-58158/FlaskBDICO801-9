import os 

class Config(object):
    SECRET_KEY = "claveSecreta"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///escuela.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False