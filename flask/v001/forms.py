from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=32)])
    submit = SubmitField('Submit')

class RegistrationForm(LoginForm):
    verify = PasswordField('Verify Password', validators=[DataRequired(), Length(min=5, max=32)])