import datetime
import json

from flask import Blueprint, render_template, jsonify, make_response, request
from flask_login import current_user
from sqlalchemy import func

from freedebtapp import db
from freedebtapp.models import Wallet, UserPersonalDetails, Predictions, Transactions

payment = Blueprint('payment', __name__)


@payment.route('/payments')
def payments():
    return render_template('homepages/pay.html')

#
# @payments.route('/paymentsPost', )
# def paymentsPost():
#     return render_template('homepages/pay.html')


@payment.route('/paymentsAjax')
def paymentsAjax():
    print("New AJax funx")
    print(request.args.get('amt', 0.0, type=float))
    enteredAmount = request.args.get('amt', 0.0, type=float)
    user_email = current_user.email

    # db_wallet = Transactions(email=user_email, transaction_amt=enteredAmount)
    # db.session.add(db_wallet)
    # db.session.commit()

    pickColumns = UserPersonalDetails.query.join(Predictions, UserPersonalDetails.cluster == Predictions.cluster) \
        .add_columns(UserPersonalDetails.save_per_day, Predictions.transaction_value, Predictions.predicted_value,
                     Predictions.amount_per_transaction).filter(UserPersonalDetails.email == user_email).all()
    pickedTupleValues = pickColumns[0][1:]
    print(pickedTupleValues)

    transactionDetails = db.session.query(func.sum(Transactions.transaction_amt).label('total'),
                                          func.count(Transactions.transaction_amt).label('count')).filter(
        Transactions.email == user_email).filter(func.date(Transactions.created_on) == datetime.date.today())
    per_amt = transactionDetails.group_by(Transactions.email,
                                          func.date(Transactions.created_on).label('day_wise')).order_by(
        func.date(Transactions.created_on).desc()).all()
    print("Ordered")
    if len(per_amt) > 0:
        per_amt = per_amt[0]
    else:
        per_amt = (0, 0)
    print(per_amt)

    # Save per day - transaction_Amt total
    newSavePerDay = pickedTupleValues[0] - per_amt[0]
    if newSavePerDay <= 0:
        newSavePerDay = pickedTupleValues[0]

    # Predicted Value - transaction_Amt total
    newPredictedValue = pickedTupleValues[2] - per_amt[0]
    if newPredictedValue <= 0:
        newPredictedValue = pickedTupleValues[2]

    # Transaction_value - transaction count
    newTransactionValue = max((pickedTupleValues[1] - per_amt[1]), 1)

    # Newly computed Amount per transaction
    newAmountPerTransaction = (newPredictedValue / newTransactionValue) / 4

    # 25% of entered amount for quantum computation
    computedAmount = enteredAmount / 4

    # Quantum as per goals set
    savePerTransaction = newSavePerDay / newTransactionValue

    # Harmonic Mean of 3 variables Calculation
    finalQuantum = (3 * newAmountPerTransaction * computedAmount * savePerTransaction) / (
                (newAmountPerTransaction * computedAmount) +
                (computedAmount * savePerTransaction) +
                (newAmountPerTransaction * savePerTransaction))

    data = {'message': 'Prediction Completed', 'code': 'SUCCESS', 'quantum': round(finalQuantum, 2)}

    return make_response(jsonify(data), 200)


@payment.route('/acceptQuantum')
def acceptQuantum():
    bal_value = request.args.get('bal', type=float)
    data = {'message': 'Payment Failure', 'code': 'FAILED'}
    if bal_value >= 0:
        email = current_user.email
        db_wallet = Wallet(
            email=email,
            transaction_amt=bal_value,
        )
        db.session.add(db_wallet)
        db.session.commit()

        print("Accepted Quantum " + str(bal_value))
        data = {'message': 'Quantum Calculated', 'code': 'SUCCESS'}

        return make_response(jsonify(data), 200)

    return make_response(jsonify(data), 500)


@payment.route('/acceptPayment')
def acceptPayment():
    payed_amount = request.args.get('pay_amt', type=float)
    data = {'message': 'Payment Failure', 'code': 'FAILED'}
    if payed_amount >= 0:
        email = current_user.email
        db_transaction = Transactions(
            email=email,
            transaction_amt=payed_amount,
        )
        db.session.add(db_transaction)
        db.session.commit()

        print("Accepted Payment " + str(payed_amount))
        data = {'message': 'Payment Completed', 'code': 'SUCCESS'}

        return make_response(jsonify(data), 200)
        # return render_template('homepages/pay.html')

    return make_response(jsonify(data), 500)
