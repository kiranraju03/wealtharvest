from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from freedebtapp import db
from freedebtapp.models import Wallet

wallets = Blueprint('wallets', __name__)


@wallets.route('/wallet')
@login_required
def wallet():
    wallet_balance_adder = db.session.query(func.sum(Wallet.transaction_amt).label('total')).filter(
        Wallet.email == current_user.email)
    per_amt = wallet_balance_adder.group_by(Wallet.email).all()

    wallet_balance = round(per_amt[0][0], 2)

    print("Combined wallet " + str(wallet_balance))
    return render_template('homepages/wallet.html', wallet_balance=wallet_balance)
