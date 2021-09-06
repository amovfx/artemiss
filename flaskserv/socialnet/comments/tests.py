import json

from flaskserv.socialnet.tests.test_base import TestBaseCase

from flaskserv.socialnet.models import Tribe
from flaskserv.socialnet.data.create_db import (generate_tribes,
                                                generate_random_post,
                                                generate_discreet_comment_tree)

class TestCommentRoutes(TestBaseCase):

    def setUp(self):
        super().setUp()
        generate_tribes(2)

        #we use this in our tests
        self.tribe = Tribe.query.all()[0]

        generate_discreet_comment_tree(self.tribe)

    def test_get_comment_route(self):
        """

        This is a test to test the comment route
        :return:

        """
        response = self.client.get(f'comments/{self.tribe.id}?c=1',
                                   content_type='json')

        print (response.data)
        self.assertEqual(200, response.status_code)


