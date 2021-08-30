"""

View methods for the tribes database.

"""

from flask import (Blueprint,
                   request,
                   redirect,
                   url_for,
                   render_template,
                   make_response,
                   jsonify)

from flask_login import login_required, current_user

from flaskserv.socialnet import db

from flaskserv.socialnet.tribes.form import TribeForm
from flaskserv.socialnet.models import Tribe, User


tribes_bp = Blueprint('tribes',
                      __name__,
                      template_folder='templates')

@login_required
@tribes_bp.route('/tribe/<uuid>')
def tribe(uuid):
    tribe = Tribe.query.filter_by(uuid=uuid).first()
    return render_template("tribe.html",
                           tribe = tribe)


@login_required
@tribes_bp.route('/tribes')
def tribes():
    """

    This is where the tribes are displayed.

    """
    return render_template("tribes.html")


@login_required
@tribes_bp.route('/tribes/new', methods=["GET", "POST"])
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


@login_required
@tribes_bp.get('/tribes/load')
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
