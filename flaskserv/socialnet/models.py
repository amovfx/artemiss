from flask_login import UserMixin
from flaskserv.socialnet import db
from werkzeug.security import generate_password_hash

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

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

    def __repr__(self):
        return '<name - {}>'.format(self.name)


class Tribe(db.Model):
    """

    Tribe is an group of users that contains a multisig wallet
    of the members of the group.

    """

    #__tablename__ = "tribes"


    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('user.id'))

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)



class Post(db.Model):
    """

    Standard social media post.

    """

    #__tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, ForeignKey('user.id'))

    title = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
