# Company Financial Modeling and Analysis

This small project contains a set of classes and Jupyter Notebook examples that model the financial situation of a company. It includes classes for handling credits, loans, bank accounts, and a model class that combines these components to simulate the company's financial status. Additionally, the Jupyter Notebook provides examples of how to use the classes for modeling, risk analysis, and foreign exchange rate simulation and analysis.

## Table of Contents

- [Classes](#classes)
- [Jupyter Notebook Usage](#jupyter-notebook-usage)
- [CrowdLoan](#CrowdLoan)

## Classes

The following classes are included in this project:

### Credit

The `Credit` class represents a credit that the company gives to a client in COP (Colombian Peso). It calculates the monthly interest, total interest, and provides methods to retrieve the final income and time of income.

### Loan

The `Loan` class represents a loan that is given to the company in any currency. It calculates the monthly interest, total interest, and provides methods to retrieve the final payment and time of payment.

### BankAccount

The `BankAccount` class represents the company's bank account. It keeps track of the balance, time, and provides methods to add money, take money, add interest, and simulate the passing of time. In the provided example, savings have a 10% annual interest rate, while loans have a 15% annual interest rate.

### Model

The `Model` class represents the model of the company's financial situation. It contains lists of fixed expenses, credits, and loans. The model tracks time, income, expenses, and various currency-specific variables. It provides methods to add fixed expenses, credits, and loans, calculate income, expenses, and update the bank account. The model can simulate the passing of time and retrieve the net flow of different currencies.

## Jupyter Notebook Usage

To use the provided Jupyter Notebook examples, install Jupyter Notebook by following the [official installation guide](https://jupyter.org/install).

## CrowdLoan

In the [Jupyter Notebook](CrowdLoan.ipynb), we show how the classes can be used to project the cash flow of a company (CrowdLoan) and analyse the risk with random exchange rate simulations. The historic rates where downloaded using the ForeignExchange API. The results are stored in csv files, which can be opened in Excel. 
