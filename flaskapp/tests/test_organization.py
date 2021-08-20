import unittest
from flaskapp.app import app as flaskapp
from flaskapp.utilities import ResponseCode
from flaskapp.models.orgs import Organization
from flaskapp.models.agent import Agent
from mongoengine import connect
from werkzeug.security import generate_password_hash



class TestOrganization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        connect('mongoenginetest', host='mongomock://localhost')


        for name in ["Alice", "Bob", "Carol"]:
            mock_agent = Agent(email=f"{ name }@gmail.com",
                          password=generate_password_hash("Password",
                                                  method="sha256"))
            mock_agent.save()



        MockOrg = Organization(name="Pet Insurance",
                               description="A co-op for pets!")
        cls.Org = MockOrg
        MockOrg.save()

    def test_organization_browser(self):
        """

        Test the loading of the organization page

        :return:
        """

        tester = flaskapp.test_client()
        response = tester.get('/orgs/',
                              content_type='html/text')

        self.assertEqual(ResponseCode.OK.value.code,
                         response.status_code)


    def test_organization_page(self):
        """

        Test the loading of the organization page.
        :return:
        """
        tester = flaskapp.test_client()
        response = tester.get(f'/orgs/{str(self.Org.id)}',
                              content_type='html/text')

        self.assertEqual(ResponseCode.OK.value.code,
                         response.status_code)
