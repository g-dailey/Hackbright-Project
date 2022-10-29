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
    feedback = db.relationship("Feedback", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} first_name={self.first_name} last_name={self.last_name} email={self.email}>'

class Feedback(db.Model):
    """Feedback"""

    __tablename__ = "feedback"
    feedback_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    score = db.Column(db.Integer)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompts.prompt_id"))
    feedback_for = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    prompt = db.relationship("Prompt", back_populates="feedback")
    user = db.relationship("User", back_populates="feedback")

    def __repr__(self):
            return f"<Feedback feedback_id={self.feedback_id} feedback_for={self.feedback_for} score={self.score}>"

class Prompt(db.Model):
    """Prompt"""

    __tablename__ = "prompts"

    prompt_id = db.Column(db.Integer, autoincrement = True, primary_key= True)
    prompt_name = db.Column(db.String)
    feedback_id = db.Column(db.Integer, db.ForeignKey("feedback.feedback_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    prompt = db.relationship("Prompt", back_populates="feedback")
    user = db.relationship("User", back_populates="feedback")

    def __repr__(self):
            return f"<Feedback feedback_id={self.feedback_id} feedback_for={self.feedback_for} score={self.score}>"



def connect_to_db(flask_app, db_uri="postgresql:///prompts", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("You have been connected to the db")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
