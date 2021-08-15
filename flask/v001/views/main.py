from flask import Blueprint, request, redirect, url_for, render_template, session

main = Blueprint('main', __name__)

#Landing page
@main.route('/')
def main():
    return render_template("sidebar.html", test = "Very Nice!")