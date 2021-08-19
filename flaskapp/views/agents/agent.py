
from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

from flaskapp.models.agent import Agent, AgentForm
from flaskapp.utilities import ResponseCode

auth = Blueprint('auth', __name__, template_folder='templates')

def reroute(endpoint, response_code):
    return redirect(url_for(endpoint), response_code)

@auth.route('/login', methods = ["GET","POST"])
def login():

    if request.method == 'POST':

        existingUser = Agent.objects(email=request.form['email']).first()
        if not existingUser:
            flash("User does not exist!", category="warning")
            return reroute('auth.register',
                           ResponseCode.NOUSER.value)

        if not check_password_hash(existingUser['password'], request.form['password']):
            flash("Password is wrong.", category="danger")
            return reroute('auth.login',
                           ResponseCode.BADPASSWORD.value)


        #session.permanent = True
        #session['id'] = existingUser.id
        return reroute('orgs.org_browse',
                        ResponseCode.OK.value)

    return render_template("agent_login.html", title="Login")

@auth.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        verified_password = request.form.get("verifypassword")

        existingUser = Agent.objects(email=email).first()
        if existingUser:
            flash("That email exists!", category="warning")
            return redirect(url_for('auth.register'))

        if password != verified_password:
            flash("Passwords dont match!", category="warning")
            return redirect(url_for('auth.register'))



        agent = Agent(email=email,
                      password=generate_password_hash(password, method='sha256'))
        agent.save()

        return redirect(url_for('auth.login'))

    return render_template("agent_create.html", title="Register")