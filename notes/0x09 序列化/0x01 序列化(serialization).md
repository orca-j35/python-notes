# 序列化(serialization)
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - https://pythonguidecn.readthedocs.io/zh/latest/scenarios/serialization.html
> - https://docs.python-guide.org/scenarios/serialization/
> - https://codingpy.com/books/thinkpython2/14-files.html
>

序列化是指将"结构化数据"转换成"可存储格式"的过程，逆向转换过程被称为逆序列化。

比如在 Python 中，结构化数据对象 `dict` 并不能直接存储到文件中:

```python
a = {
    "Type": "A",
    "field1": "value1",
    "field2": "value2",
    "field3": "value3",
}

with open('./file.txt', 'w') as f:
    f.write(a)
#> TypeError: write() argument must be str, not dict
```

但是我们可以通过序列化操作，将 `dict` 对象转换为某种可存储格式。比如可以通过序列化操作将 `dict` 对象转换为字符串序列，从而实现对 `dict` 对象的存储:

```python
a = {
    "Type": "A",
    "field1": "value1",
    "field2": "value2",
    "field3": "value3",
}

print(repr(a))  # 可将repr()理解为一种序列化方法
#> {'Type': 'A', 'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}
with open('./file.txt', 'w') as f:
    f.write(repr(a)) # 序列化后的dict对象，可写入文件

import ast
with open('./file.txt', 'r') as f:
    b = ast.literal_eval(f.readline())
print(f'{type(b)}:{b}')
#> <class 'dict'>:{'Type': 'A', 'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}
```

在某些情况下，序列化的第二个目的是减少数据大小，从而减小对磁盘和带宽的要求。



## Flat vs. Nested data

在开始序列化数据之前，我们需要先了解一下序列化之后会得到何种格式的序列(扁平或嵌套)，下面展示了这两种风格的序列:

- 扁平(*flat*)风格，经序列化后的数据将位于一个物理行中:

```
{ "Type" : "A", "field1": "value1", "field2": "value2", "field3": "value3" }
```

- 嵌套(*nested*)风格，经序列化后的数据会分散在多个物理行中:

```
{"A":
    { "field1": "value1", "field2": "value2", "field3": "value3" } }
```

有关两种风格的更多内容，请见如下讨论：[Python mailing list](https://mail.python.org/pipermail/python-list/2010-October/590762.html), [IETF mailing list](https://www.ietf.org/mail-archive/web/json/current/msg03739.html), [in stackexchange](https://softwareengineering.stackexchange.com/questions/350623/flat-or-nested-json-for-hierarchal-data).



## 序列化格式

"结构化数据"经序列化后，会得到两种序列化格式(*serialization* *format*):

- 文本序列化格式，如 JSON
- 二进制序列化格式，如 pickle



## 文本序列化格式

### 简单文件(扁平数据)

#### repr()

`repr()` 函数以单个对象作为参数，并生成一个可被解释器读取的字符串表示形式。我们可利用 `repr()` 将对象转换为可存储的扁平风格字符串扁平风格:

```python
a = {
    "Type": "A",
    "field1": "value1",
    "field2": "value2",
    "field3": "value3",
}

print(repr(a))  # 可打印序列化后的内容
#> {'Type': 'A', 'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}

with open('./file.txt', 'w') as f:
    f.write(repr(a)) # 可将序列化后的内容写入文件
```

#### ast.literal_eval()

`literal_eval()` 方法可安全地解析 Python 数据类型表达式并求值，支持的数据类型有：字符串、数字、元组、列表、字典、布尔和None。

我们可以使用 `literal_eval()` 对简单文件中的内容进行逆序列化，从而获得 Python 对象:

```python
import ast
with open('./file.txt', 'r') as f:
    inp = ast.literal_eval(f.read())
print(f'{type(inp)}:{inp}')
#> <class 'dict'>:{'Type': 'A', 'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}
```



### CSV 文件 (扁平数据)

Python 中的 CSV 模块实现了读取和写入CSV形式的表格数据的类。

读取的简单例子：

```python
# 从文件中读取CSV数据
import csv
with open('/tmp/file.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

写入的简单例子：

```python
# 将CSV数据写入文件
import csv
with open('/temp/file.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(iterable)
```

该模块的内容、函数和例子可以在 [Python 文档中](https://docs.python.org/3/library/csv.html) 查阅。

### YAML (嵌套数据)

Python 中有许多第三方库用来解析和读取/写入 YAML 文件，例子如下：

```python
# 使用load方法从文件中读取 YAML 内容
import yaml
with open('/tmp/file.yaml', 'r', newline='') as f:
    try:
        print(yaml.load(f))
    except yaml.YAMLError as ymlexcp:
        print(ymlexcp)
```

第三方库的文档可以在 [PyYAML 文档](https://pyyaml.org/wiki/PyYAMLDocumentation) 中查阅。

### JSON 文件 (嵌套数据)

Python 的 JSON 模块可以用来读取和写入 JSON 模块。示例如下：

读取：

```python
# 从文件中读取 JSON 内容
import json
with open('/tmp/file.json', 'r') as f:
    data = json.load(f)
```

写入：

```python
# 使用 dump 方法将 JSON 内容写入文件
import json
with open('/tmp/file.json', 'w') as f:
    json.dump(data, f, sort_keys=True)
```

### XML (嵌套数据)

Python 中 XML 的解析可以使用 xml 库。

示例：

```python
# 从文件中读取 XML 内容
import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
```

使用 xml.dom 和 xml.sax 包的更多文档可以在 [Python XML 库文档](https://docs.python.org/3/library/xml.html) 中找到。

## 二进制序列化格式

### NumPy Array (扁平数据)

Python 的 NumPy 数组可以将数据序列化成字节形式，或从字节形式的数据反序列化。

示例：

```python
import NumPy as np

# 将 NumPy 数组转换为字节形式
byte_output = np.array([ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]).tobytes()

# 将字节形式转换回 NumPy 数组
array_format = np.frombuffer(byte_output)
```

### Pickle (扁平数据)

Python原生的数据序列化模块称为 [Pickle](https://docs.python.org/2/library/pickle.html) 。

示例：

```python
import pickle

# 示例字典
grades = { 'Alice': 89, 'Bob': 72, 'Charles': 87 }

# 使用 dumps 将对象转换为序列化字符串
serial_grades = pickle.dumps( grades )

# 使用 loads 反序列化为对象
received_grades = pickle.loads( serial_grades )
```

## Protobuf

如果您正在寻找支持多种语言的序列化模块，那么 Google 的 [Protobuf](https://developers.google.com/protocol-buffers) 库就是一个选择。

