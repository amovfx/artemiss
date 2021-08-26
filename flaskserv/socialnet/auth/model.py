from flask_login import UserMixin
from flaskserv.socialnet import db
from werkzeug.security import generate_password_hash

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    #posts = relationship("BlogPost", backref="author")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<name - {}>'.format(self.name)