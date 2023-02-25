import sqlite3

conn = sqlite3.connect('expenses.db')
c = conn.cursor()

# create table
c.execute('''CREATE TABLE expenses
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT,
             description TEXT,
             amount REAL)''')

# commit changes and close connection
conn.commit()
conn.close()