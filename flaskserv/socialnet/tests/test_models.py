import random


from flaskserv.socialnet.models import Tribe, User, Post
from flaskserv.socialnet.tests.test_base import TestBaseCase
from flaskserv.socialnet import db

import lorem
import names

def get_random_item(Model):
    """

    Return a random entry of the argument model.
    :param Model:
    :return:
    """
    return random.choice(Model.query.all())

def create_random_user():
    """

    Generates a random user for testing.

    :return:
        A user model.
    """
    name = names.get_first_name()
    return User(name=name,
                email=f"{name}@example.com",
                password="testing_password")




def generate_comment_tree(tribe,
                          parent_post=None,
                          depth = 3,
                          count = 0):
    """

    Generate a comment tree

    :param tribe:
        The tribe the comments belong to.
    :param parent_post:
        The parent post
    :param count:
        parameter to keep track of depth.
    :return:
    """

    if count < depth:
        range_min = 2 * (2 - count)
        range_max = 5 * (2 - count)

        for _ in range(random.randint(range_min, range_max)):
            print("Creating ")
            rand_user = get_random_item(User)
            child_post = Post(title=lorem.sentence().split(" ")[0],
                            message=lorem.sentence(),
                            owner=rand_user,
                            tribe=tribe)

            if parent_post:
                child_post.parent = parent_post

            db.session.add(child_post)

            if random.uniform(0,1) < .2:
                generate_comment_tree(tribe,
                                      parent_post=child_post,
                                      count=count + 1)


    db.session.commit()
    return None

class TestIntegrations(TestBaseCase):

    def setUp(self):
        user = User()
        db.session.add(user)

        tribe = Tribe(name="Test",description="Best Tribe")
        tribe.owner_id = user.id
        tribe.owner = user
        db.session.add(tribe)

        post = Post(title=lorem.sentence().split("0")[0],
                    message=lorem.sentence(),
                    owner=user,
                    tribe=tribe)

        db.session.add(post)

        for _ in range(5):
            child_post = Post(title=lorem.sentence().split(" ")[0],
                        message=lorem.sentence(),
                        owner=user,
                        parent=post,
                        tribe=tribe)

            db.session.add(child_post)


        tribe_tree = Tribe(name="Tree Test",description="Best Tribe")
        tribe_tree.owner_id = user.id
        tribe_tree.owner = user
        db.session.add(tribe_tree)

        generate_comment_tree(tribe_tree)

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
        self.assertGreaterEqual( len(user.posts),1)

    def test_get_post_from_tribe(self):
        tribe = Tribe.query.filter_by(name="Test").first()
        for post in tribe.posts:
            print(f"title: {post.title}")
            print(f"message: {post.message}\n")
        self.assertEqual(6, len(tribe.posts))

    def test_post_tree(self):
        tribe = Tribe.query.filter_by(name="Test").first()








