#!/usr/bin/env python3.6
import sys
import csv
from datetime import datetime
import argparse
import re


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


class Wallet:
    def __init__(self):
        self.items = []

    def import_csv(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            next(reader, None)  # skip first row
            for row in reader:
                date = datetime.strptime(row[0], '%Y%m%d')
                category = row[1]
                notes = row[2]
                expense = income = 0
                if int(row[4]) == 0:
                    expense = float(row[3])
                else:
                    income = float(row[3])

                self.items.append(WalletItem(expense, income, date, notes, category))
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
                filtered_items = [item for item in filtered_items if re.match(filter_data["category"], item.category)]
            if "notes" in filter_data:
                filtered_items = [item for item in filtered_items if re.match(filter_data["notes"], item.notes)]
            if "exp_min" in filter_data:
                value = float(filter_data["exp_min"])
                filtered_items = [item for item in filtered_items if item.expense >= value]
            if "exp_max" in filter_data:
                value = float(filter_data["exp_max"])
                filtered_items = [item for item in filtered_items if item.expense <= value]
            if "inc_min" in filter_data:
                value = float(filter_data["inc_min"])
                filtered_items = [item for item in filtered_items if item.income >= value]
            if "inc_max" in filter_data:
                value = float(filter_data["inc_max"])
                filtered_items = [item for item in filtered_items if item.income <= value]
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
            print("{:10s} {:20s} {:30s} {:>10s} {:>10s}".format("Date", "Category", "Notes", "Expense", "Income"))
            print("-" * 85)
        for item in filtered_items:
            expense_sum += item.expense
            income_sum += item.income
            if not summarize:
                print(item)

        expense_sum = round(expense_sum, 2)
        income_sum = round(income_sum, 2)
        if not summarize:
            print("-" * 85)
        print("{:>62s}: \033[0;31m{:10.2f}\033[0m \033[0;32m{:10.2f}\033[0m".format(
            "TOTAL", expense_sum, income_sum))
        savings = income_sum - expense_sum
        print("{:>62s}: ".format("SAVINGS"), end='')
        if savings >= 0:
            format_str = "\033[0;32m{:10.2f}\033[0m"
        else:
            format_str = "\033[0;31m{:10.2f}\033[0m"
        print(format_str.format(savings))


parser = argparse.ArgumentParser(description='Wallet Manager', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('csv_file', metavar='CSV_FILE', help='CSV file to import')
parser.add_argument('--summarize', dest='summarize', default=False, action="store_true",
                    help='Summarize output')
parser.add_argument('--filter', metavar='FILTER', dest='filter', const=None,
                    help="""Filter data: field1:value1,field2:value2...
Supported fields:
  begin_date: specify a start date to display the results.
              Date format must be DD/MM/YYYY
    end_date: specify an end date to display the results.
              Same format as begin_date
    category: specify a regex to filter by category
       notes: specify a regex to filter by notes
     exp_min: specify minimum expense value
     exp_max: specify maximum expense value
     inc_min: specify minimum income_value
     inc_max: specify maximum income_value
""")


def main():
    args = parser.parse_args()
    csv_file = args.csv_file
    wallet = Wallet()
    wallet.import_csv(csv_file)
    wallet.filter_items(summarize=args.summarize, filter_data=args.filter)


if __name__ == '__main__':
    main()
