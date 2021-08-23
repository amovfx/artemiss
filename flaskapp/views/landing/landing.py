from flask import Blueprint, request, redirect, url_for, render_template, session
landing = Blueprint('landing', __name__, template_folder='templates')

#Landing page
@landing.route('/')
def home():
    #return render_template("sidebar.html", test ="Very Nice!")
    return redirect(url_for('auth.login'))
