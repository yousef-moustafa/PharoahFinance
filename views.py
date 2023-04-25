from flask import flash, Blueprint, render_template, request, redirect, url_for
from models import BudgetDB, Expense, ExpenseEncoder, IncomeHistoryEncoder
import sqlite3
import json
from database import create_table_database

expenses = Blueprint('expenses', __name__)


def get_expenses_from_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    expenses = []
    for row in rows:
        expense = Expense(row[1], row[2], row[3])
        expense.id = row[0]
        expenses.append(expense)
    conn.close()
    return expenses


income = 0
amount = 0
income_history = []

@expenses.route('/', methods=['GET', 'POST'])
def index():
    global income, income_history
    if request.method == 'POST':
        income = float(request.form['income'])
        income_history.clear()  # Clear income history list
        income_history.append(income)  # Append income to income history list
    # Query all expenses from the database
    expenses = get_expenses_from_db()
    expenses_json = json.dumps(expenses, cls=ExpenseEncoder)

    income_history_json = json.dumps(income_history, cls=IncomeHistoryEncoder)
    # Query all budgets from the database
    budgets = get_budgets_from_db()

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
                           daily_spending=calculate_daily_spending(), expenses_json=expenses_json, income_history_json=income_history_json)


@expenses.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    global amount
    budgets = get_budgets_from_db()  # Retrieve budgets data from the database
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        amount = request.form['amount']

        # Validate amount as a float
        global income
        try:
            amount = float(amount)
        except ValueError:
            flash('Invalid amount. Please enter a valid number.', 'error')  # Show error message
            return render_template('add_expense.html', budgets=budgets, income=income)

        if not title:
            flash('Description is required.', 'error')  # Show error message
            return render_template('add_expense.html', budgets=budgets, income=income)

        if not amount:
            flash('Amount is required.', 'error')  # Show error message
            return render_template('add_expense.html', budgets=budgets, income=income)

        if amount > income:
            flash('Expense amount cannot exceed current balance.', 'error')  # Show error message
            return render_template('add_expense.html', budgets=budgets, income=income)

        # Check if the total amount of expenses in the category exceeds the budget amount
        budget = get_budget_by_category(category)
        if budget and (get_total_expenses_by_category(category) + amount) > float(budget['amount']):
            flash('Cannot spend more money on this category. Budget limit exceeded.', 'error')  # Show error message
            return render_template('add_expense.html', budgets=budgets, income=income)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (title, category, amount) VALUES (?, ?, ?)", (title, category, amount))
        conn.commit()
        conn.close()

        # Deduct expense amount from current balance
        income -= amount
        income_history.append(income)

        flash('Expense added successfully.', 'success')  # Show success message

    return render_template('add_expense.html', budgets=budgets, income=income)  # Pass budgets data and current balance to the template



@expenses.route('/delete_expense/<int:id>', methods=['POST'])
def delete_expense(id):
    global income
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Check if expense exists in the database
    c.execute("SELECT * FROM expenses WHERE id=?", (id,))
    expense = c.fetchone()
    if not expense:
        conn.close()
        return redirect(url_for('expenses.index'))

    # Delete expense from the database
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    # Update income with the deleted expense amount
    income += expense[3]
    income_history.append(income)

    return redirect(url_for('expenses.index'))


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

        # Check for missing inputs
        if not budget_name or not category or not amount:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('expenses.create_budget'))

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Check for duplicate categories
        c.execute("SELECT * FROM budgets WHERE category=?", (category,))
        existing_budget = c.fetchone()
        if existing_budget:
            flash('Budget for this category already exists. Please choose a unique category.', 'error')
            conn.close()
            return redirect(url_for('expenses.create_budget'))

        # Insert budget into the database
        c.execute("INSERT INTO budgets (budget_name, category, amount) VALUES (?, ?, ?)",
                  (budget_name, category, amount))
        conn.commit()
        conn.close()

        flash('Budget created successfully.', 'success')
    budgets = get_budgets_from_db()

    # Render the create_budget.html template with budgets data for GET requests
    return render_template('create_budget.html', budgets=budgets)

@expenses.route('/delete_budget/<int:id>', methods=['POST'])
def delete_budget(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM budgets WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('expenses.index'))


def get_total_expenses_by_category(category):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Query the expenses table to get the total expenses for the given category
    c.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
    total_expenses = c.fetchone()[0]

    conn.close()

    # Return the total expenses for the given category
    return total_expenses or 0


def get_budget_by_category(category):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM budgets WHERE category=?", (category,))
    budget = c.fetchone()
    conn.close()

    # Check if budget exists for the given category
    if budget is not None:
        budget_dict = {
            'id': budget[0],
            'category': budget[2],
            'amount': budget[3]
        }
        return budget_dict
    else:
        return None