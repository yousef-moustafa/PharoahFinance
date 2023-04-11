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


class Budget:
    def __init__(self, budget_name, category, amount):
        self.budget_name = budget_name
        self.category = category
        self.amount = amount


class BudgetDB:
    def __init__(self, id, budget_name, category, amount):
        self.id = id
        self.budget_name = budget_name
        self.category = category
        self.amount = amount
