# csv - CSV File Reading and Writing
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - https://docs.python.org/3.7/library/csv.html
>
> 扩展阅读:
>
> - [**PEP 305**](https://www.python.org/dev/peps/pep-0305) - CSV File API
>   The Python Enhancement Proposal which proposed this addition to Python.

CSV (Comma Separated Values) 格式是在电子表格和数据库中最常用的导入和导出格式。在 [**RFC 4180**](https://tools.ietf.org/html/rfc4180.html) 尝试以标准化方式描述 CSV 的格式之前，CSV 格式已被使用了多年。缺乏明确定义的标准，意味着不同应用程序生成和使用的 CSV 格式经常存在一些细微的差别。当我们需要从多个不同的来源处理 CSV 文件时，这些差异会很烦人。尽管如此，虽然分隔符(*delimiters*)和引用(*quoting*)字符各不相同，但整体格式足够相似，因此可用编写一个模块 (`csv`) 来操纵 CSV 格式的数据，从而为程序员隐藏读取和写入数据的细节。

`csv` 模块中实现了一个使用 CSV 格式读取和写入表格数据的类。该类允许程序员"以 Excel 首选格式编辑数据"或"从 Excel 生成的文件中读取数据"，并且程序员不需要知道 Excel 所使用的 CSV 格式的精确细节。程序员同样可以处理其它应用程序理解的 CSV 格式，也可定义自己专用 CSV 格式。

当我们需要读写序列时，可使用 `reader` 和 `writer` 对象；当我们需要以字典形式读写数据时，可使用 `DictReader` 和 `DictWriter` 类

## 函数

在 `csv` 模块中定义了如下函数。

### reader()🪓

🪓csv.reader(*csvfile*, *dialect='excel'*, *\*\*fmtparams*)

该函数会返回一个支持迭代器协议的读取器 (`_csv.reader`) 对象。当你对读取器进行迭代时，每次迭代均会返回 *csvfile* 中的一行数据，并且会把数据表示为一个字符串列表。

除非指定了 `QUOTE_NONNUMERIC` 格式选项(在这种情况下，未加引号的字段将被转换为浮点数)，否则不会执行自动数据类型转换。

```python
csv_list = [
    '"Title 1","Title 2","Title 3","Title 4"',
    '1,"a","08/01/07","å"',
    '2,"b","08/02/07","∫"',
    '3,"c","08/03/07","ç"',
]

r = csv.reader(csv_list)
pprint(list(csv.reader(csv_list)))
pprint(list(csv.reader(csv_list, quoting=csv.QUOTE_NONNUMERIC)))
```

输出:

```
[['Title 1', 'Title 2', 'Title 3', 'Title 4'],
 ['1', 'a', '08/01/07', 'å'],
 ['2', 'b', '08/02/07', '∫'],
 ['3', 'c', '08/03/07', 'ç']]
[['Title 1', 'Title 2', 'Title 3', 'Title 4'],
 [1.0, 'a', '08/01/07', 'å'],
 [2.0, 'b', '08/02/07', '∫'],
 [3.0, 'c', '08/03/07', 'ç']]
```



**参数说明:**

- *csvfile* - 可以是任何可迭代(*iterable*)的对象，比如 file-like 对象和 `list` 对象

  > *csvfile* can be any object which supports the [iterator](https://docs.python.org/3.7/glossary.html#term-iterator) protocol and returns a string each time its `__next__()`method is called — [file objects](https://docs.python.org/3.7/glossary.html#term-file-object) and list objects are both suitable. If *csvfile* is a file object, it should be opened with `newline=''`. [1](https://docs.python.org/3.7/library/csv.html#id3) 
  >
  > If `newline=''` is not specified, newlines embedded inside quoted fields will not be interpreted correctly, and on platforms that use `\r\n` linendings on write an extra `\r` will be added. It should always be safe to specify `newline=''`, since the csv module does its own ([universal](https://docs.python.org/3.7/glossary.html#term-universal-newlines)) newline handling.

- *dialect* - 由于最初缺乏明确的标准，因此不同应用程序使用的 CSV 格式存在一些差异，我们使用方言(*dialect*)一词来表述特定于某个应用程序的 CSV 格式。具体而言，可选参数 *dialect* 表示特定于某种 CSV 方言的一组参数，比如用 `dialect='excel'` 来表示 excel 软件使用 CSV 格式。*dialect* 可以是 [`Dialect`](https://docs.python.org/3.7/library/csv.html#csv.Dialect) 类的子类的实例，也可以是 [`list_dialects()`](https://docs.python.org/3.7/library/csv.html#csv.list_dialects) 函数的返回值之一。

  ```python
  >>> csv.list_dialects()
  ['excel', 'excel-tab', 'unix']
  ```

- *\*\*fmtparams* - 如果要对当前 CSV 方言中的部分格式进行调整，可通过该 *\*\*fmtparams* 来完成。有关方言和格式化参数的详细介绍，请参阅 [Dialects and Formatting Parameters](https://docs.python.org/3.7/library/csv.html#csv-fmt-params)(后面也会翻译这部分内容)

### writer()🪓

🪓csv.writer(*csvfile*, *dialect='excel'*, *\*\*fmtparams*)

该函数的会返回一个写入器 (`_csv.writer`) 对象，写入器负责将用户的数据转换为带分隔符的字符串，并将字符串写至 *csvfile* 中。

为了简化和实现了 DB API 的模块的连接过程，`None` 会被写作空字符串。虽然这种转换不可逆，但这样做更容易将 SQL NULL 数据值转储到 CSV 文件中，并且无需预处理从 `cursor.fetch*`  调用返回的数据。

在写入至 *csvfile* 之前，所有 non-string 数据都会使用 `str()` 函数字符串化。

```python
import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
```

输出:(in eggs.cav)

```
Spam Spam Spam Spam Spam |Baked Beans|
Spam |Lovely Spam| |Wonderful Spam|
```



**参数说明:**

- *csvfile* - 可以是任何拥有 `write()` 方法的对象。如果 *csvfile* 是一个文件对象，那么在打开该文件对象时需设置 `newline=''` 

  > *csvfile* can be any object with a `write()` method. If *csvfile* is a file object, it should be opened with `newline=''` [1](https://docs.python.org/3.7/library/csv.html#id3).
  >
  > If `newline=''` is not specified, newlines embedded inside quoted fields will not be interpreted correctly, and on platforms that use `\r\n` linendings on write an extra `\r` will be added. It should always be safe to specify `newline=''`, since the csv module does its own ([universal](https://docs.python.org/3.7/glossary.html#term-universal-newlines)) newline handling.

- *dialect* - 由于最初缺乏明确的标准，因此不同应用程序使用的 CSV 格式存在一些差异，我们使用方言(*dialect*)一词来表述特定于某个应用程序的 CSV 格式。具体而言，可选参数 *dialect* 表示特定于某种 CSV 方言的一组参数，比如用 `dialect='excel'` 来表示 excel 软件使用 CSV 格式。*dialect* 可以是 [`Dialect`](https://docs.python.org/3.7/library/csv.html#csv.Dialect) 类的子类的实例，也可以是 [`list_dialects()`](https://docs.python.org/3.7/library/csv.html#csv.list_dialects) 函数的返回值之一。

  ```python
  >>> csv.list_dialects()
  ['excel', 'excel-tab', 'unix']
  ```

- *\*\*fmtparams* - 如果要对当前 CSV 方言中的部分格式进行调整，可通过该 *\*\*fmtparams* 来完成。有关方言和格式化参数的详细介绍，请参阅 [Dialects and Formatting Parameters](https://docs.python.org/3.7/library/csv.html#csv-fmt-params) (后面也会翻译这部分内容)



### register_dialect()🪓

🪓csv.register_dialect(*name*[, *dialect*[, *\*\*fmtparams*]])

注册名为 *name* 的 CSV 方言，*name* 必须是一个字符串。

可通过以下方式设置 CSV 方言:

- 向 *dialect* 传递一个 [`Dialect`](https://docs.python.org/3.7/library/csv.html#csv.Dialect) 的子类
- 通过 *\*\*fmtparams* 设置 CSV 方言的参数
- 同时使用上述两种方法

有关方言和格式化参数的详细介绍，请参阅 [Dialects and Formatting Parameters](https://docs.python.org/3.7/library/csv.html#csv-fmt-params) (后面也会翻译这部分内容)



### unregister_dialect()🪓

🪓csv.unregister_dialect(*name*)

从 dialect 注册注册表中删除与 *name* 关联的 CSV 方言。如果 *name* 不是已注册的 CSV 方言名，则会抛出 [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error)。



### get_dialect()🪓

🪓csv.get_dialect(*name*)

返回 *name* 对应的 dialect 对象。如果 *name* 不是已注册的 CSV 方言名，则会抛出 [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error)。

> This function returns an immutable [`Dialect`](https://docs.python.org/3.7/library/csv.html#csv.Dialect).



### list_dialects()🪓

🪓csv.list_dialects()

返回所有已注册的 dialect 的名称



### field_size_limit()🪓

🪓csv.field_size_limit([*new_limit*])

返回解析器允许的当前最大字段的长度。

如果给出了 *new_limit*，则会将当前最大字段的长度设置为 *new_limit*.。

## 类

`csv` 模块中定义了以下类。

### DictReader()🛠

*class* csv.DictReader(*f*, *fieldnames=None*, *restkey=None*, *restval=None*, *dialect='excel'*, *\*args*, *\*\*kwds*)



### DictWriter()🛠

*class* csv.DictWriter(*f*, *fieldnames*, *restval=''*, *extrasaction='raise'*, *dialect='excel'*, *\*args*, *\*\*kwds*)



### Dialect🛠

*class* csv.Dialect



### excel🛠

*class* csv.excel



### excel_tab🛠

*class* csv.excel_tab



### unix_dialect🛠

*class* csv.unix_dialect



### Sniffer🛠

*class* csv.Sniffer

## 常量

`csv` 模块中定义了如下常量。

### QUOTE_ALL🔧

csv.QUOTE_ALL

Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to quote all fields.

### QUOTE_MINIMAL🔧

csv.QUOTE_MINIMAL

Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to only quote those fields which contain special characters such as *delimiter*, *quotechar* or any of the characters in *lineterminator*.

### QUOTE_NONNUMERIC🔧

csv.QUOTE_NONNUMERIC

Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to quote all non-numeric fields.Instructs the reader to convert all non-quoted fields to type *float*.

### QUOTE_NONE🔧

csv.QUOTE_NONE

Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to never quote fields. When the current *delimiter* occurs in output data it is preceded by the current *escapechar* character. If *escapechar* is not set, the writer will raise [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error) if any characters that require escaping are encountered.Instructs [`reader`](https://docs.python.org/3.7/library/csv.html#csv.reader) to perform no special processing of quote characters.

## 异常

`csv` 模块中定义了如下异常。

### Error☣

*exception* csv.Error

Raised by any of the functions when an error is detected.

## 方言和格式化参数

Dialects and Formatting Parameters

### Dialect.delimiter

A one-character string used to separate fields. It defaults to `','`.

### Dialect.doublequote

Controls how instances of *quotechar* appearing inside a field should themselves be quoted. When [`True`](https://docs.python.org/3.7/library/constants.html#True), the character is doubled. When [`False`](https://docs.python.org/3.7/library/constants.html#False), the *escapechar* is used as a prefix to the *quotechar*. It defaults to [`True`](https://docs.python.org/3.7/library/constants.html#True).On output, if *doublequote* is [`False`](https://docs.python.org/3.7/library/constants.html#False) and no *escapechar* is set, [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error) is raised if a *quotechar* is found in a field.

### Dialect.escapechar

A one-character string used by the writer to escape the *delimiter* if *quoting* is set to [`QUOTE_NONE`](https://docs.python.org/3.7/library/csv.html#csv.QUOTE_NONE) and the *quotechar* if *doublequote* is [`False`](https://docs.python.org/3.7/library/constants.html#False). On reading, the *escapechar*removes any special meaning from the following character. It defaults to [`None`](https://docs.python.org/3.7/library/constants.html#None), which disables escaping.

### Dialect.lineterminator

The string used to terminate lines produced by the [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer). It defaults to `'\r\n'`.Note The [`reader`](https://docs.python.org/3.7/library/csv.html#csv.reader) is hard-coded to recognise either `'\r'` or `'\n'` as end-of-line, and ignores *lineterminator*. This behavior may change in the future.

### Dialect.quotechar

A one-character string used to quote fields containing special characters, such as the *delimiter* or *quotechar*, or which contain new-line characters. It defaults to `'"'`.

### Dialect.quoting

Controls when quotes should be generated by the writer and recognised by the reader. It can take on any of the `QUOTE_*` constants (see section [Module Contents](https://docs.python.org/3.7/library/csv.html#csv-contents)) and defaults to [`QUOTE_MINIMAL`](https://docs.python.org/3.7/library/csv.html#csv.QUOTE_MINIMAL).

### Dialect.skipinitialspace

When [`True`](https://docs.python.org/3.7/library/constants.html#True), whitespace immediately following the *delimiter* is ignored. The default is [`False`](https://docs.python.org/3.7/library/constants.html#False).

### Dialect.strict

When `True`, raise exception [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error) on bad CSV input. The default is `False`.

## Reader Objects

以下两种对象属于读取器(reader):

- `DictReader` 的实例
- `reader()` 函数返回的对象

### 方法

读取器对象包含以下公共方法。

#### `csvreader.__next__()`🔨

🔨`csvreader.__next__()`

Return the next row of the reader’s iterable object as a list (if the object was returned from [`reader()`](https://docs.python.org/3.7/library/csv.html#csv.reader)) or a dict (if it is a [`DictReader`](https://docs.python.org/3.7/library/csv.html#csv.DictReader) instance), parsed according to the current dialect. Usually you should call this as `next(reader)`.

### 字段

读取器对象包含以下公共字段。

#### csvreader.dialect

csvreader.dialect

A read-only description of the dialect in use by the parser.

#### csvreader.line_num

csvreader.line_num

The number of lines read from the source iterator. This is not the same as the number of records returned, as records can span multiple lines.

DictReader objects have the following public attribute:

#### csvreader.fieldnames

csvreader.fieldnames

If not passed as a parameter when creating the object, this attribute is initialized upon first access or when the first record is read from the file.

## Writer Objects

### 方法

写入器对象包含以下公共方法。

#### csvwriter.writerow()

csvwriter.writerow(*row*)

Write the *row* parameter to the writer’s file object, formatted according to the current dialect.*Changed in version 3.5:* Added support of arbitrary iterables.

#### csvwriter.writerows()

csvwriter.writerows(*rows*)

Write all elements in *rows* (an iterable of *row* objects as described above) to the writer’s file object, formatted according to the current dialect.

### 字段



#### csvwriter.dialect

csvwriter.dialect



#### DictWriter.writeheader()

DictWriter.writeheader()



## 示例

The simplest example of reading a CSV file:

```python
import csv
with open('some.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

Reading a file with an alternate format:

```python
import csv
with open('passwd', newline='') as f:
    reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
    for row in reader:
        print(row)
```

The corresponding simplest possible writing example is:

```python
import csv
with open('some.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(someiterable)
```

Since [`open()`](https://docs.python.org/3.7/library/functions.html#open) is used to open a CSV file for reading, the file will by default be decoded into unicode using the system default encoding (see [`locale.getpreferredencoding()`](https://docs.python.org/3.7/library/locale.html#locale.getpreferredencoding)). To decode a file using a different encoding, use the `encoding` argument of open:

```python
import csv
with open('some.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

The same applies to writing in something other than the system default encoding: specify the encoding argument when opening the output file.

Registering a new dialect:

```python
import csv
csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)
with open('passwd', newline='') as f:
    reader = csv.reader(f, 'unixpwd')
```

A slightly more advanced use of the reader — catching and reporting errors:

```python
import csv, sys
filename = 'some.csv'
with open(filename, newline='') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            print(row)
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
```

And while the module doesn’t directly support parsing strings, it can easily be done:

```python
import csv
for row in csv.reader(['one,two,three']):
    print(row)
```

