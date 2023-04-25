from json import JSONEncoder


class Expense:
    def __init__(self, title, category, amount):
        self.title = title
        self.category = category
        self.amount = amount


# Custom JSON encoder for Expense objects
class ExpenseEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Expense):
            return {'category': obj.category, 'amount': obj.amount}
        return super().default(obj)

class IncomeHistoryEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list):
            # Convert the list to a dictionary with a custom key
            return {'income_history': obj}
        return super(IncomeHistoryEncoder, self).default(obj)

class ExpenseDB:
    def __init__(self, id, title, category, amount):
        self.id = id
        self.title = title
        self.category = category
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
