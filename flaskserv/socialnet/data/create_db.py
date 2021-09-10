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


def generate_comment_tree(tribe,
                          parent_post=None,
                          depth = 3,
                          count = 0):
    """

    Generate a comment tree

    :param tribe:
        The tribe the comments belong to.
    :param parent_post:
        The parent post
    :param count:
        parameter to keep track of depth.
    :return:
    """

    if count < depth:
        range_min = 2 * (2 - count)
        range_max = 5 * (2 - count)

        for _ in range(random.randint(range_min, range_max)):
            print("Creating ")
            rand_user = get_random_user()
            child_post = generate_random_post(rand_user, tribe)

            if parent_post:
                child_post.parent = parent_post

            db.session.add(child_post)

            if random.uniform(0,1) < .2:
                generate_comment_tree(tribe,
                                      parent_post=child_post,
                                      count=count + 1)


    db.session.commit()
    return None

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


def generate_posts_on_first_tribe(count=10):
    """

    This is a helper function to generate
    synthetic data for the first tribe for debug purposes
    :return:
    """

    tribes = Tribe.query.all()
    for tribe in tribes:
        for i in range(count):
            post = generate_random_post(tribe, get_random_user())
            db.session.add(post)
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
        for tribe in Tribe.query.all()[:5]:
            generate_discreet_comment_tree(tribe)