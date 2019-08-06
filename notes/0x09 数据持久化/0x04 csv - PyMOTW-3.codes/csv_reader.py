# csv_reader.py
import csv
import sys
# windows默认编码方案是cp936,
# 测试文件testdata.csv的编码方案是utf-8,
# 因此,在windows上需要传递encoding参数
with open(sys.argv[1], 'rt', encoding='utf8', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)