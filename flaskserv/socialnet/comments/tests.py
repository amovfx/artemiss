from ddt import ddt, data
import json

from flaskserv.socialnet.tests.test_base import TestBaseCase

from flaskserv.socialnet.models import Tribe
from flaskserv.socialnet.data.create_db import (generate_tribes,
                                                generate_random_post,
                                                generate_discreet_comment_tree)
@ddt
class TestCommentRoutes(TestBaseCase):

    def setUp(self):
        super().setUp()
        generate_tribes(2)

        #we use this in our tests
        self.tribe = Tribe.query.all()[0]

        generate_discreet_comment_tree(self.tribe)


    @data(0, 1, 5)
    def test_get_comment_route(self, value):
        """

        This is a parameterized test for the comment route

        """
        response = self.client.get(f'comments/{self.tribe.id}?c={value}',
                                   content_type='json')

        print (response.data)
        self.assertEqual(200, response.status_code)

    def test_get_comment_route_no_arg(self):
        """

        Test for missing argument.

        """
        response = self.client.get(f'comments/{self.tribe.id}',
                                   content_type='html/text')

        self.assertEqual(404, response.status_code)


