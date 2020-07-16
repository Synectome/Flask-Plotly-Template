from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Regexp, Length, Optional
from app.models import User
import re

username_registration_validator = re.compile('[\w]+')

def user_list():
    '''querys the User table to generate options
    as a list of (value, label) pairs, to be used in the choices argument of
    radio and select fields in forms'''
    # '<User {}>' ~> the user __repr__
    username = User.query.all()
    # takes each user__repr__, splits by the space, then splits by the >, returns only the username
    username_list = [name.split()[1].split('>')[0] for name in username]
    key_name_pairs = []
    for i in range(len(username_list)):
        pair = (i, username_list[i])
        key_name_pairs.append(pair)
    return key_name_pairs


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15),
                                                   Regexp(username_registration_validator)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UploadForm(FlaskForm):
    file = FileField("Select File", validators=[DataRequired()])
    project_or_user = RadioField(label='Choose where to save file.',
                                 choices=[('0', 'Personal User Space'),
                                          ('1', 'Specific Project')])
    project_name = StringField('Project Name', validators=[Optional()])
    submit = SubmitField('Upload File')


class NewProjectForm(FlaskForm):
    project_title = StringField(label="Project Title", validators=[DataRequired(),
                                                                   Regexp(username_registration_validator)])
    members = SelectMultipleField(label="members", validators=[DataRequired()], choices=user_list())
    next = SubmitField(label="Next")

