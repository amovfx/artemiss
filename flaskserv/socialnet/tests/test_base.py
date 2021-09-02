"""

Base test case that sets up flask app and populates the database
with synthetic users.

"""

from flask_testing import TestCase
from flaskserv.socialnet import create_app, db
from flaskserv.socialnet.config import TestConfig

from flaskserv.socialnet.data.create_db import generate_users




class TestBaseCase(TestCase):
    """

    Sets up db and app.

    """

    def create_app(self):
        """

        Create an app with the testing config.
        :return:
            A flask app
        """
        return create_app(config_class=TestConfig)

    def setUp(self) -> None:
        """

        Create SQL tables. Generate users.

        :return:
        """
        db.create_all(app=self.app)
        generate_users()


    def tearDown(self):
        """

        Tear down the database.

        :return:
        """
        db.session.remove()
        db.drop_all(app=self.app)
