from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from model import User
import pandas as pd
from flask_login import current_user
import csv
import pytz

user_filename = 'User-data.csv'
# from flask_login import login_user, current_user, logout_user, login_required


class SignUpForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
  last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  #profile picture?
  prompt_difficulty_level = RadioField('Prompt Difficulty Level', choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], validators=[DataRequired()])
  primary_language = SelectField('Primary Language',choices=[('eng', 'English'), ('sp', 'Spanish'), ('fr', 'French'), ('fa', 'Farsi'), ('ge', 'German')], validators=[DataRequired()]) #how to make this a single select field and still exist in this form?
  programming_language_label = SelectMultipleField('Programming Language', choices=[('C++', 'C++'), ('py', 'Python'), ('js', 'JavaScript'), ('ja', 'Java'), ('C', 'C')]) #how to make this a multiple select field and still exist in this form?

  timezone_name = SelectField('Timezone', choices=pytz.all_timezones, validators=[DataRequired()]) #how to make this a single select field and still exist in this form?

  # day_of_week = SelectMultipleField('Day of the Week', choices=[('1', 'Sunday'), ('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday'), ('5', 'Thursday'), ('6', 'Friday'), ('7', 'Saturday')], validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?
  timeslot_label = SelectMultipleField('Time Slots', choices=[('7am', '7am - 10am'), ('10am', '10am - 1pm'), ('1pm', '1pm - 4pm'), ('4pm', '4pm - 7pm'), ('7pm', '7pm - 10pm'), ('10pm', '10pm - 12am')], validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?
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
