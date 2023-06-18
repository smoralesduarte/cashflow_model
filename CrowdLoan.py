# Description: This file contains a 15 month model of the financial situation of the CrowdLoan company. The model is based on the company's income, expenses, credits and loans. The model is used to calculate the company's financial situation in the future and to make decisions based on that information.

from model import *
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Initial values
# Three initial loans of COP 30e9, the first due in one month, the second due in two months and the third due in three months. All have 25% annual interest.
time = 0
amount = 30e9
interest = 0.25
initial_loans = []
for i in range(3):
    initial_loans.append(Loan(time, i + 1, interest, amount, "COP"))

# New credits: for each one of the following 12 months, CrowdLoan will give a credit of COP 30e9 with 25% annual interest and a duration of 3 months.
duration = 3
amount = 30e9
interest = 0.25
initial_credits = []
for i in range(12):
    initial_credits.append(Credit(i + 1, duration, interest, amount))  

# Inital Fixed Expenses: COP 400e6 per month, USD 70e3 per month and EUR 30e3 per month
initial_fixed_expenses = [(400e6, "COP"), (70e3, "USD"), (30e3, "EUR")]

# Initial debts: CrowdLoan has a debt of USD 3e6 and EUR 2e6. The debt must be paid uniformly over 12 months. The annual interest is 10%.
USD_amount = 3e6
EUR_amount = 2e6
interest = 0.1
USD_individual_debt = USD_amount / 12
EUR_individual_debt = EUR_amount / 12
for i in range(12):
    initial_loans.append(Loan(time, i + 1, interest, USD_individual_debt, "USD"))
    initial_loans.append(Loan(time, i + 1, interest, EUR_individual_debt, "EUR"))


# Initial loans: Crowdloan will take a loan every month for the next three months. The loans will be of USD 200e3 and EUR 250e3. The annual interest is 10% and the duration is one year.
USD_amount = 200e3
EUR_amount = 250e3
interest = 0.1
duration = 12
for i in range(3):
    initial_loans.append(Loan(i + 1, duration, interest, USD_amount, "USD"))
    initial_loans.append(Loan(i + 1, duration, interest, EUR_amount, "EUR"))

# Exchange rates: COP 4600 per USD and COP 4500 per EUR
USD_exchange_rate = 4600
EUR_exchange_rate = 4500

# Flow
CrowdLoan = Model(initial_fixed_expenses, initial_credits, initial_loans)
print([initial_loan.currency for initial_loan in CrowdLoan.loans])

# Simulate 15 months of the model, and save the results in a dataframe at each time step.
# The dataframe will have the following columns: COP flow, USD flow, EUR flow, total flow

# Create the dataframe
df = pd.DataFrame(columns=["COP flow", "USD flow", "EUR flow", "Total flow"])

# Simulate 15 months
for i in range(15):
    CrowdLoan.simulate_month(USD_exchange_rate, EUR_exchange_rate)
    df = df.append({"COP flow": CrowdLoan.get_COP_flow(), "USD flow": CrowdLoan.get_USD_flow(), "EUR flow": CrowdLoan.get_EUR_flow(), "Total flow": CrowdLoan.get_total_flow()}, ignore_index=True)
    df.index += 1

#pd.options.display.float_format = '${:,.2f}'.format
print(df)

CrowdLoan = Model(initial_fixed_expenses, initial_credits, initial_loans)
# Simulate 15 months of the model, and save the results in a dataframe at each time step.
# The dataframe will have the following columns: time, COP income, USD income, EUR income, total income, COP expenses, USD expenses, EUR expenses, total expenses, COP flow, USD flow, EUR flow, total flow

# Create the dataframe
df = pd.DataFrame(columns=["Time", "COP income", "USD income", "EUR income", "Total income", "COP expenses", "USD expenses", "EUR expenses", "Total expenses", "COP flow", "USD flow", "EUR flow", "Total flow"])

# Simulate 15 months
for i in range(15):
    CrowdLoan.simulate_month(USD_exchange_rate, EUR_exchange_rate)
    df = df.append({"Time": CrowdLoan.time, "COP income": CrowdLoan.COP_income, "USD income": CrowdLoan.USD_income, "EUR income": CrowdLoan.EUR_income, "Total income": CrowdLoan.income, "COP expenses": CrowdLoan.COP_expenses, "USD expenses": CrowdLoan.USD_expenses, "EUR expenses": CrowdLoan.EUR_expenses, "Total expenses": CrowdLoan.expenses, "COP flow": CrowdLoan.get_COP_flow(), "USD flow": CrowdLoan.get_USD_flow(), "EUR flow": CrowdLoan.get_EUR_flow(), "Total flow": CrowdLoan.get_total_flow()}, ignore_index=True)
    df.index += 1

pd.options.display.float_format = '${:,.2f}'.format
print(df)
print("${:,.2f}".format(df["Total flow"].sum()))

# Simulate USD_exchange_rate and EUR_exchange_rate for 15 months
# Create the dataframe
exchange_rate_df = pd.DataFrame(columns=["Time", "USD exchange rate", "EUR exchange rate"])

# Simulate 15 months with random fluctuations of COP 500 
for i in range(15):
    USD_exchange_rate += random.randint(-500, 500)
    EUR_exchange_rate += random.randint(-500, 500)
    exchange_rate_df = exchange_rate_df.append({"Time": i + 1, "USD exchange rate": USD_exchange_rate, "EUR exchange rate": EUR_exchange_rate}, ignore_index=True)
    exchange_rate_df.index += 1

CrowdLoan = Model(initial_fixed_expenses, initial_credits, initial_loans)
# Simulate 15 months using the exchange rates from the dataframe
for i in range(15):
    CrowdLoan.simulate_month(exchange_rate_df["USD exchange rate"][i + 1], exchange_rate_df["EUR exchange rate"][i + 1])
    



