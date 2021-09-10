
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class CommentsForm(FlaskForm):
    message = StringField(validators=[DataRequired()])



   
    