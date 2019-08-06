import csv

with open('test.csv', 'wt', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['鲸鱼', 'whales'])

with open('test.csv', 'rt', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    print(list(reader))

with open('test.csv', 'rb') as f:
    reader = csv.reader(f)
    print(list(reader))
