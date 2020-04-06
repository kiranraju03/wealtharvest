from flask import Blueprint, render_template, url_for, redirect, request
from .models import User, UserPersonalDetails
from . import db
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('homepages/home.html')


@main.route('/about')
def about():
    return render_template('homepages/about.html')


@main.route('/invest')
def invest():
    return render_template('homepages/invest.html')


@main.route('/wallet')
def wallet():
    return render_template('homepages/wallet.html')


@main.route('/payments')
def payments():
    return render_template('homepages/payments.html')


@main.route('/payments', methods=['POST'])
def paymentsPost():

    entered_amt = request.form.get('amount')
    comp_amt = int(entered_amt) / 4
    #compute the change
    return render_template('homepages/payments.html', num=int(comp_amt))


@main.route('/profile')
def profile():
    # user_details = User.query.filter_by(email = current_user.email)
    user_full = db.session.query(User, UserPersonalDetails).filter(User.email == current_user.email).all()
    # user_personal = UserPersonalDetails.query.first()
    print("inside profile")
    user_details = user_full[0]

    # Table 1
    user_name = user_details[0].name
    user_email = user_details[0].email

    # Table 2

    user_personal = user_details[1]
    user_occ_name = "Student" if user_personal.occupation == 1 else "Working Professional"
    user_martial_status = user_personal.martial_status
    user_education = user_personal.education
    user_region = user_personal.region

    return render_template('homepages/profile.html',
                           name=user_name,
                           email=user_email,
                           occupation=user_occ_name,
                           martial=user_martial_status,
                           education=user_education,
                           region=user_region)


