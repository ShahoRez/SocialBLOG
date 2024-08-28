# users/forms.py

from flask_wtf import FlaskForm
from blog.models import User
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileAllowed, FileField


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegistrationForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("pass_confirm", message="Passwords must be matches"),
        ],
    )
    pass_confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired()]
        )
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken.")


class UpdateUserForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    profile_image = FileField(
        'Update profile picture',
        validators=[FileAllowed(['jpg', 'png'])]
        )
    submit = SubmitField("Update")
