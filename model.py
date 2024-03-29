from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship, Session
from flask_bcrypt import Bcrypt
import pandas as pd
import csv
from flask_login import LoginManager
import enum
from sqlalchemy import Integer, Enum
import os
from os import listdir
from random import choice
import random




# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri="postgresql:///coder-lounge", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = True
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    bcrypt = Bcrypt(flask_app)
    # login_manager = LoginManager(flask_app)
    db.app = flask_app
    db.init_app(flask_app)
    print("You have been connected to the db")



def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique= True)
    password = db.Column(db.String)
    profile_picture = db.Column(db.String, default="default-image.jpeg")
    prompt_difficulty_level = db.Column(db.String)
    primary_language = db.Column(db.String)
    timezone_name = db.Column(db.String)
    programming_languages = relationship('ProgrammingLanguage', secondary='users_programming_language_mapping', back_populates='users')
    selected_timeslots = relationship('TimeSlot', secondary='users_timeslot_mapping', back_populates='users_timeslots')
    prompts_assigned = relationship('Prompt', back_populates='user_prompts')

    def __repr__(self):
        return f'<User user_id={self.user_id} first_name={self.first_name} last_name={self.last_name} email={self.email}>'


class ProgrammingLanguage(db.Model):
    __tablename__ = "programming_languages"

    programming_language_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)

    programming_language_name = db.Column(db.String)
    programming_language_label = db.Column(db.String)
    users = relationship('User', secondary='users_programming_language_mapping', back_populates='programming_languages')


    def __repr__(self):
        return f'<Programming Language programming_language_id={self.programming_language_id} programming_language_name={self.programming_language_name}>'

class UserProgrammingLanguageMapping(db.Model):
    __tablename__ = "users_programming_language_mapping"

    user_programming_language_mapping_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    programming_language_id = db.Column(db.Integer, db.ForeignKey("programming_languages.programming_language_id"))


    def __repr__(self):
        return f'<Programming Language Mapping user_programming_language_mapping_id={self.user_programming_language_mapping_id} programming_language_id={self.programming_language_id}>'



class TimeSlot(db.Model):
    __tablename__ = "timeslots"

    timeslot_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    timeslot_name = db.Column(db.String)
    timeslot_label = db.Column(db.String)
    # day_of_the_week = db.Column(db.String)
    users_timeslots = relationship('User', secondary='users_timeslot_mapping', back_populates='selected_timeslots')

    def __repr__(self):
        return f'<TimeSlot timeslot_id={self.timeslot_id} timeslot_name={self.timeslot_name}>'


class UserTimeSlotMapping(db.Model):
    __tablename__ = "users_timeslot_mapping"

    user_timeslot_mapping_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    timeslot_id = db.Column(db.Integer, db.ForeignKey("timeslots.timeslot_id"))

    def __repr__(self):
        return f'<User Timeslot Mapping user_timeslot_mapping_id={self.user_timeslot_mapping_id} timeslot_id={self.timeslot_id}>'

class PairingStatus(enum.Enum):
    pending = 'Pending'
    approved = 'Approved'
    declined = 'Declined'


class PairingRequests(db.Model):
    __tablename__ = "pairing_requests"

    pairing_list_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    receiever_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    pairing_status = db.Column(Enum(PairingStatus), default=PairingStatus.pending)

    def __repr__(self):
        return f'< User Pairing Request pairing_list_id={self.pairing_list_id} sender_id={self.sender_id} receiever_id={self.receiever_id}>'

class Comment(db.Model):
    """Comment"""
    __tablename__ = "comments"
    com_id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(200000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('prompts.prompt_id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)




class Prompt(db.Model):
    """Prompt"""

    __tablename__ = "prompts"

    prompt_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    prompt_name = db.Column(db.String)
    prompt_link = db.Column(db.String)
    prompt_difficulty = db.Column(db.String)
    prompt_description = db.Column(db.String(2000000))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_prompts = relationship('User', back_populates='prompts_assigned')

    def __repr__(self):
            return f"<Prompt prompt_id={self.prompt_id} prompt_name={self.prompt_name} prompt_link={self.prompt_link} prompt_difficulty={self.prompt_difficulty}>"


prompt_filename = 'Leetcode-data - leetcode.csv'

def populate_prompt_tb():
    with open(prompt_filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            split_data = row[0].split("--")
            prompt_name_data, prompt_link_data, prompt_difficulty_data, prompt_description_data = split_data
            populate_prompt = Prompt(prompt_name = prompt_name_data, prompt_link = prompt_link_data, prompt_difficulty = prompt_difficulty_data, prompt_description=prompt_description_data )
            db.session.add(populate_prompt)
            db.session.commit()

comment_body = ['I am very curious if anyone was able to solve this prompt using Java! The solutions section did not provide much help for me',
                'The solutions under the solutions part of Leetcode looked so elegant, my solution is not comparable, I was able to solve it though!',
                'Gotta try again, could not solve in 30 minutes!',
                'I was able to solve this problem within the timeframe!']

def populate_comment_tb():
    n = 9
    while (n > 1):
        populate_comments = Comment(body = random.choice(comment_body), user_id = random.randint(1,150), post_id = random.randint(1,10))
        db.session.add(populate_comments)
        db.session.commit()
        n-= 1


user_filename = 'User-data.csv'

def populate_user_tb():
    with open(user_filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        folder_dir = "/Users/gedailey/src/hackbright-project/static/profile_pics"

        for row in datareader:
            split_data = row[0].split("--")
            profile_pic = random.choice(os.listdir("/Users/gedailey/src/hackbright-project/static/profile_pics"))

            first_name_data, last_name_data, email_data, pwd_data, prompt_diff_data, primary_lang_data, timezone_data, prog_name_data, selected_timeslots_data = split_data
            populate_user = User(first_name = first_name_data, last_name = last_name_data, email = email_data, password = pwd_data, profile_picture= profile_pic, prompt_difficulty_level=prompt_diff_data,primary_language=primary_lang_data, timezone_name= timezone_data )
            db.session.add(populate_user)
            db.session.commit()

            user_id = User.query.filter_by(email=email_data).first().user_id
            get_timeslot_id = TimeSlot.query.filter_by(timeslot_name = selected_timeslots_data).one().timeslot_id
            populate_timeslot = UserTimeSlotMapping(user_id=user_id, timeslot_id=get_timeslot_id)
            get_prog_language_id = ProgrammingLanguage.query.filter_by(programming_language_name = prog_name_data).one().programming_language_id
            populate_prog_language = UserProgrammingLanguageMapping(user_id=user_id, programming_language_id=get_prog_language_id)
            db.session.add_all([populate_timeslot,populate_prog_language])
            db.session.commit()

def populate_initial_db():
    programming_language_py = ProgrammingLanguage(programming_language_name = 'Python', programming_language_label = 'py')
    programming_language_js = ProgrammingLanguage(programming_language_name = 'Javascript', programming_language_label = 'js')
    programming_language_ja = ProgrammingLanguage(programming_language_name = 'Java', programming_language_label = 'ja')
    prog_language_c_plus_plus = ProgrammingLanguage(programming_language_name = 'C++', programming_language_label = 'C++')
    prog_language_c = ProgrammingLanguage(programming_language_name = 'C', programming_language_label = 'C')
    timeslot_7am = TimeSlot(timeslot_name = '7am - 10am', timeslot_label = '7am')
    timeslot_10am = TimeSlot(timeslot_name = '10am - 1pm', timeslot_label = '10am')
    timeslot_1pm = TimeSlot(timeslot_name = '1pm - 4pm', timeslot_label = '1pm')
    timeslot_4pm = TimeSlot(timeslot_name = '4pm - 7pm', timeslot_label = '4pm')
    timeslot_7pm = TimeSlot(timeslot_name = ' 7pm - 10pm', timeslot_label = '7pm')
    timeslot_10pm = TimeSlot(timeslot_name = '10pm - 12am', timeslot_label = '10pm')

    db.session.add_all([programming_language_py, programming_language_js,
                        programming_language_ja, prog_language_c_plus_plus,
                        prog_language_c, timeslot_7am, timeslot_10am,
                        timeslot_1pm,timeslot_4pm, timeslot_7pm, timeslot_10pm])
    db.session.commit()

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
