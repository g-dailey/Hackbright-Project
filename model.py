from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique= True)
    password = db.Column(db.String)
    profile_picture = db.Column(db.String)
    prompt_difficulty_level = db.Column(db.String)
    primary_language_id = db.Column(db.Integer, db.ForeignKey("primary_languages.primary_language_id"))
    timezone_id = db.Column(db.Integer, db.ForeignKey("timezones.timezone_id"))


    # feedback = db.relationship("Feedback", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} first_name={self.first_name} last_name={self.last_name} email={self.email}>'

class TimeSlot(db.Model):
    __tablename__ = "timeslots"

    timeslot_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    timeslot_name = db.Column(db.String)
    day_of_the_week = db.Column(db.String)

    def __repr__(self):
        return f'<TimeSlot timeslot_id={self.timeslot_id} timeslot_name={self.timeslot_name}>'


class UserTimeSlotMapping(db.Model):
    __tablename__ = "users_timeslot_mapping"

    user_timeslot_mapping_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    timeslot_id = db.Column(db.Integer, db.ForeignKey("timeslots.timeslot_id"))


    def __repr__(self):
        return f'<User Timeslot Mapping user_timeslot_mapping_id={self.user_timeslot_mapping_id} timeslot_id={self.timeslot_id}>'

class PrimaryLanguage(db.Model):
    __tablename__ = "primary_languages"

    primary_language_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    primary_language_name = db.Column(db.String)

    def __repr__(self):
        return f'<Primary Language primary_language_id={self.primary_language_id} primary_language_name={self.primary_language_name}>'


class ProgrammingLanguage(db.Model):
    __tablename__ = "programming_languages"

    programming_language_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    programming_language_name = db.Column(db.String)

    def __repr__(self):
        return f'<Programming Language programming_language_id={self.programming_language_id} programming_language_name={self.programming_language_name}>'

class UserProgrammingLanguageMapping(db.Model):
    __tablename__ = "users_programming_language_mapping"

    user_programming_language_mapping_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    programming_language_id = db.Column(db.Integer, db.ForeignKey("programming_languages.programming_language_id"))


    def __repr__(self):
        return f'<Programming Language Mapping user_programming_language_mapping_id={self.user_programming_language_mapping_id} programming_language_id={self.programming_language_id}>'


class Timezone(db.Model):
    __tablename__ = "timezones"

    timezone_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    timezone_name = db.Column(db.String)

    def __repr__(self):
        return f'<Programming Language timezone_id={self.timezone_id} timezone_name={self.timezone_name}>'


class Feedback(db.Model):
    """Feedback"""

    __tablename__ = "feedback"

    feedback_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    score = db.Column(db.Integer)
    feedback_description = db.Column(db.Text)
    is_prompt_solved = db.Column(db.Boolean)
    pairing_id = db.Column(db.Integer, db.ForeignKey("pairings.pairing_id"))
    sender_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
            return f"<Feedback feedback_id={self.feedback_id} feedback_description={self.feedback_description} is_prompt_solved={self.is_prompt_solved}>"


class Pairing(db.Model):
    """Pairing"""

    __tablename__ = "pairings"

    pairing_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.meeting_id"))
    user_one_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_two_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
            return f"<Pairing pairing_id={self.pairing_id} >" #am I am able to print the foreign key values here?


class Meeting(db.Model):
    """Meeting"""

    __tablename__ = "meetings"

    meeting_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    meeting_date = db.Column(db.String) #is there a datetime option?

    def __repr__(self):
            return f"<Meeting meeting_id={self.meeting_id} meeting_date={self.meeting_date}>"


class Prompt(db.Model):
    """Prompt"""

    __tablename__ = "prompts"

    prompt_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    prompt_name = db.Column(db.String)
    prompt_link = db.Column(db.String)

    # prompt = db.relationship("Prompt", back_populates="feedback")
    # user = db.relationship("User", back_populates="feedback")

    def __repr__(self):
            return f"<Prompt prompt_id={self.prompt_id} prompt_name={self.prompt_name} prompt_link={self.prompt_link}>"


def connect_to_db(flask_app, db_uri="postgresql:///coder-lounge", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("You have been connected to the db")

class NamerForm(FlaskForm):
    name = StringField("What's your name")
    submit = SubmitField("Submit")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
