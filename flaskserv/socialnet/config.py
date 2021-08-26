import os

class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = '94a02f87629b69284e7d566f18ff9eba'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'


class TestConfig(DefaultConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'

class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class ProductionConfig(DefaultConfig):
    #from docker
    SQLALCHEMY_DATABASE_URI = 'sqlite://root:root@db/main'
