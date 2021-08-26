from flask import Flask

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from .config import DevelopmentConfig






login_manager = LoginManager()
login_manager.login_view = 'auth.login'


db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)


    from .auth.views import auth_bp
    from .landing.views import landing_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(landing_bp)

    db.create_all(app=app)

    return app



from .auth.model import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

