"""

Testing model integrations.

"""


from flaskserv.socialnet.models import Tribe, User
from flaskserv.socialnet.tests.test_base import TestBaseCase
from flaskserv.socialnet.data.create_db import generate_random_post
from flaskserv.socialnet import db


class TestIntegrations(TestBaseCase):
    """

    Testing database.

    """

    def setUp(self):
        """

        Create testing data, overloaded the base function.
        :return:
        """

        user = User()
        user.save()

        tribe = Tribe(name="Test",description="Best Tribe")
        tribe.owner_id = user.id
        tribe.tribe_owner = user
        tribe.save()

        post = generate_random_post(tribe, user)

        db.session.add(post)

        for _ in range(5):
            child_post = generate_random_post(tribe, user=user)
            db.session.add(child_post)

        db.session.commit()



    def test_get_user(self):
        """

        Testing getting a user.

        :return:
        """
        user = User.query.filter_by(name="TestUser").first()
        assert user is not None

    def test_get_tribe(self):
        """

        Testing getting a tribe.
        :return:
        """
        tribe = User.query.filter_by(name="Test")
        assert tribe is not None

    def test_get_post_from_user(self):
        """

        Testing getting a post from a user.

        """
        user = User.query.filter_by(name="TestUser").first()
        assert len(user.posts) >= 1

    def test_get_post_from_tribe(self):
        """

        Testing getting a post from a tribe.

        """
        tribe = Tribe.query.filter_by(name="Test").first()
        self.assertEqual(6,len(tribe.posts))


