import os

from flask import Flask, render_template, redirect, url_for


from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from redis import Redis

from forms import AgentForm, Agent

app = Flask(__name__)

#security
app.config['SECRET_KEY'] = '94a02f87629b69284e7d566f18ff9eba'

#database
app.config['MONGODB_SETTINGS'] = {
    'db'        : os.environ['MONGO_DATABASE'],
    'host'      : os.environ['MONGO_HOST'],
    'username'  : os.environ['MONGO_USERNAME'],
    'password'  : os.environ['MONGO_PASSWORD']
}


mongo_db = MongoEngine(app=app)

redis = Redis(host='redis', port=6379)


@app.route('/')
def hello_world():
    redis.incr('hits')
    count = int(redis.get('hits'))
    return f"Visits: {count}. Andrew is very lucky to have met Lili, she is the first woman that has appreciated me."

@app.route('/login/', methods = ["POST"])
def login(request):
    form = AgentForm(request.POST)
    if request.method == 'POST' and form.validate():
        body = request.get_json()
        agent = Agent(**body).save()
        return redirect(url_for('/<id>/groups'), code=302)
        #return a redirect

    return render_template("login.html", title="Register", form=AgentForm)

@app.route('/<id>/groups')
def groups(request, methods = ['POST']):
    pass

@app.route('/<id>/groups/new')
def new_group(request, methods = ['POST']):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')
