

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

from flaskserv.socialnet.models import Post, User

from flaskserv.socialnet.comments.form import CommentsForm


comments_bp = Blueprint('name',
                      __name__,
                      template_folder='templates',
                      static_url_path='/comments/static',
                      static_folder='static')


@comments_bp.get('/comments/<tribe>')
@login_required
def get_comments(tribe):
    data = db.session.query(Post, User).filter(Post.author_id == User.id).filter_by(Post.tribe_id == tribe).paginate(1, 10, False)
    print(data)

    return jsonify(data), 200





