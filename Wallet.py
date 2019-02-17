import csv
import re
from datetime import datetime
from WalletItem import WalletItem
from typing import List, Dict
from termcolor import colored, cprint


class Wallet:
    def __init__(self):
        self.items: List[WalletItem] = []

    def import_csv(self, filename: str):
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

                self.items.append(WalletItem(date=date, account=account, category=category, notes=notes, amount=amount))
        self.items.sort(key=lambda x: x.date)

    def filter_items(self, filter_data: Dict[str, str] = None) -> List[WalletItem]:
        """
        Filter items and display them.
        :param filter_data: filter data used to filter the items
        :return: a list containing the filtered items
        """
        filtered_items = self.items
        for key, value in filter_data.items():
            if key == "category":
                filtered_items = [item for item in filtered_items
                                  if re.search(value, item.category, re.IGNORECASE)]
            if key == "account":
                filtered_items = [item for item in filtered_items
                                  if re.search(value, item.account, re.IGNORECASE)]
            if key == "notes" in filter_data:
                filtered_items = [item for item in filtered_items
                                  if re.search(value, item.notes, re.IGNORECASE)]
            if key == "amt_min":
                value = float(value)
                filtered_items = [item for item in filtered_items if item.amount >= value]
            if key == "amt_max":
                value = float(value)
                filtered_items = [item for item in filtered_items if item.amount <= value]
            if key == "begin_date":
                try:
                    begin_date = datetime.strptime(value, '%d/%m/%Y')
                    filtered_items = [item for item in filtered_items if begin_date <= item.date]
                except ValueError as ex:
                    print(ex)
                    exit(1)
            if key == "end_date":
                try:
                    end_date = datetime.strptime(value, '%d/%m/%Y')
                    filtered_items = [item for item in filtered_items if item.date <= end_date]
                except ValueError as ex:
                    print(ex)
                    exit(1)
        return filtered_items

    @staticmethod
    def print_items(items_list: List[WalletItem], summarize=False, sortby: str = "date"):
        """
        :param items_list: items to print
        :param summarize: if True, don't print each item, only the totals
        :param sortby: specify WalletItem field to sort by
        :return: None
        """
        if len(items_list) == 0:
            print("No transaction specified")
            return
        expense_sum = 0
        income_sum = 0
        output_header = "{:10s} {:20s} {:20s} {:30s} {:>10s}".format("Date", "Account", "Category", "Notes", "Amount")
        if not summarize:
            print(output_header)
            print("-" * len(output_header))
        if sortby in dir(items_list[0]):
            items_list.sort(key=lambda x: getattr(x, sortby))
        else:
            items_list.sort(key=lambda x: x.date)

        for item in items_list:
            if item.amount < 0:
                expense_sum += abs(item.amount)
            else:
                income_sum += item.amount
            if not summarize:
                print(item)

        expense_sum = round(expense_sum, 2)
        income_sum = round(income_sum, 2)
        if not summarize:
            print("-" * len(output_header))

        format_str = "{:>82s}: "
        if summarize:
            format_str = "{:>20s}: "
        print((format_str + colored("{:10.2f}", "red")).format("EXPENSE", expense_sum))
        print((format_str + colored("{:10.2f}", "green")).format("INCOME", income_sum))
        savings = income_sum - expense_sum

        if savings < 0:
            term_color = "red"
        else:
            term_color = "green"
        format_str += colored('{:10.2f}', term_color)
        print(format_str.format("SAVINGS", savings))
