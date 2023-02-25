from flask import Blueprint, render_template, request, redirect, url_for
from models import Expense
from datetime import datetime, timedelta

expenses = Blueprint('expenses', __name__)

expenses_list = [
    Expense('Expense 1', 'This is expense 1', 10.99),
    Expense('Expense 2', 'This is expense 2', 19.99),
    Expense('Expense 3', 'This is expense 3', 5.99)
]

budget = 0
expenses_month = []
today = datetime.now().date()

@expenses.route('/')
def index():
    return render_template('index.html', expenses=expenses_list, total_spent=total_spent(), budget=budget, daily_spending=calculate_daily_spending())

@expenses.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        amount = float(request.form['amount'])
        expense = Expense(title, description, amount)
        expenses_list.append(expense)
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
