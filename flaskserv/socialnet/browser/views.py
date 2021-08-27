from flask import (Blueprint,
                   request,
                   redirect,
                   url_for,
                   render_template,
                   session,
                   make_response,
                   jsonify)

from flask_login import login_required

from flaskserv.socialnet import db

from flaskserv.socialnet.models import Tribe


browser_bp = Blueprint('browser',
                    __name__,
                    template_folder='templates')

@login_required
@browser_bp.get('/tribes/')
def tribes():
    return render_template("organization_browser.html",
                           tribes=db.session.query(Tribe)[0:10])

@login_required
@browser_bp.get('/tribes/new')
def create_tribe():
    return "Poopy", 200
