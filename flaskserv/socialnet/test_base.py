from flask_testing import TestCase
from flaskserv.socialnet import create_app, db
from flaskserv.socialnet.config import TestConfig
from flaskserv.socialnet.auth.model import User

class TestBaseCase(TestCase):

    def create_app(self):
        return create_app(config_class=TestConfig)

    def setUp(self) -> None:
        print ("Setting up database")
        #self.app.config['WTF_CSRF_ENABLED'] = False
        with self.app.app_context():
            db.create_all(app=self.app)
            for name in ("Alice", "Bob", "Carol"):
                user = User(name=name,
                            email=f"{name}@example.com",
                            password="bad_password")
                db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all(app=self.app)