import os


class DefaultConfig(object):
    DEBUG = False
    SECRET_KEY = "94a02f87629b69284e7d566f18ff9eda"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/development.db"


class TestConfig(DefaultConfig):
    DEBUG = True
    SECRET_KEY = "94a02f87629b69284e7d566f18ff9esa"
    TESTING = True
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/testing.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    CORS_HEADERS = "Access-Control-Allow-Origin"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(DefaultConfig):
    # from docker
    SQLALCHEMY_DATABASE_URI = "sqlite://root:root@data/main"
