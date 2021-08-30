from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """

    Standard login form.

    """
    name = StringField('name',
                       validators=[DataRequired()])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    submit = SubmitField(
        "Submit"
    )

class RegisterForm(FlaskForm):
    """

    Standard registration form.

    """

    name = StringField(
        'name',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        'email',
        validators=[DataRequired(),
                    Email(message=None),
                    Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(),
                    Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField(
        "Submit"
    )