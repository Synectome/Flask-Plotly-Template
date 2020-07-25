from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, RadioField, SelectMultipleField, \
    TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField #didn't seem to help
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Regexp, Length, Optional
from app.models import User, Project
from app import app, db
from app.privatefunctions import user_list
import re


username_registration_validator = re.compile('[\w]+')


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


def user_query():
    return User.query


class NewProjectForm(FlaskForm):
    project_title = StringField(label="Project Title", validators=[DataRequired(),
                                                                   Regexp(username_registration_validator)])
    description = TextAreaField(label="Enter a Project Description", validators=[DataRequired()])
    members_picks = SelectMultipleField(label="Select Members", choices=[], coerce=int)
    # members_picks = QuerySelectField(query_factory=user_query(), allow_blank=True)
    next = SubmitField(label="Next")

    def validate_project_title(self, project_title):
        title_check = Project.query.filter_by(title=project_title.data).first()
        if title_check is not None:
            raise ValidationError('Please use a different project name.')


class ProjectPermissionsForm(FlaskForm):
    None