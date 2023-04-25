import sqlite3


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
                 category TEXT,
                 amount REAL)''')

    c.execute('''DROP TABLE IF EXISTS budgets''')
    c.execute('''CREATE TABLE budgets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 budget_name TEXT,
                 category TEXT,
                 amount REAL)''')
    conn.commit()
    conn.close()
