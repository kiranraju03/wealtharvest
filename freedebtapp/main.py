from flask import Blueprint, render_template, url_for, redirect, request
from .models import User, UserPersonalDetails, Wallet
from . import db
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from .investValues import predictor
import random

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('homepages/home.html')


@main.route('/about')
def about():
    return render_template('homepages/about.html')


@main.route('/invest')
def invest():
    user_specific = db.session.query(UserPersonalDetails.cluster).filter(
        UserPersonalDetails.email == current_user.email).all()
    cluster_value = user_specific[0][0]
    # 2 : low
    # 1 : medium
    # 0 : high

    invest_para = predictor(cluster_value)
    risk_factor = invest_para['risk']
    mutual_fund_name = invest_para['mutual_fund_name']
    return_value = invest_para['return']
    min_value = invest_para['min_value']

    return render_template('homepages/invest.html',
                           risk_factor=risk_factor,
                           mutual_fund_name=mutual_fund_name,
                           return_value=return_value,
                           min_value=min_value)


@main.route('/wallet')
def wallet():
    wallet_balance_adder = db.session.query(func.sum(Wallet.transaction_amt).label('total')).filter(
        Wallet.email == current_user.email)
    per_amt = wallet_balance_adder.group_by(Wallet.email).all()

    wallet_balance = per_amt[0][0]


    print("Combined wallet " + str(wallet_balance))
    return render_template('homepages/wallet.html', wallet_balance=wallet_balance)


@main.route('/payments')
def payments():
    bal_value = request.args.get('bal', type=int)
    if bal_value:
        email = current_user.email
        db_wallet = Wallet(
            email=email,
            transaction_amt=bal_value,
        )
        db.session.add(db_wallet)
        db.session.commit()
        print("payamt " + str(bal_value))

    return render_template('homepages/payments.html')


@main.route('/payments', methods=['POST'])
def paymentsPost():
    entered_amt = request.form.get('amount')
    comp_amt = int(entered_amt) / 4

    user_specific = db.session.query(UserPersonalDetails).filter(UserPersonalDetails.email == current_user.email).all()
    # .user_values = user_specific
    pdv = user_specific[0].predicted_value
    print(pdv)
    cdc = 2 * (comp_amt * pdv) / (comp_amt + pdv)
    print(cdc)

    # compute the change
    return render_template('homepages/payments.html', amt=entered_amt, num=max(int(cdc), 1))


@main.route('/profile')
def profile():
    # user_details = User.query.filter_by(email = current_user.email)
    user_full = db.session.query(UserPersonalDetails).filter(UserPersonalDetails.email == current_user.email).all()
    user_table_full = db.session.query(User).filter(User.email == current_user.email).all()
    # user_personal = UserPersonalDetails.query.first()
    print("inside profile")

    user_name = user_table_full[0].name
    user_email = user_table_full[0].email

    user_occu = user_full[0].occupation

    if user_occu == 1:
        user_occ_name = "Student"
    else:
        user_occ_name = "Working Professional"

    user_personal = user_full[0]

    # user_occ_name = "Student"
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
