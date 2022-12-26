
from flask import Flask, jsonify, render_template, redirect, flash, session, request, url_for, g
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import User, TimeSlot, UserTimeSlotMapping, ProgrammingLanguage, UserProgrammingLanguageMapping, Prompt, PairingRequests, connect_to_db, db, PairingStatus
import jinja2
from forms import SignUpForm, LoginForm, UpdateAccountForm
import json
from flask_bcrypt import Bcrypt
import requests
from flask import make_response

from flask_login import login_user, current_user, logout_user
import os
from random import choice

app = Flask(__name__)

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

  # if current_user.is_authenticated:
  #   return redirect(url_for('home'))
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


@app.route("/pair_request", methods=['GET', 'POST'])
def pair_request():

  user_email=session.get('email', None)

  logged_in_user = User.query.filter_by(email= user_email).first()

  if request.method == 'POST':
    pairing_request_email = request.form.get("user_email")
    session['user_email'] = pairing_request_email
    sender_user = User.query.filter_by(email=user_email).first()
    sender_user_id = sender_user.user_id
    receiver_user = User.query.filter_by(email=pairing_request_email).first()
    pairing_request_db = PairingRequests(sender_id=sender_user.user_id,
            receiever_id=receiver_user.user_id)

    db.session.add(pairing_request_db)
    db.session.commit()

    paired_request_data = PairingRequests.query.filter_by(sender_id=sender_user_id).all()
    paired_req_receiver_id = []
    for paired_request_user in paired_request_data:
      paired_req_receiver_id.append(paired_request_user.receiever_id)

    sent_request_user = User.query.filter(User.user_id.in_(paired_req_receiver_id)).all()

    return render_template('pair_request.html', sent_request_user=sent_request_user, pairing_request_email=pairing_request_email, logged_in_user=logged_in_user)
  else:
    return render_template('homepage.html', pairing_request_email=pairing_request_email, logged_in_user=logged_in_user)


@app.route('/pairedlist')
def paired_list():

  all_users = User.query.all()
  all_prompts = Prompt.query.all()

  for prompt in all_prompts:
    random_prompt_link, random_prompt_name = prompt.prompt_link, prompt.prompt_name

  user_email=session.get('email', None)

  logged_in_user = User.query.filter_by(email= user_email).first()
  sender_user_id = logged_in_user.user_id
  logged_in_user_languages = set()

  paired_request_data = PairingRequests.query.filter_by(sender_id=sender_user_id).all()
  paired_req_receiver_id = []
  for paired_request_user in paired_request_data:
    paired_req_receiver_id.append(paired_request_user.receiever_id)

  sent_request_user = User.query.filter(User.user_id.in_(paired_req_receiver_id)).all()



  for language in logged_in_user.programming_languages:
    logged_in_user_languages.add(language.programming_language_name)
  for timeslot in logged_in_user.selected_timeslots:
    logged_in_user_timeslot = timeslot.timeslot_name
  for prompt in all_prompts:
    selected_prompts_name = prompt.prompt_name
    selected_prompt_link = prompt.prompt_link
    # selected_prompt_diff_level = prompt.prompt_difficulty
  # for timezone in logged_in_user.timezone_name:
  #   logged_in_user_timezone = timezone.timezones

  matching_users = []
  for user in all_users:
    matching = True
    if user not in sent_request_user:
      if user != logged_in_user:

        if not logged_in_user_languages.intersection((l.programming_language_name for l in user.programming_languages)):
          matching = False
        elif logged_in_user_timeslot not in [l.timeslot_name for l in user.selected_timeslots]:
          matching = False

        # elif logged_in_user_timezone != user.timezone:
        #   matching = False
        if matching:
          matching_users.append(user)

  return render_template('user_pairedlist.html', user_email=user_email, logged_in_user=logged_in_user,
                        all_users=matching_users, logged_in_user_languages=logged_in_user_languages,
                        all_prompts=all_prompts, random_prompt_link=random_prompt_link, random_prompt_name=random_prompt_name)


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
        return redirect(url_for('user_profile'))
    else:
      flash('Login Failed, please check email and password and try again!', 'danger')

  return render_template('login.html', form=form)


@app.route("/pairing/<requestee_user_id>/confirm", methods=['POST'])
def pairing_confirm(requestee_user_id):

  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id

  pairing_request = PairingRequests.query.filter_by(sender_id=requestee_user_id).\
    filter_by(receiever_id=current_user_id).\
    filter_by(pairing_status=PairingStatus.pending).first()

  pairing_request.pairing_status = PairingStatus.approved
  db.session.commit()

  return redirect('/profile')


@app.route("/profile", methods=['GET', 'POST'])
def user_profile():

  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id

  sent_request_data = PairingRequests.query.filter_by(sender_id=current_user_id).filter_by(pairing_status=PairingStatus.pending).all()
  sent_req_user_ids = []
  for sent_request_user in sent_request_data:
    sent_req_user_ids.append(sent_request_user.receiever_id)

  received_request_data = PairingRequests.query.filter_by(receiever_id=current_user_id).filter_by(pairing_status=PairingStatus.pending).all()

  received_req_user_ids = []
  for recieved_request_user in received_request_data:
    received_req_user_ids.append(recieved_request_user.sender_id)


  # paired_req_receiver_id = []
  # paired_con_reciever_id = []

  # for paired_request_user in paired_request_data:
  #   if paired_request_user.pairing_status:
  #     paired_req_receiver_id.append(paired_request_user.sender_id)
  #   else :
  #     paired_con_reciever_id.append(paired_request_user.sender_id)

  sent_request_users = User.query.filter(User.user_id.in_(sent_req_user_ids)).all()
  received_request_users = User.query.filter(User.user_id.in_(received_req_user_ids)).all()

  # pending_user = User.query.filter(User.user_id.in_(paired_req_receiver_id)).all()


  return render_template('user_profile.html', logged_in_user=logged_in_user, sent_request_users=sent_request_users, received_request_users=received_request_users )


@app.route('/home/users')
def get_users():

  all_users = User.query.all()
  all_prompts = Prompt.query.all()
  user_email = session['email']

  return render_template('user_list.html',all_users=all_users, all_prompts=all_prompts )


@app.route('/logout')
def logout():
  # logout_user()

  resp = make_response(redirect("/home"))
  resp.set_cookie('session', '')
  return resp

  # clearing_session = session.clear()

  # return redirect('/home', clearing_session=clearing_session)


@app.route("/thank-you", methods=['GET', 'POST'])
def thankyou():

  return render_template("thank-you.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

