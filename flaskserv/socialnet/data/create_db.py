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

def get_random_user():
    """

    Return a random entry of the argument model.
    :param Model:
    :return:
    """
    return random.choice(User.query.all())

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
                      creator=random.choice(users))

        db.session.add(tribe)

    db.session.commit()

def generate_random_post(tribe : Tribe,
                         user=None,
                         parent_comment=None):
    """

    Generate a random post.
    :param user:
        default calls get_random_item
    :param tribe:
    :return:
    """
    if tribe is None:
        raise ValueError("Tribe must be valid")

    child_post = Post(title=lorem.sentence().split(" ")[0],
                      message=lorem.paragraph(),
                      author=user,
                      tribe=tribe,
                      parent=parent_comment)
    return child_post


def generate_discreet_comment_tree(tribe):
    """

    Generates a discreet comment tree in the database.
    :return:
    """


    p1 = generate_random_post(tribe, user=get_random_user())
    p2 = generate_random_post(tribe, user=get_random_user(), parent_comment=p1)
    p3 = generate_random_post(tribe, user=get_random_user(), parent_comment=p1)
    p4 = generate_random_post(tribe, user=get_random_user())
    p5 = generate_random_post(tribe, user=get_random_user(), parent_comment=p4)
    p6 = generate_random_post(tribe, user=get_random_user(), parent_comment=p5)

    posts = [p1,p2,p3,p4,p5,p6]
    for post in posts:
        post.save()

    return posts

if __name__ == '__main__': # pragma: no cover
    """
    
    This is for development only
    
    """
    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()
        generate_users(10)
        admin = User(name="admin",
                     email="admin@example.com",
                     password="admin")
        admin.save()
        generate_tribes(50)
        for tribe in Tribe.query.all()[:3]:
            for _ in range(5):
                generate_discreet_comment_tree(tribe)