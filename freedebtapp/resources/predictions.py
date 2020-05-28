import os
import pickle

import numpy as np

from freedebtapp.models import Predictions


def predictions_caller():
    dirname = os.path.dirname(__file__)

    for cluster in range(3):
        filename1 = os.path.join(dirname, 'resources/basicclusterpicklefiles/PIK_' + str(
            cluster) + ".p")

        # with open("./resources/basicclusterpicklefiles/PIK_" + str(
        #         cluster) + ".p", "rb") as f:
        with open(filename1, "rb") as f:
            n_sc = pickle.load(f)

            n_data = pickle.load(f)
            n_m0 = pickle.load(f)
        amount = n_sc.inverse_transform(n_m0.predict(np.reshape(n_data, (n_data.shape[0], 1, n_data.shape[1]))))[0][0]
        # invert predictions : AMOUNT PREDICTION
        print("Amount")
        print(amount)

        filename2 = os.path.join(dirname, 'resources/basicclusterpicklefiles/NUM_PIK_' + str(
            cluster) + ".p")

        with open(filename2, "rb") as f:
            n_sc = pickle.load(f)
            n_data = pickle.load(f)
            n_m0 = pickle.load(f)

        transaction = n_sc.inverse_transform(n_m0.predict(np.reshape(n_data, (n_data.shape[0], 1, n_data.shape[1]))))[0][0]
        # invert predictions : TRANSACTION PREDICTION
        print("transaction")
        transaction_value = int(transaction)
        print(transaction_value)

        # Saved per day per transaction
        # save_per_transaction = save_per_day / transaction_value
        # Amount per transaction
        # amount_per_transaction = amount / transaction_value

        """INsert to Table"""
        Predictions(cluster=cluster,
                    transaction_value=transaction_value,
                    predicted_value=amount,
                    amount_per_transaction=amount / transaction_value)

        db.session.add(userpersonaldetails)
        db.session.commit()

        # id = db.Column(db.Integer, primary_key=True)
        # cluster = db.Column(db.Integer)
        # transaction_value = db.Column(db.Integer)
        # predicted_value = db.Column(db.Float)
        # amount_per_transaction = db.Column(db.Float)

    # predicted_value = 2 * (save_per_transaction * amount_per_transaction) / (
    #         save_per_transaction + amount_per_transaction)

    # print("Predicted Value " + str(predicted_value))
