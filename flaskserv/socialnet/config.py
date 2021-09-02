import os

class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = '94a02f87629b69284e7d566f18ff9eda'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/development.db'


class TestConfig(DefaultConfig):
    DEBUG = True
    TESTING = True
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/testing.db'

class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class ProductionConfig(DefaultConfig):
    #from docker
    SQLALCHEMY_DATABASE_URI = 'sqlite://root:root@data/main'

