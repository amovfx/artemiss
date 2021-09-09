
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class CommentsForm(FlaskForm):
    author = StringField()
    message = StringField(validators=[DataRequired()])
    parent = IntegerField()


   
    