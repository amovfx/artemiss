import random
import json

from flaskserv.socialnet.test_base import TestBaseCase
from flaskserv.socialnet.tribes.form import TribeForm, PostForm


from flaskserv.socialnet.data.create_db import generate_tribes
from flaskserv.socialnet.models import User, Tribe, Post



class TestBrowser(TestBaseCase):
    """

    Test tribe tribes.

    """

    def setUp(self):
        """

        For setup we generate some tribes, keep the amount to make sure
        the db is working correctly.

        """
        super().setUp()
        self.tribe_count = 30
        generate_tribes(self.tribe_count)


    def test_tribe_form(self):
        """

        Test validation of the tribe form.

        """

        tribe_form = TribeForm(name="Test",
                               description="Lame ass description")

        self.assertTrue(tribe_form.validate())


    def test_post_form(self):
        """

        Test validation of the post form.

        """

        post_form = PostForm(title="The title",
                             message="The message")

        self.assertTrue(post_form.validate())


    def test_tribe_count(self):
        """

        Test that the database is working from setUp.

        """

        tribe_count = len(Tribe.query.all())
        self.assertEqual(self.tribe_count, tribe_count)


    def test_create_tribe_page(self):
        """

        Test the create tribe page.

        """

        response = self.client.get('/tribes/new',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)

    def test_tribe_browser(self):
        """

        Test the create tribe page.

        """

        response = self.client.get('/tribes',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)

    def test_tribe_loader_0(self):
        """

        Test the tribe loader.

        """
        response = self.client.get('/tribes/load?c=0',
                                    content_type='json')
        json_data = json.loads(response.data)
        print( json.dumps(json_data, indent=2) )
        self.assertEqual(15, len(json_data))

    def test_tribe_loader_5(self):
        """

        Test the tribe loader.

        """
        response = self.client.get('/tribes/load?c=5',
                                    content_type='json')
        json_data = json.loads(response.data)
        print( json.dumps(json_data, indent=2) )
        self.assertEqual(5, len(json_data))

    def test_tribe_loader_full(self):
        """

        Test the tribe loader.

        """
        tribe_count = len(Tribe.query.all())
        response = self.client.get(f'/tribes/load?c={tribe_count}',
                                    content_type='json')
        json_data = json.loads(response.data)
        print( json.dumps(json_data, indent=2) )

        self.assertEqual(0, len(json_data))

    def test_create_tribe(self):
        """

        Test to create a tribe

        """

        tribe_name = "Testing Tribe"
        post_data = dict(name=tribe_name,
                         description="This is testing data.")

        response = self.client.post('/tribes/new',
                                    data=post_data)

        created_tribe = Tribe.query.filter_by(name="Testing Tribe").first()
        self.assertEqual(created_tribe.name, tribe_name)








