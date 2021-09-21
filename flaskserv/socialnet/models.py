"""

Models for storeing data for a basic social media site.

"""

from datetime import datetime
from enum import Enum, unique
import os
import uuid

from flask_login import UserMixin, current_user
from flaskserv.socialnet import db
from werkzeug.security import generate_password_hash

from sqlalchemy import (
    Enum as SQLEnum,
    ForeignKey,
    UniqueConstraint,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    and_,
    Table,
)

from sqlalchemy.orm import relationship, backref

if os.environ.get("TESTING"):
    generate_password_hash = lambda x: x


def generate_uuid():
    """

    Function to generate a unique identifier for models.
    :return:
    """
    return uuid.uuid4().hex[:16]


@unique
class PERMISSIONS(Enum):
    NONE = 0
    READ = 1
    WRITE = 3
    EXECUTE = 4

    @classmethod
    def unittest_idata_generator(cls):
        for enum_val in cls.__iter__():
            setattr(
                enum_val, "__doc__", f"{enum_val.__class__.__name__}.{enum_val.name}"
            )
            yield enum_val


class DataModelMixin(object):
    """

    Mixin class that contains essential creation
    attributes for all the models.

    """

    created_date = Column(DateTime, default=datetime.utcnow)
    uuid = Column(String, default=generate_uuid, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def foreign_key(cls):
        return ForeignKey(f"{cls.get_name()}.id")

    @classmethod
    def foreign_key_column(cls):
        return Column(f"{cls.get_name()}_id", Integer, cls.foreign_key())


class PermissionsGroup(db.Model, DataModelMixin):
    # many to many relationship
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    tribe_id = Column(ForeignKey("tribe.id"), primary_key=True)
    user = relationship("User", back_populates="tribes")
    tribe = relationship("Tribe", back_populates="users")

    # extra data to describe the relationship
    name = Column(String, nullable=False)
    permissions = Column(
        SQLEnum(PERMISSIONS), default=PERMISSIONS.EXECUTE, nullable=False
    )

    def __init__(self, name, user, tribe, permissions):
        self.name = name
        self.user = user
        self.tribe = tribe
        self.permissions = permissions


class User(db.Model, DataModelMixin, UserMixin):
    """

    Standard User Model contains group memebership and posts.

    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String)

    posts = relationship("Post", backref="author")

    UniqueConstraint("email", name="unique_constraint_1")

    # bi-directional many to many
    tribes = relationship("PermissionsGroup", back_populates="user", lazy="dynamic")

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

    def join_tribe(self, tribe):
        """

        Join a tribe.

        :param tribe:
            A tribe ORM.

        """

        if not self.in_tribe(tribe):
            permissions_group = PermissionsGroup(
                name="applicant", user=self, tribe=tribe, permissions=PERMISSIONS.READ
            )
            permissions_group.save()

    def in_tribe(self, tribe):
        """

                Return if this user is a member of this tribe.
        x
                :param tribe:
                    A tribe ORM.

        """

        return tribe.users.filter(PermissionsGroup.user_id == self.id).count() > 0

    def leave_tribe(self, tribe):
        """

        Remove this user from a tribe.

        :param tribe:
            A tribe ORM.

        """

        if self.in_tribe(tribe):
            self.tribes.remove(tribe)

    def __repr__(self):
        return f"<User {self.id} {self.name} -- {self.email} >"


class Tribe(db.Model, DataModelMixin):
    """

    Tribe is an group of users that contains a multisig wallet
    of the members of the group.

    """

    # __tablename__ = "tribes"
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("user.id"))

    # content
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # bi-directional many to many
    users = relationship("PermissionsGroup", back_populates="tribe", lazy="dynamic")

    # Expenses one to many
    posts = relationship("Post", backref="tribe")

    # Chat one to many
    rooms = relationship("Room", backref="channel")

    # Wallet

    def __init__(self, name, description, creator):
        self.name = name
        self.description = description
        self.creator = creator.id
        self.create_permissions_group(
            name="admin", user=creator, permissions=PERMISSIONS.EXECUTE
        )

        self.save()

        # set permissions

        # self.create_room()

    def preview(self):
        """

        A dict for a limited number of parameters.

        """
        return dict(
            name=self.name,
            description=self.description,
            owner_id=self.creator_id,
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

    def create_permissions_group(self, name, user, permissions=PERMISSIONS.EXECUTE):
        """

        :param name:
        :return:
        """
        permissions_group = PermissionsGroup(
            name=name, user=user, tribe=self, permissions=permissions
        )
        permissions_group.save()

    def create_room(self, user, name):
        pass

    def __repr__(self):
        return f"<Tribe {self.id} -- {self.name}>"


class Room(db.Model, DataModelMixin):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    creator_id = Column(Integer, ForeignKey("user.id"))
    tribe_id = Column(Integer, ForeignKey("tribe.id"))

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
        super().save()
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
