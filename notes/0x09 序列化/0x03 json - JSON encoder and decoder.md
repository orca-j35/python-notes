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

将 *obj* 对象序列化为 JSON 格式的数据流，并写入到 *fp* 中，序列化过程遵守如下[转换表](https://docs.python.org/3/library/json.html#py-to-json-table):

| Python                                 | JSON   |
| :------------------------------------- | :----- |
| dict                                   | object |
| list, tuple                            | array  |
| str                                    | string |
| int, float, int- & float-derived Enums | number |
| True                                   | true   |
| False                                  | false  |
| None                                   | null   |

**参数说明**:

- *fp* - 支持 `.write()` 方法的 file-like 对象，`json` 模块只会生成 `str` 对象，不会生成 `bytes` 对象。因此 `fp.write()` 必须支持 `str` 输入。

- *skipkeys* - 是否跳过由 dict 中由使用非基本类型的键

  > If *skipkeys* is true (default: `False`), then dict keys that are not of a basic type ([`str`](https://docs.python.org/3/library/stdtypes.html#str), [`int`](https://docs.python.org/3/library/functions.html#int), [`float`](https://docs.python.org/3/library/functions.html#float), [`bool`](https://docs.python.org/3/library/functions.html#bool), `None`) will be skipped instead of raising a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError).

- *ensure_ascii* - 是否在输出中转义非 ASCII 字符

  > If *ensure_ascii* is true (the default), the output is guaranteed to have all incoming non-ASCII characters escaped. If *ensure_ascii* is false, these characters will be output as-is.

  ```python
  >>> import json
  >>> json.dumps('鲸鱼')
  '"\\u9cb8\\u9c7c"'
  >>> json.dumps('鲸鱼',ensure_ascii=False)
  '"鲸鱼"'
  ```

- If *check_circular* is false (default: `True`), then the circular reference check for container types will be skipped and a circular reference will result in an [`OverflowError`](https://docs.python.org/3/library/exceptions.html#OverflowError) (or worse).

- If *allow_nan* is false (default: `True`), then it will be a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) to serialize out of range [`float`](https://docs.python.org/3/library/functions.html#float) values (`nan`, `inf`, `-inf`) in strict compliance of the JSON specification. If *allow_nan*is true, their JavaScript equivalents (`NaN`, `Infinity`, `-Infinity`) will be used.

- If *indent* is a non-negative integer or string, then JSON array elements and object members will be pretty-printed with that indent level. An indent level of 0, negative, or `""`will only insert newlines. `None` (the default) selects the most compact representation. Using a positive integer indent indents that many spaces per level. If *indent* is a string (such as `"\t"`), that string is used to indent each level.

### json.dumps()🔨



### json.load()🔨



### json.loads()🔨



## 编码器和解码器

### json.JSONDecoder()🛠



### json.JSONEncoder()🛠



## 异常

### json.JSONDecodeError☣

















