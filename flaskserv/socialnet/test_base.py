from flask_testing import TestCase
from flaskserv.socialnet import create_app, db
from flaskserv.socialnet.config import TestConfig
from flaskserv.socialnet.models import User

from flaskserv.socialnet.data.create_db import generate_users




class TestBaseCase(TestCase):

    def create_app(self):
        return create_app(config_class=TestConfig)

    def setUp(self) -> None:
        db.create_all(app=self.app)
        generate_users()


    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)