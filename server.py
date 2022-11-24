
from flask import Flask, jsonify, render_template, redirect, flash, session, request, url_for, g
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import User, TimeSlot, UserTimeSlotMapping, ProgrammingLanguage, UserProgrammingLanguageMapping, Prompt, connect_to_db, db
import jinja2
from forms import SignUpForm, LoginForm, UpdateAccountForm
import json
from flask_bcrypt import Bcrypt
import requests
from flask_mail import Mail, Message
import os
# import smtplib



app = Flask(__name__)
mail = Mail(app)
bcrypt = Bcrypt(app)

connect_to_db(app)

app.secret_key = "DEV"



@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
  all_users = User.query.all()
  user_email=session.get('email', None)

  for user in all_users:
    logged_in_user = User.query.filter_by(email= user_email).first()

  return render_template("homepage.html",user_email=user_email, logged_in_user=logged_in_user )



@app.route("/register", methods=['GET', 'POST'])
def register():
  form = SignUpForm(request.form)

  if form.validate_on_submit():
    print('***** This is working')
    # bcrypt = Bcrypt(app)
    # hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')

    flash(f'Account Created for {form.first_name.data}! You can now login!', 'success') #this success message is not showing

    user = User(email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                primary_language=form.primary_language.data,
                prompt_difficulty_level=form.prompt_difficulty_level.data,
                timezone_name=form.timezone_name.data
              )

    db.session.add(user)
    db.session.commit()

    for language in form.programming_language_label.data:
      db_language = ProgrammingLanguage.query.filter(ProgrammingLanguage.programming_language_label == language).first()
      prog_lang_mapping = UserProgrammingLanguageMapping(
        user_id = user.user_id,
        programming_language_id = db_language.programming_language_id)
      db.session.add(prog_lang_mapping)
    db.session.commit()

    for times in form.timeslot_label.data:

      db_timeslots = TimeSlot.query.filter(TimeSlot.timeslot_label == times).first()
      time_slot_mapping = UserTimeSlotMapping(
        user_id = user.user_id,
        timeslot_id = db_timeslots.timeslot_id)
      db.session.add(time_slot_mapping)
    db.session.commit()


    return redirect(url_for('login'))
  else:
    print(form.errors)
  return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      password = User.query.filter_by(password=form.password.data).first()

      if user and password:
        session['email'] = form.email.data
        user_email = session['email']

        print(session)
        print('#################################')
        return redirect(url_for('home'))
    else:
      flash('Login Failed, please check email and password and try again!', 'danger')

  return render_template('login.html', form=form)



@app.route('/home/users')
def get_users():

  all_users = User.query.all()
  all_prompts = Prompt.query.all()
  user_email = session['email']

  return render_template('user_list.html',all_users=all_users, all_prompts=all_prompts )



@app.route('/home/pairedlist')
def paired_list():

  all_users = User.query.all()
  all_prompts = Prompt.query.all()
  user_email=session.get('email', None)



  logged_in_user = User.query.filter_by(email= user_email).first()

  for language in logged_in_user.programming_languages:
    logged_in_user_language = language.programming_language_name

  matching_users = []
  for user in all_users:
    if logged_in_user_language in [l.programming_language_name for l in user.programming_languages]:
      matching_users.append(user)


  # for user in all_users:
  # matching = True
  # if logged_in_user_language not in [l.name for l in …]:
  #   matching = False
  # if logged_in_user_time_slot not in [t.time_slot_name for t in …]:
  #   matching = False
  # if logged_in_user_timezone != user.timezone:
  #   matching = False

  # if matching:
  #   matching_users.append(user)

  return render_template('user_pairedlist.html', user_email=user_email, logged_in_user=logged_in_user,all_prompts=all_prompts, all_users=matching_users, logged_in_user_language=logged_in_user_language)


@app.route('/logout')
def logout():
  clearning_session = session.clear()

  return render_template('homepage.html', clearning_session=clearning_session)


@app.route("/thank-you", methods=['GET', 'POST'])
def thankyou():

  return render_template("thank-you.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

