"""

View methods for the tribes database.

"""

import json


from flask import (Blueprint,
                   request,
                   redirect,
                   session,
                   url_for,
                   render_template,
                   make_response,
                   jsonify)

from flask_login import login_required, current_user
from flaskserv.socialnet import db

from flaskserv.socialnet.tribes.form import TribeForm, CommentReplyForm
from flaskserv.socialnet.models import Tribe, User

from flaskserv.socialnet.comments.views import comments_bp


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
    session["TRIBE_ID"] = tribe.id
    session["TRIBE_UUID"] = tribe.uuid
    return render_template("tribe.html",
                           tribe=tribe,
                           user=current_user)



@tribes_bp.route('/tribes')
@login_required
def tribes():
    """

    This is where the tribes are displayed.

    """
    return render_template("tribes.html",)



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
        tribes_slice = Tribe.query.paginate(counter, quantity).items

        for tribe in tribes_slice:
            light_response_objects.append(tribe.preview())

        return light_response_objects

    if request.args:

        counter = int(request.args.get("c"))

        if counter == 0:
            response = make_response(jsonify(get_tribes(counter=1,
                                                        quantity=15)), 200)

        elif counter == len(Tribe.query.all()):
            response = make_response(jsonify({}), 200)

        else:
            response = make_response(jsonify(get_tribes(counter)), 200)

    return response


