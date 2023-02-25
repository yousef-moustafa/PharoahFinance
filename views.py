from flask import Blueprint, render_template
from models import Expense

expenses = Blueprint('expenses', __name__)

@expenses.route('/')
def index():
    expenses = [
        Expense('Expense 1', 'This is expense 1', 10.99),
        Expense('Expense 2', 'This is expense 2', 19.99),
        Expense('Expense 3', 'This is expense 3', 5.99)
    ]
    return render_template('index.html', expenses=expenses)
