from dataclasses import dataclass, asdict

from flask import make_response, jsonify

from mongoengine import Document, EmailField, StringField,  ObjectIdField, ReferenceField, EmbeddedDocumentField, ListField, EmbeddedDocument, IntField
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from flask_login import UserMixin

class Agent(Document):
    pass

class Post(Document):
    pass

class Expense(Document):
    pass




class Organization(Document):

    """

    This model contains all the data for the data. A template will be built from this.

    """

    name = StringField(required=True)
    description = StringField(required=True)
    creator = ObjectIdField()

    #group communications
    members = ListField(ReferenceField(Agent))
    posts = ListField(ReferenceField(Post))
    expenses = ListField(ReferenceField(Expense))

    #bitcoin info
    public_key = StringField()
    next_public_key = StringField()
    taproot_script = StringField()

    #withdrawl policy stack
    meta = {"collection": "orgs"}

@dataclass
class OrganizationLiteResponse():
    """

    This is an object that trims out a bunch of unneccessary data in a response.
    and makes reading the data a little bit more easiser for the organization_broswer.
    TODO: turn this into a factory object like model_form.


    """

    id: str
    name: str
    description: str

    def __init__(self, Org):
        self.id = str(Org.id)
        self.name = Org.name
        self.description = Org.description




OrganizationForm = model_form(Organization,
                              base_class=FlaskForm,
                              only=['name', 'description'])


