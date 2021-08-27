from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, Length

class TribeForm(FlaskForm):
    """

    Form for creating a tribe.

    """

    name = TextField('name', validators=[DataRequired()])
    description = TextField('description', validators=[DataRequired()])


class PostForm(FlaskForm):
    """

    Form for creating a text post.

    """

    title = TextField('title', validators=[DataRequired()])
    message = TextField('message', validators=[DataRequired(), Length(min=6, max=10000)])

