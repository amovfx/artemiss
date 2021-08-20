from flask import Blueprint, request, redirect, url_for, render_template, session
from flaskapp.models.orgs import Organization, OrganizationForm

feed = Blueprint('feed',
                 __name__,
                 template_folder='templates')

@feed.route('/feed/create', methods = ["GET", "POST"])
def create_post():
    return 'Creating Post'


@feed.route('/feed/', methods = ["GET"])
def load_posts():
    return 'Loading posts'

