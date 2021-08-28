import random

from werkzeug.security import generate_password_hash

from flaskserv.socialnet import db, create_app
from flaskserv.socialnet.models import User, Tribe, Post

import names
import lorem

def generate_users(count = 10):
    """

    Function to create three users in the database.

    """
    for i in range(count):
        name = names.get_first_name()
        user = User(name=name,
                    email=f"{name}@example.com",
                    password="bad_password")
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
                      owner_id=random.choice(users).id)

        db.session.add(tribe)

    db.session.commit()

if __name__ == '__main__': # pragma: no cover
    """
    
    This is for development only
    
    """
    app = create_app()
    db.drop_all()
    with app.app_context():

        db.create_all()
        generate_users(10)
        generate_tribes(10)