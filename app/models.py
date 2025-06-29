from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




class Sport(db.Model):
    __tablename__ = "sport"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Optional: backref to athletes
    athletes = db.relationship("Athlete", back_populates="sport")



class School(db.Model):
    __tablename__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Optional: backref to athletes
    athletes = db.relationship("Athlete", back_populates="school")   


class Athlete(db.Model):
    __tablename__ = "athlete"

    id = db.Column(db.Integer primary_key=True)
    athlete_key = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)


    sport_id = db.Column(db.Integer, db.ForeignKey("sport.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=False)

    sport = db.relationship("Sport", back_populates="athletes")
    school = db.relationship("School", back_populates="athletes")
    images = db.relationship("Image", back_populates="athlete", cascade="all, delete-orphan")


class Image(db.Model):
    __table_name__ = "image"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)

    athlete_id = db.Column(db.Integer, db.ForeignKey("athlete.id"), nullable=False)
    athlete = db.relationship("Athlete", back_populates="images")
