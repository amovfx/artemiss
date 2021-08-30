from flask import url_for

from flaskserv.socialnet import db
from flaskserv.socialnet.models import User
from flaskserv.socialnet.auth.views import LoginForm, RegisterForm

from flaskserv.socialnet.test_base import TestBaseCase

class TestRegistrationForm(TestBaseCase):
    """

    Class to test Registration Form.

    """
    def test_registration_form(self):
        """

        Test a good form.

        """
        register_form = RegisterForm(name="Alice",
                                     email="Alice@example.com",
                                     password="very_bad_password",
                                     confirm="very_bad_password")

        self.assertTrue(register_form.validate())

    def test_registration_form_missing_email(self):
        """

        Test a missing email.

        """
        register_form = RegisterForm(name="Alice",
                                     email="",
                                     password="very_bad_password",
                                     confirm="very_bad_password")

        self.assertFalse(register_form.validate())

    def test_registration_form_missing_name(self):
        """

        Test a good form.

        """
        register_form = RegisterForm(name="Alice",
                                     email="",
                                     password="very_bad_password",
                                     confirm="very_bad_password")

        self.assertFalse(register_form.validate())

    def test_registration_form_password_mismatch(self):
        """

        Test password mismatch.

        """
        register_form = RegisterForm(name="Alice",
                                     email="Alice@example.com",
                                     password="very_bad_password",
                                     confirm="bad_confirmation")

        self.assertFalse(register_form.validate())

    def test_registration_form_bad_email(self):
        """

        Test a bad email.

        """
        register_form = RegisterForm(name="Alice",
                                     email="Alice",
                                     password="very_bad_password",
                                     confirm="very_bad_password")

        self.assertFalse(register_form.validate())

class TestLoginForm(TestBaseCase):

    def test_login_form(self):
        """

        Test a good login form

        """
        login_form = LoginForm(name="Bob",
                               password="very_bad_password")

        self.assertTrue(login_form.validate())

    def test_login_form_missing_name(self):
        """

        Test for a login form with a missing name.

        """
        login_form = LoginForm(name="",
                               password="very_bad_password")

        self.assertFalse(login_form.validate())

    def test_login_form_missing_password(self):
        """

        Test for a login with a missing password.

        """
        login_form = LoginForm(name="BestName",
                               password="")

        self.assertFalse(login_form.validate())

    def test_login_form_empty(self):
        """

        Test for a empty login form.

        """
        login_form = LoginForm(name="",
                               password="")

        self.assertFalse(login_form.validate())



class TestRegistrationRoute(TestBaseCase):

    def setUp(self):
        super().setUp()

        self.post_data = dict(name="Erica",
                              email="Erica@example.com",
                              password="bad_password",
                              confirm="bad_password")

        user_data = self.post_data.copy()
        user_data.pop("confirm")
        existing_user = User(**user_data)
        db.session.add(existing_user)
        db.session.commit()



    def test_registration_page(self):
        """

            Test if login page loads

        """
        response = self.client.get('/register',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)

    def test_register_new_user(self):
        """

        Register a user and check if they are in the database.
        post_data is set in the setUp function.

        """
        post_data = {"name": "NewUser",
                     "email": "NewUser@example.com",
                     "password": "bad_password",
                     "confirm": "bad_password"}

        response = self.client.post("/register",
                                    data = post_data,
                                    follow_redirects=True)

        new_user = User.query.filter_by(name=self.post_data['name']).first()
        self.assertEqual(new_user.name, self.post_data['name'])
        self.assertEqual(200,
                         response.status_code)

    def test_register_existing_user(self):
        """

        Register an existing user.

        """
        post_data= self.post_data.copy()
        post_data['email'] = "Erica@example.com"

        response = self.client.post("/register",
                                   data = post_data)

        self.assertEqual(302, response.status_code)

    def test_register_bad_confirm(self):
        post_data= self.post_data.copy()
        post_data['confirm'] = "bad_confirm"

        response = self.client.post("/register",
                                   data = post_data)

        self.assertEqual(200, response.status_code)



class TestLoginRoute(TestBaseCase):

    def setUp(self):
        """

        Store post data.
        :return:
        """
        super().setUp()
        for name in ("Alice", "Bob", "Carol"):
            user = User(name=name,
                        email=f"{name}@example.com",
                        password="bad_password")
            db.session.add(user)
        db.session.commit()
        self.post_data = {"name": "Alice",
                          "password": "bad_password"}

    def test_user_in_db(self):
        """

            Test if user is in the database

        """
        name = self.post_data['name']
        registered_user = User.query.filter_by(name=name).first()
        self.assertEqual(registered_user.name, name)

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

        response = self.client.post('/login',
                                    data=self.post_data)

        self.assertRedirects(response, url_for('tribes.tribes'))

    def test_bad_password(self):
        """

        Testing a bad password login

        """
        post_data = self.post_data.copy()
        post_data['password'] = 'wrong_password'
        response = self.client.post('/login',
                                    data=post_data)

        self.assertEqual(response.status_code,400)


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


    def test_logout_page(self):
        response = self.client.get('/logout',
                                    content_type='html/text')
        self.assertEqual(302,
                         response.status_code)


    def test_bad_form(self):
        response = self.client.post('/login',
                               data={})

        self.assertEqual(400,
                         response.status_code)








