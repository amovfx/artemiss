"""

Models for storeing data for a basic social media site.

"""

from datetime import datetime
from enum import Enum, unique
import os
import uuid

from .constants import *

import lorem
import names
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


join_table = Table(
    "association",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("tribe_id", ForeignKey("tribe.id"), primary_key=True),
)


class PermissionsGroup(db.Model, DataModelMixin):
    """

    Association Object pattern.
    This allows us to treat a relationship between a user and a tribe
    as an object and store custom data.


    """
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    tribe_id = Column(ForeignKey("tribe.id"))
    user = relationship("User", back_populates="tribes")
    tribe = relationship("Tribe", back_populates="users")

    # extra data to describe the relationship, permissions restrict access.
    name = Column(String, nullable=True)
    permissions = Column(SQLEnum(PERMISSIONS), default=PERMISSIONS.NONE, nullable=False)

    @classmethod
    def is_user_in_tribe(cls, user, tribe):
        return (
            db.session.query(PermissionsGroup)
            .filter(PermissionsGroup.user_id == user.id)
            .filter(PermissionsGroup.tribe_id == tribe.id)
            .count()
        ) > 0

    @classmethod
    def get_tribe_user_permissions(cls, user, tribe):
        """

        Get the permissions of the user in the tribe

        :param user:
            sql orm
        :param tribe:
            sql orm
        :return: Enum(PERMISSION)

        """
        user_permissions = (
            db.session.query(PermissionsGroup)
            .filter(
                and_(
                    PermissionsGroup.user_id == user.id,
                    PermissionsGroup.tribe_id == tribe.id,
                )
            )
            .first()
        )
        return user_permissions.permissions

    @classmethod
    def set_tribe_user_permissions(cls, user, tribe, permissions):
        """

        Set the permissions of the user in the tribe to permissions.

        :param user:
            User orm
        :param tribe:
            Tribe orm
        :param permissions:
            Enum.PERMISSIONS

        """
        (
            db.session.query(PermissionsGroup)
            .where(
                and_(
                    PermissionsGroup.user_id == user.id,
                    PermissionsGroup.tribe_id == tribe.id,
                )
            )
            .update(values={"permissions": permissions})
        )

    def __init__(self, name, permissions=PERMISSIONS.NONE, save=True):
        """

        Create a new permissions group if user is not already in the tribe.

        :param name:
            The name of the permissions group. Something like "admin", "mod"
        :param user:
            User orm
        :param tribe:
            Tribe orm
        :param permissions:
            Enum(PERMISSIONS)
        :param save:
            bool to not save if you want to adjust settings past initialization.
        """
        self.name = name
        self.permissions = permissions

        if save:
            self.save()

    def __repr__(self):
        return f"< PermissionsGroup: {self.name} -- {self.user_id} - {self.tribe_id} -- {self.permissions.name}>"


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

    tribes = relationship("PermissionsGroup", back_populates="user", lazy="dynamic")

    # trust self relationship that allows people to automatically approve expenditures.

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
        self.save()

    def join_tribe(self, tribe, permission_group_name, permissions=PERMISSIONS.NONE):
        """

        Join a tribe.

        :param tribe:
            A tribe ORM.

        """

        if not self.is_in_tribe(tribe):
            pg = PermissionsGroup(name=permission_group_name, permissions=permissions)
            pg.tribe = tribe
            self.tribes.append(pg)



    def is_in_tribe(self, tribe):
        """

        Return if this user is a member of this tribe.

        :param tribe:
            A tribe ORM.

        """

        return (
            tribe.users.filter(PermissionsGroup.user_id == self.id).count()
            > 0
        )

    def leave_tribe(self, tribe):
        """

        Remove this user from a tribe.

        :param tribe:
            A tribe ORM.

        """

        if self.is_in_tribe(tribe):
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
    users = relationship(
        "PermissionsGroup", back_populates="tribe", lazy="dynamic"
    )

    # Expenses one to many
    posts = relationship("Post", backref="tribe")

    # Chat one to many
    rooms = relationship("Room", backref="channel")

    # Wallet

    @classmethod
    def create_test_tribe(cls):
        return cls.__init__(name=lorem.sentence().split())

    def __init__(self, name, description, creator, save=True):
        self.name = name
        self.description = description
        creator.save()
        self.creator = creator.id

        self.add_user(creator, "admin", PERMISSIONS.EXECUTE)

        if save:
            self.save()

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

    def add_user(self, user, permission_group_name, permissions):
        pg = PermissionsGroup(name=permission_group_name, permissions=permissions)
        pg.user = user
        self.users.append(pg)


    def create_permissions_group(self, name, user, permissions=PERMISSIONS.EXECUTE):
        """

        :param name:
        :return:
        """
        permissions_group = PermissionsGroup(
            name=name, user=user, tribe=self, permissions=permissions
        )
        permissions_group.save()

    def get_user_permissions(self, user):
        return PermissionsGroup.get_tribe_user_permissions(user, self)

    def update_user_permissions(self, user):
        pass

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
