"""Samll utility to help with the creation of flask bps."""

import pathlib

def get_views_content(name : str) -> str:
    """

    :param name:
    :return:
    """
    bp_content =f"""

import json

from flask import (Blueprint,
                   request,
                   redirect,
                   url_for,
                   render_template,
                   make_response,
                   jsonify)

from flask_login import login_required, current_user
from flaskserv.socialnet import db

from flaskserv.socialnet.{name}.form import {name.capitalize()}Form


{name}_bp = Blueprint('{name}',
                      __name__,
                      template_folder='templates',
                      static_url_path='/{name}/static',
                      static_folder='static')
"""

    return bp_content

def get_forms_content(name: str) -> str:
    return \
    f"""
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

class {name.capitalize()}Form(FlaskForm):
    pass
   
    """



def create_file(path, py_file_name, contents=""):
    f = open(path / f'{py_file_name}.py', '+w')
    f.write(contents)
    f.close()

def make_blueprint_folder(name):
    path = pathlib.Path(__file__).parents[1] / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def make_blueprint(name):
    bp_folder = make_blueprint_folder(name)

    static_folder = bp_folder / 'static'
    static_folder.mkdir(exist_ok=True)

    template_folder = bp_folder / 'templates'
    template_folder.mkdir(exist_ok=True)

    js_folder = static_folder / 'js'
    js_folder.mkdir(exist_ok=True, parents=True)

    css_folder = static_folder / 'css'
    css_folder.mkdir(exist_ok=True,parents=True)

    file_names = ["form", "tests", "views", "__init__"]

    file_content = [get_forms_content ,
                    None,
                    get_views_content,
                    None]

    for file_name, content_fn in zip(file_names, file_content):
        content = content_fn(name) if callable(content_fn) else ""
        create_file(bp_folder, file_name, contents=content)

if __name__ == '__main__':
    make_blueprint("chat")