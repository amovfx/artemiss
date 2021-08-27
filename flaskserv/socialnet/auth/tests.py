from flask import url_for

from flaskserv.socialnet.models import User
from flaskserv.socialnet.auth.views import LoginForm

from flaskserv.socialnet.test_base import TestBaseCase

class TestFlaskAuth(TestBaseCase):

    def setUp(self):
        """

        Store post data.
        :return:
        """
        super().setUp()
        self.post_data = {"name": "Alice",
                     "password": "bad_password"}

    def test_user_exists(self):
        """

            Test if user is in the database

        """
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

        Testing a valid login

        """
        print (self.post_data)
        response = self.client.post('/login',
                                    data=self.post_data)
        print (response.data)
        #self.assertEqual(url_for('browser.tribes'),response.location)
        self.assertRedirects(response, url_for('browser.tribes'))

    def test_user_doesnt_exist(self):
        """

        Test if member isn't created in the database

        """
        post_data = self.post_data.copy()
        post_data['name'] = "Dylan"

        response = self.client.post('/login',
                               data=post_data)

        self.assertEqual(400,
                         response.status_code)
