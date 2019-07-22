# json - JSON encoder and decoder
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`json` — JSON encoder and decoder](https://docs.python.org/3/library/json.html)
> - https://pymotw.com/3/json/index.html
> - https://codingpy.com/books/thinkpython2/14-files.html
> - https://codingpy.com/books/thinkpython2/14-files.html

## 概述

[`json`](https://docs.python.org/3/library/json.html#module-json) 模块采用了与 [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal) 和 [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) 的相似的 API，用于将内存中的 Python 对象转换为 JSON 对象。与 pickle 不同，JSON 具有以多种语言（尤其是 JavaScript）实现的优点。在使用 REST API 的 Web 服务端和客户端之间通常会使用 JSON 进行通信，同时对于应用程序间的通信需求也非常有用。

`json` 和 `pickle` 模块虽然都可以对 Python 对象进行序列化，但是存在如下差异:

- 







不同之处在于 JSON 基于文本，而 pickle 基于二进制模式。

### JavaScript 与 JSON

> [JSON (JavaScript Object Notation - JavaScript 对象标记)](http://json.org/), specified by [**RFC 7159**](https://tools.ietf.org/html/rfc7159.html) (which obsoletes [**RFC 4627**](https://tools.ietf.org/html/rfc4627.html)) and by [ECMA-404](http://www.ecma-international.org/publications/standards/Ecma-404.htm), is a lightweight data interchange format inspired by [JavaScript](https://en.wikipedia.org/wiki/JavaScript) object literal syntax (although it is not a strict subset of JavaScript [1](https://docs.python.org/3/library/json.html#rfc-errata) ).

在 JavaScript 中，一切皆是对象，任何 JavaScript 支持的类型都可通过 JSON 来表示，如字符串、数字、对象、数组等等，其中对象和数组是比较特殊的两种类型:

- 对象(object) - 在 JavaScript 中由 `{}` 包围的内容被称为对象，数据结构为键值对结构 `{key1：value1, key2：value2, ...} `，key 是对象的属性，value 是属性的值。key 可以是整数或字符串，value 可以是任何类型。
- 数组(array) - 在 JavaScript 中由 `[]` 包围的内容被称为数组，数据结构为索引结构 ` ["java", "javascript", "vb", ...] `。在 JavaScript 中，数组是一种比较特殊的数据类型，既可以采用索引结构也可以采用键值对结构。

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





