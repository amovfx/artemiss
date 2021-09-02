"""

App factory for a basic social net.

"""

from flask import Flask

from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav import Nav, register_renderer

from .config import DevelopmentConfig
from .nav import navbar

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'




db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    """

    Flask factory app.

    :param config_class:
        The class appropriate for the stage of production
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)


    login_manager.init_app(app)

    Bootstrap(app=app)
    nav = Nav(app=app)
    register_renderer(app=app,
                      id='bootstrap',
                      renderer=BootstrapRenderer)
    nav.register_element("main_nav_bar", navbar)


    from .auth.views import auth_bp
    from .landing.views import landing_bp
    from .tribes.views import tribes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(landing_bp)
    app.register_blueprint(tribes_bp)

    db.create_all(app=app)

    return app



from .models import User

@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

