from mongoengine import Document, EmailField, StringField,  ObjectIdField, ReferenceField, EmbeddedDocumentField, ListField, EmbeddedDocument, IntField
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from flask_login import UserMixin

class Organization(Document):

    """

    This model contains all the data for the data. A template will be built from this.

    """

    name = StringField(required=True)
    description = StringField(required=True)
    creator = ObjectIdField(required=True)

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




OrganizationForm = model_form(Organization,
                              base_class=FlaskForm,
                              only=['name', 'description'])