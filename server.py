
from flask import Flask, jsonify, render_template, redirect, flash, session, request, url_for
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import User, TimeSlot, UserTimeSlotMapping, ProgrammingLanguage, UserProgrammingLanguageMapping, connect_to_db, db
import jinja2
from forms import SignUpForm, LoginForm, UpdateAccountForm
import json

app = Flask(__name__)
connect_to_db(app)

app.secret_key = "DEV"
@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
  return render_template("homepage.html")



@app.route("/register", methods=['GET', 'POST'])
def register():
  form = SignUpForm(request.form)

  if form.validate_on_submit():
    print('***** This is working')

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

    timeslot = TimeSlot(
                day_of_the_week=form.day_of_week.data,
                timeslot_name=form.timeslots.data)
    db.session.add(timeslot)
    db.session.commit()


    timeslotmapping = UserTimeSlotMapping(
      user_id = user.user_id,
      timeslot_id = timeslot.timeslot_id)

    db.session.add(timeslotmapping)
    db.session.commit()

    # programming_lang = ProgrammingLanguage(
    #             programming_language_name=form.programming_language.data)
    # db.session.add(programming_lang)
    # db.session.commit()
    for language in form.programming_language_labels.data:
      print(language)
      db_language = ProgrammingLanguage.query.filter(ProgrammingLanguage.programming_language_label == language).first()
      prog_lang_mapping = UserProgrammingLanguageMapping(
        user_id = user.user_id,
        programming_language_id = db_language.programming_language_id)
      db.session.add(prog_lang_mapping)
    db.session.commit()

    return redirect(url_for('login'))
  return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      password = User.query.filter_by(password=form.password.data).first()

      return redirect(url_for('home'))
    else:
      flash('Login Failed, please check email and password and try again!', 'danger')

  return render_template('login.html', form=form)

# route for pairing info:
# pair the user based on info selected.

@app.route('/home/users')
def get_users():
  # test = request("https://leetcode.com/problems/random-one-question/all")
  users = User.query.all()
  for user in users:
    print(user.programming_languages)
  return render_template('user_list.html', users=users)



  return render_template('user_list.html', test=test)

    # users = User.query.all()
    # return jsonify({user.email: [user.first_name, user.last_name, user.timezone_name,
    #                 user.primary_language, user.prompt_difficulty_level] for user in users})

  #for user in users:
  #   print(user.ProgrammingLanguage[relationshipname].programming_language)
  # return render_template()

# @app.route('/home/users/<email>')
# def get_melon(email):

#     users = User.query.get(email)
#     return jsonify(users.to_dict())

@app.route("/thank-you", methods=['GET', 'POST'])
def thankyou():

  return render_template("thank-you.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

