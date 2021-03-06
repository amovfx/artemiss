from flaskserv.socialnet.tests.test_base import TestBaseCase

class TestLandingRoutes(TestBaseCase):
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