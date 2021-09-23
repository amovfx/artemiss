from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

class TribeForm(FlaskForm):
    """

    Form for creating a tribe.

    """

    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField("submit")


class PostForm(FlaskForm):
    """

    Form for creating a text post.

    """

    title = StringField('title', validators=[DataRequired()])
    message = StringField('message', validators=[DataRequired(), Length(min=2, max=10000)])


class CommentReplyForm(FlaskForm):
    """

    Form for replying to comments.

    """
    parent_uuid = HiddenField('parent_uuid', validators=[DataRequired()])
    reply = StringField('reply',validators=[DataRequired(),Length(min=6, max=10000)])
    submit = SubmitField('Submit')





