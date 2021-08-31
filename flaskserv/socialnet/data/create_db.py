import random

from werkzeug.security import generate_password_hash

from flaskserv.socialnet import db, create_app
from flaskserv.socialnet.models import User, Tribe, Post

import names
import lorem


def create_random_user():
    """

    Generates a random user for testing.

    :return:
        A user model.
    """
    name = names.get_first_name()
    return User(name=name,
                email=f"{name}@example.com",
                password="testing_password")

def generate_users(count = 10):
    """

    Function to create a number of random users in the database.

    """
    for i in range(count):
        user = create_random_user()
        db.session.add(user)
    db.session.commit()

def generate_tribes(count=10):
    """

    Random Tribe Generator

    """
    users = User.query.all()

    for i in range(count):
        tribe = Tribe(name=f" {i} : {lorem.sentence().split(' ')[0]}",
                      description=lorem.sentence(),
                      owner=random.choice(users))

        db.session.add(tribe)

    db.session.commit()

if __name__ == '__main__': # pragma: no cover
    """
    
    This is for development only
    
    """
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()
        generate_users(10)
        generate_tribes(50)