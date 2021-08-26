from flask import Blueprint, redirect, url_for, render_template, session


landing_bp = Blueprint('landing',
                       __name__,
                       template_folder='templates')

#Landing page
@landing_bp.route('/')
def landing():
    return render_template("navbar.html")