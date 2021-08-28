from flaskserv.socialnet.test_base import TestBaseCase

class TestLanding(TestBaseCase):
    def test_index_page(self):

        response = self.client.get('/',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)

    def test_landing_page(self):

        response = self.client.get('/home',
                                    content_type='html/text')
        self.assertEqual(200,
                         response.status_code)