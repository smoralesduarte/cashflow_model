
# This file contains the classes that are used to model the company's financial situation

# Credit class (credit that the company gives to the client in COP)
class Credit:
    # Params time: int (months), duration: int (months), annual_interest: float (0 to 1) (annual), amount: float (COP)
    def __init__(self, time=int, duration=int, annual_interest=float, amount=float):
        self.time = time
        self.duration = duration
        # Calculate monthly interest and total interest
        self.monthly_interest = annual_interest / 12
        self.total_interest = self.monthly_interest * duration	
        self.amount = amount

    # Returns the final income of the credit
    def get_final_income(self):
        return self.amount * (1 + self.total_interest)
    
    # Returns the time of the final income
    def get_time_of_income(self):
        return self.time + self.duration

# Loan class (loan that is given to the company in any currency)
class Loan:
    #Params time: int (months), duration: int (months), annual_interest: float (0 to 1) (annual), amount: float, currency: str (COP, USD, EUR)
    def __init__(self, time=int, duration=int, annual_interest=float, amount=float, currency=str):
        self.time = time
        self.duration = duration
        # Calculate monthly interest and total interest
        self.monthly_interest = annual_interest / 12
        self.total_interest = self.monthly_interest * duration	
        self.amount = amount
        self.currency = currency

    # Returns the final payment of the loan and the currency
    def get_final_payment(self):
        return self.amount * (1 + self.total_interest)
    
    # Returns the time of the final payment
    def get_time_of_payment(self):
        return self.time + self.duration
    
# Bank account class (account of the company in any COP, savings give 10% annualy and loans take 15% annualy)
class BankAccount:
    # Params initial_balance: float (COP), saving_interest: float (0 to 1) (annual), loan_interest: float (0 to 1) (annual), duration: int (months)
    def __init__(self, initial_balance=float, saving_interest=float, loan_interest=float, duration=12):
        self.balance = initial_balance
        self.time = 0
        self.monthly_saving_interest = saving_interest / 12
        self.monthly_loan_interest = loan_interest / 12
        self.duration = duration
        self.total_saving_interest = self.monthly_saving_interest * duration
        self.total_loan_interest = self.monthly_loan_interest * duration

    # Add money to the account
    def add_money(self, amount=float):
        self.balance += amount
    
    # Take money from the account
    def take_money(self, amount=float):
        self.balance -= amount
    
    # Add interest to the account and returns the interest
    def add_interest(self):
        if self.balance > 0:
            interest = self.balance * self.total_saving_interest
            self.balance += interest
            return interest
        else:
            interest = self.balance * self.total_loan_interest
            self.balance += interest
            return interest
        

    # Increase the time of the account by one month, add interest and returns the interest
    def simulate_month(self):
        self.time += 1
        if self.time % self.duration == 0:
            return self.add_interest()
        else:
            return 0


# Model class (model of the company's financial situation)
class Model:
    # params fixed_expenses: list of (expense, currency) (fixed expenses are paid every month in any currency), initial_credits: list of Credit (credits that the company has to pay in COP), initial_loans: list of Loan (loans that the company has to pay in any currency), initial_balance: float (COP), bank_account_duration: int (months)
    def __init__(self, initial_fixed_expenses=[], initial_credits=[], initial_loans=[], initial_balance=0.0, bank_account_duration=12):
        self.fixed_expenses = initial_fixed_expenses.copy()
        self.credits = initial_credits.copy()
        self.loans = initial_loans.copy()
        self.time = 0
        self.income = 0.0
        self.expenses = 0.0
        self.COP_income = 0.0
        self.USD_income = 0.0
        self.EUR_income = 0.0
        self.COP_expenses = 0.0
        self.USD_expenses = 0.0
        self.EUR_expenses = 0.0
        # Create the bank account of the company with 10% annual interest for savings and 15% annual interest for loans
        self.bank_account = BankAccount(initial_balance, 0.1, 0.15, bank_account_duration)

    # Add a fixed expense to the model
    def add_fixed_expense(self, expense=float):
        self.expenses.append(expense)

    # Add a credit to the model
    def add_credit(self, credit=Credit):
        self.credits.append(credit)

    # Add a loan to the model
    def add_loan(self, loan=Loan):
        self.loans.append(loan)
    
    # Calculate the COP income of the model	at the current time
    def calculate_COP_income(self, bank_interest=float):
        total = 0
        # Add credits income
        for credit in self.credits:
            if credit.get_time_of_income() == self.time:
                total += credit.get_final_income()

        # Add loans income
        for loan in self.loans:
            if loan.time == self.time and loan.currency == 'COP':
                total += loan.amount

        # Add bank interest
        if bank_interest > 0:
            total += bank_interest

        self.COP_income += total

    # Calculate the USD income of the model at the current time
    def calculate_USD_income(self):
        total = 0
        # Add loans income
        for loan in self.loans:
            if loan.time == self.time and loan.currency == 'USD':
                total += loan.amount

        self.USD_income += total
    
    # Calculate the EUR income of the model at the current time
    def calculate_EUR_income(self):
        total = 0
        # Add loans income
        for loan in self.loans:
            if loan.time == self.time and loan.currency == 'EUR':
                total += loan.amount

        self.EUR_income += total

    # Calculate the income of the model at the current time
    def calculate_income(self, EUR_exchange_rate=float, USD_exchange_rate=float, bank_interest=float):
        self.calculate_COP_income(bank_interest)
        self.calculate_USD_income()
        self.calculate_EUR_income()
        self.income = self.COP_income + self.USD_income * USD_exchange_rate + self.EUR_income * EUR_exchange_rate

    # Calculate the COP expenses of the model at the current time
    def calculate_COP_expenses(self, bank_interest=float):
        
        total = 0
        # Add loans payments
        for loan in self.loans:
            if loan.get_time_of_payment() == self.time and loan.currency == 'COP':
                total += loan.get_final_payment()

        # Add credits payments
        for credit in self.credits:
            if credit.time == self.time:
                total += credit.amount

        # Add fixed expenses
        for expense in self.fixed_expenses:
            if expense[1] == 'COP':
                total += expense[0]
        
        # Add bank interest	
        if bank_interest < 0:
            total -= bank_interest

        self.COP_expenses += total

    # Calculate the USD expenses of the modelat the current time
    def calculate_USD_expenses(self):

        total = 0
        # Add loans payments
        for loan in self.loans:
            if loan.get_time_of_payment() == self.time and loan.currency == 'USD':
                total += loan.get_final_payment() 

        # Add fixed expenses
        for expense in self.fixed_expenses:
            if expense[1] == 'USD':
                total += expense[0]

        self.USD_expenses += total

    # Calculate the EUR expenses of the model
    def calculate_EUR_expenses(self):
        
        total = 0
        # Add loans payments
        for loan in self.loans:
            if loan.get_time_of_payment() == self.time and loan.currency == 'EUR':
                total += loan.get_final_payment() 

        # Add fixed expenses
        for expense in self.fixed_expenses:
            if expense[1] == 'EUR':
                total += expense[0] 

        self.EUR_expenses += total
        
    # Calculate the expenses of the model at the current time
    def calculate_expenses(self, USD_exchange_rate=float, EUR_exchange_rate=float, bank_interest=float):
        self.calculate_COP_expenses(bank_interest)
        self.calculate_USD_expenses()
        self.calculate_EUR_expenses()
        self.expenses = self.COP_expenses + self.USD_expenses * USD_exchange_rate + self.EUR_expenses * EUR_exchange_rate
        
    # Deposit and withdraw money from the bank account of the model
    def update_bank_account(self, bank_interest=float):
        # Take interest from the bank account
        self.bank_account.take_money(bank_interest)
        # Add income to the bank account
        self.bank_account.add_money(self.income)
        # Take expenses from the bank account
        self.bank_account.take_money(self.expenses)


    # Reset all expenses and income of the model to 0
    def reset(self):
        self.income = 0.0
        self.expenses = 0.0
        self.COP_income = 0.0
        self.USD_income = 0.0
        self.EUR_income = 0.0
        self.COP_expenses = 0.0
        self.USD_expenses = 0.0
        self.EUR_expenses = 0.0

    # Increase the time of the model by one month and update the income, expenses and flow, adds bank income to the income and bank expenses to the expenses
    def simulate_month(self, EUR_exchange_rate=float, USD_exchange_rate=float):
        self.time += 1
        # Reset all expenses and income of the model to 0
        self.reset()
        # Calculate bank account interest
        bank_interest = self.bank_account.simulate_month()
        # Calculate the income and expenses of the model
        self.calculate_income(EUR_exchange_rate, USD_exchange_rate, bank_interest)
        self.calculate_expenses(EUR_exchange_rate, USD_exchange_rate, bank_interest)
        # Update the bank account
        self.update_bank_account(bank_interest)

                   

    # Get the COP net flow of the model
    def get_COP_flow(self):
        return self.COP_income - self.COP_expenses
    
    # Get the USD flow of the model
    def get_USD_flow(self):
        return self.USD_income - self.USD_expenses
    
    # Get the EUR flow of the model
    def get_EUR_flow(self):
        return self.EUR_income - self.EUR_expenses
    
    # Get the total flow of the model
    def get_total_flow(self):
        return self.income - self.expenses

    
