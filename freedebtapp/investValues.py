import random
from collections import defaultdict

invest = {
    'high': {
        1: {
            'mutual_fund_name': 'Axis Bluechip Fund',
            'risk': 'High',
            'return': '10.87',
            'min_value': 500
        },
        2: {
            'mutual_fund_name': 'Mirae Asset Large Cap Fund',
            'risk': 'High',
            'return': '12.08',
            'min_value': 500
        },
        3: {
            'mutual_fund_name': 'SBI Bluechip Fund',
            'risk': 'High',
            'return': '11.41',
            'min_value': 500
        }
    },
    'medium': {
        1: {
            'mutual_fund_name': 'HDFC Hybrid Equity Fund',
            'risk': 'Medium',
            'return': '8.44',
            'min_value': 100
        },
        2: {
            'mutual_fund_name': 'Mirae Asset Hybrid Equity Fund',
            'risk': 'Medium',
            'return': '11.64',
            'min_value': 500
        },
        3: {
            'mutual_fund_name': 'Franklin India Focused Equity Fund',
            'risk': 'Medium',
            'return': '10.33',
            'min_value': 500
        }
    },
    'low': {
        1: {
            'mutual_fund_name': 'Aditya Birla Sun Life Savings Fund',
            'risk': 'Moderately Low',
            'return': '8.66',
            'min_value': 100
        },
        2: {
            'mutual_fund_name': 'HDFC Short Term Debt Fund',
            'risk': 'Moderately Low',
            'return': '8.73',
            'min_value': 100
        },
        3: {
            'mutual_fund_name': 'Principal Equity Savings Fund',
            'risk': 'Moderately Low',
            'return': '6.78',
            'min_value': 100
        }
    }
}


def predict(risk_factor):
    rand_num = random.randint(1, 3)
    invest_values = invest[risk_factor][rand_num]
    print(invest_values)
    print(type(invest_values))
    return invest_values


def predictor(cluster_num):

    if cluster_num == 0:
        inv = predict("high")
    elif cluster_num == 1:
        inv = predict("medium")
    else:
        inv = predict("low")

    return inv
