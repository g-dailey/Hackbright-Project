
from flask import Flask, render_template, redirect, flash, session, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model import User, Pairing, Meeting, Prompt, TimeSlot, Timezone, Feedback
import jinja2

app = Flask(__name__)


app.secret_key = "DEV"

@app.route("/", methods=['GET', 'POST'])

def home():
  return render_template("homepage.html")


@app.route("/register", methods=['GET', 'POST'])

def register():
  name = session.get("name")
  if request.method == 'POST':
      name = session.get("name")
      session['name'] = name
      return f"<h1> {name} </h1>"
  return render_template("register.html")


@app.route("/form-signup", methods=['GET', 'POST'])
def get_name():
    name = request.form['name']
    session['name'] = name
    return redirect('register.html')


@app.route("/login", methods=['GET', 'POST'])

def login():
  return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

