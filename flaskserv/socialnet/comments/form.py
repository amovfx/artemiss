
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class CommentsForm(FlaskForm):
    message = TextAreaField(validators=[DataRequired()], render_kw={"placeholder": "Reply"})
    submit = SubmitField("Reply")
    cancel = SubmitField("Cancel")



   
    