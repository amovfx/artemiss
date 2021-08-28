from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class TribeForm(FlaskForm):
    """

    Form for creating a tribe.

    """

    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class PostForm(FlaskForm):
    """

    Form for creating a text post.

    """

    title = StringField('title', validators=[DataRequired()])
    message = StringField('message', validators=[DataRequired(), Length(min=6, max=10000)])

