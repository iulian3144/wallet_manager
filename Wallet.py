import csv
import re
from datetime import datetime
from WalletItem import WalletItem


class Wallet:
    def __init__(self):
        self.items = []

    def import_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            next(reader, None)  # skip first row
            for row in reader:
                date = datetime.strptime(row[0], '%Y%m%d')
                account = row[1]
                category = row[2]
                notes = row[3]
                amount_value = float(row[4])
                if int(row[5]) == 0:
                    amount = -amount_value
                else:
                    amount = amount_value

                self.items.append(WalletItem(
                    date=date,
                    account=account,
                    category=category,
                    notes=notes,
                    amount=amount))
        self.items.sort(key=lambda x: x.date)

    def filter_items(self, summarize=False, filter_data=None):
        """
        Filter items and display them.
        :param summarize: boolean value indicating whether to summarize the results or not
        :param filter_data: filter data used to filter the items
        :return:
        """
        filtered_items = self.items
        if filter_data:
            filter_data = dict(item.split(':') for item in filter_data.split(','))
            if "category" in filter_data:
                filtered_items = [item for item in filtered_items
                                  if re.search(filter_data["category"], item.category, re.IGNORECASE)]
            if "account" in filter_data:
                filtered_items = [item for item in filtered_items
                                  if re.search(filter_data["account"], item.account, re.IGNORECASE)]
            if "notes" in filter_data:
                filtered_items = [item for item in filtered_items
                                  if re.search(filter_data["notes"], item.notes, re.IGNORECASE)]
            if "amt_min" in filter_data:
                value = float(filter_data["amt_min"])
                filtered_items = [item for item in filtered_items if item.amount >= value]
            if "amt_max" in filter_data:
                value = float(filter_data["amt_max"])
                filtered_items = [item for item in filtered_items if item.amount <= value]
            if "begin_date" in filter_data:
                try:
                    begin_date = datetime.strptime(filter_data["begin_date"], '%d/%m/%Y')
                    filtered_items = [item for item in filtered_items if begin_date <= item.date]
                except ValueError as ex:
                    print(ex)
                    exit(1)
            if "end_date" in filter_data:
                try:
                    end_date = datetime.strptime(filter_data["end_date"], '%d/%m/%Y')
                    filtered_items = [item for item in filtered_items if item.date <= end_date]
                except ValueError as ex:
                    print(ex)
                    exit(1)
        expense_sum = 0
        income_sum = 0
        if not summarize:
            print("{:10s} {:20s} {:20s} {:30s} {:>10s}".format("Date", "Account", "Category", "Notes", "Amount"))
            print("-" * 94)
        for item in filtered_items:
            if item.amount < 0:
                expense_sum += abs(item.amount)
            else:
                income_sum += item.amount
            if not summarize:
                print(item)

        expense_sum = round(expense_sum, 2)
        income_sum = round(income_sum, 2)
        if not summarize:
            print("-" * 94)

        print("{:>82s}: \033[0;31m{:10.2f}\033[0m".format("EXPENSE", expense_sum))
        print("{:>82s}: \033[0;32m{:10.2f}\033[0m".format("INCOME", income_sum))
        savings = income_sum - expense_sum

        format_str = "{:>82s}: "
        if savings < 0:
            format_str += "\033[0;31m{:10.2f}\033[0m"
        else:
            format_str += "\033[0;32m{:10.2f}\033[0m"
        print(format_str.format("SAVINGS", savings))
