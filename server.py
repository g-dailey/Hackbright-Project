
from flask import Flask, jsonify, render_template, redirect, flash, session, request, url_for, g
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import User, TimeSlot, UserTimeSlotMapping, ProgrammingLanguage, UserProgrammingLanguageMapping, Prompt, \
  PairingRequests, connect_to_db, db, PairingStatus, Comment
import jinja2
from forms import SignUpForm, LoginForm, UpdateAccountForm, CommentForm
import json
from flask_bcrypt import Bcrypt
import requests
from flask import make_response
from flask_login import login_user, current_user, logout_user
from random import choice
import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

api_file = "/Users/gedailey/src/hackbright-project/sendgrid_api.json"
cred_file = open(api_file, 'r')
cred_json = json.load(cred_file)
sendgrid_api_key = cred_json["sendggrid_api_key"]

app = Flask(__name__)

bcrypt = Bcrypt(app)
connect_to_db(app)
app.secret_key = "DEV"


animated_gifs = ["https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif",
                "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif",
                "https://media.giphy.com/media/scZPhLqaVOM1qG4lT9/giphy.gif",
                "https://media.giphy.com/media/u2pmTWUi0MXjyrMaVj/giphy.gif",
                "https://media.giphy.com/media/CuuSHzuc0O166MRfjt/giphy.gif",
                "https://media.giphy.com/media/fwbZnTftCXVocKzfxR/giphy.gif",
                "https://media.giphy.com/media/bAQH7WXKqtIBrPs7sR/giphy.gif",
                "https://media.giphy.com/media/MT5UUV1d4CXE2A37Dg/giphy.gif",
                "https://media.giphy.com/media/vzO0Vc8b2VBLi/giphy.gif",
                "https://media.giphy.com/media/dBlZwFc1QjzXseX7aT/giphy.gif",
                "https://media.giphy.com/media/R03zWv5p1oNSQd91EP/giphy.gif",
                "https://media.giphy.com/media/B2591lrr3PHTM4cHuD/giphy.gif",
                "https://media.giphy.com/media/VTtANKl0beDFQRLDTh/giphy.gif",
                "https://media.giphy.com/media/wGEymBvo6FUlR9bbda/giphy.gif"
                ]
@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
  all_users = User.query.all()
  user_email=session.get('email', None)
  all_prompts = Prompt.query.all()
  gifs = animated_gifs
  all_prompts = Prompt.query.all()

  for user in all_users:
    logged_in_user = User.query.filter_by(email= user_email).first()
  return render_template("homepage.html",user_email=user_email, logged_in_user=logged_in_user, all_prompts=all_prompts,gifs=gifs)

@app.route("/register", methods=['GET', 'POST'])
def register():

  form = SignUpForm(request.form)

  if form.validate_on_submit():
    print('***** This is working')
    # bcrypt = Bcrypt(app)
    # hashed_password = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
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

    message = Mail(
        from_email='gulafroz.test@gmail.com',
        to_emails= form.email.data,
        subject='Thank you for Signing up for Coder Lounge!',
        html_content='<strong> Hello! We are so happy you are here! </strong> \
        <p> Time to connect to fellow Programmers and code problems away! </p>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

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

    return render_template('pair_request.html', sent_request_user=sent_request_user, pairing_request_email=pairing_request_email,
                          logged_in_user=logged_in_user)
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
        return redirect(url_for('home'))
    else:
      flash('Login Failed, please check email and password and try again!', 'danger')

  return render_template('login.html', form=form)


@app.route("/pairing/<requestee_user_id>/confirm", methods=['POST'])
def pairing_confirm(requestee_user_id):

  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id
  current_user_email = logged_in_user.email

  pairing_request = PairingRequests.query.filter_by(sender_id=requestee_user_id).\
    filter_by(receiever_id=current_user_id).\
    filter_by(pairing_status=PairingStatus.pending).first()

  pairing_request.pairing_status = PairingStatus.approved

  db.session.commit()

  message = Mail(
      from_email='gulafroz.test@gmail.com',
      to_emails= current_user_email,
      subject='Thank you for Signing up for Coder Lounge!',
      html_content='<strong> Hello! We are so happy you are here! </strong> \
      <p> Time to connect to fellow Programmers and code problems away! </p>')
  # try:
  #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
  #     response = sg.send(message)
  #     print(response.status_code)
  #     print(response.body)
  #     print(response.headers)
  # except Exception as e:


  return redirect('/profile')

@app.route("/pairing/<requestee_user_id>/decline", methods=['POST'])
def pairing_decline(requestee_user_id):

  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id

  pairing_request = PairingRequests.query.filter_by(sender_id=requestee_user_id).\
    filter_by(receiever_id=current_user_id).\
    filter_by(pairing_status=PairingStatus.pending).first()

  pairing_request.pairing_status = PairingStatus.declined
  db.session.commit()

  return redirect('/profile')

@app.route("/pairing/<requestee_user_id>/cancel", methods=['POST'])
def pairing_cancel(requestee_user_id):

  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id

  pairing_request_cancel = PairingRequests.query.filter_by(sender_id=current_user_id).\
    filter_by(receiever_id=requestee_user_id).\
    filter_by(pairing_status=PairingStatus.pending).first()
  db.session.delete(pairing_request_cancel)
  db.session.commit()

  return redirect('/profile')

@app.route("/profile", methods=['GET', 'POST'])
def user_profile():

  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id

  sent_request_data = PairingRequests.query.filter_by(sender_id=current_user_id).\
    filter_by(pairing_status=PairingStatus.pending).all()
  sent_req_user_ids = []
  for sent_request_user in sent_request_data:
    sent_req_user_ids.append(sent_request_user.receiever_id)

  received_request_data = PairingRequests.query.filter_by(receiever_id=current_user_id).\
    filter_by(pairing_status=PairingStatus.pending).all()

  approved_request_data = PairingRequests.query.filter_by(receiever_id=current_user_id).\
    filter_by(pairing_status=PairingStatus.approved).all()

  received_req_user_ids = []
  for recieved_request_user in received_request_data:
    received_req_user_ids.append(recieved_request_user.sender_id)

  approved_req_user_ids = []
  for approved_request_user in approved_request_data:
    approved_req_user_ids.append(approved_request_user.sender_id)

  sent_request_users = User.query.filter(User.user_id.in_(sent_req_user_ids)).all()
  received_request_users = User.query.filter(User.user_id.in_(received_req_user_ids)).all()
  approved_request_users = User.query.filter(User.user_id.in_(approved_req_user_ids)).all()


  return render_template('user_profile.html', logged_in_user=logged_in_user, sent_request_users=sent_request_users,
                        received_request_users=received_request_users,approved_request_users=approved_request_users)

@app.route("/update_account", methods=['GET', 'POST'])
def update_account():
  form = UpdateAccountForm()
  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id
  saved_password = logged_in_user.password

  if request.method == 'POST':
    logged_in_user.first_name = form.first_name.data
    logged_in_user.last_name = form.last_name.data
    # logged_in_user.email = form.email.data
    # logged_in_user.profile_picture = form.profile_picture.data
    logged_in_user.prompt_difficulty_level = form.prompt_difficulty_level.data
    logged_in_user.primary_language = form.primary_language.data
    # logged_in_user.programming_language_label = form.programming_language_label.data
    logged_in_user.timezone_name = form.timezone_name.data
    User.query.filter(User.user_id == current_user_id).update({"first_name": logged_in_user.first_name,
                                                    "last_name": logged_in_user.last_name,
                                                    "prompt_difficulty_level": logged_in_user.prompt_difficulty_level,
                                                    "primary_language": logged_in_user.primary_language,
                                                    "timezone_name": logged_in_user.timezone_name
                                                    },
                                                   synchronize_session=False)


    program_to_delete = UserProgrammingLanguageMapping.query.filter_by(user_id = current_user_id).all()
    for i in program_to_delete:

      db.session.delete(i)
      # db.session.commit()

    for language in form.programming_language_label.data:
        db_language = ProgrammingLanguage.query.filter(ProgrammingLanguage.programming_language_label == language).first()
        prog_lang_mapping = UserProgrammingLanguageMapping(
          user_id = logged_in_user.user_id,
          programming_language_id = db_language.programming_language_id)
        db.session.add(prog_lang_mapping)
    db.session.commit()

    time_delete = UserTimeSlotMapping.query.filter_by(user_id = current_user_id).all()
    for i in time_delete:
      db.session.delete(i)

    for time in form.timeslot_label.data:
        db_time = TimeSlot.query.filter(TimeSlot.timeslot_label == time).first()
        time_mapping = UserTimeSlotMapping(
          user_id = logged_in_user.user_id,
          timeslot_id = db_time.timeslot_id)
        db.session.add(time_mapping)
    db.session.commit()



    flash('Your account has been updated!', 'success')

    return redirect('/profile')
  elif request.method == 'GET':
    form.first_name.data = logged_in_user.first_name
    form.last_name.data = logged_in_user.last_name
    form.email.data = logged_in_user.email
    # form.picture.data = logged_in_user.picture
    form.prompt_difficulty_level.data = logged_in_user.prompt_difficulty_level
    form.primary_language.data = logged_in_user.primary_language
    # for language in form.programming_language_label.data:
    #   db_language = ProgrammingLanguage.query.filter(ProgrammingLanguage.programming_language_label == language).first()
    #   prog_lang_mapping = UserProgrammingLanguageMapping(
    #     user_id = logged_in_user.user_id,
    #     programming_language_id = db_language.programming_language_id)
      # db.session.add(prog_lang_mapping)
    # form.programming_language_label.data = logged_in_user.programming_language_label
    form.timezone_name.data = logged_in_user.timezone_name

  profile_picture = url_for('static', filename="profile_pics/"+logged_in_user.profile_picture)

  return render_template('update_account.html', logged_in_user=logged_in_user, form=form, profile_picture=profile_picture)

@app.route("/dailyprompt", methods=['GET', 'POST'])
def dailyprompt():

  form = CommentForm()

  user_email=session.get('email', None)
  logged_in_user = User.query.filter_by(email= user_email).first()
  current_user_id = logged_in_user.user_id

  all_prompts = Prompt.query.all()
  random_prompt = random.choice(all_prompts)
  prompt_id = random_prompt.prompt_id

  if form.validate_on_submit():
    comment = Comment(body = form.body.data,
                      user_id = current_user_id,
                      post_id = prompt_id )
    db.session.add(comment)
    db.session.commit()

  all_comments = Comment.query.filter_by(post_id = prompt_id)

  commented_users_id = []
  for comment in all_comments:
    commented_users_id.append(comment.user_id)

  commented_users = User.query.filter(User.user_id.in_(commented_users_id)).all()


  # for prompt in all_prompts:
  #   random_prompt_link, random_prompt_name = prompt.prompt_link, prompt.prompt_name

  return render_template('dailyprompt.html', commented_users=commented_users, logged_in_user=logged_in_user, random_prompt=random_prompt, all_prompts=all_prompts, form=form, all_comments = all_comments)


@app.route('/home/users')
def get_users():

  all_users = User.query.all()
  all_prompts = Prompt.query.all()
  user_email = session['email']

  return render_template('user_list.html',all_users=all_users, all_prompts=all_prompts )


@app.route('/logout')
def logout():

  resp = make_response(redirect("/thank-you"))
  resp.set_cookie('session', '')
  return resp

@app.route("/thank-you", methods=['GET', 'POST'])
def thankyou():

  return render_template("thank-you.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
