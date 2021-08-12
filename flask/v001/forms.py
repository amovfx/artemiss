
from mongoengine import Document, EmailField, StringField,  ObjectIdField, ReferenceField, EmbeddedDocumentField, ListField, EmbeddedDocument, IntField
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from wtforms import StringField as SF, TextAreaField, Form
class Organization(Document):
    pass

class Agent(Document):
    """

    Agent Model contains data for a single login and a record of the essential information
    needed for creating tap root bitcoin multi-sig wallets.

    """
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    organizations = ListField(ReferenceField(Organization))
    role = ListField(StringField())

    #This should be replaced on client side, enabled with storing their own node.
    private_key = StringField(required=False) #this needs to be encrypted.
    zpub = StringField(required=False)

    def __repr__(self):
        return f"Agent<{self.email}::{self.password}>"

class Post(Document):
    """
    This model contains all the data for a post.
    """

    title = StringField(required=True)
    content = StringField(required=True)

class Expense(Document):
    """

    This model contains the data to report an expense to the group.

    """
    title = StringField(required=True)
    content = StringField(required=True)
    deny = IntField()
    abstain = IntField()
    approve = IntField()

    #this just might be a transaction id for the group to identify.
    pbst = StringField(required=True)


class policy(Document):
    """

    Policy of the taproot script to consruct.

    """




class Organization(Document):

    """

    This model contains all the data for the data. A template will be built from this.

    """

    name = EmailField(required=True)
    description = StringField(required=True)
    members = ListField(ReferenceField(Agent))

    #group communications
    posts = ListField(ReferenceField(Post))
    expenses = ListField(ReferenceField(Expense))

    #bitcoin info
    public_key = StringField()
    next_public_key = StringField()
    taproot_script = StringField()

    #withdrawl policy stack



OrganizationForm = model_form(Organization,
                              base_class=FlaskForm,
                              only=['name', 'description'])








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
