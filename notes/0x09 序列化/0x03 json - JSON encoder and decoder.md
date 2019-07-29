# json - JSON encoder and decoder
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`json` — JSON encoder and decoder](https://docs.python.org/3/library/json.html)
> - https://pymotw.com/3/json/index.html
> - https://codingpy.com/books/thinkpython2/14-files.html

在阅读本文时，务必配合﹝0x04 json - PyMOTW-3﹞一起食用

## 概述

[`json`](https://docs.python.org/3/library/json.html#module-json) 模块采用了与 [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal) 和 [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) 的类似的 API，其功能是将内存中的 Python 对象转换为 JSON 对象。与 pickle 不同，JSON 具有以多种语言（尤其是 JavaScript）实现的优点。在使用 REST API 的 Web 服务端和客户端之间通常会使用 JSON 进行通信，同时对于应用程序间的通信需求也非常有用。

pickle 协议和 [JSON (JavaScript Object Notation)](http://json.org/) 主要存在以下区别:

- JSON 是一种文本序列化格式(*text* *serialization* *format*)，输出结果是 Unicode 文本(在大多数时候 Unicode 文本会被编码为 UTF-8)；pickle 是一种二进制序列化格式(*binary* *serialization* format)，输出结果是二进制数据。
- JSON 的输出结果人类可读，pickle 的输出结果人类不可读。
- JSON 是可互操作的，并且在 Python 生态系统之外广泛使用，而 pickle 只能在 Python 中使用。
- 默认情况下，JSON 仅支持部分 Python 内置类型，并不支持自定义类；pickle 支持任意 Python 类型 (many of them automatically, by clever usage of Python’s introspection facilities; complex cases can be tackled by implementing [specific object APIs](https://docs.python.org/3/library/pickle.html#pickle-inst)).



> ⚠ JSON is a subset of [YAML](http://yaml.org/) 1.2. The JSON produced by this module’s default settings (in particular, the default *separators* value) is also a subset of YAML 1.0 and 1.1. This module can thus also be used as a YAML serializer.



### JavaScript 与 JSON

> [JSON (JavaScript Object Notation - JavaScript 对象标记)](http://json.org/), specified by [**RFC 7159**](https://tools.ietf.org/html/rfc7159.html) (which obsoletes [**RFC 4627**](https://tools.ietf.org/html/rfc4627.html)) and by [ECMA-404](http://www.ecma-international.org/publications/standards/Ecma-404.htm), is a lightweight data interchange format inspired by [JavaScript](https://en.wikipedia.org/wiki/JavaScript) object literal syntax (although it is not a strict subset of JavaScript [1](https://docs.python.org/3/library/json.html#rfc-errata) ).

任何 JavaScript 支持的类型都可通过 JSON 来表示，如字符串、数字、对象、数组等等，其中对象和数组是比较特殊的两种类型:

- 对象(*object*) - 在 JavaScript 中由 `{}` 包围的内容被称为对象，数据结构为键值对结构 `{key1：value1, key2：value2, ...} `，key 是对象的属性，value 是属性的值。key 可以是整数或字符串，value 可以是任何类型。
- 数组(*array*) - 在 JavaScript 中由 `[]` 包围的内容被称为数组，数据结构为索引结构 ` ["java", "javascript", "vb", ...] `。在 JavaScript 中，数组是一种比较特殊的数据类型，既可以采用索引结构也可以采用键值对结构。

JSON 示例:

```json
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}, {
     "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
```

对象和数组可以以任意方式进行嵌套。

## 基本用法

### json.dump()🔨

json.dump(*obj*, *fp*, *\**, *skipkeys=False*, *ensure_ascii=True*, *check_circular=True*, *allow_nan=True*, *cls=None*, *indent=None*, *separators=None*, *default=None*, *sort_keys=False*, ***kw*)

`dump()` 会将 *obj* 对象序列化为 JSON 格式的数据流，并写入到 *fp* 中，序列化过程遵守如下[转换表](https://docs.python.org/3/library/json.html#py-to-json-table):

| Python                                 | JSON      |
| :------------------------------------- | :-------- |
| dict                                   | {} object |
| list, tuple                            | [] array  |
| str                                    | "string"  |
| int, float, int- & float-derived Enums | number    |
| True                                   | true      |
| False                                  | false     |
| None                                   | null      |

⚠与 [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) 和 [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal) 不同，JSON 并非一个框架协议(*framed* *protocol*)。如果在同一个 *fp* 上，试图通过重复调用 `dump()` 来序列化多个对象，将会获得一个无效的 JSON 文件。

⚠JSON 中的 key/value 的 key 始终是 `str` 类型。当 `dict` 对象被序列化为 JSON 格式后，`dict` 中的所有 key 都会被强制转换为字符串。因此，如果将 `dict` 序列化为 JSON，然后又再次逆序列化为 `dict`，那么新 `dict` 对象可能与原 `dict` 对象并不相等。也就是说，如果字典 x 包含非字符串 key，则 `loads(dumps(x)) != x`。

```python
import json

original_dict = [1, {'2': 2, 1: 1}]
print(json.dumps(original_dict))
new_dict = json.loads(json.dumps(original_dict))
print(new_dict)
print(original_dict == new_dict)
```

输出:

```
[1, {"2": 2, "1": 1}]
[1, {'2': 2, '1': 1}]
False
```

下面的子章节是对各个参数的说明。

#### fp📌

*fp* - 支持 `.write()` 方法的 file-like 对象，`json` 模块只会生成 `str` 对象，不会生成 `bytes` 对象，因此 `fp.write()` 必须支持 `str` 输入。

在使用 `open()` 函数打开文件时，只能使用 RFC 规定的编码格式: UTF-8、UTF-16、UTF-32，UTF-8 是最大互操作性的推荐默认值

#### skipkeys📌

*skipkeys* - 假如 *obj* 内含 `dict` 对象，并且 `dict` 中的某些键属于非基本类型(keys must be `str`, `int`, `float`, `bool` or `None`, not `tuple`)，可使用 *skipkeys* 表明是否跳过这些非基本类型的键。

> If *skipkeys* is true (default: `False`), then dict keys that are not of a basic type ([`str`](https://docs.python.org/3/library/stdtypes.html#str), [`int`](https://docs.python.org/3/library/functions.html#int), [`float`](https://docs.python.org/3/library/functions.html#float), [`bool`](https://docs.python.org/3/library/functions.html#bool), `None`) will be skipped instead of raising a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError).

#### ensure_ascii📌

*ensure_ascii* - 是否转义输出中非 ASCII 字符，默认转义

> If *ensure_ascii* is true (the default), the output is guaranteed to have all incoming non-ASCII characters escaped. If *ensure_ascii* is false, these characters will be output as-is.

```python
>>> import json
>>> json.dumps('鲸鱼')
'"\\u9cb8\\u9c7c"'
>>> json.dumps('鲸鱼',ensure_ascii=False)
'"鲸鱼"'
```

#### check_circular📌

*check_circular* - 是否检测循环引用

> If *check_circular* is false (default: `True`), then the circular reference check for container types will be skipped and a circular reference will result in an [`OverflowError`](https://docs.python.org/3/library/exceptions.html#OverflowError) (or worse).

```python
import json
a = [1, 2]
a.append(a)
print(json.dumps(a)) # 默认进行循环引用
#> ValueError: Circular reference detected
print(json.dumps(a, check_circular=False))
#> RecursionError: maximum recursion depth exceeded while encoding a JSON object
```

#### allow_nan📌

*allow_nan* - 是否将超范围的 `float` 值 (`nan`, `inf`, `-inf`) 显式为 JavaScript 中的等效属性 (`NaN`, `Infinity`, `-Infinity`)。注意，JSON 规范并不支持超范围的 `float` 值

> If *allow_nan* is false (default: `True`), then it will be a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) to serialize out of range [`float`](https://docs.python.org/3/library/functions.html#float) values (`nan`, `inf`, `-inf`) in strict compliance of the JSON specification. If *allow_nan*is true, their JavaScript equivalents (`NaN`, `Infinity`, `-Infinity`) will be used.

```python
import json
a = [float('nan'), float('inf'), float('-inf')]
print(json.dumps(a))
#> [NaN, Infinity, -Infinity]
print(json.dumps(a, allow_nan=False))
#> ValueError: Out of range float values are not JSON compliant
```

#### cls📌

如果要使用自定义的 [`JSONEncoder`](https://docs.python.org/3/library/json.html#json.JSONEncoder) 子类，可通过 *cls* 进行设置

> To use a custom [`JSONEncoder`](https://docs.python.org/3/library/json.html#json.JSONEncoder) subclass (e.g. one that overrides the `default()` method to serialize additional types), specify it with the *cls* kwarg; otherwise [`JSONEncoder`](https://docs.python.org/3/library/json.html#json.JSONEncoder) is used.
>
> *Changed in version 3.6:* All optional parameters are now [keyword-only](https://docs.python.org/3/glossary.html#keyword-only-parameter).



#### indent📌

*indent* - 设置 JSON 的缩进方式

> If *indent* is a non-negative integer or string, then JSON array elements and object members will be pretty-printed with that indent level. An indent level of 0, negative, or `""`will only insert newlines. 
>
> `None` (the default) selects the most compact representation. 
>
> Using a positive integer indent indents that many spaces per level. 
>
> If *indent* is a string (such as `"\t"`), that string is used to indent each level.
>
> *Changed in version 3.2:* Allow strings for *indent* in addition to integers.

```python
import json

a = [1, {'a': 1, 'b': 2}]
print(json.dumps(a))
print(json.dumps(a, indent='--'))
```

输出:

```
[1, {"a": 1, "b": 2}]
[
--1,
--{
----"a": 1,
----"b": 2
--}
]
```

#### separators📌

*separators* - 设置分隔 item 和 key 的方式

> If specified, *separators* should be an `(item_separator, key_separator)` tuple. The default is `(', ', ': ')` if *indent* is `None` and `(',', ': ')` otherwise. To get the most compact JSON representation, you should specify `(',', ':')` to eliminate whitespace.
>
> *Changed in version 3.4:* Use `(',', ': ')` as default if *indent* is not `None`.

```python
import json

a = [1, {'a': 1, 'b': 2}]
print(json.dumps(a))
#> [1, {"a": 1, "b": 2}]
print(json.dumps(a, separators=('>', '^')))
#> [1>{"a"^1>"b"^2}]
```

#### default📌

*default* - 当遇到无法序列化的对象时，便会调用 *default* 函数

> If specified, *default* should be a function that gets called for objects that can’t otherwise be serialized. It should return a JSON encodable version of the object or raise a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError). If not specified, [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError) is raised.

```python
import json
def func(arg):
    return str(arg)

a = [1, {'a': 1, 'b': 2}, lambda: 2]
# lambda对象无法序列化为JSON
print(json.dumps(a, default=func))
#> [1, {"a": 1, "b": 2}, "<function <lambda> at 0x000002002257D9D8>"]
```

#### sort_keys📌

*sort_keys* - 是否对输出结果中的字典进行排序，按照 key 的升序排列

> If *sort_keys* is true (default: `False`), then the output of dictionaries will be sorted by key.

```python
import json

a = [1, {'b': 2, 'a': 1}]
print(json.dumps(a, sort_keys=True))
#> [1, {"a": 1, "b": 2}]
```



### json.dumps()🔨

🔨json.dumps(*obj*, *\**, *skipkeys=False*, *ensure_ascii=True*, *check_circular=True*, *allow_nan=True*, *cls=None*, *indent=None*, *separators=None*, *default=None*, *sort_keys=False*, ***kw*)

`dumps()` 会将 *obj* 对象序列化为 JSON 格式的 `str` 序列，序列化过程遵守如下[转换表](https://docs.python.org/3/library/json.html#py-to-json-table):

| Python                                 | JSON   |
| :------------------------------------- | :----- |
| dict                                   | object |
| list, tuple                            | array  |
| str                                    | string |
| int, float, int- & float-derived Enums | number |
| True                                   | true   |
| False                                  | false  |
| None                                   | null   |

各个参数的含义与前面的 `dump()` 相同。

⚠JSON 中的 key/value 的 key 始终是 `str` 类型。当 `dict` 对象被序列化为 JSON 格式后，`dict` 中的所有 key 都会被强制转换为字符串。因此，如果将 `dict` 序列化为 JSON，然后又再次逆序列化为 `dict`，那么新 `dict` 对象可能与原 `dict` 对象并不相等。也就是说，如果字典 x 包含非字符串 key，则 `loads(dumps(x)) != x`。

```python
import json

original_dict = [1, {'2': 2, 1: 1}]
print(json.dumps(original_dict))
new_dict = json.loads(json.dumps(original_dict))
print(new_dict)
print(original_dict == new_dict)
```

输出:

```
[1, {"2": 2, "1": 1}]
[1, {'2': 2, '1': 1}]
False
```



### json.load()🔨

🔨json.load(*fp*, *\**, *cls=None*, *object_hook=None*, *parse_float=None*, *parse_int=None*, *parse_constant=None*, *object_pairs_hook=None*, ***kw*)

读取 *fp* 中 JSON 格式的序列化字符串，并将其逆序列化为 Python 对象，逆序列化过程遵守如下[转换表](https://docs.python.org/3/library/json.html#json-to-py-table):

| JSON          | Python |
| :------------ | :----- |
| object        | dict   |
| array         | list   |
| string        | str    |
| number (int)  | int    |
| number (real) | float  |
| true          | True   |
| false         | False  |
| null          | None   |

如果参与逆序列化的数据不是有效的 JSON 文档，则会抛出 [`JSONDecodeError`](https://docs.python.org/3/library/json.html#json.JSONDecodeError)。

> *Changed in version 3.6:* All optional parameters are now [keyword-only](https://docs.python.org/3/glossary.html#keyword-only-parameter)

下面的子章节是对各个参数的说明。

#### fp📌

*fp* - a `.read()`-supporting [text file](https://docs.python.org/3/glossary.html#term-text-file) or [binary file](https://docs.python.org/3/glossary.html#term-binary-file) containing a JSON document

在使用 `open()` 函数打开文件时，只能使用 RFC 规定的编码格式: UTF-8、UTF-16、UTF-32，UTF-8 是最大互操作性的推荐默认值

> *Changed in version 3.6:* *fp* can now be a [binary file](https://docs.python.org/3/glossary.html#term-binary-file). The input encoding should be UTF-8, UTF-16 or UTF-32.

#### cls📌

如果要使用自定义的 [`JSONDecoder`](https://docs.python.org/3/library/json.html#json.JSONDecoder) 子类，可通过 *cls* 进行设置

> To use a custom [`JSONDecoder`](https://docs.python.org/3/library/json.html#json.JSONDecoder) subclass, specify it with the `cls` kwarg; otherwise [`JSONDecoder`](https://docs.python.org/3/library/json.html#json.JSONDecoder) is used. Additional keyword arguments will be passed to the constructor of the class.

#### object_hook📌

*object_hook* - 在逆序列化过程中，如果遇到 `dict` 对象，就会调用 *object_hook* 函数(以 `dict` 对象做实参)，并将 *object_hook* 的返回值用作逆序列化的结果，并且结果中不会包含 `dict` 对象。该功能可用于实现自定义解码器(e.g. [JSON-RPC](http://www.jsonrpc.org/) class hinting)。

默认值 `None` 表示不适用 *object_hook* 函数，将遇到的 `dict` 对象直接用作逆序列化的结果。

> *object_hook* is an optional function that will be called with the result of any object literal decoded (a [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)).「这里的 object 是指 JSON 对象」The return value of *object_hook* will be used instead of the [`dict`](https://docs.python.org/3/library/stdtypes.html#dict). This feature can be used to implement custom decoders (e.g. [JSON-RPC](http://www.jsonrpc.org/) class hinting).

```python
import json
def as_complex(dct):
    print('in')
    if '__complex__' in dct:
        return complex(dct['real'], dct['imag'])
    return dct

obj = json.loads(
    '[{"__complex__": true, "real": 1, "imag": 2},["1","2"]]',
    object_hook=as_complex)

print(obj)
#> [(1+2j), ['1', '2']]
```



#### parse_float📌

*parse_float* - 在逆序列化过程中，如果遇到 JSON float，便会调用 *parse_float* (以 JSON float 为实参)。默认 `parse_float=None`，此时会调用内置函数 `float()`。

> *parse_float*, if specified, will be called with the string of every JSON float to be decoded. By default, this is equivalent to `float(num_str)`. This can be used to use another datatype or parser for JSON floats (e.g. [`decimal.Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal)).

```python
import json
import decimal
obj = json.loads('1.1', parse_float=decimal.Decimal)
print(repr(obj))
#> Decimal('1.1')
```



#### parse_int📌

*parse_int* - 在逆序列化过程中，如果遇到 JSON int，便会调用 *parse_int* (以 JSON int为实参)。默认 `parse_float=None`，此时会调用内置函数 `int()`。

> *parse_int*, if specified, will be called with the string of every JSON int to be decoded. By default, this is equivalent to `int(num_str)`. This can be used to use another datatype or parser for JSON integers (e.g. [`float`](https://docs.python.org/3/library/functions.html#float)).

```python
import json
import decimal
obj = json.loads('1', parse_int=float)
print(obj)
#> 1.0
```



#### parse_constant📌

*parse_constant* - 当在字符串序列中遇到以下 JSON 内容时，将会调用 *parse_constant* 函数。

- `-Infinity`
- `Infinity`
- `NaN`

⚠超范围的 `float` 值 (`nan`, `inf`, `-inf`) 在 JavaScript 中的等效属性 (`NaN`, `Infinity`, `-Infinity`)是没有被 `""` 包围的。

> *parse_constant*, if specified, will be called with one of the following strings: `'-Infinity'`, `'Infinity'`, `'NaN'`. This can be used to raise an exception if invalid JSON numbers are encountered.
>
> *Changed in version 3.1:* *parse_constant* doesn’t get called on ‘null’, ‘true’, ‘false’ anymore.

```python
import json
import decimal


def func(obj):
    return obj[0]


obj = json.loads("[NaN, Infinity, -Infinity]", parse_constant=func)
print(obj)
#> ['N', 'I', '-']
obj = json.loads("[NaN, Infinity, -Infinity]")
print(obj)
#> [nan, inf, -inf]
```

#### object_pairs_hook📌

*object_pairs_hook* - 在逆序列化过程中，如果遇到 `dict` 对象，会先将 `dict` 转换成由 `(key, value)` 组成的 `list`，然后以 `list` 为实参调用 *object_pairs_hook* 函数，并将函数的返回值用作逆序列化逆序列化的结果，并且结果中不会包含 `dict` 对象。该功能可用于实现自定义解码器。

如果同时实现了 *object_hook* 和 *object_pairs_hook*，会优先使用后者。

> *object_pairs_hook* is an optional function that will be called with the result of any object literal decoded with an ordered list of pairs. The return value of *object_pairs_hook* will be used instead of the [`dict`](https://docs.python.org/3/library/stdtypes.html#dict). This feature can be used to implement custom decoders. If *object_hook* is also defined, the *object_pairs_hook* takes priority.
>
> *Changed in version 3.1:* Added support for *object_pairs_hook*.

```python
import json


def as_complex(container):
    print(container)
    if isinstance(container, dict) and '__complex__' in container:
        return complex(container['real'], container['imag'])
    elif isinstance(container,
                    list) and '__complex__' in [i[0] for i in container]:
        r, i = (0, 0)
        for k, v in container:
            if k == 'real':
                r = v
            elif k == 'imag':
                i = v
        return complex(r, i)


obj = json.loads(
    '[{"__complex__": true, "real": 1, "imag": 2},["1","2"]]',
    object_pairs_hook=as_complex)

print(obj)

obj = json.loads(
    '[{"__complex__": true, "real": 1, "imag": 2},["1","2"]]',
    object_hook=as_complex)

print(obj)
```

输出:

```
[('__complex__', True), ('real', 1), ('imag', 2)]
[(1+2j), ['1', '2']]
{'__complex__': True, 'real': 1, 'imag': 2}
[(1+2j), ['1', '2']]
```



### json.loads()🔨

🔨json.loads(*s*, *\**, *encoding=None*, *cls=None*, *object_hook=None*, *parse_float=None*, *parse_int=None*, *parse_constant=None*, *object_pairs_hook=None*, ***kw*)

> Deserialize *s* (a [`str`](https://docs.python.org/3/library/stdtypes.html#str), [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) or [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray) instance containing a JSON document) to a Python object using this [conversion table](https://docs.python.org/3/library/json.html#json-to-py-table).
>
> | JSON          | Python |
> | :------------ | :----- |
> | object        | dict   |
> | array         | list   |
> | string        | str    |
> | number (int)  | int    |
> | number (real) | float  |
> | true          | True   |
> | false         | False  |
> | null          | None   |
>
> The other arguments have the same meaning as in [`load()`](https://docs.python.org/3/library/json.html#json.load), except *encoding* which is ignored and deprecated.
>
> If the data being deserialized is not a valid JSON document, a [`JSONDecodeError`](https://docs.python.org/3/library/json.html#json.JSONDecodeError) will be raised.
>
> *Changed in version 3.6:* *s* can now be of type [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) or [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray). The input encoding should be UTF-8, UTF-16 or UTF-32.
>
> 

## 编码器和解码器

> 使用示例，详见﹝0x04 json - PyMOTW-3﹞

### json.JSONDecoder()🛠

*class* json.JSONDecoder(*\**, *object_hook=None*, *parse_float=None*, *parse_int=None*, *parse_constant=None*, *strict=True*, *object_pairs_hook=None*)

该类是一个简单的 JSON 解码器，默认情况下在解码时遵循以下转换规则:

| JSON          | Python |
| :------------ | :----- |
| object        | dict   |
| array         | list   |
| string        | str    |
| number (int)  | int    |
| number (real) | float  |
| true          | True   |
| false         | False  |
| null          | None   |

该 JSON 解码还会将 `NaN`, `Infinity`, `-Infinity` 理解为相应的浮点值，但这超出了 JSON 规范。

如果参与逆序列化的数据不是有效的 JSON 文档，则会抛出 [`JSONDecodeError`](https://docs.python.org/3/library/json.html#json.JSONDecodeError)。

> *Changed in version 3.6:* All parameters are now [keyword-only](https://docs.python.org/3/glossary.html#keyword-only-parameter).

#### 参数说明

请先参考 `json.load()` 的参数说明，这两部分内容及其相识，这里就不再翻译了

- *object_hook*

  > if specified, will be called with the result of every JSON object decoded and its return value will be used in place of the given [`dict`](https://docs.python.org/3/library/stdtypes.html#dict). This can be used to provide custom deserializations (e.g. to support JSON-RPC class hinting).

- *object_pairs_hook*

  > if specified will be called with the result of every JSON object decoded with an ordered list of pairs. The return value of *object_pairs_hook* will be used instead of the [`dict`](https://docs.python.org/3/library/stdtypes.html#dict). This feature can be used to implement custom decoders. If *object_hook* is also defined, the *object_pairs_hook* takes priority.
  >
  > *Changed in version 3.1:* Added support for *object_pairs_hook*.

- *parse_float*

  > if specified, will be called with the string of every JSON float to be decoded. By default, this is equivalent to `float(num_str)`. This can be used to use another datatype or parser for JSON floats (e.g. [`decimal.Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal)).

- *parse_int*

  > if specified, will be called with the string of every JSON int to be decoded. By default, this is equivalent to `int(num_str)`. This can be used to use another datatype or parser for JSON integers (e.g. [`float`](https://docs.python.org/3/library/functions.html#float)).

- *parse_constant*

  > if specified, will be called with one of the following strings: `'-Infinity'`, `'Infinity'`, `'NaN'`. This can be used to raise an exception if invalid JSON numbers are encountered.

- *strict* - 是否允许在字符串包含控制字符。这里说的控制字符是指字符编码在 0-31 范围内的字符，例如 `'\t'` (tab), `'\n'`, `'\r'`, `'\0'`.

  > If *strict* is false (`True` is the default), then control characters will be allowed inside strings. Control characters in this context are those with character codes in the 0–31 range, including `'\t'` (tab), `'\n'`, `'\r'` and `'\0'`.

#### 方法

- decode(*s*)

  > Return the Python representation of *s* (a [`str`](https://docs.python.org/3/library/stdtypes.html#str) instance containing a JSON document).[`JSONDecodeError`](https://docs.python.org/3/library/json.html#json.JSONDecodeError) will be raised if the given JSON document is not valid.

- raw_decode(*s*) - 当 JSON 数据后面跟有额外数据时，可用此方法解码。返回值是一个元组，其中包含解码 JSON 序列得到的 Python 对象和解码结束的位置的索引值。JSON 数据只能位于字符串的最前端。

  > Decode a JSON document from *s* (a [`str`](https://docs.python.org/3/library/stdtypes.html#str) beginning with a JSON document) and return a 2-tuple of the Python representation and the index in *s* where the document ended.This can be used to decode a JSON document from a string that may have extraneous data at the end.



### json.JSONEncoder()🛠

🛠*class* json.JSONEncoder(*\**, *skipkeys=False*, *ensure_ascii=True*, *check_circular=True*, *allow_nan=True*, *sort_keys=False*, *indent=None*, *separators=None*, *default=None*)

适用 Python 数据结构的可扩展 JSON 编码器，默认支持以下对象和类型:

| Python                                 | JSON   |
| :------------------------------------- | :----- |
| dict                                   | object |
| list, tuple                            | array  |
| str                                    | string |
| int, float, int- & float-derived Enums | number |
| True                                   | true   |
| False                                  | false  |
| None                                   | null   |

> *Changed in version 3.4:* Added support for int- and float-derived Enum classes.

如果想要识别上表中未包含的对象，则需要对 `JSONEncode` 进行扩展。在进行扩展时，你需要子类化 `JSONEncode`，并重新实现 `default()` 方法，如果可能话，`default()` 应返回 `o` 的可序列化对象，否则应该调用超类中的实现(抛出 [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError))。

#### 参数说明

请先参考 `json.load()` 的参数说明，这两部分内容极其相识，这里就不再翻译了

- *skipkeys*

  > If *skipkeys* is false (the default), then it is a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError) to attempt encoding of keys that are not [`str`](https://docs.python.org/3/library/stdtypes.html#str), [`int`](https://docs.python.org/3/library/functions.html#int), [`float`](https://docs.python.org/3/library/functions.html#float) or `None`. If *skipkeys* is true, such items are simply skipped.

- *ensure_ascii*

  > If *ensure_ascii* is true (the default), the output is guaranteed to have all incoming non-ASCII characters escaped. If *ensure_ascii* is false, these characters will be output as-is.

- *check_circular*

  > If *check_circular* is true (the default), then lists, dicts, and custom encoded objects will be checked for circular references during encoding to prevent an infinite recursion (which would cause an [`OverflowError`](https://docs.python.org/3/library/exceptions.html#OverflowError)). Otherwise, no such check takes place.

- *allow_nan*

  > If *allow_nan* is true (the default), then `NaN`, `Infinity`, and `-Infinity` will be encoded as such. This behavior is not JSON specification compliant, but is consistent with most JavaScript based encoders and decoders. Otherwise, it will be a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) to encode such floats.

- *sort_keys*

  > If *sort_keys* is true (default: `False`), then the output of dictionaries will be sorted by key; this is useful for regression tests to ensure that JSON serializations can be compared on a day-to-day basis.

- *indent*

  > If *indent* is a non-negative integer or string, then JSON array elements and object members will be pretty-printed with that indent level. An indent level of 0, negative, or `""`will only insert newlines. `None` (the default) selects the most compact representation. Using a positive integer indent indents that many spaces per level. If *indent* is a string (such as `"\t"`), that string is used to indent each level.
  >
  > *Changed in version 3.2:* Allow strings for *indent* in addition to integers.

- *separators*

  > If specified, *separators* should be an `(item_separator, key_separator)` tuple. The default is `(', ', ': ')` if *indent* is `None` and `(',', ': ')` otherwise. To get the most compact JSON representation, you should specify `(',', ':')` to eliminate whitespace.
  >
  > *Changed in version 3.4:* Use `(',', ': ')` as default if *indent* is not `None`.

- *default*

  > If specified, *default* should be a function that gets called for objects that can’t otherwise be serialized. It should return a JSON encodable version of the object or raise a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError). If not specified, [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError) is raised.
  >
  > *Changed in version 3.6:* All parameters are now [keyword-only](https://docs.python.org/3/glossary.html#keyword-only-parameter).

#### 方法

- default(*o*)

  Implement this method in a subclass such that it returns a serializable object for *o*, or calls the base implementation (to raise a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError)).For example, to support arbitrary iterators, you could implement default like this:

  ```python
  def default(self, o):
     try:
         iterable = iter(o)
     except TypeError:
         pass
     else:
         return list(iterable)
     # Let the base class default method raise the TypeError
     return json.JSONEncoder.default(self, o)
  ```

- encode(*o*)

  Return a JSON string representation of a Python data structure, *o*. For example:

  ```python
  >>> json.JSONEncoder().encode({"foo": ["bar", "baz"]})
  '{"foo": ["bar", "baz"]}'
  ```

- iterencode(*o*)

  Encode the given object, *o*, and yield each string representation as available. For example:

  ```python
  for chunk in json.JSONEncoder().iterencode(bigobject):
      mysocket.write(chunk)
  ```



## 异常

### json.JSONDecodeError☣

☣*exception* json.JSONDecodeError(*msg*, *doc*, *pos*)

Subclass of [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) with the following additional attributes:

- `msg`

  The unformatted error message.

- `doc`

  The JSON document being parsed.

- `pos`

  The start index of *doc* where parsing failed.

- `lineno`

  The line corresponding to *pos*.

- `colno`

  The column corresponding to *pos*.

*New in version 3.5.*

## 命令行接口

[`json.tool`](https://docs.python.org/3/library/json.html#module-json.tool) 模块提供了一个简单的命令行接口来验证和 pretty-print JSON 对象。

```shell
(spider) C:\Users\iwhal\Desktop\PyTest>python -m json.tool -h
usage: python -m json.tool [-h] [--sort-keys] [infile] [outfile]

A simple command line interface for json module to validate and pretty-print
JSON objects.

positional arguments:
  infile       a JSON file to be validated or pretty-printed
  outfile      write the output of infile to outfile

optional arguments:
  -h, --help   show this help message and exit
  --sort-keys  sort the output of dictionaries alphabetically by key
```

如果未指定可选参数 `infile` 和 `outfile`，则会分别使用 [`sys.stdin`](https://docs.python.org/3/library/sys.html#sys.stdin) 和 [`sys.stdout`](https://docs.python.org/3/library/sys.html#sys.stdout):

```shell
$ echo '{"json": "obj"}' | python -m json.tool
{
    "json": "obj"
}
$ echo '{1.2:3.4}' | python -m json.tool
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

> *Changed in version 3.5:* The output is now in the same order as the input. Use the [`--sort-keys`](https://docs.python.org/3/library/json.html#cmdoption-json-tool-sort-keys) option to sort the output of dictionaries alphabetically by key.

### 命令行选项

- `infile`

  The JSON file to be validated or pretty-printed:

  ```shell
  $ python -m json.tool mp_films.json
  [
      {
          "title": "And Now for Something Completely Different",
          "year": 1971
      },
      {
          "title": "Monty Python and the Holy Grail",
          "year": 1975
      }
  ]
  ```

  If *infile* is not specified, read from [`sys.stdin`](https://docs.python.org/3/library/sys.html#sys.stdin).

- `outfile`

  Write the output of the *infile* to the given *outfile*. Otherwise, write it to [`sys.stdout`](https://docs.python.org/3/library/sys.html#sys.stdout).

- `--sort-keys`

  Sort the output of dictionaries alphabetically by key.*New in version 3.5.*

- `-h` 和 `--help`

  Show the help message.

## 遵守的标准和互操作性

> 参考: https://docs.python.org/3/library/json.html#standard-compliance-and-interoperability
>
> 本节内容机翻占多数，我调整了格式和语序，并进行了少量修改

JSON 格式由 [**RFC 7159**](https://tools.ietf.org/html/rfc7159.html) 和 [ECMA-404](http://www.ecma-international.org/publications/standards/Ecma-404.htm) 指定。本节会详细介绍 `json` 模块遵守 RFC 的层度。为了简单起见，不考虑 `JSONEncode` 和 `JSONDecode` 的子类，也不考虑没有明确提及的参数。

`json` 模块并没有严格遵守 RFC，并实现了一些对 JavaScript 有效，但不属于 JSON 的扩展功能，特别是:

- 接受并输出 `Infinite` 和 `NaN` 数值
- 接受对象中的重复名称，并且仅使用最后一个 name-value 对

由于 RFC 允许符合 RFC 的解析器接受不符合 RFC 的输入文本，因此再默认设置下 `json` 模块的 deserializer 在技术上符合 RFC。

因此该模块的 deserializer 在默认设置下在技术上符合 RFC。

### 字符编码

RFC 要求使用 UTF-8、UTF-16、UTF-32 表示 JSON，UTF-8 是最大互操作性的推荐默认值。

在 RFC 允许的情况下，尽管不是必需的，但该模块的序列化器默认设置 `ensure_ascii = True`，因此转义输出以使得结果字符串仅包含 ASCII 字符。

除了 `ensure_ascii` 参数之外，`json` 模块严格按照 Python 对象和 [Unicode字符串](https://docs.python.org/3/library/stdtypes.html#str) 之间的转换进行定义，因此不会直接涉及字符编码的问题。我们只需要在 `open()` 函数中设置编码方案即可。

RFC 禁止在 JSON 文本的开头添加字节顺序标记(BOM)，并且 `json` 模块的 serializer 不会向其输出添加 BOM。RFC 允许但不要求 JSON 反序列化器忽略其输入中的初始 BOM。当存在初始 BOM 时，`json` 模块的反序列化器会引发 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)。

RFC 没有在 JSON 字符串中，明确禁止包含与有效 Unicode 字符不对应的字节序列(例如，未配对的 UTF-16 代理)，但 RFC 确实注意到这样做可能会导致互操作性问题。默认情况下，`json` 模块接受并输出(当存在于原始 `str` 中时)此类序列的代码点。

### Infinite 和 NaN 数字值

RFC 不允许表示 Infinite 或 NaN 数值。尽管如此，在默认情况下，此模块接受并输出 `Infinity`, `-Infinity`, `NaN`，就像它们是有效的 JSON 数字字面值一样：

```python
>>> # Neither of these calls raises an exception, but the results are not valid JSON
>>> json.dumps(float('-inf'))
'-Infinity'
>>> json.dumps(float('nan'))
'NaN'
>>> # Same when deserializing
>>> json.loads('-Infinity')
-inf
>>> json.loads('NaN')
nan
```

在 serializer 中，`allow_nan` 参数可用于更改此行为。在 deserializer 中，`parse_constant` 参数可用于更改此行为。

### JSON 对象中的重复名称

RFC 指定 JSON 对象中的名称应该是唯一的，但不强制要求如何处理 JSON 对象中的重复名称。默认情况下，此模块不会引发异常;相反，它会忽略除给定名称的最后一个名称 - 值对之外的所有内容:

```
>>> weird_json = '{"x": 1, "x": 2, "x": 3}'
>>> json.loads(weird_json)
{'x': 3}
```

`object_pairs_hook` 参数可用于更改此行为。

### Top-level Non-Object, Non-Array Values

在老版本 JSON (由废弃 [**RFC 4627**](https://tools.ietf.org/html/rfc4627.html) 定义)中要求 JSON 文本的顶层值(*top-level*)必须时 JSON 对象或数组(对应 Python `dict` 和 `list`)，不能时 JSON null、boolean、number、string。在 [**RFC 7159**](https://tools.ietf.org/html/rfc7159.html) 中移除了该限制，`json` 模块在其 serializer 和 deserializer 中从未实现过前面的限制条件。

无论如何，为了实现最大的互操作性，您可能希望自己坚持自己的限制。



### 实现中存在的限制

部分 JSON deserializer 的实现可能会对下述内容做出限制:

- 可接受的 JSON 文本的大小
- JSON 对象和数组的最大嵌套级别
- JSON 数字的范围和精度
- JSON 字符串的内容和最大长度

除了相关的 Python 数据类型本身或 Python 解释器本身之外，该模块不会施加任何此类限制。

序列化为 JSON 时，请注意那些可能会使用该 JSON 文本的应用是否存在上述限制。特别是，JSON number 通常会被反序列化为 IEEE 754 双精度数，因此会受到该表示的范围和精度限制。在序列化非常大的 Python int 值时，或者在序列化"独特的"数值类型的实例(如[`decimal.Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal))时，这尤其重要。



## 术语

### serializer

用于完成"序列化"的工具，比如 `json.dump` 和 `json.dumps`

### deserializer

用于完成"逆序列化"的程序，比如 `json.load` 和 `json.loads`

### JSON object

在 JavaScript 中由 `{}` 包围的内容被称为对象，数据结构为键值对结构 `{key1：value1, key2：value2, ...} `，key 是对象的属性，value 是属性的值。key 可以是整数或字符串，value 可以是任何类型。

注意区别 Python 对象和 JSON 对象的含义





