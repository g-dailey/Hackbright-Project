
from flask import Flask, render_template, redirect, flash, session, request, url_for
# from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import User, Pairing,  Prompt, TimeSlot
import jinja2
from forms import SignUpForm, LoginForm, UpdateAccountForm
from model import db
import json

app = Flask(__name__)


app.secret_key = "DEV"

@app.route("/", methods=['GET', 'POST'])
def home():
  return render_template("homepage.html")


# @app.route("/api/v1/user", methods=["POST"])
# def get_data():
#   data = request.json()
#   user_name = data['username']
#   user_name = request.args.get('username')
#   crud.create_user(user_name=user_name)

#   response = {"response_code": 200,
#   "message": "Welcome to the Site"}

#   return jsonify(response)


@app.route("/register", methods=['GET', 'POST'])
def register():
  form = SignUpForm()

  if form.validate_on_submit():
    print(form)
    flash(f'Account Created for {form.first_name.data}!', 'success') #this success message is not showing
    user = User(email=form.email.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                prompt_difficulty_level=form.prompt_difficulty_level.data,
                primary_language=form.primary_language.data,
                programming_language=form.programming_language.data,
                timezone=form.timezone.data,
                day_of_week=form.day_of_week.data,
                timeslots=form.timeslots.data
    )
    db.session.add(user)
    db.session.commit()
    return redirect('thank-you.html')
  return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  return render_template("login.html", form=form)

@app.route("/thank-you", methods=['GET', 'POST'])
def thankyou():

  return render_template("thank-you.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

