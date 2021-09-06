

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
    """

    Gets the comments of a tribe.
    This should be a generic function.

    :param tribe:
        The tribe of the comments.
    :return:
        json of the orms comments.
    """


    counter = int(request.args.get("c"))

    page = db.session.query(Post, User) \
        .filter(Post.author_id == User.id) \
        .filter(Post.tribe_id == tribe) \
        .paginate(counter, 10, False)


    data = []
    for post, user in page.items:
        data.append(post.preview(user))


    return jsonify(data), 200





