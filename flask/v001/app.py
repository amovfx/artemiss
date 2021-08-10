import os

from flask import Flask, render_template, redirect, url_for, request


from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from redis import Redis

from forms import Agent

app = Flask(__name__)





@app.route('/')
def hello_world():
    return "Welcome!"

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        agent = Agent()
        print(request.form['email'])
        print(request.form['password'])
        agent.email = request.form['email']
        agent.password = request.form['password']
        agent.save()
        print(agent)
        return agent.__repr__()

    return render_template("login.html", title="Register")



if __name__ == '__main__':
    # security
    app.config['SECRET_KEY'] = '94a02f87629b69284e7d566f18ff9eba'

    # database
    try:
        app.config['MONGODB_SETTINGS'] = {
            'db': os.environ['MONGO_DATABASE'],
            'host': os.environ['MONGO_HOST'],
            'username': os.environ['MONGO_USERNAME'],
            'password': os.environ['MONGO_PASSWORD']
        }

        mongo_db = MongoEngine(app=app)

        redis = Redis(host='redis', port=6379)


    except KeyError:
        app.config['MONGODB_SETTINGS'] = {
            'db': 'user_db',
            'host': '0.0.0.0:27017',
            'username': 'flask_user',
            'password': 'flask_user_password'
        }

        mongo_db = MongoEngine(app=app)

    app.run(host='0.0.0.0')
