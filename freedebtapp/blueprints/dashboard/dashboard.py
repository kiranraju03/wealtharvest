from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from freedebtapp import db
from freedebtapp.models import UserPersonalDetails, User, Wallet

dashboards = Blueprint('dashboards', __name__)


@dashboards.route('/dashboard')
@login_required
def dashboard():
    user_personal_info = db.session.query(UserPersonalDetails).filter(
        UserPersonalDetails.email == current_user.email).all()
    user_name = db.session.query(User.name).filter(User.email == current_user.email).all()[0][0]
    wallet_balance = round(db.session.query(func.sum(Wallet.transaction_amt).label('total')).filter(
        Wallet.email == current_user.email).group_by(Wallet.email).all()[0][0], 2)
    getGoal = user_personal_info[0].goal_type
    if getGoal == "Student Loan":
        goalSet = {'amount': user_personal_info[0].loan_amt,
                   'int_val': user_personal_info[0].interest_value,
                   'timeSpan': user_personal_info[0].loan_span}
    else:
        goalSet = {'goalName': user_personal_info[0].goal_name,
                   'goalAmt': user_personal_info[0].amt_value,
                   'goalSpan': user_personal_info[0].goal_span}

    invest_flag = True

    # Call db and send the values
    return render_template('homepages/dashboard.html', name=user_name,
                           wallet_balance=wallet_balance,
                           invest_flag=invest_flag,
                           getGoal=getGoal,
                           goalSet=goalSet)
