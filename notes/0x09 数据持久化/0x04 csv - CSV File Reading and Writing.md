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
> The Python Enhancement Proposal which proposed this addition to Python.
> - https://en.wikipedia.org/wiki/Comma-separated_values

CSV (Comma Separated Values) 格式是在电子表格和数据库中最常用的导入和导出格式。在 [**RFC 4180**](https://tools.ietf.org/html/rfc4180.html) 尝试以标准化方式描述 CSV 的格式之前，CSV 格式已被使用了多年。缺乏明确定义的标准，意味着不同应用程序生成和使用的 CSV 格式经常存在一些细微的差别。当我们需要从多个不同的来源处理 CSV 文件时，这些差异会很烦人。尽管如此，虽然分隔符(*delimiters*)和引用(*quoting*)字符各不相同，但整体格式足够相似，因此可用编写一个模块 (`csv`) 来操纵 CSV 格式的数据，从而为程序员隐藏读取和写入数据的细节。

`csv` 模块中实现了一个使用 CSV 格式读取和写入表格数据的类。该类允许程序员"以 Excel 首选格式编辑数据"或"从 Excel 生成的文件中读取数据"，并且程序员不需要知道 Excel 所使用的 CSV 格式的精确细节。程序员同样可以处理其它应用程序理解的 CSV 格式，也可定义自己专用 CSV 格式。

当我们需要读写序列时，可使用 `reader` 和 `writer` 对象；当我们需要以字典形式读写数据时，可使用 `DictReader` 和 `DictWriter` 类

## 函数

在 `csv` 模块中定义了如下函数。

### reader()🪓

🪓csv.reader(*csvfile*, *dialect='excel'*, *\*\*fmtparams*)

该函数会返回一个支持迭代器协议的读取器 (`_csv.reader`) 对象。对读取器进行迭代时，每次迭代会返回 *csvfile* 中的一行数据，并且会把数据表示为一个字符串列表。

❗有关 `_csv.reader` 对象的更多细节，另见后文 "Reader Object" 小节。

除非设置了 `QUOTE_NONNUMERIC` 格式选项(在这种情况下，未加引号的字段将被转换为浮点数)，否则不会执行自动数据类型转换。详见后文 "QUOTE_NONNUMERIC" 小节

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

- *\*\*fmtparams* - 如果要对当前 CSV 方言(*dialect*)中的部分格式进行调整，可通过该 *\*\*fmtparams* 来完成，可用参数如下: delimiter, doublequote, escapechar, lineterminator, quotechar, quoting, skipinitialspace, strict。详见后文中 "[方言的格式化参数](#方言和格式化参数)" 一节

  

### writer()🪓

🪓csv.writer(*csvfile*, *dialect='excel'*, *\*\*fmtparams*)

该函数的会返回一个写入器 (`_csv.writer`) 对象，写入器负责将用户的数据转换为带分隔符的字符串，并将字符串写至 *csvfile* 中。

❗有关 `_csv.writer` 对象的更多细节，另见后文 "Writer Object" 小节

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

- *\*\*fmtparams* - 如果要对当前 CSV 方言(*dialect*)中的部分格式进行调整，可通过该 *\*\*fmtparams* 来完成。可用参数如下: delimiter, doublequote, escapechar, lineterminator, quotechar, quoting, skipinitialspace, strict。详见后文中 "[方言的格式化参数](#方言和格式化参数)" 一节



### register_dialect()🪓

🪓csv.register_dialect(*name*[, *dialect*[, *\*\*fmtparams*]])

注册名为 *name* 的 CSV 方言，*name* 必须是一个字符串。

可通过以下方式设置 CSV 方言:

- 向 *dialect* 传递一个 [`Dialect`](https://docs.python.org/3.7/library/csv.html#csv.Dialect) 的子类
- 通过 *\*\*fmtparams* 设置 CSV 方言的参数
- 同时使用上述两种方法

有关方言和格式化参数的详细介绍，详见后文中 "[方言的格式化参数](#方言和格式化参数)" 一节

示例 - 注册新 dialect:

```python
import csv
csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)
with open('passwd', newline='') as f:
    reader = csv.reader(f, 'unixpwd')
```



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

在 `csv` 模块中定义了以下类。

### DictReader()🛠

> 请交叉参考 "Reader Object" 小节

*class* csv.DictReader(*f*, *fieldnames=None*, *restkey=None*, *restval=None*, *dialect='excel'*, *\*args*, *\*\*kwds*)

该构造函数会创建一个 `csv.DictReader` 类的实例，你可以像操作 `_csv.reader` 实例(由 `reader()` 返回) 一样操作 `DictReader` 实例，也就是说 `DictReader` 实例同样支持迭代操作。

❗有关 `csv.DictReader` 对象的更多细节，另见后文 "Reader Object" 小节。

对 `DictReader` 实例进行迭代时，每次迭代会返回一个 [`OrderedDict`](https://docs.python.org/3.7/library/collections.html#collections.OrderedDict) 映射，映射中的键值对由 *fieldnames* 中的内容和 *f* 中的一行数据组成，如果没有传递 *fieldname* 则会将 *f* 中的第一行视作 *fieldnames*。

```python
'''in eggs.csv
Title 1,Title 2,Title 3,Title 4
1,a,08/01/07,å
2,b,08/02/07,∫
'''
with open('eggs.csv', 'r', newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    pprint(list(reader))
print('=============')
with open('eggs.csv', 'r', newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(
        csvfile, fieldnames=["Title 1", "Title 2", "Title 3", "Title 4"])
    pprint(list(reader))
```

输出 - 注意观察有无 *fieldnames* 的差别:

```
[OrderedDict([('Title 1', '1'),
              ('Title 2', 'a'),
              ('Title 3', '08/01/07'),
              ('Title 4', 'å')]),
 OrderedDict([('Title 1', '2'),
              ('Title 2', 'b'),
              ('Title 3', '08/02/07'),
              ('Title 4', '∫')])]
=============
[OrderedDict([('Title 1', 'Title 1'),
              ('Title 2', 'Title 2'),
              ('Title 3', 'Title 3'),
              ('Title 4', 'Title 4')]),
 OrderedDict([('Title 1', '1'),
              ('Title 2', 'a'),
              ('Title 3', '08/01/07'),
              ('Title 4', 'å')]),
 OrderedDict([('Title 1', '2'),
              ('Title 2', 'b'),
              ('Title 3', '08/02/07'),
              ('Title 4', '∫')])]
```

> *Changed in version 3.6:* Returned rows are now of type `OrderedDict`.



**参数说明:** 

下面未提及的关键字参数都会在构造器 `__init__` 中传递给 `reader()` 函数，请交叉参考 "reader()" 小节中参数说明部分的内容

- *f* - 可以是任何可迭代(*iterable*)的对象，比如 file-like 对象和 `list` 对象。对于文件对象，同样需要设置 `newline=''`

  ```python
  csv_list = [
      '"Title 1","Title 2","Title 3","Title 4"',
      '1,"a","08/01/07","å"',
      '2,"b","08/02/07","∫"',
  ]
  dr = csv.DictReader(
      csv_list, fieldnames=["Title 1", "Title 2", "Title 3", "Title 4"])
  pprint(list(dr))
  ```

  输出:

  ```
  [OrderedDict([('Title 1', 'Title 1'),
                ('Title 2', 'Title 2'),
                ('Title 3', 'Title 3'),
                ('Title 4', 'Title 4')]),
   OrderedDict([('Title 1', '1'),
                ('Title 2', 'a'),
                ('Title 3', '08/01/07'),
                ('Title 4', 'å')]),
   OrderedDict([('Title 1', '2'),
                ('Title 2', 'b'),
                ('Title 3', '08/02/07'),
                ('Title 4', '∫')])]
  ```

- *fieldnames* - 实参值是一个序列([*sequence*](https://docs.python.org/3.7/glossary.html#term-sequence))。如果省略 *fieldnames*，则会将 *f* 中的第一行用作 *fieldnames*。[`OrderedDict`](https://docs.python.org/3.7/library/collections.html#collections.OrderedDict) 映射中的键值对始终按照 *fieldnames* 的顺序排序。

- *restkey* - 如果一行中字段的数量大于字段名的数量，则会将多余的字段放置在一个列表中，并以 *restkey* 作为键(默认值是 `None`)。

- *restval* - 如果某个非空行中字段的数量少于字段名的数量，则会将这些字段设置为 *restval* (默认值是 `None`)。

  ```python
  csv_list = [
      '"Title 1","Title 2","Title 3","Title 4"',
      '1,"a","08/01/07","å"',
      '2,"b","08/02/07","∫","j"',
      '3,"c","08/03/07"',
  ]
  dr = csv.DictReader(csv_list, restkey='!!!', restval='???')
  pprint(list(dr))
  ```

  输出:

  ```
  [OrderedDict([('Title 1', '1'),
                ('Title 2', 'a'),
                ('Title 3', '08/01/07'),
                ('Title 4', 'å')]),
   OrderedDict([('Title 1', '2'),
                ('Title 2', 'b'),
                ('Title 3', '08/02/07'),
                ('Title 4', '∫'),
                ('!!!', ['j'])]),
   OrderedDict([('Title 1', '3'),
                ('Title 2', 'c'),
                ('Title 3', '08/03/07'),
                ('Title 4', '???')])]
  ```



### DictWriter()🛠

> 请交叉参考 "Writer Object" 小节

*class* csv.DictWriter(*f*, *fieldnames*, *restval=''*, *extrasaction='raise'*, *dialect='excel'*, *\*args*, *\*\*kwds*)

该构造函数会创建一个 `csv.DictWriter` 类的实例，你可以像操作 `_csv.writer` 实例(由 `writer()` 返回) 一样操作 `DictWriter` 实例。区别在于，前者将序列中的内容写入文件，后者将字典中的内容写入文件。

```python
import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
```

输出(in names.csv):

```
first_name,last_name
Baked,Beans
Lovely,Spam
Wonderful,Spam
```



**参数说明:** 

下面未提及的关键字参数都会在构造器 `__init__` 中传递给 `writer()` 函数，请交叉参考 "writer()" 小节中参数说明部分的内容

- *fieldnames* - 实参值是一个由 key 组成的序列([*sequence*](https://docs.python.org/3.7/glossary.html#term-sequence))

  > The *fieldnames* parameter is a [`sequence`](https://docs.python.org/3.7/library/collections.abc.html#module-collections.abc) of keys that identify the order in which values in the dictionary passed to the `writerow()` method are written to file *f*. 
  >
  > Note that unlike the [`DictReader`](https://docs.python.org/3.7/library/csv.html#csv.DictReader) class, the *fieldnames* parameter of the [`DictWriter`](https://docs.python.org/3.7/library/csv.html#csv.DictWriter) class is not optional.

- *restval* - 如果传递给 `writerow()` 的字典中缺少某个 field，则会将 *resrval* 填充到对应的 fieldname 中。

  > The optional *restval* parameter specifies the value to be written if the dictionary is missing a key in *fieldnames*. 

- *extrasaction* - 如果传递给 `writerow()` 的字典中含有 *fieldname* 以外的键，则会采取 *extrasaction* 中给定的操作。

  > If it is set to `'raise'`, the default value, a [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError) is raised. If it is set to `'ignore'`, extra values in the dictionary are ignored. 



### Dialect🛠

*class* csv.Dialect

`Dialect` 类是一个依赖于类属性的容器类，用于描述特定的 CSV 方言。必须通过继承方式来使用 `Dialect` 类，使用方法可以参考 `csv.excel` 类。

`Dialect` 子类中的可用属性如下: delimiter, doublequote, escapechar, lineterminator, quotechar, quoting, skipinitialspace, strict.

在创建 reader 或 writer 对象时，可用通过 *dialect* 参数设置所需的 `Dialect` 子类，也可以是已注册的子类的名称。

在创建 reader 或 writer 对象时，如果需要对当前 CSV 方言(*dialect*)中的部分格式进行调整，可通过格式化参数来完成，这些参数的含义与 `Dialect` 类中的同名属性相同。可用参数如下: delimiter, doublequote, escapechar, lineterminator, quotechar, quoting, skipinitialspace, strict 



#### 方言的格式化参数

在 `Dialect` 的子类中，我们可以通过以下类属性来设置 CSV 方言(*dialect*)的格式。

##### Dialect.delimiter

> A one-character string used to separate fields. It defaults to `','`.

用来分隔字段的单个字符，默认是 `,`

```python
import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name', 'age']
    writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames,
        delimiter='|',# 将|用作分隔符
    )

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans', 'age': 12})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam', 'age': 13})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam', 'age': 9})
```

输出: (in name.csv)

```
first_name|last_name|age
Baked|Beans|12
Lovely|Spam|13
Wonderful|Spam|9
```



##### Dialect.doublequote

> Controls how instances of *quotechar* appearing inside a field should themselves be quoted. When [`True`](https://docs.python.org/3.7/library/constants.html#True), the character is doubled. When [`False`](https://docs.python.org/3.7/library/constants.html#False), the *escapechar* is used as a prefix to the *quotechar*. It defaults to [`True`](https://docs.python.org/3.7/library/constants.html#True).On output, if *doublequote* is [`False`](https://docs.python.org/3.7/library/constants.html#False) and no *escapechar* is set, [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error) is raised if a *quotechar* is found in a field.

当字段中出现 *quotechar* 时，需使用 `Dialect.doublequote` 来控制 *quotechar* 的显式方式:

- `doublequote=True` - 会将字段中的 *quotechar* 重复显式两次，默认情况。
- `doublequote=False` - 会在字段中的 *quotechar* 前添加 *escapechar*，如果未设置 *escapechar* 则会抛出异常。

```python
import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name', 'age']
    writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames,
        quotechar='~',
    )

    writer.writeheader()
    writer.writerow({'first_name': 'Baked~!', 'last_name': 'Beans', 'age': 12})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam', 'age': 13})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam', 'age': 9})
```

输出: (in name.csv)

```
first_name,last_name,age
~Baked~~!~,Beans,12
Lovely,Spam,13
Wonderful,Spam,9
```



##### Dialect.escapechar

> A one-character string used by the writer to escape the *delimiter* if *quoting* is set to [`QUOTE_NONE`](https://docs.python.org/3.7/library/csv.html#csv.QUOTE_NONE) and the *quotechar* if *doublequote* is [`False`](https://docs.python.org/3.7/library/constants.html#False). 
>
> ❓On reading, the *escapechar* removes any special meaning from the following character. It defaults to [`None`](https://docs.python.org/3.7/library/constants.html#None), which disables escaping.

设置转义字符，默认值是 `None`，有以下两种使用情况:

- 在创建 writer 对象时，如果 `quoting=csv.QUOTE_NONE`，那么当某个输出字段中包含 *delimiter* (分隔符)，便会在 *delimiter* 前方添加 *escapechar* 字符。如果需要使用 *escapechar*，但并未设置 *escapechar*，则会抛出 [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error)。
- 会在字段中的 *quotechar* 前添加 *escapechar*，如果未设置 *escapechar* 则会抛出异常。



##### Dialect.lineterminator

> The string used to terminate lines produced by the [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer). It defaults to `'\r\n'`.
>
> Note The [`reader`](https://docs.python.org/3.7/library/csv.html#csv.reader) is hard-coded to recognise either `'\r'` or `'\n'` as end-of-line, and ignores *lineterminator*. This behavior may change in the future.

设置写入文件时使用的行终止符，默认值是 `'\r\n'`。

在读取文件时会忽略 *lineterminator*，并使用 `'\r'` 或 `'\n'` 作为行尾。



##### Dialect.quotechar

> A one-character string used to quote fields containing special characters, such as the *delimiter* or *quotechar*, or which contain new-line characters. It defaults to `'"'`.

设置用来引用字段的字符



##### Dialect.quoting

> Controls when quotes should be generated by the writer and recognised by the reader. It can take on any of the `QUOTE_*` constants (see section [Module Contents](https://docs.python.org/3.7/library/csv.html#csv-contents)) and defaults to [`QUOTE_MINIMAL`](https://docs.python.org/3.7/library/csv.html#csv.QUOTE_MINIMAL).

设置在什么情况下会对字段进行引用



##### Dialect.skipinitialspace

> When [`True`](https://docs.python.org/3.7/library/constants.html#True), whitespace immediately following the *delimiter* is ignored. The default is [`False`](https://docs.python.org/3.7/library/constants.html#False).

是否忽略 *delimiter* 后的空白符，默认时 `False`

##### Dialect.strict

> When `True`, raise exception [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error) on bad CSV input. The default is `False`.

在输入中遇到错误的 CSV 时，是否抛出异常，默认是 `False`



#### 子类

##### excel🛠

*class* csv.excel

`excel` 类定义了 Excel 生成的 CSV 文件的常用属性，其方言名被注册为 `'excel'`。 



##### excel_tab🛠

*class* csv.excel_tab

`excel_tab` 类定义了 Excel 生成的 TAB-delimited 文件的常用属性，其方言名被注册为 `'excel-tab'`。



##### unix_dialect🛠

*class* csv.unix_dialect

`unix_dialect` 类定义了在 UNIX 系统上生成的 CSV 文件的常用属性，即使用 `'\n'` 作为行终止符并引用所有字段，其方言名被注册为 `'unix'`。

> *New in version 3.2.*

### Sniffer🛠

*class* csv.Sniffer

Sniffer 类用于推断 CSV 文件的格式，该类提供下述两个方法:

- `sniff`(*sample*, *delimiters=None*)

  分析给定的样本 *sample* 并返回样本使用的 dialect

  > Analyze the given *sample* and return a [`Dialect`](https://docs.python.org/3.7/library/csv.html#csv.Dialect) subclass reflecting the parameters found. If the optional *delimiters* parameter is given, it is interpreted as a string containing possible valid delimiter characters.

- `has_header`(*sample*)

  分析给定的样本 *sample* 是否包含标题行

  > Analyze the sample text (presumed to be in CSV format) and return [`True`](https://docs.python.org/3.7/library/constants.html#True) if the first row appears to be a series of column headers.

示例

```python
with open('example.csv', newline='') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)
    # ... process CSV file contents here ...
```



## 常量

在 `csv` 模块中定义了如下常量。

### QUOTE_ALL🔧

🔧csv.QUOTE_ALL

> Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to quote all fields.

writer 对象在向文件写入内容时，会对所有字段进行引用，用于设置格式化参数 `quoting`。

```python
import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['first_name', 'last_name', 'age']
    writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames,
        quotechar='|',
        quoting=csv.QUOTE_ALL
        # doublequote=True,
    )

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans', 'age': 12})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam', 'age': 13})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam', 'age': 9})
```

输出: (in names.csv)

```
|first_name|,|last_name|,|age|
|Baked|,|Beans|,|12|
|Lovely|,|Spam|,|13|
|Wonderful|,|Spam|,|9|
```



### QUOTE_MINIMAL🔧

🔧csv.QUOTE_MINIMAL

> Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to only quote those fields which contain special characters such as *delimiter*, *quotechar* or any of the characters in *lineterminator*.

writer 对象在向文件写入内容时，只会对包含特殊字符的字段进行引用，特殊字符是指  *delimiter*, *quotechar* 或 *lineterminator* 中的字符串



### QUOTE_NONNUMERIC🔧

🔧csv.QUOTE_NONNUMERIC

> Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to quote all non-numeric fields. 
>
> Instructs the reader to convert all non-quoted fields to type *float*.

writer 对象在向文件写入内容时，会对所有非数字字段进行引用。

reader 对象在读取内容时，会将所有未引用的字段转换为 `float` 类型。



### QUOTE_NONE🔧

🔧csv.QUOTE_NONE

> Instructs [`writer`](https://docs.python.org/3.7/library/csv.html#csv.writer) objects to never quote fields. When the current *delimiter* occurs in output data it is preceded by the current *escapechar* character. If *escapechar* is not set, the writer will raise [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error) if any characters that require escaping are encountered.
>
> Instructs [`reader`](https://docs.python.org/3.7/library/csv.html#csv.reader) to perform no special processing of quote characters.

writer 对象在向文件写入内容时，永远不会对任何字段进行引用。如果某个输出字段中包含 *delimiter* (分隔符)，会在 *delimiter* 前方添加 *escapechar* 字符。如果需要使用 *escapechar*，但并未设置 *escapechar*，则会抛出 [`Error`](https://docs.python.org/3.7/library/csv.html#csv.Error)。

reader 对象在读取内容时，不会对引用字符执行任何特殊处理。

## 异常

`csv` 模块中定义了如下异常。

### Error☣

*exception* csv.Error

在检测到错误时，函数会抛出此异常。

> Raised by any of the functions when an error is detected.
>

示例 - 捕获并报告错误:

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



## Reader Objects

reader 对象并非是特指某个类型的对象，而是指支持 CSV 读取操作的对象，以下两种类型均是 reader 对象:

- `DictReader` 的对象
- `reader()` 函数返回的 `_csv.reader` 对象



### `__next__()`🔨

🔨`csvreader.__next__()`

> Return the next row of the reader’s iterable object as a list (if the object was returned from [`reader()`](https://docs.python.org/3.7/library/csv.html#csv.reader)) or a dict (if it is a [`DictReader`](https://docs.python.org/3.7/library/csv.html#csv.DictReader) instance), parsed according to the current dialect. Usually you should call this as `next(reader)`.

两种 reader 对象都包含该公共方法。



### dialect🔧

🔧csvreader.dialect

> A read-only description of the dialect in use by the parser.

两种 reader 对象都包含该公共属性。



### line_num🔧

🔧csvreader.line_num

> The number of lines read from the source iterator. This is not the same as the number of records returned, as records can span multiple lines.

两种 reader 对象都包含该公共属性。



### fieldnames🔧

🔧csvreader.fieldnames

> If not passed as a parameter when creating the object, this attribute is initialized upon first access or when the first record is read from the file.

只有 `DictReader` 对象包含该公共属性



## Writer Objects

writer 对象并非是特指某个类型的对象，而是指支持 CSV 写操作的对象，以下两种类型均是 reader 对象:

- `DictWriter` 的对象
- `Writer()` 函数返回 `_csv.writer` 对象

### 参数 *row*

对 `_csv.writer` 而言，*row* 必须是由字符串或数字组成的可迭代序列；
对 `DictWriter` 而言，*row* 必须是一个字典，并以 fieldname 为键，字符串或数字为值。

数字会先经过 `str()` 处理，然后在写入文件。

>  Note that complex numbers are written out surrounded by parens. This may cause some problems for other programs which read CSV files (assuming they support complex numbers at all).

### writerow()🔨

🔨csvwriter.writerow(*row*)

> Write the *row* parameter to the writer’s file object, formatted according to the current dialect.
>
> *Changed in version 3.5:* Added support of arbitrary iterables.

两种 writer 对象都支持该公共方法。



### writerows()🔨

🔨csvwriter.writerows(*rows*)

> Write all elements in *rows* (an iterable of *row* objects as described above) to the writer’s file object, formatted according to the current dialect.

两种 writer 对象都支持该公共方法。



### csvwriter.dialect🔧

🔧csvwriter.dialect

> A read-only description of the dialect in use by the writer.

只有 `Writer()` 函数返回的对象支持该公共属性



### writeheader()🔨

🔨DictWriter.writeheader()

> Write a row with the field names (as specified in the constructor).

只有 `DictWriter` 对象支持该公共方法



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

And while the module doesn’t directly support parsing strings, it can easily be done:

```python
import csv
for row in csv.reader(['one,two,three']):
    print(row)
```

## 术语

### field

在 csv 文件中，两个分隔符之间的部分被称为一个字段(*feild*)。

```
first_name|last_name|age
Bake,d|Beans|12
Lovely|Spam|13
Wonderful|Spam|9
```

在上面这个 csv 文件中，`first_name`, `last_name`, `age` 均表示一个字段

###  record

在 csv 文件中，每一行数据被称为一条数据记录(*record*)