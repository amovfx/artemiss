import random

from flaskserv.socialnet.test_base import TestBaseCase
from flaskserv.socialnet.browser.form import TribeForm, PostForm


from flaskserv.socialnet.data.create_db import generate_tribes
from flaskserv.socialnet.models import User, Tribe, Post



class TestBrowser(TestBaseCase):
    """

    Test base case

    """

    def setUp(self):
        """

        For setup we generate some tribes, keep the amount to make sure
        the db is working correctly.

        """
        super().setUp()
        print()
        self.tribe_count = 10
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


    def test_tribe_page(self):
        """

        Test the tribes page.

        """

        response = self.client.get('/tribes/new',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)







