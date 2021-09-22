"""

Testing model integrations.

"""

from ddt import ddt, data, idata
import sys
import warnings

from flaskserv.socialnet.models import Tribe, User, PermissionsGroup, PERMISSIONS
from flaskserv.socialnet.tests.test_base import TestBaseCase
from flaskserv.socialnet.data.create_db import *
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
            user.join_tribe(self.tribe)

        self.assertEqual(value + 1, self.tribe.permissiongroup.count())


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
            PermissionsGroup("name", user, tribe)


        q = db.session.query(PermissionsGroup).filter(PermissionsGroup.user_id == user.id)
        print (q.all())
        self.assertEqual(value, q.count())

    def test_join_tribe(self):
        tribe = generate_random_tribe() #make a tribe with a random user as owner
        user = generate_random_user()
        user.name="join test"
        user.save()
        user.join_tribe(tribe)

        print (tribe.permissiongroup.all())
        self.assertEqual(tribe.permissiongroup.count(), 2)

    def test_append(self):
        tribe = Tribe(name="testJoinTribe",
                      description="unitTest for joining a tribe.",
                      creator=generate_random_user())

        user = generate_random_user()
        user.name="append test"
        user.save()
        print(tribe.users.append(user))
        print(tribe.users.all())
        self.assertEqual(2, tribe.users.count())


@ddt
class TestPermissionsGroup(TestBaseCase):

    def setUp(self):
        self.user = User()
        self.tribe = Tribe("default", "test", self.user)
        generate_users(5)

    def test_init(self):
        PermissionsGroup("test", user=self.user, tribe=self.tribe)
        PermissionsGroup("test2", user=self.user, tribe=self.tribe)
        self.assertEqual(PermissionsGroup.query.count(), 1)

    def test_is_user_in_tribe(self):
        PermissionsGroup("test", user=self.user, tribe=self.tribe)
        self.assertTrue(PermissionsGroup.is_user_in_tribe(self.user, self.tribe))


    @idata(PERMISSIONS.unittest_idata_generator())
    def test_get_permissions(self, value):
        user = User()

        pg = PermissionsGroup("test", user=user, tribe=self.tribe, permissions=value)
        permissions = pg.get_tribe_user_permissions(user, self.tribe)
        self.assertIs(permissions, value)

    @idata(PERMISSIONS.unittest_idata_generator())
    def test_set_permissions(self, value):
        user = User()
        pg = PermissionsGroup("test", user=user, tribe=self.tribe, permissions=PERMISSIONS.NONE)
        PermissionsGroup.set_tribe_user_permissions(user, self.tribe, permissions=value)
        permissions = PermissionsGroup.get_tribe_user_permissions(user, self.tribe)
        self.assertIs(permissions, value)





