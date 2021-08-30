from flask_nav import Nav
from flask_nav.elements import Text, Navbar, View, RawTag
from dominate import tags
from flask_bootstrap.nav import BootstrapRenderer



navbar = Navbar(
    "Artemiss",
    #View('About', 'landing.about'),
    #View('Culture', 'landing.culture'),
    View('Login', 'auth.login'),
    View('Register', 'auth.register')
)

