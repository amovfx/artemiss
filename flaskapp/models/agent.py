

from mongoengine import Document, EmailField, StringField,  ObjectIdField, ReferenceField, EmbeddedDocumentField, ListField, EmbeddedDocument, IntField
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from flask_login import UserMixin


class Organization(Document):
    pass


class Agent(Document, UserMixin):
    """

    Agent Model contains data for a single login and a record of the essential information
    needed for creating tap root bitcoin multi-sig wallets.

    """
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    organizations = ListField(ReferenceField(Organization))
    role = ListField(StringField())

    #This should be replaced on client side, enabled with storing their own node.
    private_key = StringField(required=False) #this needs to be encrypted.
    zpub = StringField(required=False)

    def __repr__(self):
        return f"Agent<{self.email}::{self.password}>"

    meta = {"collection": "agents"}

AgentForm = model_form(Agent,
                       base_class=FlaskForm,
                       only=['email', 'password'])
