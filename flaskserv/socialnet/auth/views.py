
from flask import (Blueprint,
                   request,
                   redirect,
                   url_for,
                   render_template,
                   session,
                   flash)

from flask_login import (login_user,
                         login_required,
                         logout_user)

from werkzeug.security import check_password_hash

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

                return redirect(url_for('browser.tribes'))
            else:
                return "User does not exist", 400

        else:
            return "Bad Form", 400

    return render_template("login.html",
                           title="Login",
                           form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('landing'))

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
            verified_password = request.form.get("confirm")

            existingUser = User.query.filter_by(email=email).first()
            if existingUser:
                return redirect(url_for('auth.login'), code=302)

            if password != verified_password:
                return redirect(url_for('auth.register'),302)

            user = User(email=email,
                         name=name,
                         password=password)

            db.session.add(user)
            db.session.commit()

            login_user(user=user,
                       remember=True)

            return redirect(url_for('browser.tribes'))
        else:
            print (form.errors)
            return 'Bad Form', 400

    return render_template("register.html",
                           title="Register",
                           form=form)

