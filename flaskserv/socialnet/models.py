"""

Models for storeing data for a basic social media site.

"""

from datetime import datetime
from enum import Enum, unique
import functools
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


TribeMembers = Table(
    "tribe_members",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("tribe_id", Integer, ForeignKey("tribe.id")),
    Column("permissions", SQLEnum(PERMISSIONS)),
)

rooms = Table(
    "rooms",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("room_id", Integer, ForeignKey("room.id")),
    Column("permissions", SQLEnum(PERMISSIONS)),
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

    # coms
    tribe_membership = relationship(
        "Tribe",
        secondary=TribeMembers,
        backref=backref("members", lazy="dynamic"),
        lazy="dynamic",
    )
    room_membership = relationship(
        "Room",
        secondary=rooms,
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

    def create_tribe(self, name, description, category):
        tribe = Tribe(name=name, description=description, creator=self)
        tribe.save()
        self.join_tribe(tribe)
        self.set_permissions(tribe, PERMISSIONS.EXECUTE)

    def set_permissions(self, tribe, value):

        db.session.query(TribeMembers).where(
            TribeMembers.c.tribe_id == tribe.id
        ).update(values={"permissions": value})

        db.session.commit()

    def get_permissions(self, tribe):
        return (
            db.session.query(TribeMembers.c.permissions)
            .where(TribeMembers.c.user_id == self.id)
            .scalar()
        )

    def set_group(self, tribe, user):
        pass

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
        x
                :param tribe:
                    A tribe ORM.

        """

        return tribe.members.filter(TribeMembers.c.user_id == self.id).count() > 0

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
    creator_id = Column(Integer, ForeignKey("user.id"))

    # content
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # Expenses one to many
    posts = relationship("Post", backref="tribe")

    # Chat one to many
    rooms = relationship("Room", backref="channel")
    user_groups = relationship("UserGroup", backref="tribe")

    # Wallet

    def __init__(self, name, description, creator):
        self.name = name
        self.description = description
        self.creator = creator.id
        self.members.append(creator)
        self.create_group("admin")

        # set permissions

        # self.create_room()

    def requires_permission(self, func, value):
        @functools.wraps(func)
        def wrapper_decorator(*args, **kwargs):
            if value == current_user.get_permissions():
                func(*args, **kwargs)
            else:
                raise PermissionError("Current User is not an admin")

        return wrapper_decorator

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

    def create_group(self, name):
        """

        :param name:
        :return:
        """
        group = UserGroup(name=name)
        group.save()

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


# class UserTribeData(db.Model):
#     groups = relationship("Post", backref="room_msgs")


class UserGroup(db.Model, DataModelMixin):
    """

    Group attribute for user

    """

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(Integer, default=0, nullable=False)

    tribe_id = Column(Integer, ForeignKey("tribe.id"))

    def __init__(self, name):
        self.name = name
