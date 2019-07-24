# json - JSON encoder and decoder
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`json` — JSON encoder and decoder](https://docs.python.org/3/library/json.html)
> - https://pymotw.com/3/json/index.html
> - https://codingpy.com/books/thinkpython2/14-files.html

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

| Python                                 | JSON   |
| :------------------------------------- | :----- |
| dict                                   | object |
| list, tuple                            | array  |
| str                                    | string |
| int, float, int- & float-derived Enums | number |
| True                                   | true   |
| False                                  | false  |
| None                                   | null   |

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



#### skipkeys📌

*skipkeys* - 假如 *obj* 内含 `dict` 对象，并且 `dict` 中的某些键属于非基本类型，可使用 *skipkeys* 表明是否跳过这些非基本类型的键

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

*cls* 用于设置要使用的自定义 [`JSONEncoder`](https://docs.python.org/3/library/json.html#json.JSONEncoder) 子类

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

下面的子章节是对各个参数的说明。

#### fp📌

*fp* - a `.read()`-supporting [text file](https://docs.python.org/3/glossary.html#term-text-file) or [binary file](https://docs.python.org/3/glossary.html#term-binary-file) containing a JSON document

#### cls📌



> To use a custom [`JSONDecoder`](https://docs.python.org/3/library/json.html#json.JSONDecoder) subclass, specify it with the `cls` kwarg; otherwise [`JSONDecoder`](https://docs.python.org/3/library/json.html#json.JSONDecoder) is used. Additional keyword arguments will be passed to the constructor of the class.

#### object_hook📌

*object_hook* - 在逆序列化过程中获得 `dict` 对象时，就会调用 *object_hook* 函数(`dict` 对象做实参)，并将 *object_hook* 的返回值(而非 `dict` 对象)用作逆序列化的结果。该功能可用于实现自定义解码器(e.g. [JSON-RPC](http://www.jsonrpc.org/) class hinting).。

默认值 `None` 表示缺少 *object_hook* 函数，将 `dict` 对象用作逆序列化的结果。

> *object_hook* is an optional function that will be called with the result of any object literal decoded (a [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)). The return value of *object_hook* will be used instead of the [`dict`](https://docs.python.org/3/library/stdtypes.html#dict). This feature can be used to implement custom decoders (e.g. [JSON-RPC](http://www.jsonrpc.org/) class hinting).

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



> *parse_float*, if specified, will be called with the string of every JSON float to be decoded. By default, this is equivalent to `float(num_str)`. This can be used to use another datatype or parser for JSON floats (e.g. [`decimal.Decimal`](https://docs.python.org/3/library/decimal.html#decimal.Decimal)).

#### parse_int📌



> *parse_int*, if specified, will be called with the string of every JSON int to be decoded. By default, this is equivalent to `int(num_str)`. This can be used to use another datatype or parser for JSON integers (e.g. [`float`](https://docs.python.org/3/library/functions.html#float)).

#### parse_constant📌



> *parse_constant*, if specified, will be called with one of the following strings: `'-Infinity'`, `'Infinity'`, `'NaN'`. This can be used to raise an exception if invalid JSON numbers are encountered.
>
> *Changed in version 3.1:* *parse_constant* doesn’t get called on ‘null’, ‘true’, ‘false’ anymore.

#### object_pairs_hook📌



> *object_pairs_hook* is an optional function that will be called with the result of any object literal decoded with an ordered list of pairs. The return value of *object_pairs_hook* will be used instead of the [`dict`](https://docs.python.org/3/library/stdtypes.html#dict). This feature can be used to implement custom decoders. If *object_hook* is also defined, the *object_pairs_hook* takes priority.
>
> *Changed in version 3.1:* Added support for *object_pairs_hook*.



### json.loads()🔨



## 编码器和解码器

### json.JSONDecoder()🛠



### json.JSONEncoder()🛠



## 异常

### json.JSONDecodeError☣

















