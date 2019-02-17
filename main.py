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
parser.add_argument('--sort-by', metavar='SORTBY', dest='sortby', default='date',
                    help="""Specify item field to sort by.
Supported fields:
  amount: sort by item amount value
    date: sort by item date (default)
   notes: sort by item notes string
category: sort by item category
 account: sort by item account
""")


def main():
    args = parser.parse_args()
    csv_file = args.csv_file
    wallet = Wallet()
    wallet.import_csv(csv_file)
    # build filter dictionary
    filter_data = dict(item.split(':') for item in args.filter.split(','))
    filtered_items = wallet.filter_items(filter_data=filter_data)
    wallet.print_items(filtered_items, summarize=args.summarize, sortby=args.sortby)


if __name__ == '__main__':
    main()
