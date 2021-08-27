from flask_testing import TestCase
from flaskserv.socialnet import create_app, db
from flaskserv.socialnet.config import TestConfig
from flaskserv.socialnet.models import User

class TestBaseCase(TestCase):

    def create_app(self):
        return create_app(config_class=TestConfig)

    def setUp(self) -> None:
        db.create_all(app=self.app)
        for name in ("Alice", "Bob", "Carol"):
            user = User(name=name,
                        email=f"{name}@example.com",
                        password="bad_password")
            db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=self.app)