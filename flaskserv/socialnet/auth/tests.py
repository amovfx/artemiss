from flaskserv.socialnet.auth.model import User
from flaskserv.socialnet.auth.views import LoginForm

from flaskserv.socialnet.test_base import TestBaseCase

class TestFlaskAuth(TestBaseCase):

    def setUp(self):
        super().setUp()
        self.post_data = {"name": "Alice",
                     "password": "bad_password"}

    def test_user_exists(self):
        alice = User.query.filter_by(name="Alice").first()
        self.assertEquals(alice.name, "Alice")

    #test if login page loads
    def test_login_page(self):
        """

            Test if login page loads

        """
        response = self.client.get('/login',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)

    def test_valid_login(self):
        """

        Testing a valid login. This simply posts the valid data from the setup.

        """
        login_form = LoginForm(**self.post_data)
        print (self.post_data)
        response = self.client.post('/login',
                                    data=self.post_data,
                                    )
        print (response.data)
        self.assertEqual(200,
                         response.status_code)

    def test_user_doesnt_exist(self):
        """

        Test if member isn't created in the database.

        """
        post_data = self.post_data.copy()
        post_data['name'] = "Dylan"

        response = self.client.post('/login',
                               data=post_data)

        self.assertEqual(400,
                         response.status_code)
