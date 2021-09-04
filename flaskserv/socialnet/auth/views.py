import os

from flask import (Blueprint,
                   request,
                   redirect,
                   url_for,
                   render_template,
                   make_response,
                   flash)

from flask_login import (login_user,
                         login_required,
                         logout_user,
                         current_user)

from werkzeug.security import check_password_hash

if os.environ.get("TESTING"):
    check_password_hash = lambda x, y: x == y

from .forms import LoginForm, RegisterForm
from flaskserv.socialnet.models import User

from flaskserv.socialnet import db

auth_bp = Blueprint('auth',
                    __name__,
                    template_folder='templates')

@auth_bp.route('/login', methods = ["GET", "POST"])
def login():
    """

    Main login route
    :return:
    """
    form = LoginForm(request.form)
    if request.method == 'POST':

        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()


            if (user is not None):
                if check_password_hash(user.password, request.form['password']):
                    login_user(user=user,
                               remember=True)

                    return redirect(url_for('tribes.tribes'))
                else:
                    return "Bad password", 400
            else:
                return "User does not exist", 400

        else:
            return "Bad Form", 400

    return render_template("login.html",
                           title="Login",
                           form=form)

@auth_bp.route('/user')
@login_required
def user():
    """

    A route to get which user is logged in.

    :return:
        The current user
    """

    return str(current_user.name) # pragma: no cover

@auth_bp.route('/logout')
@login_required
def logout():
    """

    Route to logout
    :return:
        Returns user to landing page.
    """
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('landing.landing'))

@auth_bp.route('/register', methods = ["GET", "POST"])
def register():
    """

        Route to register a new member of the website.

    :return:
    """
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            existingUser = User.query.filter_by(email=email).first()
            if existingUser:
                flash("User already exists.")
                form.email.errors = ["User already exists"]
                return render_template("register.html",
                                       title="Register",
                                       form=form), 302


            user = User(email=email,
                         name=name,
                         password=password)

            db.session.add(user)
            db.session.commit()

            login_user(user=user,
                       remember=True)

            return redirect(url_for('tribes.tribes'))

    return render_template("register.html",
                   title="Register",
                   form=form)



