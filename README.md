# Wallet Manager
This script allows you to generate useful reports out of a CSV file
storing transaction details in the following format:
```
Date,Account,Category,Note,Amount,Debit
Date: formatted as `YYYYMMDD`
Category: any string
Account: any string
Note: any string
Amount: a valid floating point number
Debit: 0 or 1; 0 if it's an expense, 1 if it's an income.
```

For help on how to run the script, you can execute `./main.py -h`

## Import data from a SQLite 3.x database
CSV files can be imported from a SQLite 3.x database (backed up by _My Wallet_).
using the _import_script.sql_ SQL script and the following commands.
<pre>
$ sqlite3 <em>&lt;dbfile&gt;</em>
sqlite&gt; .mode csv
sqlite&gt; output <em>csv_file_path</em>
sqlite&gt; .read <em>import_script_path</em>
</pre>

## Colored output using termcolor
Because termcolor does not verify if _stdout_ is a tty, it is recommended to apply the _termcolor.patch_ if you want
to, for example, redirect the output to a file. Otherwise, the escape character (ANSI color codes) will also be present
in the output file (generally, this is not desired).
The patch simply adds a check (_sys.stdout.isatty()_) to see if the _stdout_ is a tty.