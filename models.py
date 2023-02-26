class Expense:
    def __init__(self, title, description, amount):
        self.title = title
        self.description = description
        self.amount = amount

class ExpenseDB:
    def __init__(self, id, title, description, amount):
        self.id = id
        self.title = title
        self.description = description
        self.amount = amount
