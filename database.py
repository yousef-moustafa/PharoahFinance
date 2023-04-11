import sqlite3
from models import Expense, Budget


def connect_database():
    conn = sqlite3.connect('database.db')
    return conn


def create_table_database():
    conn = connect_database()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS expenses''')
    c.execute('''CREATE TABLE expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT,
                 description TEXT,
                 amount REAL)''')

    c.execute('''DROP TABLE IF EXISTS budgets''')
    c.execute('''CREATE TABLE budgets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 budget_name TEXT,
                 category TEXT,
                 amount REAL)''')
    conn.commit()
    conn.close()


def add_expense_to_db(expense):
    conn = connect_database()
    c = conn.cursor()
    c.execute("INSERT INTO expenses (title, description, amount) VALUES (?, ?, ?)",
              (expense.title, expense.description, expense.amount))
    conn.commit()
    conn.close()


def create_budget(budget_name, category, amount):
    # Connect to SQLite database
    conn = connect_database()
    c = conn.cursor()

    # Insert data into 'budgets' table
    c.execute("INSERT INTO budgets (budget_name, category, amount) VALUES (?, ?, ?)",
              (budget_name, category, amount))

    # Commit changes and close database connection
    conn.commit()
    conn.close()


def get_expenses():
    conn = connect_database()
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
    conn = connect_database()
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
    conn = connect_database()
    c = conn.cursor()
    c.execute("UPDATE expenses SET title=?, description=?, amount=? WHERE id=?",
              (expense.title, expense.description, expense.amount, expense.id))
    conn.commit()
    conn.close()


def delete_expense(id):
    conn = connect_database()
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()


def get_budgets():
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT * FROM budgets")
    rows = c.fetchall()
    budgets = []
    for row in rows:
        budget = Budget(row[1], row[2], row[3])
        budget.id = row[0]
        budgets.append(budget)
    conn.close()
    return budgets


def get_budget(id):
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT * FROM budgets WHERE id=?", (id,))
    row = c.fetchone()
    if row:
        budget = Budget(row[1], row[2], row[3])
        budget.id = row[0]
        conn.close()
        return budget
    conn.close()
    return None


def update_budget(budget):
    conn = connect_database()
    c = conn.cursor()
    c.execute("UPDATE budgets SET budget_name=?, category=?, amount=? WHERE id=?",
              (budget.budget_name, budget.category, budget.amount, budget.id))
    conn.commit()
    conn.close()


def delete_budget(id):
    conn = connect_database()
    c = conn.cursor()
    c.execute("DELETE FROM budgets WHERE id=?", (id,))
    conn.commit()
    conn.close()
