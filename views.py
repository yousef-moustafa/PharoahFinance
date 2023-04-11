from flask import Blueprint, render_template, request, redirect, url_for
from models import ExpenseDB
from datetime import datetime, timedelta
import sqlite3

expenses = Blueprint('expenses', __name__)

def get_expenses_from_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    expenses = []
    for row in c.execute('SELECT * FROM expenses'):
        expenses.append(ExpenseDB(row[0], row[1], row[2], row[3]))

    conn.close()
    return expenses

expenses_list = get_expenses_from_db()

income = 0
expenses_month = []
today = datetime.now().date()

@expenses.route('/', methods=['GET', 'POST'])
def index():
    global income
    if request.method == 'POST':
        income = float(request.form['income'])
    def total_spent():
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()

        c.execute("SELECT SUM(amount) FROM expenses")
        total = c.fetchone()[0] or 0

        conn.close()

        return round(total, 2)
    return render_template('index.html', expenses=expenses_list, total_spent=total_spent(), income=income, daily_spending=calculate_daily_spending())


@expenses.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        amount = float(request.form['amount'])
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (title, description, amount) VALUES (?, ?, ?)", (title, description, amount))
        conn.commit()
        conn.close()
        return redirect(url_for('expenses.index'))
    return render_template('add_expense.html')


def total_spent():
    total = sum(expense.amount for expense in expenses_list)
    return round(total, 2)

def get_income(amount):
    global income
    income = float(amount)

def calculate_daily_spending():
    days_in_a_month = 30.4166667
    if income == 0:
        daily_spending = 0
    else:
        daily_spending = round(income / days_in_a_month)
    return daily_spending


@expenses.route('/create_budget', methods=['GET', 'POST'])
def create_budget():
    if request.method == 'POST':
        # Get the data from the request form
        budget_name = request.form['budget-name']
        category = request.form['category']
        amount = request.form['amount']

        # Code for handling the create budget request
        # ... (process the data and save it to the database, etc.)

        # Redirect to the same create_budget route
        return redirect(url_for('expenses.create_budget'))

    # Render the create_budget.html template for GET requests
    return render_template('create_budget.html')



