
from mongoengine import Document, StringField, EmbeddedDocumentField, ListField, IntField
from flask_mongoengine.wtf import model_form


class Organization(Document):
    public_key = StringField()


class Agent(Document):
    email = StringField(required=True)


class Account(Document):
    agent = EmbeddedDocumentField(Agent)
    organizations = ListField(EmbeddedDocumentField(Organization))
    private_key = StringField(required=True)



class Post(Document):
    message = StringField(required=True)
    user = EmbeddedDocumentField(Agent)
    org = EmbeddedDocumentField(Organization)


class Request(Post):
    psbt = StringField()


AgentForm = model_form(Agent)
OrganizationForm = model_form(Organization)
