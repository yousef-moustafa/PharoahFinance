import sqlite3
from models import Expense

def connect():
    conn = sqlite3.connect('expenses.db')
    return conn

def create_table():
    conn = connect()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS expenses''')
    c.execute('''CREATE TABLE expenses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT,
             description TEXT,
             amount REAL)''')
    conn.commit()
    conn.close()

def add_expense_to_db(expense):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO expenses (title, description, amount) VALUES (?, ?, ?)", (expense.title, expense.description, expense.amount))
    conn.commit()
    conn.close()

def get_expenses():
    conn = connect()
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

def get_expense(id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM expenses WHERE id=?", (id,))
    row = c.fetchone()
    if row:
        expense = Expense(row[1], row[2], row[3])
        expense.id = row[0]
        conn.close()
        return expense
    conn.close()
    return None

def update_expense(expense):
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE expenses SET title=?, description=?, amount=? WHERE id=?", (expense.title, expense.description, expense.amount, expense.id))
    conn.commit()
    conn.close()

def delete_expense(id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()

