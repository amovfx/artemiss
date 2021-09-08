

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


comments_bp = Blueprint('comments',
                      __name__,
                      template_folder='templates',
                      static_url_path='/comments/static',
                      static_folder='static')


@comments_bp.get('/comments/<tribe>')
@login_required
def get_comments(tribe):

    PAGE_COUNT = 15

    def get_tribe_posts():
        tribe_posts = db.session.query(Post, User).filter(Post.tribe_id == tribe)
        return tribe_posts

    def get_comment_page(tribe_posts, page, quantity):
        page = tribe_posts.filter(Post.author_id == User.id).paginate(page, quantity, False)
        data = []
        for post, user in page.items:
            data.append(post.preview(user))
        return jsonify(data)


    if request.args:
        counter = int(request.args.get("c"))

        tribe_posts_query = get_tribe_posts()

        if counter == 0:
            response = make_response(get_comment_page(tribe_posts_query,
                                                              page=0,
                                                              quantity=PAGE_COUNT), 200)

        elif counter == tribe_posts_query.count():
            response = make_response(jsonify({}), 200)

        else:
            response = make_response(get_comment_page(tribe_posts_query,
                                                              page=counter,
                                                              quantity=PAGE_COUNT), 200)

        return response

    return "No argument c", 404





