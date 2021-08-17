from flask import Blueprint, request, redirect, url_for, render_template, session

landing = Blueprint('landing', __name__)

#Landing page
@landing.route('/')
def home():
    return render_template("sidebar.html", test = "Very Nice!")