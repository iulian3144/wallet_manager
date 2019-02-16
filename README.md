# Wallet Manager
This script allows you to generate useful reports out of a CSV file
storing transaction details in the following format:
```
Date,Category,Note,Amount,Debit
Date: formatted as `YYYYMMDD`
Category: any string
Note: any string
Amount: a valid floating point number
Debit: 0 or 1; 0 if it's an expense, 1 if it's an income.
```
