import pickle
import numpy as np
from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import UserPersonalDetails, Wallet
from . import db
import os

dirname = os.path.dirname(__file__)


# from flask_login import login_required, current_user

survey_blu = Blueprint('survey_blu', __name__)


@survey_blu.route('/survey')
def survey():
    return render_template('surveypages/survey.html')


@survey_blu.route('/survey', methods=['POST'])
def surveyPost():
    email_id = request.form['takeemail']
    print("EMAIL : " + email_id)

    occupation = request.form['occupation']
    print(occupation)

    if occupation == "Student":
        occupation = 1
    else:
        occupation = 0

    print(occupation)

    martial_status = request.form['marital']
    print(martial_status)

    # Not Captured
    education = request.form.get('education')
    print(education)

    # ENSW
    regionStates = {
        'North': [0, 1, 0],
        'South': [0, 0, 1],
        'East': [1, 0, 0],
        'West': [0, 0, 0]
    }

    region = request.form['region']
    print(region)
    regionEncoded = regionStates[region]
    print(regionEncoded)

    salary = request.form.get('salary', type=int)
    print(type(salary))
    print(salary)

    expense = request.form.get('expenses', type=int)
    print(type(expense))
    print(expense)

    savings = request.form.get('savings', type=int)
    print(type(savings))
    print(savings)

    goalType = request.form['goalname']
    print(goalType)

    # Student Loan form
    loan_amt = request.form.get('loan_amt', type=int)
    int_rate = request.form.get('int_rate', type=int)
    loan_span = request.form.get('loan_span', type=int)
    print(type(loan_amt))
    print(loan_amt)

    goal_name = request.form.get('goal_name')
    goal_amt = request.form.get('goal_amt', type=int)
    goal_span = request.form.get('goal_span', type=int)
    print(type(goal_amt))
    print(goal_amt)

    if goalType == "Student Loan":
        save_per_day = loan_amt / (loan_span * 30.417)
    else:
        save_per_day = goal_amt / (goal_span * 30.417)

    print("Saved per day : " + str(save_per_day))

    collective_values = [occupation, savings, expense] + regionEncoded

    filename = os.path.join(dirname, 'resources/basicclusterpicklefiles/B_Clust_PIK_0.p')
    # with open("./resources/basicclusterpicklefiles/B_Clust_PIK_0.p",
    #           "rb") as f:
    with open(filename, "rb") as f:
        n_km = pickle.load(f)

    cluster = int(n_km.predict(np.array(collective_values).reshape(1, -1))[0])
    print("New cluster value : ")
    print(type(cluster))
    print(cluster)

    filename1 = os.path.join(dirname, 'resources/basicclusterpicklefiles/PIK_' + str(
            cluster) + ".p")

    # with open("./resources/basicclusterpicklefiles/PIK_" + str(
    #         cluster) + ".p", "rb") as f:
    with open(filename1, "rb") as f:
        n_sc = pickle.load(f)
        n_data = pickle.load(f)
        n_m0 = pickle.load(f)
    amount = n_sc.inverse_transform(n_m0.predict(np.reshape(n_data, (n_data.shape[0], 1, n_data.shape[1]))))[0][0]
    # invert predictions
    print("Amount")
    print(amount)

    filename2 = os.path.join(dirname, 'resources/basicclusterpicklefiles/NUM_PIK_' + str(
        cluster) + ".p")

    # with open("./resources/basicclusterpicklefiles/NUM_PIK_" + str(
    #         cluster) + ".p", "rb") as f:
    with open(filename2, "rb") as f:
        n_sc = pickle.load(f)
        n_data = pickle.load(f)
        n_m0 = pickle.load(f)

    transaction = n_sc.inverse_transform(n_m0.predict(np.reshape(n_data, (n_data.shape[0], 1, n_data.shape[1]))))[0][0]
    # invert predictions
    print("transaction")
    transaction_value = int(transaction)
    print(transaction_value)

    # Saved per day per transaction
    save_per_transaction = save_per_day / transaction_value
    # Amount per transaction
    amount_per_transaction = amount / transaction_value

    predicted_value = 2 * (save_per_transaction * amount_per_transaction) / (
            save_per_transaction + amount_per_transaction)

    print("Predicted Value " + str(predicted_value))

    userpersonaldetails = UserPersonalDetails(occupation=occupation,
                                              martial_status=martial_status,
                                              education=education,
                                              region=region,
                                              salary=salary,
                                              monthly_exp=expense,
                                              savings=savings,
                                              goal_type=goalType,
                                              loan_amt=loan_amt,
                                              interest_value=int_rate,
                                              loan_span=loan_span,
                                              goal_name=goal_name,
                                              amt_value=goal_amt,
                                              goal_span=goal_span,
                                              save_per_day=save_per_day,
                                              transaction_value=transaction_value,
                                              amount_per_transaction=amount_per_transaction,
                                              predicted_value=predicted_value,
                                              email=email_id,
                                              cluster=cluster)

    db_wallet = Wallet(email=email_id, transaction_amt=0)
    db.session.add(db_wallet)

    db.session.add(userpersonaldetails)
    db.session.commit()

    return redirect(url_for('authorize.login'))



