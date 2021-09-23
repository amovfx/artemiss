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

if os.environ.get("TESTING"):
    generate_password_hash = lambda x: x

from sqlalchemy import (
    Enum as SQLEnum,
    ForeignKey,
    UniqueConstraint,
    Column,
    Integer,
    String,
    DateTime,
    and_,
)

from sqlalchemy.orm import relationship


class DataModelMixin(object):
    """

    Mixin class that contains essential creation
    attributes for all the models.

    """

    created_date = Column(DateTime, default=datetime.utcnow)
    uuid = Column(String, default=lambda: uuid.uuid4().hex[:16], nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
        """

        Checks the user to see is in the tribe.

        :param user:
            USER orm.
        :param tribe:
            Tribe. ORM
        :return:
            True if count is greater than 0 False if otherise.

        """
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

        return tribe.users.filter(PermissionsGroup.user_id == self.id).count() > 0

    def leave_tribe(self, tribe):
        """

        Remove this user from a tribe.

        :param tribe:
            A tribe ORM.

        """

        if self.is_in_tribe(tribe):
            permissions_group = tribe.users.filter(
                PermissionsGroup.user_id == self.id
            ).first()
            tribe.users.remove(permissions_group)

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

    def __init__(self, name, description, creator, save=True):
        """

        Create a new tribe. This is a collection of users. Tribes can also form tribes.
        THis is where people create a joint escrow.

        :param name:
            Name of the tribe
        :param description:
            A short description of what the tribe is about.

        :param creator:
        :param save:
        """
        self.name = name
        self.description = description
        self.creator_id = creator.id

        self.add_user(creator, "admin", PERMISSIONS.EXECUTE)

        if save:
            self.save()

    def add_user(
        self,
        user: User,
        permission_group_name: str = "applicant",
        permissions: PERMISSIONS = PERMISSIONS.NONE,
    ):
        """

        Creates a permissions group and appends it to users.
        :param user:
            User orm
        :param permission_group_name:
            name of the permissions group
        :param permissions:
            Enum(PERMISSIONS)
        :return:
        """
        pg = PermissionsGroup(name=permission_group_name, permissions=permissions)
        pg.user = user
        self.users.append(pg)

    def get_users(self, custom_filter=None):
        """

        Return the users with their permissions group that are in this tribe.

        :param custom_filter:
            A custom filter that can be used on the query.

        :return:
        """
        conditional = PermissionsGroup.tribe_id == self.id
        custom_conditional = and_(conditional, custom_filter)
        condition = conditional if custom_filter is None else custom_conditional

        q = (
            db.session.query(User, PermissionsGroup)
            .join(PermissionsGroup, PermissionsGroup.user_id == User.id)
            .filter(condition)
            .order_by(PermissionsGroup.permissions)
        )

        return q

    def get_user_permissions(self, user: User):
        """

        Return the permissions of the user for this tribe.

        :param user:
            User orm
        :return:
            Enum(PERMISSIONS)
        """
        return PermissionsGroup.get_tribe_user_permissions(user, self)

    def set_user_permissions(self, user: User, permissions: PERMISSIONS):
        """

        Set the user permissions for this tribe.

        :param user:
            User orm.
        :param permissions:
            Enum(PERMISSIONS)

        """
        PermissionsGroup.set_tribe_user_permissions(user, self, permissions)

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
