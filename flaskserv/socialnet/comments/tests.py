from ddt import ddt, data
import json

from flaskserv.socialnet.comments.form import CommentsForm

from flaskserv.socialnet.tests.test_base import TestBaseCase

from flaskserv.socialnet.models import Tribe, User
from flaskserv.socialnet.data.create_db import (generate_tribes,
                                                generate_random_post,
                                                generate_discreet_comment_tree)

from unittest import mock

class TestCommentForm(TestBaseCase):

    def test_valid_comment_form(self):
        comment_form = CommentsForm(message = "This is a test")
        self.assertTrue(comment_form.validate())

    def test_invalid_comment_form(self):
        comment_form = CommentsForm()
        self.assertFalse(comment_form.validate())


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
        response = self.client.get(f'comments/{self.tribe.uuid}?c={value}',
                                   content_type='json')

        print (response.data)
        self.assertEqual(200, response.status_code)

    def test_get_comment_route_no_arg(self):
        """

        Test for missing argument.

        """
        response = self.client.get(f'comments/{self.tribe.uuid}',
                                   content_type='html/text')

        self.assertEqual(404, response.status_code)

    @mock.patch('flask_login.utils._get_user')
    def test_reply_to_comment_route(self, current_user):
        """

        Test for a reply to a comment in a tribe.

        """
        user = User.query.get(1)
        current_user.return_value = user
        post = self.tribe.posts[0]
        with self.client as c:
            with c.session_transaction() as sess:
                sess["TRIBE_ID"] = self.tribe.id
                sess["TRIBE_UUID"] = self.tribe.uuid

            response = self.client.post(f'comments/reply?post_uuid={post.uuid}',
                                   data={"message":"This is a test message"})

        comment_reply = post.replies[-1]
        self.assertTrue(comment_reply.message == "This is a test message")


    @mock.patch('flask_login.utils._get_user')
    def test_reply_to_tribe_route(self, current_user):
        """

        Reply is to the main tribe route.
        :param current_user:
            a mocked up user.
        :return:
        """
        user = User.query.get(1)
        current_user.return_value = user
        with self.client as c:
            with c.session_transaction() as sess:
                sess["TRIBE_ID"] = self.tribe.id
                sess["TRIBE_UUID"] = self.tribe.uuid

            response = self.client.post(f'comments/reply',
                                   data={"message":"This is a reply to the tribe"})

        comment_reply = self.tribe.posts[-1]
        self.assertTrue(comment_reply.message == "This is a reply to the tribe")


    def test_reply_with_badform(self):
        """

        Reply to the main route with no message.

        """


        response = self.client.post(f'comments/reply',
                                   data={})

        self.assertTrue(404, response.status_code)




