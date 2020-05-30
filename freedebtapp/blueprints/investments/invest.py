from flask import Blueprint, render_template
from flask_login import login_required, current_user

from freedebtapp import db
from freedebtapp.investValues import predictor
from freedebtapp.models import UserPersonalDetails

investment = Blueprint('investment', __name__)


@investment.route('/invest')
@login_required
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
