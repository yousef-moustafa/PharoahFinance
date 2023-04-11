from flask import Blueprint, render_template, request, redirect, url_for

from database import create_table_database, get_budgets, get_expenses
from models import ExpenseDB, BudgetDB
from datetime import datetime
import sqlite3

expenses = Blueprint('expenses', __name__)


def get_expenses_from_db():
    conn = sqlite3.connect('database.db')
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
    # Query all expenses from the database
    expenses = get_expenses()
    # Query all budgets from the database
    budgets = get_budgets()
    # Define the total_spent() function
    def total_spent():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT SUM(amount) FROM expenses")
        total = c.fetchone()[0] or 0
        conn.close()
        return round(total, 2)
    # Render the index template with the expenses, budgets, and other variables
    return render_template('index.html', expenses=expenses, budgets=budgets, total_spent=total_spent(), income=income,
                           daily_spending=calculate_daily_spending())


@expenses.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        amount = float(request.form['amount'])
        conn = sqlite3.connect('database.db')
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


def get_budgets_from_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    budgets = []
    for row in c.execute('SELECT * FROM budgets'):
        budgets.append(BudgetDB(row[0], row[1], row[2], row[3]))

    conn.close()
    return budgets


@expenses.route('/create_budget', methods=['GET', 'POST'])
def create_budget():
    if request.method == 'POST':
        budget_name = request.form['budget-name']
        category = request.form['category']
        amount = float(request.form['amount'])

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO budgets (budget_name, category, amount) VALUES (?, ?, ?)",
                  (budget_name, category, amount))
        conn.commit()
        conn.close()
        # Redirect to some success page or URL after inserting the budget into the database
        return redirect(url_for('expenses.index'))

    # Render the create_budget.html template for GET requests
    return render_template('create_budget.html')
