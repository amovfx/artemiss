import random

from flaskserv.socialnet.models import Tribe, User, Post
from flaskserv.socialnet.tests.test_base import TestBaseCase
from flaskserv.socialnet import db

import lorem

def get_random_item(Model):
    """

    Return a random entry of the argument model.
    :param Model:
    :return:
    """
    return random.choice(Model.query.all())

def build_reply_tree(tribe, post=None, count = 0):
    if count > 3:
        range_min = 2 * (3 - count)
        range_max = 5 * (3 - count)

        for _ in range(random.randint(range_min, range_max)):

            rand_user = get_random_item(User)
            child_post = Post(title=lorem.sentence().split(" ")[0],
                            message=lorem.sentence(),
                            owner=rand_user,
                            tribe=tribe)

            if post:
                child_post.parent = post

            db.session.add(child_post)

            build_reply_tree(tribe,
                             post=child_post,
                             count=count + 1)

            return
    return

class TestUserModel(TestBaseCase):

    def setUp(self):
        user = User()
        db.session.add(user)

        tribe = Tribe(name="Test",description="Best Tribe")
        tribe.owner_id = user.id
        tribe.owner = user
        db.session.add(tribe)
        db.session.commit()

        post = Post(title=lorem.sentence().split("0")[0],
                    message=lorem.sentence(),
                    owner=user,
                    tribe=tribe)

        db.session.add(post)
        db.session.commit()
        for _ in range(5):
            child_post = Post(title=lorem.sentence().split(" ")[0],
                        message=lorem.sentence(),
                        owner=user,
                        parent=post,
                        tribe=tribe)

            db.session.add(child_post)


        db.session.commit()

    def test_get_user(self):
        user = User.query.filter_by(name="TestUser").first()
        self.assertTrue((user is not None))

    def test_get_tribe(self):
        tribe = User.query.filter_by(name="Test")
        self.assertTrue((tribe is not None))

    def test_get_post_from_user(self):
        user = User.query.filter_by(name="TestUser").first()
        for post in user.posts:
            print(f"title: {post.title}")
            print(f"message: {post.message}\n")
        self.assertEqual(6, len(user.posts))

    def test_get_post_from_tribe(self):
        tribe = Tribe.query.filter_by(name="Test").first()
        for post in tribe.posts:
            print(f"title: {post.title}")
            print(f"message: {post.message}\n")
        self.assertEqual(6, len(tribe.posts))







