from datetime import datetime


class WalletItem:
    """ Represents an expense or an income.
    item_type:
      0 - expense
      1 - income
    """
    def __init__(self, amount, date, notes="", category=""):
        """
        :param amount: income value
        :param notes: notes string
        :param category: category name
        """
        self.amount: float = amount
        self.date: datetime = date
        self.notes: str = notes
        self.category: str = category

    def __str__(self):
        format_str = '{:10s} {:20s} {:30s} '
        if self.amount < 0:
            format_str += '\033[0;31m{:10.2f}\033[0m'
        else:
            format_str += '\033[0;32m{:10.2f}\033[0m'
        return format_str.format(
            self.date.strftime('%d/%m/%Y'),
            self.category,
            self.notes[:30],
            self.amount)
