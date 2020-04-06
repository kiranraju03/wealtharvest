from sqlalchemy.orm import backref

from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String(20))

    # child = relationship("Child", uselist=False, back_populates="parent")
    # user_personal_details = db.relationship('UserPersonalDetails', uselist=False, back_populates="user")


class UserPersonalDetails(db.Model):
    __tablename__ = 'user_personal_details'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    request = db.relationship("User", backref=backref("user_personal_details", uselist=False))
    # user = db.relationship("User", back_populates="user_personal_details")

    occupation = db.Column(db.Integer)
    martial_status = db.Column(db.String(20))
    education = db.Column(db.String(20))

    region = db.Column(db.String(10))

    salary = db.Column(db.Integer)
    monthly_exp = db.Column(db.Integer)
    savings = db.Column(db.Integer)
    goal_type = db.Column(db.String(20))

    loan_amt = db.Column(db.Integer)
    interest_value = db.Column(db.Float)
    loan_span = db.Column(db.Integer)

    goal_name = db.Column(db.String(20))
    amt_value = db.Column(db.Integer)
    goal_span = db.Column(db.Integer)

    save_per_day = db.Column(db.Float)

    cluster = db.Column(db.Integer)











