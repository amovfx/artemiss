
from flask import Blueprint, request, redirect, url_for, render_template, session
from werkzeug.security import check_password_hash

from models.forms import Agent

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        existingUser = Agent.objects(email=request.form['email']).first()
        if check_password_hash(existingUser['password'], request.form['password']):

            session['id'] = existingUser.id
            return redirect(url_for('orgs'), id="MyId")

    return render_template("agents/agent_login.html", title="Login")

@auth.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == 'POST':
        agent = Agent(**request.form)
        agent.save()
        return redirect(url_for('login'))

    return render_template("agents/agent_create.html", title="Register")