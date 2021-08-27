from flaskserv.socialnet.test_base import TestBaseCase
from flaskserv.socialnet.browser.form import TribeForm, PostForm

class TestBrowser(TestBaseCase):
    """

    Test base case

    """

    def setUP(self):
        super().setUp()
        self.post_data = {}

    def test_tribe_form(self):
        tribe_form = TribeForm(name="Test",
                               description="Lame ass description")

        self.assertTrue(tribe_form.validate())


    def test_post_form(self):
        post_form = PostForm(title="The title",
                             message="The message")

        self.assertTrue(post_form.validate())





