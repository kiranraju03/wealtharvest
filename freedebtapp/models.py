from sqlalchemy.orm import backref

from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user_wh'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String(20))


class UserPersonalDetails(db.Model):
    __tablename__ = 'user_personal_details'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy

    # user_id = db.Column(db.Integer, db.ForeignKey('user_wh.id'))
    # request = db.relationship("User", backref=backref("user_personal_details", uselist=False))

    email = db.Column(db.String(30), db.ForeignKey('user_wh.email'))
    request = db.relationship("User", backref=backref("user_personal_details", uselist=False))

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

    # Moving from survey to payments
    # transaction_value = db.Column(db.Integer)
    # amount_per_transaction = db.Column(db.Float)
    # predicted_value = db.Column(db.Float)

    cluster = db.Column(db.Integer)


# Called as a cron job each day.
class Predictions(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    cluster = db.Column(db.Integer)
    transaction_value = db.Column(db.Integer)
    predicted_value = db.Column(db.Float)
    amount_per_transaction = db.Column(db.Float)
    created_on = db.Column(db.DateTime, server_default=db.func.now())


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(30))
    transaction_amt = db.Column(db.Float)
    created_on = db.Column(db.DateTime, server_default=db.func.now())


class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(30))
    transaction_amt = db.Column(db.Float)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    # updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())











