from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from model import User
# from flask_login import login_user, current_user, logout_user, login_required


class SignUpForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
  last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  #profile picture?
  prompt_difficulty_level = RadioField('Prompt Difficulty Level', choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], validators=[DataRequired()])
  primary_language = SelectField('Primary Language',choices=[('eng', 'English'), ('sp', 'Spanish'), ('fr', 'French'), ('fa', 'Farsi'), ('ge', 'German')], validators=[DataRequired()]) #how to make this a single select field and still exist in this form?
  programming_language = SelectMultipleField('Programming Language', choices=[('C++', 'C++'), ('py', 'Python'), ('js', 'JavaScript'), ('ja', 'Java'), ('text', 'Plain Text')]) #how to make this a multiple select field and still exist in this form?
  timezone_name = SelectField('Timezone', choices=[('1', 'Pacific Time Zone'), ('2', 'Central Time Zone'), ('3', 'Eastern Time Zone'), ('4', 'Alaska Time Zone')], validators=[DataRequired()]) #how to make this a single select field and still exist in this form?
  # how to make it easy to select slots from day of the week and timeslots quickly rather than manualy entry for every day of the week?
  day_of_week = SelectMultipleField('Day of the Week', choices=[('1', 'Sunday'), ('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday')], validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?
  timeslots = SelectMultipleField('Time Slots', choices=[('1', '7am - 10am'), ('2', '10am - 1pm'), ('3', '1pm - 4pm'), ('4', '4m - 7pm'), ('5', '7pm - 10pm'), ('6', '10pm - 12am')], validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?
  submit = SubmitField('Sign Up')

  def validate_email(self, email):

    user = User.query.filter_by(email=email.data).first()

    if user:
      raise ValidationError('That email is taken, please choose a different one.')


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Update')

  def validate_email(self, email):
    #how to validate if email already exists?
    if email.data != email.email:

      user = User.query.filter_by(email=email.data).first()

      if user:
        raise ValidationError('That email is taken, please choose a different one.')
