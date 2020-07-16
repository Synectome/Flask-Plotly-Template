from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Regexp, Length, Optional
from app.models import User
from re import compile

username_registration_validator = compile('[\w]+')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
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
