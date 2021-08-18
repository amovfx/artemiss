
from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

from models.forms import Agent

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        existingUser = Agent.objects(email=request.form['email']).first()
        if not existingUser:
            flash("User does not exist!", category="warning")
            redirect(url_for('auth.register'))

        if not check_password_hash(existingUser['password'], request.form['password']):
            flash("Password is wrong.", category="danger")
            return redirect(url_for('auth.login'))

        #session.permanent = True
        #session['id'] = existingUser.id
        return redirect(url_for('orgs.org_browse'))

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