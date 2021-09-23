"""

View methods for the tribes database.

"""

import json
from functools import wraps

from flask import (
flash,
g,
copy_current_request_context,
    Blueprint,
    request,
    redirect,
    session,
    url_for,
    render_template,
    make_response,
    jsonify,
)

from flask_login import login_required, current_user
from flaskserv.socialnet import db

from flaskserv.socialnet.tribes.form import TribeForm, CommentReplyForm
from flaskserv.socialnet.comments.form import CommentsForm
from flaskserv.socialnet.models import Tribe, User

from flaskserv.socialnet.comments.views import comments_bp
from flaskserv.socialnet.constants import PERMISSIONS


tribes_bp = Blueprint(
    "tribes",
    __name__,
    template_folder="templates",
    static_url_path="/tribes/static",
    static_folder="static",
)


def requires_permissions(value):
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):

            print(f"From decorator {session['TRIBE']}")
            if 'TRIBE' in session:
                tribe = Tribe.query.get(session['TRIBE'])[0]
                print (tribe)
                print (current_user.get_permissions(tribe))
                if (current_user.get_permissions(tribe)) is value:
                    print("Permissions not allowed")
                    flash("You do not have permission to view that page", "warning")
                    return func(*args, **kwargs)
                else:
                    print("Permissions allowed")
                    return func(*args, **kwargs)
            else:
                print("no tribe attr")
                return func(*args, **kwargs)

        return wrapped_func
    return decorator


@tribes_bp.route("/tribe/<uuid>")
@login_required
def tribe(uuid):
    """

    The route for the tribe.
    :param uuid:
        This fetches a specific tribe from the db.
    :return:
        Rendered template.
    """
    comment_form = CommentsForm()
    tribe = Tribe.query.filter_by(uuid=uuid).first()

    session["TRIBE_ID"] = tribe.id
    session["TRIBE_UUID"] = tribe.uuid
    session["TRIBE"] = tribe.id
    session["room"] = f"{tribe.id}:general"
    setattr(current_user, "tribe", tribe)
    print ("Tribe:", current_user.tribe)
    current_user.set_active_tribe(tribe)


    return render_template(
        "tribe.html",
        tribe=tribe,
        user=current_user,
        form=comment_form,
        room=f"{tribe.id}:general",
    )


@tribes_bp.route("/tribe/<uuid>/createGroup")
@requires_permissions(PERMISSIONS.EXECUTE)
@login_required
def makeGroup(uuid):
    print(f"Making Group on tribe {uuid}")
    return "This is a new group"


@tribes_bp.route("/tribes")
def tribes():
    """

    This is where the tribes are displayed.

    """
    return render_template("tribes.html")


@tribes_bp.get("/tribelayout")
def tribe_layout():
    """

    Prototype route.

    """
    form = CommentsForm()
    tribe = Tribe.query.all()[0]
    return render_template("tribe_layout.html", form=form, tribe=tribe)


@tribes_bp.route("/tribes/new", methods=["GET", "POST"])
@login_required
def create_tribe():
    """

    This route allows the auth to create an organization and save it to the database.

    """

    form = TribeForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():

            # an unfortunate method for testing the creation of tribes
            if current_user.is_anonymous:
                user = User(
                    name="Anon", email="Anon@example.com", password="bad_password"
                )

            else:  # pragma: no cover
                user = current_user

            tribe = Tribe(
                name=request.form["name"],
                description=request.form["description"],
                creator=user,
            )

            db.session.add(tribe)
            db.session.commit()

            return redirect(url_for("tribes.tribes"))

    return render_template("tribes_create.html", form=form)


@tribes_bp.get("/tribes/load")
@login_required
def load():

    """

    This is a route to handle infinite scroll. The relevant java script
    is in tribes.html.

    :return:
        A JSON of the Tribes, an object that just has the
        relevant data of what is needed.


    """

    def get_tribes(counter, quantity=5):
        """

        :param counter:

        :return:
        """

        light_response_objects = []
        tribes_slice = Tribe.query.paginate(counter, quantity).items

        for tribe in tribes_slice:
            light_response_objects.append(tribe.as_dict())

        return light_response_objects

    if request.args:

        counter = int(request.args.get("c"))

        if counter == 0:
            response = make_response(jsonify(get_tribes(counter=1, quantity=15)), 200)

        elif counter == len(Tribe.query.all()):
            response = make_response(jsonify({}), 200)

        else:
            response = make_response(jsonify(get_tribes(counter)), 200)

    return response
