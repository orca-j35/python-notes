# urllib.parse - Parse URLs into components

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`urllib.parse`](https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse) — Parse URLs into components
> - [urllib.parse — Split URLs into Components](https://pymotw.com/3/urllib.parse/index.html)
> - [13.2. urllib.parse — 将 URL 拆分为各组成部分](https://learnku.com/docs/pymotw/urllibparse-split-urls-into-components)
>
> 扩展阅读:
>
> - [**RFC 3986**](https://tools.ietf.org/html/rfc3986.html) - Uniform Resource Identifiers
>
> This is the current standard (STD66). Any changes to urllib.parse module should conform to this. Certain deviations could be observed, which are mostly for backward compatibility purposes and for certain de-facto parsing requirements as commonly observed in major browsers.
>
> - [**RFC 2732**](https://tools.ietf.org/html/rfc2732.html) - Format for Literal IPv6 Addresses in URL’s.
>
> This specifies the parsing requirements of IPv6 URLs.
>
> - [**RFC 2396**](https://tools.ietf.org/html/rfc2396.html) - Uniform Resource Identifiers (URI): Generic Syntax
>
> Document describing the generic syntactic requirements for both Uniform Resource Names (URNs) and Uniform Resource Locators (URLs).
>
> - [**RFC 2368**](https://tools.ietf.org/html/rfc2368.html) - The mailto URL scheme.
>
> Parsing requirements for mailto URL schemes.
>
> - [**RFC 1808**](https://tools.ietf.org/html/rfc1808.html) - Relative Uniform Resource Locators
>
> This Request For Comments includes the rules for joining an absolute and a relative URL, including a fair number of “Abnormal Examples” which govern the treatment of border cases.
>
> - [**RFC 1738**](https://tools.ietf.org/html/rfc1738.html) - Uniform Resource Locators (URL)
>
> This specifies the formal syntax and semantics of absolute URLs.

`urllib.parse` 模块提供了以下三种功能:

- break Uniform Resource Locator (URL) strings up in components (addressing scheme, network location, path etc.)
- combine the components back into a URL string
- convert a “relative URL” to an absolute URL given a “base URL.”

`urllib.parse` 模块支持以下 URL schemes: `file`, `ftp`, `gopher`, `hdl`, `http`, `https`, `imap`, `mailto`, `mms`, `news`, `nntp`, `prospero`, `rsync`, `rtsp`, `rtspu`, `sftp`, `shttp`, `sip`, `sips`, `snews`, `svn`, `svn+ssh`, `telnet`, `wais`, `ws`, `wss`.

`urllib.parse` 模块的功能可分为两大类: URL parsing 和 URL quoting. 

## URL 解析函数

### 概述

URL 解析函数可分为以下几类:

- 解析函数:
  - [urlparse()](#urlparse())
  - [urlsplit()](#urlsplit())
  - [urldefrag()](#urldefrag())
  - [parse_qs()](#parse_qs())
  - [parse_qsl()](#parse_qsl())
- 逆解析函数:(把分解后的 URL 重新组合为一个完整的 URL 的过程被成为逆解析(*unparsing*))
  - [.geturl()](#.geturl())
  - [urlunparse()](#urlunparse())
  - [urlunsplit()](#urlunsplit())
- 拼接函数:
  - [urljoin()](#urljoin())

### urlparse()

🔨 urllib.parse.urlparse(*urlstring*, *scheme=*'', *allow_fragments=True*)

该函数会按照如下格式将 URL 解析为 6 个部分，其返回值是 ParseResult 对象。

```
scheme://netloc/path;parameters?query#fragment
   1        2     3     4         5      6
```

#### 参数说明

- *urlstring* - 用于设置待解析的 URL。

  ```python
  from urllib.parse import urlparse
  url = 'http://netloc:80/path;param?query=arg#frag'
  print(urlparse(url))
  '''Out:
  ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='frag')
  '''
  ```

- *scheme* - 用于设置 `scheme` 的默认值，当且仅当 *urlstring* 中缺少 `scheme` 时会使用该值，*scheme* 应与 *urlstring* 保持相同的类型(text 或 bytes)。虽然 *scheme* 的默认值是 `''`，但如果 *urlstring* 的值是 bytes，则会自动将 *scheme* 的默认值转换为 `b''`，不过并不会自动转换自定义的 *scheme* 值。

  ```python
  from urllib.parse import urlparse
  url = 'http://netloc:80/path;param?query=arg#frag'
  print(urlparse(url, scheme='https'))
  #> ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='frag')
  url = '//netloc:80/path;param?query=arg#frag'
  print(urlparse(url, scheme='https'))
  #> ParseResult(scheme='https', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='frag')
  ```

- *allow_fragments* - 若 `allow_fragments=False` 则无法识别 `fragment`，并且会将 `fragment` 解析为 `path`, `parameters` 或 `query` 中的一部分。

  ```python
  from urllib.parse import urlparse
  url = 'http://netloc:80/path;param?query=arg#frag'
  print(urlparse(url, allow_fragments=False))
  #> ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg#frag', fragment='')
  ```

#### 返回值

`urlparse` 的返回值是基于 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) 的 ParseResult 对象，所含属性如下:

| Attribute  | Index | Value                                    | Value if not present                                         |
| :--------- | :---- | :--------------------------------------- | :----------------------------------------------------------- |
| `scheme`   | 0     | URL scheme specifier                     | *scheme* parameter                                           |
| `netloc`   | 1     | Network location part                    | empty string                                                 |
| `path`     | 2     | Hierarchical path                        | empty string                                                 |
| `params`   | 3     | Parameters for last path element         | empty string                                                 |
| `query`    | 4     | Query component, 一般用于 GET 类型的 URL | empty string                                                 |
| `fragment` | 5     | Fragment identifier                      | empty string                                                 |
| `username` |       | User name                                | [`None`](https://docs.python.org/3/library/constants.html#None) |
| `password` |       | Password                                 | [`None`](https://docs.python.org/3/library/constants.html#None) |
| `hostname` |       | Host name (lower case)                   | [`None`](https://docs.python.org/3/library/constants.html#None) |
| `port`     |       | Port number as integer, if present       | [`None`](https://docs.python.org/3/library/constants.html#None) |

如果 URL 中的端口是无效端口，则会在读取 `port` 属性时抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)，参考 [Structured Parse Results](https://docs.python.org/3/library/urllib.parse.html#urlparse-result-object) 可了解更多信息。

如果在 `netloc` 属性中包含未闭合的方括号，则会抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)。

Characters in the `netloc` attribute that decompose under NFKC normalization (as used by the IDNA encoding) into any of `/`, `?`, `#`, `@`, or `:` will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError). If the URL is decomposed before parsing, no error will be raised.

示例代码:

```python
from urllib.parse import urlparse

url = 'http://user:pwd@NetLoc:80/path;param?query=arg#frag'
parsed = urlparse(url)
print(parsed.scheme) #> http
print( parsed.netloc) #> user:pwd@NetLoc:80
print( parsed.path) #> /path
print(parsed.params) #> param
print(parsed.query) #>  query=arg
print(parsed.fragment) #> frag
print(parsed.username) #> user
print(parsed.password) #> pwd
print(parsed.hostname) #> netloc
print(parsed.port) #> 80
print(parsed.geturl()) #> http://user:pwd@NetLoc:80/path;param?query=arg#frag
```

ParseResult 对象属于 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple)，因此该对象还拥有一些特殊方法，比如  `_replace()`:

```python
>>> from urllib.parse import urlparse
>>> u = urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
>>> u
ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            params='', query='', fragment='')
>>> u._replace(scheme='http')
ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
            params='', query='', fragment='')
```

#### Notes

`urlparse()` 遵循 [RFC 1808](https://tools.ietf.org/html/rfc1808.html) 的语法规范，只有在使用 `//` 引入 `netloc` 时，`urlparse()` 才会识别 `netloc`；否则 `urlparse()` 会假定正在使用相对 URL:

```python
from urllib.parse import urlparse
urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
#> ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
urlparse('www.cwi.nl/%7Eguido/Python.html')
#> ParseResult(scheme='', netloc='', path='www.cwi.nl/%7Eguido/Python.html', params='', query='', fragment='')
urlparse('help/Python.html')
#> ParseResult(scheme='', netloc='', path='help/Python.html', params='', query='', fragment='')
```

*Changed in version 3.2:* Added IPv6 URL parsing capabilities.

*Changed in version 3.3:* The fragment is now parsed for all URL schemes (unless *allow_fragment* is false), in accordance with [**RFC 3986**](https://tools.ietf.org/html/rfc3986.html). Previously, a whitelist of schemes that support fragments existed.

*Changed in version 3.6:* Out-of-range port numbers now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError), instead of returning [`None`](https://docs.python.org/3/library/constants.html#None).

*Changed in version 3.7.3:* Characters that affect netloc parsing under NFKC normalization will now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError).

### urlsplit()

🔨 urllib.parse.urlsplit(*urlstring*, *scheme*='', *allow_fragments*=True)

`urlsplit()` 和 `urlparse()` 的区别在于前者会将 `path` 和 `parameters` 视为一个整体。

```
scheme://netloc/path;parameters?query#fragment
   1       2         3            4      5
```

`urlsplite()` 对于遵循 [**RFC 2396**](https://tools.ietf.org/html/rfc2396.html) 的 URL 非常有用，因为这些 URL 支持为每段路径配置参数。

```python
from urllib.parse import urlsplit
url = 'http://user:pwd@NetLoc:80/p1;para/p2;para?query=arg#frag'
print(urlsplit(url))
#> SplitResult(scheme='http', netloc='user:pwd@NetLoc:80', path='/p1;para/p2;para', query='query=arg', fragment='frag')
```

`urlsplit()` 各参数的用法与 `urlparse()` 相同

`urlparse()` 的返回值是基于 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) 的 SplitResult 对象，所含属性如下:

| Attribute  | Index | Value                              | Value if not present                                         |
| :--------- | :---- | :--------------------------------- | :----------------------------------------------------------- |
| `scheme`   | 0     | URL scheme specifier               | *scheme* parameter                                           |
| `netloc`   | 1     | Network location part              | empty string                                                 |
| `path`     | 2     | Hierarchical path                  | empty string                                                 |
| `query`    | 3     | Query component                    | empty string                                                 |
| `fragment` | 4     | Fragment identifier                | empty string                                                 |
| `username` |       | User name                          | [`None`](https://docs.python.org/3/library/constants.html#None) |
| `password` |       | Password                           | [`None`](https://docs.python.org/3/library/constants.html#None) |
| `hostname` |       | Host name (lower case)             | [`None`](https://docs.python.org/3/library/constants.html#None) |
| `port`     |       | Port number as integer, if present | [`None`](https://docs.python.org/3/library/constants.html#None) |

如果 URL 中的端口是无效端口，则会在读取 `port` 属性时抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)，参考 [Structured Parse Results](https://docs.python.org/3/library/urllib.parse.html#urlparse-result-object) 可了解更多信息。

如果在 `netloc` 属性中包含未闭合的方括号，则会抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)。

Characters in the `netloc` attribute that decompose under NFKC normalization (as used by the IDNA encoding) into any of `/`, `?`, `#`, `@`, or `:` will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError). If the URL is decomposed before parsing, no error will be raised.

#### Notes

*Changed in version 3.6:* Out-of-range port numbers now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError), instead of returning [`None`](https://docs.python.org/3/library/constants.html#None).

*Changed in version 3.7.3:* Characters that affect netloc parsing under NFKC normalization will now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError).

### urldefrag()

🔨 urllib.parse.urldefrag(*url*)

该函数会将 *url* 解析为 2 个部分:

- 第一部分 - `scheme://netloc/path;parameters?query` 
- 第二部分 - `fragment`

```python
from urllib.parse import urldefrag

original = 'http://netloc/path;param?query=arg#frag'
d = urldefrag(original)
print(d.url) #> http://netloc/path;param?query=arg
print(d.fragment) #> frag
print(d.geturl()) #> http://netloc/path;param?query=arg#frag
```

`urldefrag()` 的返回值是基于 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) 的 DefragResult 对象，所含属性如下:

| Attribute  | Index | Value                | Value if not present |
| :--------- | :---- | :------------------- | :------------------- |
| `url`      | 0     | URL with no fragment | empty string         |
| `fragment` | 1     | Fragment identifier  | empty string         |

有关 DefragResult 的更多信息，详见 [Structured Parse Results](https://docs.python.org/3/library/urllib.parse.html#urlparse-result-object) 

*Changed in version 3.2:* Result is a structured object rather than a simple 2-tuple.

### parse_qs()

🔨 urllib.parse.parse_qs(*qs*, *keep_blank_values*=False, *strict_parsing*=False, *encoding*='utf-8', *errors*='replace', *max_num_fields*=None)

该函数用于解析 URL 中的 `query` 字符串[(data of type *application/x-www-form-urlencoded*)](https://imququ.com/post/four-ways-to-post-data-in-http.html)，其返回值是一个字典:

```python
from urllib.parse import parse_qs, parse_qsl

encoded = 'foo=foo1&foo=foo2&wd=hello'
print(parse_qs(encoded))
#> {'foo': ['foo1', 'foo2'], 'wd': ['hello']}
```

使用 [`urllib.parse.urlencode()`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode) 函数(需 `doseq=True`)可将 `parse_qs()` 返回的字典再次转换为 `query` 字符串

*Changed in version 3.2:* Add *encoding* and *errors* parameters.

*Changed in version 3.7.2:* Added *max_num_fields* parameter.

#### 参数说明

- *keep_blank_values* - 是否将百分比编码(*percent*-*encoded*)查询中的空值视为空字符串。`True` 表示将空值保留为空字符串；`False`(默认值)表示忽略空值。

  ```python
  encoded = 'foo=foo1&wd'
  print(parse_qs(encoded))
  #> {'foo': ['foo1']}
  print(parse_qs(encoded, keep_blank_values=True))
  #> {'foo': ['foo1'], 'wd': ['']}
  ```

- *strict_parsing* - 用于指示如何处理解析错误，`False` (默认值)表示忽略错误；`True` 表示在出现错误时会抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) 异常。

- *encoding* 和 *errors* - 用于设置如何将百分比编码(*percent*-*encoded*)序列解码为 Unicode 字符，这两个参数的用法与 [`bytes.decode()`](https://docs.python.org/3/library/stdtypes.html#bytes.decode) 相同。

  ```python
  from urllib.parse import parse_qs, parse_qsl
  
  print(parse_qs('foo=foo1&wd=%e9%b2%b8', encoding='utf8'))
  #> {'foo': ['foo1'], 'wd': ['鲸']}
  ```

- *max_num_fields* - 用于设置可被读取的最大字段数，如果设置了 *max_num_fields* 的值，那么当 `query` 字符串中的字段数大于该设定值时，便会抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) 

  ```python
  from urllib.parse import parse_qs, parse_qsl
  parse_qs('foo=foo1&wd=%e9%b2%b8', max_num_fields=1)
  #> ValueError: Max number of fields exceeded
  ```

### parse_qsl()

🔨 urllib.parse.parse_qsl(*qs*, *keep_blank_values*=False, *strict_parsing*=False, *encoding*='utf-8', *errors*='replace', *max_num_fields*=None)

该函数用于解析 URL 中的 `query` 字符串[(data of type *application/x-www-form-urlencoded*)](https://imququ.com/post/four-ways-to-post-data-in-http.html)，其返回值是一个列表:

```python
from urllib.parse import parse_qs, parse_qsl

encoded = 'foo=foo1&foo=foo2&wd=hello'
print(parse_qsl(encoded))
#> [('foo', 'foo1'), ('foo', 'foo2'), ('wd', 'hello')]
```

使用 [`urllib.parse.urlencode()`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode) 函数可将 `parse_qsl()` 返回的列表再次转换为 `query` 字符串

各参数的含义与 `parse_qs()` 相同。

*Changed in version 3.2:* Add *encoding* and *errors* parameters.

*Changed in version 3.7.2:* Added *max_num_fields* parameter.

### .geturl()

`geturl()` 方法用于逆解析 URL，以下对象均具备该方法:

- ParseResult 对象(由 `urlparse()` 产生)
- SplitResult 对象(由 `urlsplite()` 产生)
- DefragResult 对象(由 `urldefrag` 产生)

```python
from urllib.parse import urlparse

original = 'http://netloc/path;param?query=arg#frag'
print('ORIG  :', original)
parsed = urlparse(original)
print('PARSED:', parsed.geturl())
'''Out:
ORIG  : http://netloc/path;param?query=arg#frag
PARSED: http://netloc/path;param?query=arg#frag
'''
```

### urlunparse()

🔨 urllib.parse.urlunparse(*parts*)

该函数用于从可迭代对象 *parts* 逆解析 URL

```python
from urllib.parse import urlunparse
data = ['http', 'netloc', '/path', 'parameters', 'query', 'fragment']
print(urlunparse(data))
#> http://netloc/path;parameters?query#fragment
```

注: *parts* 的长度必须等于 6，否则会抛出异常。

如果原始 URL 中包含不必要的分隔符(比如，虽然有 `?` 分隔符，但是 `query` 内容为空)，当此 URL 经过解析和逆解析后，可能会丢失这些不必要的分隔符:

```python
from urllib.parse import urlunparse, urlparse
original = 'http://netloc/path;?#'
# 原始URL中;?#的内容均为空
# 经逆解析获得URL会丢失这些不必要的分隔符
# 不过按照RFC标准来说，这两个URL是等价的
parsed = urlparse(original)
print(urlunparse(parsed))
#> http://netloc/path
```

### urlunsplit()

🔨 urllib.parse.urlunsplit(*parts*)

该函数用于从可迭代对象 *parts* 逆解析 URL

```python
from urllib.parse import urlunsplit
data = ['http', 'netloc', '/path;parameters', 'query', 'fragment']
print(urlunsplit(data))
#> http://netloc/path;parameters?query#fragment
```

注: *parts* 的长度必须等于 5，否则会抛出异常。

如果原始 URL 中包含不必要的分隔符(比如，虽然有 `?` 分隔符，但是 `query` 内容为空)，当此 URL 经过解析和逆解析后，可能会丢失这些不必要的分隔符:

```python
from urllib.parse import urlunsplit, urlsplit
original = 'http://netloc/path;?#'
# 原始URL中?#的内容均为空
# 经逆解析获得URL会丢失这些不必要的分隔符
# 不过按照RFC标准来说，这两个URL是等价的
parsed = urlsplit(original)
print(urlunsplit(parsed))
#> http://netloc/path;
```



### urljoin()

🔨 urllib.parse.urljoin(*base*, *url*, *allow_fragments*=True)

`urljoin()` 用于将 *base* (base URL) 和 *url* 拼接为一个完整的 URL，该函数会分析 *base* 的 `scheme`, `netloc` 和 `path` 

```
scheme://netloc/path;parameters?query#fragment
```

若 `allow_fragments=False` 则无法识别 `fragment`，并且会将 `fragment` 解析为 `path`, `parameters` 或 `query` 中的一部分，这与 `urlparse()` 相同。

如果 *url* 是相对路径，效果如下:

```python
from urllib.parse import urljoin

print(urljoin('http://www.example.com/path/file.html',
              'anotherfile.html'))
print(urljoin('http://www.example.com/path/file.html',
              './anotherfile.html'))
print(urljoin('http://www.example.com/path/file.html',
              '../anotherfile.html'))
'''Out:
http://www.example.com/path/anotherfile.html
http://www.example.com/path/anotherfile.html
http://www.example.com/anotherfile.html
'''
```

如果 *url* 是非相对路径，处理方式与 `os.path.join()` 相同:

- 如果 *url* 以 `/` 开头，则会重设 *base* 的 `path` 部分
- 如果 *url* 不以 `/` 开头，则会将 *url* 拼接到 *base* 的尾部

```python
from urllib.parse import urljoin

print(urljoin('http://www.example.com/path/',
              '/subpath/file.html'))
print(urljoin('http://www.example.com/path/',
              'subpath/file.html'))
'''Out:
http://www.example.com/subpath/file.html
http://www.example.com/path/subpath/file.html
'''
```

如果 *url* 是绝对 URL (以 `//` 或  `scheme://` 开头的 URL)，那么 *url* 的 `netloc` 和 `scheme` 将出现在结果中:

```python
print(
    urljoin(
        'http://www.cwi.nl/%7Eguido/Python.html',
        '//www.python.org/%7Eguido',
    ))
#> http://www.python.org/%7Eguido
print(
    urljoin(
        'http://www.cwi.nl/%7Eguido/Python.html',
        'https://www.python.org/%7Eguido',
    ))
#> https://www.python.org/%7Eguido
```

如果 *url* 是 `;parameters`, `?query` 或 `#fragment`，效果如下:

```python
print(urljoin(
    'http://netloc/path;parameters?query#fragment',
    ';p#f',
))
```

*Changed in version 3.5:* Behaviour updated to match the semantics defined in [**RFC 3986**](https://tools.ietf.org/html/rfc3986.html).

## Parsing ASCII Encoded Bytes

本节中描述的行为仅适用于 URL 解析函数，不适用于 URL 引用函数。

本模块中的 URL 解析函数不仅可处理 [`str`](https://docs.python.org/3/library/stdtypes.html#str) 对象，还可处理 [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) (或 [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray))对象：

- 如果向解析函数传递 `str` 类型的数据，那么其返回值中将包含 `str` 类型的数据
- 如果向解析函数传递 `byte` (或 `byteattay`)类型的数据，那么其返回值中将包含 `byte` (或 `byteattay`)类型的数据

如果在调用解析函数时混用 `str` 和 `byte` (或 `byteattay`)，则会抛出 [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError)；如果尝试传入非 ASCII 字节值，则会抛出 [`UnicodeDecodeError`](https://docs.python.org/3/library/exceptions.html#UnicodeDecodeError)。

```python
from urllib.parse import urlparse
url = 'http://netloc:80/path;param?query=arg#鲸'
p = urlparse(url)
print(p) #> ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='鲸')
print(p.encode()) #> UnicodeEncodeError: 'ascii' codec can't encode character '\u9cb8' in position 0: ordinal not in range(128)
```

为了便于将解析结果在 `str` 和 `bytes` 间进行转换，URL 解析函数返回的对象会提供以下两种方法:

- 如果返回对象中所含数据是 `str` 类型，则会为其提供 `encode()` 方法，该方法用于将数据类型转换为 `bytes`，`encode()` 方法的签名与内置函数 `byte()` 一致，唯一的区别是 `encode()` 会使用 `ascii` 编码，而不是 `utf-8`。
- 如果返回对象中所含数据是 `bytes` 类型，则会为其提供 `decode()` 方法，该方法用于将数据类型转换为 `str`，`decode()` 方法的签名与内置函数 `str()` 一致，唯一的区别是 `decode()` 会使用 `ascii` 编码，而不是 `utf-8`。

```python
from urllib.parse import urlparse
url = b'http://netloc:80/path;param?query=arg#frag'
p = urlparse(url)
print(p) #> ParseResultBytes(scheme=b'http', netloc=b'netloc:80', path=b'/path', params=b'param', query=b'query=arg', fragment=b'frag')
print(p.decode()) #> ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='frag')
```

如果 bytes 类型的 URL 本身包含非 ASCII 字符，则需要在解析该 URL 之前先对其手动节码，否则会抛出异常:

```python
urlb = bytes('http://netloc:80/path;param?query=arg#鲸', encoding='utf8')
print(urlb) # urlb包含非ASCII字符
#> b'http://netloc:80/path;param?query=arg#\xe9\xb2\xb8'
print(urlparse(urlb.decode('utf-8'))) # 解析前需先解码
#> ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='鲸')
print(urlparse(urlb))
#> UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 38: ordinal not in range(128)
```

*Changed in version 3.2:* URL parsing functions now accept ASCII encoded byte sequences

## Structured Parse Results

`urlparse()`, `urlsplit()` 和 `urldefrag()` 返回的对象均是 [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple) 类型的子类。这些子类拥有之前提及的附加属性，并且支持 `encode()` (或 `decode`)方法，还包含 `geturl()` 方法:

🔨 urllib.parse.SplitResult.geturl()

利用 `SplitResult` 中的内容逆解析出原 URL。由逆解析获得的 URL 可能会与原 URL 存在如下差别:

- 将 `scheme` 规范为小写
- 会丢弃原 URL 中的空组件(*component*)，如下:
  - ParseResult 对象(由 `urlparse()` 产生)和 SplitResult 对象(由 `urlsplite()` 产生)将会丢弃空属性(*parameters*)、空查询(*queries*)和空片段标识符(*fragment* identifiers)
  - DefragResult 对象(由 `urldefrag` 产生)，仅会丢弃空片段标识符

```python
>>> from urllib.parse import urlsplit
>>> url = 'HTTP://www.Python.org/doc/#'
>>> r1 = urlsplit(url)
>>> r1.geturl()
'http://www.Python.org/doc/'
>>> r2 = urlsplit(r1.geturl())
>>> r2.geturl()
'http://www.Python.org/doc/'
```

以下类提供了在 `str` 对象上操作结构化解析结果(*structured* *parse* *results*)的实现:

- class urllib.parse.DefragResult(url, fragment)

  Concrete class for urldefrag() results containing str data. The encode() method returns a DefragResultBytes instance.

  *New in version 3.2.*

- class urllib.parse.ParseResult(scheme, netloc, path, params, query, fragment)

  Concrete class for [`urlparse()`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse) results containing [`str`](https://docs.python.org/3/library/stdtypes.html#str) data. The `encode()` method returns a [`ParseResultBytes`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.ParseResultBytes) instance.

- class urllib.parse.SplitResult(scheme, netloc, path, query, fragment)

  Concrete class for [`urlsplit()`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit) results containing [`str`](https://docs.python.org/3/library/stdtypes.html#str) data. The `encode()` method returns a [`SplitResultBytes`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.SplitResultBytes) instance.

以下类提供了在 `bytes` (或 `bytearray`)对象上操作结构化解析结的实现:

- class urllib.parse.DefragResultBytes(url, fragment)

  Concrete class for [`urldefrag()`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urldefrag) results containing [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) data. The `decode()` method returns a [`DefragResult`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.DefragResult) instance.

  *New in version 3.2.*

- class urllib.parse.ParseResultBytes(scheme, netloc, path, params, query, fragment)

  Concrete class for [`urlparse()`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse) results containing [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) data. The `decode()` method returns a [`ParseResult`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.ParseResult) instance.

  *New in version 3.2.*

- class urllib.parse.SplitResultBytes(scheme, netloc, path, query, fragment)

  Concrete class for [`urlsplit()`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit) results containing [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) data. The `decode()` method returns a [`SplitResult`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.SplitResult) instance.

  *New in version 3.2.*

## URL Quoting

首先来思考两个场景:

- 我们在 `query` 中使用 `&` 来分割 `key=value` 对，但是如果 `value` 中包含 `=` 或 `&`，势必会造成 URL 解析错误
- URL 使用 `ascii` 编码方案进行编码，如在 URL 中包含非 ASCII 字符，同样会造成 URL 解析错误

为了解决上述问题，我们需要使用安全字符(没有特殊用途或特殊意义的可打印字符)去表示那些会造成解析错误的不安全字符，这个便是 URL Quote。

Note: 浏览器地址栏中的 URL 已经过 qoute，但浏览器为了便于人们理解 URL 的含义，它会在地址栏中显示未经 qoute 的 URL。如果我们将浏览器中的 URL 复制到任意文本编辑器中，便会得到 qoute 后的 URL。

```
# 在浏览器中看到的URL
https://cn.bing.com/search?q=鲸+鱼
# 从浏览器中复制的URL
https://cn.bing.com/search?q=%E9%B2%B8+%E9%B1%BC
```

### quote()

🔨 urllib.parse.quote(*string*, *safe*='/', *encoding*=None, *errors*=None)

该函数会使用 `%xx` 转义(*escape*)序列替换 *string* 中的特殊字符，并且总会原样保留字母(*letter*)、数字(*digit*)以及 `'_.-~'`:

```python
from urllib.parse import quote

url = 'http://localhost:8080/_.-~/鲸'
print(quote(url))
#> http%3A//localhost%3A8080/_.-~/%E9%B2%B8
```

通常情况下，`quote()` 函数被用来 quote URL 中的 `path` 部分。

```
scheme://netloc/path;parameters?query#fragment
```

以下两段代码等效

```python
quote(string, safe, encoding, errors)
quote_from_bytes(string.encode(encoding, errors), safe)
```

*Changed in version 3.7:* Moved from [**RFC 2396**](https://tools.ietf.org/html/rfc2396.html) to [**RFC 3986**](https://tools.ietf.org/html/rfc3986.html) for quoting URL strings. “~” is now included in the set of reserved characters.

#### 参数说明

- *string* - 可以是  [`str`](https://docs.python.org/3/library/stdtypes.html#str) 或 [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes)，但 `quote()` 的返回值始终是 `str`

- *safe* - 用于设置不应被 quote 的其它 ASCII 字符，默认值是 `'/'`

  ```python
  from urllib.parse import quote
  
  url = 'http://localhost:8080/_.-~/鲸'
  print(quote(url))
  print(quote(url, safe=':/'))
  '''Out:
  http%3A//localhost%3A8080/_.-~/%E9%B2%B8
  http://localhost:8080/_.-~/%E9%B2%B8
  '''
  ```

- *encoding* 和 *errors* - 用于设置如何处理 non-ASCII 字符，使用方法和 [`str.encode()`](https://docs.python.org/3/library/stdtypes.html#str.encode) 类似。*encoding* 的默认值是 `'utf-8'`；*eorrs* 的默认值是 `'strict'`(在遇到不支持的字符时，会抛出 [`UnicodeEncodeError`](https://docs.python.org/3/library/exceptions.html#UnicodeEncodeError))。当 *string* 的实参属于 `bytes` 类型时，不支持 *encoding* 和 *errors* 参数，强行使用这两个参数的话，会抛出 [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError)。

### quote_plus

🔨 urllib.parse.quote_plus(*string*, *safe*='', *encoding*=None, *errors*=None)

类似于 `quote()`，但是会利用加号 `'+'` 来替换空格，并且会对原始字符串中的加号进行转义。

```python
from urllib.parse import quote, quote_plus

url = 'http://localhost:8080/_.-~/鲸'
print(quote('/El +Niño/'))
print(quote_plus('/El +Niño/'))
'''Out:
/El%20%2BNi%C3%B1o/
%2FEl+%2BNi%C3%B1o%2F
'''
```

在 URL 中构建 `query` 字符串时，需使用 `quote_plus()` 来 quote HTML 表单(*form*)的值。例如，将搜索框中的空格转换为加号:

```
# bing搜索框中的内容是
鲸 鱼
# 经quote后，得到的URL是
https://cn.bing.com/search?q=%E9%B2%B8+%E9%B1%BC
```

Note: *safe* 的默认值是 `''`

### quote_from_bytes

🔨 urllib.parse.quote_from_bytes(*bytes*, *safe*='/')

类似于 `quote()`，但只能接收 `bytes` 对象。

以下两段代码等效

```python
quote(string, safe, encoding, errors)
quote_from_bytes(string.encode(encoding, errors), safe)
```

### unquote

🔨 urllib.parse.unquote(*string*, *encoding*='utf-8', *errors*='replace')

`unquote()` 是 `quote()` 的逆操作，用于还原 *string* 中的转义序列(`%xx`)

```python
from urllib.parse import unquote
print(unquote('/El%20Ni%C3%B1o/'))
#> '/El Niño/'
print(unquote('http%3A//localhost%3A8080/%7Ehellmann/'))
#> http://localhost:8080/~hellmann/
```

#### 参数说明

- *string* - 必须是 `str`
- *encoding* 和 *errors* - 用于设置将百分比编码(*percent*-*encoded*)序列的解码方案，使用方法和 [`bytes.decode()`](https://docs.python.org/3/library/stdtypes.html#bytes.decode) 类似。依照给定的解码方案，可以将百分比编码序列解码为 Unicode 字符。由于 *error* 的默认值是 `replace`，因此会将无效序列替换为占位符(*placeholder*)。

### unquote_plus

🔨 urllib.parse.unquote_plus(*string*, *encoding*='utf-8', *errors*='replace')

`unquote_plus()` 是 `quote_plus()` 的逆操作，使用方法类似于 `unquote()`，但会将加号 `+` 替换为空格。

```python
from urllib.parse import unquote_plus
print(unquote_plus('/El+Ni%C3%B1o/'))
#> /El Niño/
print(unquote_plus('http%3A%2F%2Flocalhost%3A8080%2F%7Ehellmann%2F'))
#> http://localhost:8080/~hellmann/
```

需使用该方法来 unquote 已引用的 HTML 表单值。

### unquote_to_bytes

🔨 urllib.parse.unquote_to_bytes(*string*)

该方法会将 *string* 中的百分比转义序列 `%xx` 逐一替换为等效的八位字节，其返回值是 `bytes` 对象。

```python
from urllib.parse import unquote_to_bytes
print(unquote_to_bytes('a%26%EF'))
#> b'a&\xef'
```

*string* 可以是 `str` 或 `bytes`。如果 *string* 是 `str` 类型，则会将 *string* 中的未转义的 non-ASCII 字符编码为 UTF-8 字节。

### urlencode

🔨 urllib.parse.urlencode(*query*, *doseq*=False, *safe*='', *encoding*=None, *errors*=None, *quote_via*=quote_plus)

该函数是 `parse_qs()` 和 `parse_qsl()` 的逆操作，用于将映射对象或序列对象(必须是由双元素元组组成的序列)转换为百分比编码(*percent*-*encoded*)的 ASCII 文本字符串。`query` 必须在编码后才能被加入到 URL 中。

```python
from urllib.parse import urlencode
query_args = {
    'q': 'query string',
    'foo': 'bar',
    'foo': ['foo1', 'foo2'],
}
print(urlencode(query_args, doseq=True))
#> q=query+string&foo=foo1&foo=foo2
```

映射对象中的键值可以是 `str` 或 `bytes`，序列对象中的元素也可以是 `str` 或 `bytes`，`urlencode()` 的返回值总是 `str`

```python
from urllib.parse import urlencode
query_args = [
    (b'a', b'1'),
    (b'b', '2'),
    ('c', b'3'),
    ('d', '4'),
]
print(urlencode(query_args))
#> a=1&b=2&c=3&d=4
```

`urlencode()` 的返回值是由 `&` 分割的 `key=value` 对组成的字符串，*query* 中提供的数据需经 *quote_via* 函数 quote 后，才能用于 `key=value` 对。

如果需要将 `urlencode()` 返回值用作 [`urlopen()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) 函数的 *data* 参数，那么应先将 `urlencode()` 的返回值编码为 `bytes`，否则会抛出 [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError)。

在 [urllib examples](https://docs.python.org/3/library/urllib.request.html#urllib-examples) 中展示了如何使用 `urlencode()` 方法生成 URL  query 字符串和 POST 数据。

*Changed in version 3.2:* Query parameter supports bytes and string objects.

*New in version 3.5:* *quote_via* parameter.

#### 参数说明

- *doseq* - 用于控制输出结果中 `key=value` 对的形式:

  ```python
  from urllib.parse import urlencode
  query_args = {
      # 当映射中的值是序列时,
      # 若doseq=True,则会为每个值生成一个key=value对
      'foo': ['foo1', 'foo2'],
  }
  print(urlencode(query_args))
  #> foo=%5B%27foo1%27%2C+%27foo2%27%5D
  print(urlencode(query_args, doseq=True))
  #> foo=foo1&foo=foo2
  
  query_args = (
      # 序列对象也有类似效果
      ('foo', ['foo1', 'foo2']), )
  print(urlencode(query_args))
  #> foo=%5B%27foo1%27%2C+%27foo2%27%5D
  print(urlencode(query_args, doseq=True))
  #> foo=foo1&foo=foo2
  ```

- *safe*, *encoding*, *errors* - 这三个参数将被传递给 *quote_via*。当且仅当 *query* 是 `str` 时，才会向 *quote_via* 传递 *encoding* 和 *errors*  参数。

- *quote_via* 的默认值是 `quote_plus()`，这意味着空格将被替换为 `'+'`，并且 `'/'` 将被编码为 `%2F` —— 符合 GET 请求的标准 [(*application/x-www-form-urlencoded*)](https://imququ.com/post/four-ways-to-post-data-in-http.html)。还可以将 *quote_via* 设为 `quote()`，此时空格会被编码为 `%20`，但不会对 `'/'` 进行编码。为了最大限度的控制 quote 的内容，可使用 `quote()` 方法并指定 *safe* 参数。













