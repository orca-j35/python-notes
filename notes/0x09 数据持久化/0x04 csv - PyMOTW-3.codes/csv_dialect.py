# csv_dialect.py
import csv

csv.register_dialect('pipes', delimiter='|')

with open('testdata.pipes', 'rt', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, dialect='pipes')
    for row in reader:
        print(row)
