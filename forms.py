from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from model import User, Pairing, Meeting, Prompt, TimeSlot, Timezone, Feedback


class SignUpForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
  last_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  #profile picture?
  prompt_difficulty_level = StringField('Prompt Difficulty Level', validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?
  primary_language = StringField('Primary Language', validators=[DataRequired()]) #how to make this a single select field and still exist in this form?
  programming_language = StringField('Programming Language', validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?
  timezone = StringField('Timezone', validators=[DataRequired()]) #how to make this a single select field and still exist in this form?
  #how to make it easy to select slots from day of the week and timeslots quickly rather than manualy entry for every day of the week?
  day_of_week = StringField('Time Slots', validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?
  timeslots = StringField('Time Slots', validators=[DataRequired()]) #how to make this a multiple select field and still exist in this form?



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
