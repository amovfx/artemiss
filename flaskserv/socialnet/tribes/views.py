"""

View methods for the tribes database.

"""

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

from flaskserv.socialnet.tribes.form import TribeForm, CommentReplyForm
from flaskserv.socialnet.models import Tribe, User


tribes_bp = Blueprint('tribes',
                      __name__,
                      template_folder='templates',
                      static_url_path='/tribes/static',
                      static_folder='static')

@login_required
@tribes_bp.route('/tribe/<uuid>')
def tribe(uuid):
    """

    The route for the tribe.
    :param uuid:
        This fetches a specific tribe from the db.
    :return:
        Rendered template.
    """

    tribe = Tribe.query.filter_by(uuid=uuid).first()
    return render_template("tribe.html",
                           tribe = tribe)



@tribes_bp.route('/tribes')
@login_required
def tribes():
    """

    This is where the tribes are displayed.

    """
    return render_template("tribes.html")



@tribes_bp.route('/tribes/new', methods=["GET", "POST"])
@login_required
def create_tribe():
    """

    This route allows the auth to create an organization and save it to the database.

    """

    form = TribeForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():

            tribe = Tribe()
            tribe.name = request.form["name"]
            tribe.description = request.form["description"]

            #an unfortunate method for testing the creation of tribes
            if current_user.is_anonymous:
                user = User(name="Anon",
                            email="Anon@example.com",
                            password="bad_password")

            else: # pragma: no cover
                user = current_user

            tribe.owner = user
            db.session.add(tribe)
            db.session.commit()

            return redirect(url_for('tribes.tribes'))


    return render_template("tribes_create.html",
                           form=form)


@tribes_bp.get('/tribes/load')
@login_required
def load():

    """

    This is a route to handle infinite scroll. The relevant java script
    is in tribes.html.

    :return:
        A JSON of the Tribes, an object that just has the
        relevant data of what is needed.


    """

    def get_tribes(counter, quantity = 5):
        """

        :param counter:

        :return:
        """

        light_response_objects = []
        tribes_slice = Tribe.query.all()[counter:counter+quantity]

        for tribe in tribes_slice:
            light_response_objects.append(tribe.preview())

        return light_response_objects

    if request.args:

        counter = int(request.args.get("c"))

        if counter == 0:
            response = make_response(jsonify(get_tribes(counter=0,quantity=15)), 200)

        elif counter == len(Tribe.query.all()):
            response = make_response(jsonify({}), 200)

        else:
            response = make_response(jsonify(get_tribes(counter)), 200)

    return response


@tribes_bp.get('/tribes/comment/post/<tribe_uuid>')
@login_required
def get_comments_from_tribe(tribe_uuid):
    """

    Get tribe comments.

    """

    tribe = Tribe.query.filter_by(uuid=tribe_uuid).first()
    comment_tree = build_nested_comment_tree_from_tribe(tribe)


    return jsonify(comment_tree), 200


def build_nested_comment_tree_from_tribe(tribe):
    """
    Build a nested comment tree from a tribe.

    :param tribe:
        Tribe is a SQL orm
    :return:
        Nested dictionary
    """


    def build_nested(post, comment_tree, depth=0):
        """

        Get a posts path and build up a nested dictionary
        to pass to javascript.

        :param post:
            Post SQL orm object
        :param comment_tree:
            dictionary to hold data
        :param depth:
            level of tree traversal.
        :return:
        """
        path = post.path.split(".")
        head = path[depth]
        if head not in comment_tree.keys():
            comment_tree[head] = {'post': post.preview(),
                                  'replies': {}}
        else:
            build_nested(post, comment_tree[head]['replies'], depth + 1)

    comment_tree = dict()
    for post in tribe.posts:
        build_nested(post, comment_tree)
    print (json.dumps(comment_tree, indent=4))
    return comment_tree





