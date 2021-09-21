"""

Testing model integrations.

"""

from ddt import ddt, data, unpack, idata, DATA_ATTR

from flaskserv.socialnet.models import Tribe, User, PermissionsGroup, PERMISSIONS
from flaskserv.socialnet.tests.test_base import TestBaseCase
from flaskserv.socialnet.data.create_db import (
    get_random_user,
    generate_random_post,
    generate_users,
    generate_tribes,
)
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

    @data(1, 5, 8, 10, 25, 50, 100)
    def test_tribe_users(self, value):
        users = User.query.paginate(page=1, per_page=value).items
        print(users)

        for user in users:
            user.join_tribe(self.tribe)

        self.assertEqual(value + 1, self.tribe.users.count())


@ddt
class TestUserTribes(TestBaseCase):
    def setUp(self):

        generate_users(1)

        self.user = User()

        generate_tribes(100)
        self.tribes = Tribe.query.all()

    @data(1, 5, 8, 10, 25, 50, 100)
    def test_user_tribes(self, value):
        for tribe in self.tribes[:value]:
            self.user.join_tribe(tribe)
            self.user.join_tribe(tribe)

        print(self.user.tribe_membership.all())
        self.assertEqual(value + 1, self.user.tribe_membership.count())

@ddt
class TestPermissionsGroup(TestBaseCase):

    def setUp(self):
        self.user = User()
        self.tribe = Tribe("default", "test", self.user)
        generate_users(5)

    @idata(PERMISSIONS.unittest_idata_generator())
    def test_permissions(self, value):
        user = get_random_user()
        pg = PermissionsGroup("test", user=user, tribe=self.tribe, permissions=value)
        permissions = pg.get_user_tribe_permissions(user, self.tribe)
        self.assertIs(permissions, value)



@ddt
class TestTribeMethods(TestBaseCase):
    def setUp(self):
        u = User()
        tribe = Tribe(name="TestTribe",
                      creator=u,
                      description="Best Tribe")
        self.user = u

    def test_tribe(self):
        tribe = Tribe.query.all()
        assert tribe is not None

    @idata(PERMISSIONS.unittest_idata_generator())
    def test_permissions(self, value):
        tribe = Tribe.query.all()[0]
        self.user.set_permissions(tribe, value)
        permissions = self.user.get_permissions(tribe)
        self.assertEqual(value, permissions)
