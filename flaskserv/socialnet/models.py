"""

Models for storeing data for a basic social media site.

"""

from datetime import datetime
import os
import uuid

from flask_login import UserMixin
from flaskserv.socialnet import db
from werkzeug.security import generate_password_hash

from sqlalchemy import (ForeignKey,
                        UniqueConstraint,
                        Column,
                        Integer,
                        String,
                        DateTime)

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection

Base = declarative_base()

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
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    uuid = Column(String, default=generate_uuid, nullable=False)

class User(db.Model, DataModelMixin):
    """

    Standard User Model contains group memebership and posts.

    """

    __tablename__ = 'user'

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)

    tribes = relationship('Tribe', backref='creator')
    posts = relationship('Post', backref='author')

    UniqueConstraint('email', name='unique_constraint_1')


    def __init__(self, name="TestUser",
                 email="Test@Example.com",
                 password="Bad_Password",
                 posts=[]):
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
        self.posts = posts

    def save(self):
        db.session.add(self)
        db.session.commit()


class Tribe(db.Model, DataModelMixin):
    """

    Tribe is an group of users that contains a multisig wallet
    of the members of the group.

    """

    #__tablename__ = "tribes"

    owner_id = Column(Integer, ForeignKey('user.id'))


    #content
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

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


    def save(self):
        """

        Quick save function.
        :return:
        """
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    """

    Model for a post with replys.

    """
    _N = 6

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    message = Column(String(1400))

    author_id = Column(Integer, ForeignKey('user.id'))
    tribe_id = Column(Integer, ForeignKey('tribe.id'))

    path = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('post.id'))

    replies = db.relationship(
        'Post', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        db.session.commit()

    def level(self):
        return len(self.path) // self._N - 1