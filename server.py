from flask import Flask
from flask import Flask, render_template, redirect, flash, session, request, url_for

import jinja2

app = Flask(__name__)

@app.route("/")

def home():
  return render_template("homepage.html")


@app.route("/register")

def register():
  return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

