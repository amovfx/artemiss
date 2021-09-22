"""

Testing model integrations.

"""

from ddt import ddt, data, idata

from flaskserv.socialnet import db
from flaskserv.socialnet.constants import PERMISSIONS
from flaskserv.socialnet.data.create_db import *
from flaskserv.socialnet.models import Tribe, User, PermissionsGroup
from flaskserv.socialnet.tests.test_base import TestBaseCase







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

        tribe = Tribe(name="Test", description="Best Tribe", creator=user)
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
        self.assertEqual(6, len(tribe.posts))


@ddt
class TestTribeSubs(TestBaseCase):
    """

    A class to test users subscribing to tribes.


    """

    def setUp(self):
        """

        Generates users and joins them to a tribe.

        """
        generate_users(100)

        user = User()

        tribe = Tribe(name="Test", description="Best Tribe", creator=user)
        tribe.tribe_owner = user.id
        tribe.save()
        self.tribe = tribe

    @data(1, 5, 8)
    def test_tribe_users(self, value):
        users = User.query.paginate(page=1, per_page=value).items
        print(users)

        for user in users:
            user.join_tribe(self.tribe, permission_group_name="applicant")

        self.assertEqual(value + 1, self.tribe.users.count())


@ddt
class TestUser(TestBaseCase):
    def setUp(self):

        generate_users(1)

        self.user = User()

        generate_tribes(10)
        self.tribes = Tribe.query.all()

    @data(1, 5, 8)
    def test_user_tribes(self, value):
        """

        Test how many tribes the user has joined

        :param value:
            ddt values
        :return:
        """
        user = generate_random_user()
        for tribe in self.tribes[:value]:
            user.join_tribe(tribe, permission_group_name="applicant")

        self.assertEqual(value, user.tribes.count())

    def test_join_tribe(self):
        tribe = generate_random_tribe() #make a tribe with a random user as owner
        user = generate_random_user()
        user.join_tribe(tribe, permission_group_name="applicant")

        self.assertEqual(tribe.users.count(), 2)



@ddt
class TestPermissionsGroup(TestBaseCase):

    def setUp(self):
        self.user = User()
        self.tribe = Tribe("default", "test", self.user)
        generate_users(5)

    def test_is_user_in_tribe(self):
        user = User()
        self.tribe.add_user(user, "applicant", PERMISSIONS.READ)
        self.assertTrue(PermissionsGroup.is_user_in_tribe(self.user, self.tribe))


    @idata(PERMISSIONS.unittest_idata_generator())
    def test_get_permissions(self, value):
        user = User()
        self.tribe.add_user(user, "applicant", value)
        permissions = PermissionsGroup.get_tribe_user_permissions(user, self.tribe)
        self.assertIs(permissions, value)

    @idata(PERMISSIONS.unittest_idata_generator())
    def test_set_permissions(self, value):
        user = User()
        self.tribe.add_user(user, "applicant", PERMISSIONS.NONE)
        PermissionsGroup.set_tribe_user_permissions(user, self.tribe, permissions=value)
        permissions = PermissionsGroup.get_tribe_user_permissions(user, self.tribe)
        self.assertIs(permissions, value)





