from flask import url_for

from flaskserv.socialnet.models import User
from flaskserv.socialnet.auth.views import LoginForm

from flaskserv.socialnet.test_base import TestBaseCase
class TestRegistration(TestBaseCase):

    def setUp(self):
        super()
        self.post_data = {"name": "Erica",
                            "email": "Erica@example.com",
                           "password": "bad_password",
                           "confirm": "bad_password"}

    def test_registration_page(self):
        """

            Test if login page loads

        """
        response = self.client.get('/register',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)

    def test_register_user(self):
        """

        Register a user and check if they are in the database.
        post_data is set in the setUp function.

        """

        response = self.client.post("/register",
                                   data = self.post_data,
                                    follow_redirects=True)

        new_user = User.query.filter_by(name=self.post_data['name']).first()
        self.assertEquals(new_user.name, self.post_data['name'])
        self.assertEqual(200,
                         response.status_code)

    def test_register_existing_user(self):
        """

        Register an existing user.

        """
        post_data= self.post_data.copy()
        post_data['name'] = "Alice"

        response = self.client.post("/register",
                                   data = post_data)

        self.assertEquals(302, response.status_code)

    def test_register_bad_confirm(self):
        post_data= self.post_data.copy()
        post_data['confirm'] = "bad_confirm"

        response = self.client.post("/register",
                                   data = post_data)

        self.assertEquals(400, response.status_code)



class TestLogin(TestBaseCase):

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
        name = self.post_data['name']
        print(name)
        registered_user = User.query.filter_by(name=name).first()
        self.assertEquals(registered_user.name, name)

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






