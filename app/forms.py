from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, EmailField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password')])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateChannelForm(FlaskForm):
    number = StringField('Number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    logo = FileField('Logo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    description = StringField('Description', validators=[DataRequired()])
    pack = SelectField('Pack', choices=[], render_kw={'class': 'form-control'})
    submit = SubmitField('Create Channel')


class CreatePackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Pack')


