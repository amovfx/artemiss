

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

from flaskserv.socialnet.chat.form import ChatForm

from . import chat_bp

@chat_bp.route("/chat_window")
def open():
    user = current_user
    return render_template("room.html",
                    room="debug",
                    username=user.name)



