"""

Testing model integrations.

"""

from ddt import ddt, data, idata

from flaskserv.socialnet import db
from flaskserv.socialnet.constants import PERMISSIONS
from flaskserv.socialnet.data.create_db import *
from flaskserv.socialnet.models import Tribe, User, PermissionsGroup
from flaskserv.socialnet.tests.test_base import TestBaseCase


@ddt
class TestUserModel(TestBaseCase):

    def setUp(self) -> None:
        generate_users(1)

        self.user = User()

        generate_tribes(10)
        self.tribes = Tribe.query.all()

    def test_init(self):
        """

        Test default user for testing.

        :return:
        """

        u = User()
        published_user = User.query.get(u.id)

        self.assertEqual("TestUser", published_user.name)
        self.assertEqual("Test@Example.com", published_user.email)
        self.assertEqual("Bad_Password", published_user.password)

    def test_init_custom_user(self):
        """

        Test custom user.

        :return:
        """
        u = User(name="name",
                 email="name@panopticon.com",
                 password="12345")

        published_user = User.query.get(u.id)

        self.assertEqual("name", published_user.name)
        self.assertEqual("name@panopticon.com", published_user.email)
        self.assertEqual("12345", published_user.password)

    @data(1, 5, 8)
    def test_user_tribes(self, value):
        """

        Test how many tribes the user has joined

        """
        user = generate_random_user()
        for tribe in self.tribes[:value]:
            user.join_tribe(tribe, permission_group_name="applicant")

        self.assertEqual(value, user.tribes.count())

    def test_join_tribe(self):
        """

        Create a random tribe and user , user joins the tribe and sets permissions.

        """
        tribe = generate_random_tribe() #make a tribe with a random user as owner
        user = generate_random_user()
        user.join_tribe(tribe, permission_group_name="applicant")

        self.assertEqual(tribe.users.count(), 2)

    def test_leave_tribe(self):
        """

        Create a user, join a tribe and

        """
        tribe = generate_random_tribe()
        user = generate_random_user()
        user.join_tribe(tribe, "applciant", PERMISSIONS.NONE)
        user.leave_tribe(tribe)
        self.assertFalse(user.is_in_tribe(tribe))

    def test_as_dict(self):
        """

        Testing the as_dict mixin fun.

        """
        user = generate_random_user()
        self.assertTrue(isinstance(user.as_dict(), dict))
        self.assertIn("name", user.as_dict().keys())
        self.assertIn("email", user.as_dict().keys())


class TestTribeModel(TestBaseCase):

    def setUp(self):
        """

        Set up data

        """

        generate_users(15)
        generate_tribes(10)
        self.tribe = generate_random_tribe()
        for i in range(5):
            self.tribe.add_user(generate_random_user(), "applicant", PERMISSIONS.READ)

        self.test_user = generate_random_user()



    def test_add_user(self):
        """

        Adding a user and testing the incriment.

        """

        self.tribe.add_user(generate_random_user(), "applicant", PERMISSIONS.READ)
        self.assertEqual(7, self.tribe.users.count())


    def test_get_users(self):
        """

        Get a query of the users.

        """

        users = self.tribe.get_users()
        self.assertEqual(6, users.count())


    def test_get_filtered_users(self):
        """

        Get the users with a custom filter.

        """

        users = self.tribe.get_users(custom_filter= PermissionsGroup.permissions == PERMISSIONS.READ)
        self.assertEqual(5, users.count())


    def test_get_user_permissions(self):
        """

        test user permissions

        """

        test_user = generate_random_user()
        tribe = generate_random_tribe()
        tribe.add_user(test_user)
        self.assertIs(tribe.get_user_permissions(test_user), PERMISSIONS.NONE)


    def test_set_user_permissions(self):
        """

        sets user permissions to Execute.

        """

        test_user = generate_random_user()
        tribe = generate_random_tribe()
        tribe.add_user(test_user, "test", PERMISSIONS.READ)
        tribe.set_user_permissions(test_user, PERMISSIONS.EXECUTE)

        self.assertIs(tribe.get_user_permissions(test_user), PERMISSIONS.EXECUTE)

    def test_as_dict(self):
        """

        Testing the as_dict mixin fun.

        """
        tribe = generate_random_tribe()
        print(tribe.as_dict())
        self.assertTrue(isinstance(tribe.as_dict(), dict))
        self.assertIn("name", tribe.as_dict().keys())
        self.assertIn("description", tribe.as_dict().keys())


@ddt
class TestPermissionsGroupModel(TestBaseCase):

    def setUp(self):
        self.user = User()
        self.tribe = Tribe("default", "test", self.user)
        generate_users(5)

    def test_is_user_in_tribe(self):
        """

        Create a random user and check if the user is in a tribe.

        """
        user = generate_random_user()
        self.tribe.add_user(user, "applicant", PERMISSIONS.READ)
        self.assertTrue(PermissionsGroup.is_user_in_tribe(self.user, self.tribe))


    @idata(PERMISSIONS.unittest_idata_generator())
    def test_get_permissions(self, value):
        """

        Create a user and add it to tribe. Check if the permissions are being set.

        """
        user = generate_random_user()
        self.tribe.add_user(user, "applicant", value)
        permissions = PermissionsGroup.get_tribe_user_permissions(user, self.tribe)
        self.assertIs(permissions, value)

    @idata(PERMISSIONS.unittest_idata_generator())
    def test_set_permissions(self, value):
        """

        Create a user and add it to an existing tribe.

        """

        user = User()
        self.tribe.add_user(user, "applicant", PERMISSIONS.NONE)
        PermissionsGroup.set_tribe_user_permissions(user, self.tribe, permissions=value)
        permissions = PermissionsGroup.get_tribe_user_permissions(user, self.tribe)
        self.assertIs(permissions, value)
        
    def test_as_dict(self):
        """

        Testing the as_dict mixin fun.

        """

        pg = PermissionsGroup(name="applicant")
        self.assertTrue(isinstance(pg.as_dict(), dict))
        self.assertIn("name", pg.as_dict().keys())
        self.assertIn("permissions", pg.as_dict().keys())





