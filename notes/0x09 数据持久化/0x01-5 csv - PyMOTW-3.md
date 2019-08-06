# csv - PyMOTW-3
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 在阅读本文时，请交叉参考﹝0x04 csv - CSV File Reading and Writing.md﹞
>
> 参考:
>
> - https://pymotw.com/3/csv/index.html
> - https://en.wikipedia.org/wiki/Comma-separated_values
>
> 扩展阅读:
>
> - [**PEP 305**](https://www.python.org/dev/peps/pep-0305) – CSV File API
> - [Python 2 to 3 porting notes for csv](https://pymotw.com/3/porting_notes.html#porting-csv)



**Purpose: **读写 CSV (*Comma* *Separated* *Value*) 文件

CSV 文件以**纯文本形式**存储表格状的数据(数字和文本)。CSV 文件中的每一行被称为一条数据记录(*record*)，每条记录由一个或多个字段(*field*)组成，字段之间会填充分隔符。由于通常会将逗号(*commas*)用作分隔符，因此这种格式被称为 Comma-Separated Values。

`csv` 模块的功能就是帮助我们处理 CSV 文件中的数据。当我们将数据从电子表格(*spreadsheets*)和数据库(*databases*)导出至 CSV 文件以后，便可以使用 `csv` 模块来处理 CSV 文件中的数据。



## open()

利用 `csv` 模块读写 CSV 文件中的数据时，我们需要使用已打开的 file 流。在使用 `open()` 函数打开文件时，需要注意以下几点:

- 需要以文本模式 `'t'` 打开文件，不能使用字节模式 `'b'`
- 在打开文件时，如果文本并为采用系统默认编码方式，应使用 *encoding* 参数指定编码方式
- 需将 *newline* 设置为 `''`



## Reading

当你需要从 CSV 文件中读取数据时，可使用 `reader()` 函数创建一个 reader 对象。reader 对象支持迭代器(*itertor*)协议，你可以使用 reader 依次处理 CSV 文件中的每一行 record。

```python
# csv_reader.py
import csv
import sys
# windows默认编码方案是cp936,
# 测试文件testdata.csv的编码方案是utf-8,
# 因此,在windows上需使用encoding参数
# 为保证正确解析换行符需newline=''
with open(sys.argv[1], 'rt', encoding='utf8', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

`reader()` 的第一个位置参数表示文本行的来源。本例中使用 file 对象作为第一参数，但实际上任何可迭代(*iterable*)对象都可以用作第一参数，如 `StringIO` 实例、`list` 对象等均可。`reader()` 定义中的其它可选参数被用来控制如何解析来自输入源的数据。

下面是 CSV 测试文件 testdata.csv 中的文本数据:

```
"Title 1","Title 2","Title 3","Title 4"
1,"a",08/18/07,"å"
2,"b",08/19/07,"∫"
3,"c",08/20/07,"ç"
```

在使用 reader 对象读取 `.csv` 文件时，输入数据中的每一行都会被转换为一个字符串列表:

```bash
$ python csv_reader.py testdata.csv

['Title 1', 'Title 2', 'Title 3', 'Title 4']
['1', 'a', '08/18/07', 'å']
['2', 'b', '08/19/07', '∫']
['3', 'c', '08/20/07', 'ç']
```

解析器会处理嵌入在 field 中的换行符，因此 record 和输入文件中的行并不是一一对应的关系。

下面是 CSV 测试文件 testlinebreak.csv 中的文本数据:

```
"Title 1","Title 2","Title 3"
1,"first line
second line",08/18/07
```

对于输入数据中内嵌换行符的 field，解析器会保留这些内嵌换行符:

```bash
$ python csv_reader.py testlinebreak.csv

['Title 1', 'Title 2', 'Title 3']
['1', 'first line\nsecond line', '08/18/07']
```



## Writing

当你需要将数据写入 CSV 文件时，可使用 `writer()` 函数创建一个 writer 对象，然后调用 writer 对象的 `writerow()` 方法将数据写入 `.csv` 文件。

```python
# csv_writer.py
import csv
import sys

unicode_chars = 'å∫ç'

with open(sys.argv[1], 'wt', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(('Title 1', 'Title 2', 'Title 3', 'Title 4'))
    for i in range(3):
        row = (
            i + 1,
            chr(ord('a') + i),
            '08/{:02d}/07'.format(i + 1),
            unicode_chars[i],
        )
        writer.writerow(row)

print(open(sys.argv[1], 'rt', encoding='utf8', newline='').read())
```

输出:

```bash
$ python csv_writer.py testout.csv

Title 1,Title 2,Title 3,Title 4
1,a,08/01/07,å
2,b,08/02/07,∫
3,c,08/03/07,ç
```

输出到 testout.csv 中的内容看起来与之前 testdata.csv 中的内容并不完全相同，并没有为 field 添加引号。

in testout.csv 中的数据:

```
Title 1,Title 2,Title 3,Title 4
1,a,08/01/07,å
2,b,08/02/07,∫
3,c,08/03/07,ç
```

in testdata.csv

```
"Title 1","Title 2","Title 3","Title 4"
1,"a",08/18/07,"å"
2,"b",08/19/07,"∫"
3,"c",08/20/07,"ç"
```



## Quoting

不同 CSV 方言(*dialect*)会采用不同的引用(*quoting*)模式，`writer()` 默认的 CSV dialect 是 `excel`，该 dialect 的源码如下:

```python
class excel(Dialect):
    """Describe the usual properties of Excel-generated CSV files."""
    delimiter = ','
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = QUOTE_MINIMAL
```

`quoting = QUOTE_MINIMAL` 表示在向文件写入内容时，writer 只会对包含特殊字符的字段进行引用，特殊字符是指与 *delimiter*, *quotechar* 或 *lineterminator* 相关的字符。

在调用 `writer()` 时，我们可以使用 *quoting* 参数来修改 dialect 的引用模式，例如:

```python
# csv_writer_quoted.py
import csv
import sys

unicode_chars = 'å∫ç'

with open(sys.argv[1], 'wt', encoding='utf8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(('Title 1', 'Title 2', 'Title 3', 'Title 4'))
    for i in range(3):
        row = (
            i + 1,
            chr(ord('a') + i),
            '08/{:02d}/07'.format(i + 1),
            unicode_chars[i],
        )
        writer.writerow(row)

print(open(sys.argv[1], 'rt', encoding='utf8', newline='').read())
```

`csv.QUOTE_NONNUMERIC` 表示会对所有"非数字"字段进行引用，输出如下:

```bash
$ python csv_writer_quoted.py testout_quoted.csv

"Title 1","Title 2","Title 3","Title 4"
1,"a","08/01/07","å"
2,"b","08/02/07","∫"
3,"c","08/03/07","ç"
```

in testout_quoted.csv

```
"Title 1","Title 2","Title 3","Title 4"
1,"a","08/01/07","å"
2,"b","08/02/07","∫"
3,"c","08/03/07","ç"
```

`csv` 模块中定义了四个常量来表示四种不同的引用模式，如下:

- `QUOTE_ALL` - 对所有字段进行引用，不考虑字段类型

- `QUOTE_MINIMAL` - 对带有特殊字符的字段进行引用，特殊字符是指与 *delimiter*, *quotechar* 或 *lineterminator* 相关的字符，默认模式
- `QUOTE_NONNUMERIC` - 搭配 writer 对象使用时，会对所有"非数字"字段进行引用；搭配 reader 对象使用时，会将所有未被引用的字段转换为 `float` 类型
- `QUOTE_NONE` - 搭配 writer 对象使用时，不会对任何字段进行引用；搭配 reader 对象使用时，不会对引用字符执行任何特殊处理，返回的字段中会包含引用字符

相关笔记:﹝csv - CSV File Reading and Writing.md﹞-> 常量



## Dialects

由于缺乏明确定义 CSV 文件格式的标准，因此需要让解析器保持灵活性，以应对不同的 CSV dialect。要保持灵活性，就意味着需要提供许多参数来控制 CSV 解析和写 CSV 数据。为了避免在构造 reader 或 writer 时需要逐一传递每个参数，可使用 dialect 对象来统一管理所有参数。

在使用 dialect 时可以为其注册一个名称，因此 `csv` 模块的调用者无需事先知道 dialect 的参数设置。可以使用 `list_dialects()` 来检索已注册的 dialect 的完整列表。

```python
# csv_list_dialects.py
import csv
print(csv.list_dialects())
#> ['excel', 'excel-tab', 'unix']
```

`csv` 模块中包含以下三种 dialect: 

- `excel` - 用于处理 Microsoft Excel 以默认 CSV 格式导出的数据，也适用于 [LibreOffice](http://www.libreoffice.org/)

  ```python
  class excel(Dialect):
      """Describe the usual properties of Excel-generated CSV files."""
      delimiter = ','
      quotechar = '"'
      doublequote = True
      skipinitialspace = False
      lineterminator = '\r\n'
      quoting = QUOTE_MINIMAL
  register_dialect("excel", excel)
  ```

- `excel-tabs` - 继承自 `excel`，但将分隔符(*delimiter*)改为 tab

  ```python
  class excel_tab(excel):
      """Describe the usual properties of Excel-generated TAB-delimited files."""
      delimiter = '\t'
  register_dialect("excel-tab", excel_tab)
  ```

- `unix` - 使用双引号引用所有字段，并使用 `\n` 分隔 record

  ```python
  class unix_dialect(Dialect):
      """Describe the usual properties of Unix-generated CSV files."""
      delimiter = ','
      quotechar = '"'
      doublequote = True
      skipinitialspace = False
      lineterminator = '\n'
      quoting = QUOTE_ALL
  register_dialect("unix", unix_dialect)
  ```



### Creating a Dialect

假设输入文件 testdata.pipes 使用 pipes(`|`) 来分隔字段:

```
"Title 1"|"Title 2"|"Title 3"
1|"first line
second line"|08/18/07
```

你可以使用需要的分隔符来注册一个新的 dialect:

```python
# csv_dialect.py
import csv

csv.register_dialect('pipes', delimiter='|')

with open('testdata.pipes', 'rt', encoding='utf-8', newline='') as f:
    reader = csv.reader(f, dialect='pipes')
    for row in reader:
        print(row)
```

使用 pipes dialect 解析文件对象，其输出符合期望:

```bash
$ python csv_dialect.py

['Title 1', 'Title 2', 'Title 3']
['1', 'first line\nsecond line', '08/18/07']
```

还可以通过子类化 `Dialect` 类来创建方言，详见﹝csv - CSV File Reading and Writing.md﹞-> Dialect🛠



### Dialect Parameters

dialect 提供的格式化参数涵盖了解析数据(或写入文件)时需要用到的所有标记(*token*)，下表列出了这些格式化参数:

| Attribute        | Default         | Meaning                                                      |
| ---------------- | --------------- | ------------------------------------------------------------ |
| delimiter        | `,`             | Field separator (one character)                              |
| doublequote      | True            | Flag controlling whether quotechar instances are doubled     |
| escapechar       | None            | Character used to indicate an escape sequence                |
| lineterminator   | `\r\n`          | String used by writer to terminate a line                    |
| quotechar        | `"`             | String to surround fields containing special values (one character) |
| quoting          | `QUOTE_MINIMAL` | Controls quoting behavior described earlier                  |
| skipinitialspace | False           | Ignore whitespace after the field delimiter                  |

—— CSV Dialect Parameters

```python
# csv_dialect_variations.py
import csv
import sys

csv.register_dialect(
    'escaped',
    escapechar='\\',
    doublequote=False,
    quoting=csv.QUOTE_NONE,
)
csv.register_dialect(
    'singlequote',
    quotechar="'",
    quoting=csv.QUOTE_ALL,
)

quoting_modes = {
    getattr(csv, n): n
    for n in dir(csv) if n.startswith('QUOTE_')
}

TEMPLATE = '''\
Dialect: "{name}"

  delimiter   = {dl!r:<6}    skipinitialspace = {si!r}
  doublequote = {dq!r:<6}    quoting          = {qu}
  quotechar   = {qc!r:<6}    lineterminator   = {lt!r}
  escapechar  = {ec!r:<6}
'''

for name in sorted(csv.list_dialects()):
    dialect = csv.get_dialect(name)

    print(
        TEMPLATE.format(
            name=name,
            dl=dialect.delimiter,
            si=dialect.skipinitialspace,
            dq=dialect.doublequote,
            qu=quoting_modes[dialect.quoting],
            qc=dialect.quotechar,
            lt=dialect.lineterminator,
            ec=dialect.escapechar,
        ))

    writer = csv.writer(sys.stdout, dialect=dialect)
    writer.writerow(
        ('col1', 1, '10/01/2010',
         'Special chars: " \' {} to parse'.format(dialect.delimiter)))
    print()
```

上面这个程序会使用不同的 dialect 来解析相同数据，输出结果如下:

```bash
$ python csv_dialect_variations.py

Dialect: "escaped"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 0         quoting          = QUOTE_NONE
  quotechar   = '"'       lineterminator   = '\r\n'
  escapechar  = '\\'

col1,1,10/01/2010,Special chars: \" ' \, to parse

Dialect: "excel"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_MINIMAL
  quotechar   = '"'       lineterminator   = '\r\n'
  escapechar  = None

col1,1,10/01/2010,"Special chars: "" ' , to parse"

Dialect: "excel-tab"

  delimiter   = '\t'      skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_MINIMAL
  quotechar   = '"'       lineterminator   = '\r\n'
  escapechar  = None

col1    1       10/01/2010      "Special chars: "" '     to parse"

Dialect: "singlequote"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_ALL
  quotechar   = "'"       lineterminator   = '\r\n'
  escapechar  = None

'col1','1','10/01/2010','Special chars: " '' , to parse'

Dialect: "unix"

  delimiter   = ','       skipinitialspace = 0
  doublequote = 1         quoting          = QUOTE_ALL
  quotechar   = '"'       lineterminator   = '\n'
  escapechar  = None

"col1","1","10/01/2010","Special chars: "" ' , to parse"
```



### Automatically Detecting Dialects

在解析输入文件时，如果能事先知道与文件相关的 dialect 参数是最完美的。当你不知道输入数据的 dialect 参数时，可以使用 `Sniffer` 类来推断 CSV 数据的 dialect 参数。

`Sniffer` 类提供了以下两个用于推断 dialect 参数的方法:

- `sniff`(*sample*, *delimiters=None*)

  分析给定的样本 *sample* 并返回样本使用的 dialect。

  *delimiters* 是一个字符串，其中包含可能会用作 field 分隔符的字符。

  > Analyze the given *sample* and return a [`Dialect`](https://docs.python.org/3.7/library/csv.html#csv.Dialect) subclass reflecting the parameters found. If the optional *delimiters* parameter is given, it is interpreted as a string containing possible valid delimiter characters.

- `has_header`(*sample*)

  分析给定的样本 *sample* 是否包含标题行

  > Analyze the sample text (presumed to be in CSV format) and return [`True`](https://docs.python.org/3.7/library/constants.html#True) if the first row appears to be a series of column headers.

```python
# csv_dialect_sniffer.py
import csv
from io import StringIO
import textwrap

csv.register_dialect(
    'escaped',
    escapechar='\\',
    doublequote=False,
    quoting=csv.QUOTE_NONE,
)
csv.register_dialect(
    'singlequote',
    quotechar="'",
    quoting=csv.QUOTE_ALL,
)

# Generate sample data for all known dialects
samples = []
for name in sorted(csv.list_dialects()):
    buffer = StringIO()
    dialect = csv.get_dialect(name)
    writer = csv.writer(buffer, dialect=dialect)
    writer.writerow(
        ('col1', 1, '10/01/2010',
         'Special chars " \' {} to parse'.format(dialect.delimiter)))
    samples.append((name, dialect, buffer.getvalue()))

# Guess the dialect for a given sample, and then use the results
# to parse the data.
sniffer = csv.Sniffer()
for name, expected, sample in samples:
    print('Dialect: "{}"'.format(name))
    print('In: {}'.format(sample.rstrip()))
    dialect = sniffer.sniff(sample, delimiters=',\t')
    reader = csv.reader(StringIO(sample), dialect=dialect)
    print('Parsed:\n  {}\n'.format('\n  '.join(repr(r) for r in next(reader))))
```

`sniff()` 会返回一个 `Dialect` 实例，其中包含用于解析数据的相关设置，但结果并不总是完美的，正如示例中的 escaped 方言证明的那样。

```
$ python csv_dialect_sniffer.py

Dialect: "escaped"
In: col1,1,10/01/2010,Special chars \" ' \, to parse
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars \\" \' \\'
  ' to parse'

Dialect: "excel"
In: col1,1,10/01/2010,"Special chars "" ' , to parse"
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' , to parse'

Dialect: "excel-tab"
In: col1        1       10/01/2010      "Special chars "" '      to parse"
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' \t to parse'

Dialect: "singlequote"
In: 'col1','1','10/01/2010','Special chars " '' , to parse'
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' , to parse'

Dialect: "unix"
In: "col1","1","10/01/2010","Special chars "" ' , to parse"
Parsed:
  'col1'
  '1'
  '10/01/2010'
  'Special chars " \' , to parse'
```



## Using Field Names

`csv` 模块不仅能处理序列类型的数据(如 `list`, `set`...)，还可以处理存放在字典中的数据，字典的 key 被表示为 fieldname，字典的 value 被表示为 field。`DictWriter` 用于将字典中的数据转换为 record，`DictReader` 用于将 record 转为字典中的数据。

使用 `DictReader` 类时，可通过 *fieldnames* 参数向 `DictReader` 传递字典的 key；如果省略 *fieldnames* 参数，则会将输入流中的第一行视作字典的 key。使用 `DictWriter` 类时，必须传递 *fielnames* 参数。

```python
import csv
import sys

with open(sys.argv[1], 'rt', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# $ python csv_dictreader.py testdata.csv
```

基于字典的读取器(`DictReader`)和写入器(`DictWriter`)被实现为基于序列的类的包装器，并使用相同的方法和属性。`DictReader` 和 `reader` 的区别是:

- `DictReader` 以 [OrderedDict](https://pymotw.com/3/collections/ordereddict.html#ordereddict) 实例返回 record
- `reader` 以列表或元组返回 record，早期的 Python 版本会将 record 以 `dict` 实例返回

```
$ python csv_dictreader.py testdata.csv

OrderedDict([('Title 1', '1'), ('Title 2', 'a'), ('Title 3',
'08/18/07'), ('Title 4', 'å')])
OrderedDict([('Title 1', '2'), ('Title 2', 'b'), ('Title 3',
'08/19/07'), ('Title 4', '∫')])
OrderedDict([('Title 1', '3'), ('Title 2', 'c'), ('Title 3',
'08/20/07'), ('Title 4', 'ç')])
```

在构造 `DictWriter` 时，必须给出 fieldname 列表，以便 `DictWriter` 实例知道如何在输出中对 record 进行排序。

```python
# csv_dictwriter.py
import csv
import sys

fieldnames = ('Title 1', 'Title 2', 'Title 3', 'Title 4')
headers = {n: n for n in fieldnames}
unicode_chars = 'å∫ç'

with open(sys.argv[1], 'wt', encoding='utf-8', newline='') as f:

    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(3):
        writer.writerow({
            'Title 1': i + 1,
            'Title 2': chr(ord('a') + i),
            'Title 3': '08/{:02d}/07'.format(i + 1),
            'Title 4': unicode_chars[i],
        })

print(open(sys.argv[1], 'rt', encoding='utf-8', newline='').read())
# $ python csv_dictwriter.py testout.csv
```

`DictWriter` 不会将 fieldname 自动写入到文件中，需使用 `writeheader()` 方法显式写入:

```
$ python csv_dictwriter.py testout.csv

Title 1,Title 2,Title 3,Title 4
1,a,08/01/07,å
2,b,08/02/07,∫
3,c,08/03/07,ç
```





## 术语

### record 和 field

CSV 文件中的每一行被称为一条数据记录(*record*)，每条记录由一个或多个字段(*field*)组成，字段之间会填充分隔符。