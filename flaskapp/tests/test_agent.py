import unittest
from flaskapp.app import app as flaskapp
from flaskapp.utilities import ResponseCode
from flaskapp.models.agent import Agent
from mongoengine import connect
from werkzeug.security import generate_password_hash



class TestAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        connect('mongoenginetest', host='mongomock://localhost')
        cls.email = "TestingUser@email.com"
        cls.password = "Aa1!_1234567890"

        cls.post_data = {"email": cls.email,
                        "password": cls.password}

        hashed_password = generate_password_hash(cls.password,
                                                 method='sha256')

        User = Agent(email=cls.email,
                     password=hashed_password)
        User.save()

    #test if login page loads
    def test_login_page(self):
        """

            Test if login page loads

        """
        tester = flaskapp.test_client()
        response = tester.get('/login',
                              content_type='html/text')
        self.assertEqual(ResponseCode.OK.value.code,
                         response.status_code)


    def test_valid_login(self):
        """

        Testing a valid login. This simply posts the valid data from the setup.

        """
        tester = flaskapp.test_client()

        response = tester.post('/login',
                               data=self.post_data)

        self.assertEqual(ResponseCode.CREATED.value.code,
                         response.status_code)

    def test_user_doesnt_exist(self):
        """

        Test if member isn't created in the database.

        """
        tester = flaskapp.test_client()

        post_data = self.post_data.copy()
        post_data['email'] = "different@email.com"

        response = tester.post('/login',
                               data=post_data)

        self.assertEqual(ResponseCode.USER_DOES_NOT_EXIST.value.code,
                         response.status_code)


    def test_wrong_password(self):
        """

        Test if wrong password is entered but the user is correct.

        """
        tester = flaskapp.test_client()

        post_data = {}
        post_data['email'] = self.email
        post_data['password'] = "different_password"

        response = tester.post('/login',
                               data=post_data)

        self.assertEqual(ResponseCode.BAD_PASSWORD.value.code,
                         response.status_code)











