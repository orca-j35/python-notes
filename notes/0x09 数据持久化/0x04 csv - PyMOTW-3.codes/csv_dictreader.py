import csv
import sys

with open(sys.argv[1], 'rt', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# $ python csv_dictreader.py testdata.csv
