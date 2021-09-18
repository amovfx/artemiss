"""

Models for storeing data for a basic social media site.

"""

from datetime import datetime
import os
import uuid

from flask_login import UserMixin
from flaskserv.socialnet import db
from werkzeug.security import generate_password_hash

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    Column,
    Integer,
    String,
    DateTime,
    Table,
    Boolean,
)

from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

if os.environ.get("TESTING"):
    generate_password_hash = lambda x: x


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

    created_date = Column(DateTime, default=datetime.utcnow)
    uuid = Column(String, default=generate_uuid, nullable=False)


subs = Table(
    "subs",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("tribe_id", Integer, ForeignKey("tribe.id")),
)

rooms = Table(
    "rooms",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("room_id", Integer, ForeignKey("room.id")),
)


class User(db.Model, DataModelMixin, UserMixin):
    """

    Standard User Model contains group memebership and posts.

    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)

    tribe_creator = relationship("Tribe", backref="creator")

    # coms
    tribe_membership = relationship(
        "Tribe",
        secondary=subs,
        backref=backref("members", lazy="dynamic"),
        lazy="dynamic",
    )

    posts = relationship("Post", backref="author")

    UniqueConstraint("email", name="unique_constraint_1")

    # wallets

    # expenses

    def __init__(
        self,
        name="TestUser",
        email="Test@Example.com",
        password="Bad_Password",
        posts=[],
    ):
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

    def join_tribe(self, tribe):
        """

        Join a tribe.

        :param tribe:
            A tribe ORM.

        """

        if not self.in_tribe(tribe):
            self.tribe_membership.append(tribe)

    def in_tribe(self, tribe):
        """

        Return if this user is a member of this tribe.

        :param tribe:
            A tribe ORM.

        """
        # db.session.query(subs, User, Tribe).
        # return self.tribe_membership.filter(subs.c.tribe_id == tribe.id).count() > 0
        return tribe.members.filter(subs.c.user_id == self.id).count() > 0

    def leave_tribe(self, tribe):
        """

        Remove this user from a tribe.

        :param tribe:
            A tribe ORM.

        """

        if self.in_tribe(tribe):
            self.tribe_membership.remove(tribe)

    def __repr__(self):
        return f"<User {self.id} {self.name} -- {self.email} >"


class Tribe(db.Model, DataModelMixin):
    """

    Tribe is an group of users that contains a multisig wallet
    of the members of the group.

    """

    # __tablename__ = "tribes"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id"))

    # content
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Expenses
    posts = relationship("Post", backref="tribe")

    # Chat
    channels = relationship("Room", backref="channel")

    # Wallet

    def preview(self):
        """

        A dict for a limited number of parameters.

        """
        return dict(
            name=self.name,
            description=self.description,
            owner_id=self.owner_id,
            created_date=self.created_date,
            uuid=self.uuid,
        )

    def save(self):
        """

        Quick save function.
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Tribe {self.id} -- {self.name}>"


class Room(db.Model, DataModelMixin):

    name = Column(String)
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("tribe.id"))

    messages = relationship("Post", backref="room_msgs")


class Post(db.Model, DataModelMixin):
    """

    Model for a post with replys.

    """

    _N = 6

    id = Column(Integer, primary_key=True)
    title = Column(String)
    message = Column(String(1400))

    author_id = Column(Integer, ForeignKey("user.id"))
    tribe_id = Column(Integer, ForeignKey("tribe.id"))

    # chat
    room_id = Column(Integer, ForeignKey("room.id"))

    path = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("post.id"))

    replies = db.relationship(
        "Post", backref=db.backref("parent", remote_side=[id]), lazy="dynamic"
    )

    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.parent.path + "." if self.parent else ""
        self.path = prefix + "{:0{}d}".format(self.id, self._N)
        db.session.commit()

    def level(self):
        return len(self.path) // self._N - 1

    def preview(self, user):
        """

        A dict for a limited number of parameters.

        :param user:
            User orm to populate the author data.

        :return:
            dict of the expanded data.

        """
        return dict(
            title=self.title,
            message=self.message,
            uuid=self.uuid,
            path=self.path,
            author=user.name,
            parent=self.parent_id,
        )


class Permissions(db.Model):
    id = Column(Integer, primary_key=True)
    read = Column(Boolean)
