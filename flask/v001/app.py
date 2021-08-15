import os

from flask import (Flask,
                   render_template,
                   redirect,
                   url_for,
                   request,
                   session)

from flask_mongoengine import MongoEngine

from models.forms import Agent, OrganizationForm, Organization

app = Flask(__name__)

app.config['SECRET_KEY'] = '94a02f87629b69284e7d566f18ff9eba'

app.config['MONGODB_SETTINGS'] = {
    'db': os.environ['MONGO_DATABASE'],
    'host': os.environ['MONGO_HOST'],
    'username': os.environ['MONGO_USERNAME'],
    'password': os.environ['MONGO_PASSWORD']
}

mongo_db = MongoEngine(app=app)
# security

#Register views

from views.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from views.agent import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from views.orgs import orgs as org_blueprint
app.register_blueprint(org_blueprint)





"""

Organization routes to view and create.

"""




if __name__ == '__main__':
    app.run(host='0.0.0.0')
