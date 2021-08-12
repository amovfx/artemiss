import os

from flask import Flask, render_template, redirect, url_for, request, session


from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from redis import Redis

from forms import Agent, OrganizationForm, Organization

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




@app.route('/')
def hello_world():
    return render_template("sidebar.html", test = "Very Nice!")

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        agent = Agent(**request.form)
        agent.save()
        session['id'] = agent.id
        return redirect(url_for('groups', id=agent.id))

    return render_template("agents/agent_login.html", title="Login")

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == 'POST':
        return redirect(url_for('login'))

    return render_template("agents/agent_create.html", title="Register")



@app.route('/groups/<id>', methods = ["GET", "POST"])
def groups(id):
    if request.method == 'POST':
        pass
        #make a propert template
    return f"Agent: {id} is logged in"

@app.route('/orgs/', methods = ["GET", "POST"])
def orgs():
    return render_template("organization/organization_layout.html",
                           orgs=Organization.objects())


@app.route('/orgs/new/', methods = ["GET", "POST"])
def neworg():
    form = OrganizationForm()
    if request.method == 'POST':
        print ("POSTING:")
        data = Organization()
        data.name = request.form["name"]
        data.description = request.form["description"]
        data.save()
        return redirect(url_for('orgs'))

    return render_template("organization/organization_create.html",
                           form=form,
                           form_name="Organization")



if __name__ == '__main__':
    app.run(host='0.0.0.0')
