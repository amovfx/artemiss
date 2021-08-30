
import os
import uuid

from datetime import datetime

from flask_login import UserMixin
from flaskserv.socialnet import db
from werkzeug.security import generate_password_hash
if os.environ.get("TESTING"):
    generate_password_hash = lambda x : x

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


def generate_uuid():
    return uuid.uuid4().hex[:16]

class User(db.Model, UserMixin):
    """

    Standard User Model contains group memebership and posts.

    """

    #__tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)

    tribes = relationship('Tribe', backref='owner')
    posts = relationship('Post', backref='owner')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)


class Tribe(db.Model):
    """

    Tribe is an group of users that contains a multisig wallet
    of the members of the group.

    """

    #__tablename__ = "tribes"


    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    uuid = db.Column(db.String, default=generate_uuid, nullable=False)

    #content
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)








    # def __init__(self):
    #     """
    #     Ingest a flask form, set user to current_user
    #     """
    #     pass

    def preview(self):
        """

        A dict for a limited number of parameters.

        """
        return dict(name=self.name,
                    description=self.description,
                    owner_id=self.owner_id,
                    created_date=self.created_date,
                    uuid=self.uuid)



class Post(db.Model):
    """

    Standard social media post.

    """

    #__tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    #content
    title = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
