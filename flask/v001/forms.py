
from mongoengine import Document, StringField, EmbeddedDocumentField, ListField, EmbeddedDocument, IntField
from flask_mongoengine.wtf import model_form


class Organization(EmbeddedDocument):
    public_key = StringField()


class Agent(Document):
    email = StringField(required=True)
    password = StringField(required=True)

    def __repr__(self):
        return f"Agent<{self.email}::{self.password}>"


# class Account(Document):
#     agent = EmbeddedDocumentField(Agent)
#     organizations = ListField(EmbeddedDocumentField(Organization))
#     private_key = StringField(required=True)
#
#
#
# class Post(Document):
#     message = StringField(required=True)
#     user = EmbeddedDocumentField(Agent)
#     org = EmbeddedDocumentField(Organization)
