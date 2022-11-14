from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship, Session

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique= True)
    password = db.Column(db.String)
    profile_picture = db.Column(db.String, default='default-image.jpeg')
    prompt_difficulty_level = db.Column(db.String)
    primary_language = db.Column(db.String)
    timezone_name = db.Column(db.String)
    programming_languages = relationship('ProgrammingLanguage', secondary='users_programming_language_mapping', back_populates='users')

    #User.query.get(7).__dict__
    #_[0].__dict__

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
    timeslot_name = db.Column(db.ARRAY(db.String))
    day_of_the_week = db.Column(db.ARRAY(db.String))



#     class User(Base):
#     tablename = "users"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     projects = relationship('Project', secondary='project_users', back_populates='users')


# class Project(Base):
#     tablename = "projects"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     users = relationship('User', secondary='project_users', back_populates='projects')


# class ProjectUser(Base):
#     tablename = "project_users"

#     id = Column(Integer, primary_key=True)
#     notes = Column(String, nullable=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     project_id = Column(Integer, ForeignKey('projects.id'))

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

# result = db.session.query(User, UserProgrammingLanguageMapping).join(User).all()

# for user, userprogramminglanguagemapping in result:
#     print(user.first_name, userprogramminglanguagemapping.programming_language_id)



# class Pairing(db.Model):
#     """Pairing"""

#     __tablename__ = "pairings_sessions"

#     pairing_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
#     user_one_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     user_two_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     # meeting_date = db.Column(db.Datetime, nullable=False) #is there a datetime option?
#     feedback_description = db.Column(db.Text)
#     sender_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     recipient_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     is_prompt_solved = db.Column(db.Boolean)
#     prompt_id = db.Column(db.Integer, db.ForeignKey("prompts.prompt_id"))

#     def __repr__(self):
#             return f"<Pairing pairing_id={self.pairing_id} >" #am I am able to print the foreign key values here?


# class Prompt(db.Model):
#     """Prompt"""

#     __tablename__ = "prompts"

#     prompt_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
#     prompt_name = db.Column(db.String)
#     prompt_link = db.Column(db.String)

#     # prompt = db.relationship("Prompt", back_populates="feedback")
#     # user = db.relationship("User", back_populates="feedback")

#     def __repr__(self):
#             return f"<Prompt prompt_id={self.prompt_id} prompt_name={self.prompt_name} prompt_link={self.prompt_link}>"


def connect_to_db(flask_app, db_uri="postgresql:///coder-lounge", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)



    print("You have been connected to the db")

def populate_initial_db():
    programming_language_py = ProgrammingLanguage(programming_language_name = 'Python', programming_language_label = 'py')
    programming_language_js = ProgrammingLanguage(programming_language_name = 'Javascript', programming_language_label = 'js')

    db.session.add_all([programming_language_py, programming_language_js])
    db.session.commit()

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
