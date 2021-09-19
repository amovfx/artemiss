

import json

from flask import (Blueprint,
                   request,
                   redirect,
                   url_for,
                   render_template,
                   make_response,
                   jsonify,
                   session)

from flask_login import login_required, current_user
from flaskserv.socialnet import db

from flaskserv.socialnet.models import Post, User, Tribe

from flaskserv.socialnet.comments.form import CommentsForm


comments_bp = Blueprint('comments',
                      __name__,
                      template_folder='templates',
                      static_url_path='/comments/static',
                      static_folder='static')


@comments_bp.get('/comments/<tribe_uuid>')
@login_required
def get_tribe_comments(tribe_uuid):
    """

    Get the posts of a tribe.

    :param tribe_uuid:
        The UUID of a tribe to disguise the tribe id.
    :return:
        Json of the comments.

    """
    PAGE_COUNT = 15

    def get_tribe_posts(tribe):
        tribe_posts = db.session.query(Post, User).order_by(Post.path).filter(Post.tribe_id == tribe.id)
        return tribe_posts

    def get_comment_page(tribe_posts, page, quantity):
        page_query = tribe_posts.filter(Post.author_id == User.id).paginate(page, quantity, False)

        data = []
        for post, user in page_query.items:
            data.append(post.preview(user))

        return make_response(jsonify(data), 200)

    if request.args:
        counter = int(request.args.get("c"))
        tribe = Tribe.query.filter_by(uuid = tribe_uuid).first();
        tribe_posts_query = get_tribe_posts(tribe)

        if counter == 0:
            response = get_comment_page(tribe_posts_query,
                                        page=0,
                                        quantity=PAGE_COUNT)

        elif counter == tribe_posts_query.count() % PAGE_COUNT:
            response = make_response(jsonify({}), 200)

        else:
            response = get_comment_page(tribe_posts_query,
                                        page=counter,
                                        quantity=PAGE_COUNT)

        return response

    return "No argument c", 404

@comments_bp.post('/comments/reply')
@login_required
def tribe_reply():
    """

    Reply from then
    :return:
    """

    form = CommentsForm(request.form)
    tribe_uuid = ""
    if form.validate_on_submit():
        tribe_id = session.get("TRIBE_ID")
        tribe_uuid = session.get("TRIBE_UUID")
        if (tribe_id is not None) and (tribe_uuid is not None):
            reply = Post()
            reply.tribe_id = tribe_id
            reply.author = current_user
            reply.message = form.message.data

            if request.args:
                post_uuid = request.args.get("post_uuid")
                if post_uuid:
                    parent_post = Post.query.filter_by(uuid=post_uuid).first()
                    reply.parent = parent_post


            reply.save()

            return redirect(url_for('tribes.tribe',
                                    uuid=tribe_uuid))

    return redirect(url_for('tribes.tribe',
                            uuid=tribe_uuid))











