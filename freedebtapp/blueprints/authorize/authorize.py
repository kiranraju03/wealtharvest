from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from freedebtapp.models import User
from freedebtapp import db
from flask_login import login_user, login_required, logout_user

authorize = Blueprint('authorize', __name__)


@authorize.route('/login')
def login():
    return render_template('auth/login.html')


@authorize.route('/login', methods=['POST'])
def loginPost():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Check your login credentials')
        return redirect(url_for('authorize.login'))

    login_user(user, remember=remember)

    return redirect(url_for('dashboards.dashboard'))


@authorize.route('/signup')
def signup():
    return render_template('auth/signup.html')


@authorize.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('authorize.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=True)
    # redirect(url_for('survey_blu.survey')
    # return redirect(url_for('survey_blu.survey'))
    return redirect(url_for('surveys.survey', email=email))
    # return render_template('surveypages/survey.html', email=email)


@authorize.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('authorize.login'))
