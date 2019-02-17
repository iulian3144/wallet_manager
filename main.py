#!/usr/bin/env python3.6
import argparse
from Wallet import Wallet


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
     account: specify a regex to filter by account name
     amt_min: specify minimum amount value
     amt_max: specify maximum amount value
  NOTE: regex is case insensitive
""")


def main():
    args = parser.parse_args()
    csv_file = args.csv_file
    wallet = Wallet()
    wallet.import_csv(csv_file)
    wallet.filter_items(summarize=args.summarize, filter_data=args.filter)


if __name__ == '__main__':
    main()
