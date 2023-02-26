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

budget = 0
expenses_month = []
today = datetime.now().date()

@expenses.route('/', methods=['GET', 'POST'])
def index():
    global budget
    if request.method == 'POST':
        budget = float(request.form['budget'])
    def total_spent():
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()

        c.execute("SELECT SUM(amount) FROM expenses")
        total = c.fetchone()[0] or 0

        conn.close()

        return round(total, 2)
    return render_template('index.html', expenses=expenses_list, total_spent=total_spent(), budget=budget, daily_spending=calculate_daily_spending())


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

def get_budget(amount):
    global budget
    budget = float(amount)

def calculate_daily_spending():
    days_remaining = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - today
    days_remaining = days_remaining.days
    if days_remaining == 0:
        daily_spending = 0
    else:
        daily_spending = round((budget - total_spent()) / days_remaining, 2)
    return daily_spending
