from datetime import datetime


class WalletItem:
    """ Represents an expense or an income.
    item_type:
      0 - expense
      1 - income
    """
    def __init__(self, expense, income, date, notes="", category=""):
        """
        :param expense: expense value
        :param income: income value
        :param notes: notes string
        :param category: category name
        """
        self.expense: float = expense
        self.income: float = income
        self.date: datetime = date
        self.notes: str = notes
        self.category: str = category

    def __str__(self):
        return '{:10s} {:20s} {:30s} \033[0;31m{:10.2f}\033[0m \033[0;32m{:10.2f}\033[0m'.format(
            self.date.strftime('%d/%m/%Y'),
            self.category,
            self.notes[:30],
            self.expense,
            self.income)
