"""

Models for storeing data for a basic social media site.

"""

from datetime import datetime
import os
import uuid

from flask_login import UserMixin
from flaskserv.socialnet import db
from werkzeug.security import generate_password_hash

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


if os.environ.get("TESTING"):
    generate_password_hash = lambda x : x


def generate_uuid():
    """

    Function to generate a unique identifier for models.
    :return:
    """
    return uuid.uuid4().hex[:16]

class DataModelMixin(object):
    """

    Mixin class that contains essential creation
    attributes for all the models.

    """
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    uuid = db.Column(db.String, default=generate_uuid, nullable=False)

class User(UserMixin,DataModelMixin,db.Model ):
    """

    Standard User Model contains group memebership and posts.

    """

    #__tablename__ = "users"

    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)

    tribes = relationship('Tribe', backref='tribe_owner')
    posts = relationship('Post', backref='post_owner')

    UniqueConstraint('email', name='unique_constraint_1')


    def __init__(self, name="TestUser",
                 email="Test@Example.com",
                 password="Bad_Password"):
        """

        Enabling hashing of password on the model.

        :param name:
            Name of user
        :param email:
            user's email
        :param password:
            Users plain text password.
        """

        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Tribe(db.Model, DataModelMixin):
    """

    Tribe is an group of users that contains a multisig wallet
    of the members of the group.

    """

    #__tablename__ = "tribes"

    owner_id = db.Column(db.Integer, ForeignKey('user.id'))


    #content
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    posts = relationship('Post', backref='tribe')


    def preview(self):
        """

        A dict for a limited number of parameters.

        """
        return dict(name=self.name,
                    description=self.description,
                    owner_id=self.owner_id,
                    created_date=self.created_date,
                    uuid=self.uuid)



class Post(db.Model, DataModelMixin):
    """

    This will be a standard social media post.

    """

    #__tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)


    owner_id = db.Column(db.Integer, ForeignKey('user.id'))
    tribe_id = db.Column(db.Integer, ForeignKey('tribe.id'))

    #owner from User

    #content
    title = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

    #parent child structure
    parent_id = db.Column(db.Integer, ForeignKey('post.id'))
    children = relationship("Post",
                            backref=backref('parent', remote_side=[id])
                            )


