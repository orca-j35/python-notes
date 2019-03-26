# urllib.parse - Parse URLs into components
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - https://docs.python.org/3/library/urllib.parse.html#url-quoting
> - https://pymotw.com/3/urllib.parse/index.html
> - https://learnku.com/docs/pymotw/urllibparse-split-urls-into-components/3432#6fb0b9

`urllib.parse` 模块提供了以下三种功能:

- break Uniform Resource Locator (URL) strings up in components (addressing scheme, network location, path etc.)
- combine the components back into a URL string
- convert a “relative URL” to an absolute URL given a “base URL.”

`urllib.parse` 模块支持以下 URL schemes: `file`, `ftp`, `gopher`, `hdl`, `http`, `https`, `imap`, `mailto`, `mms`, `news`, `nntp`, `prospero`, `rsync`, `rtsp`, `rtspu`, `sftp`, `shttp`, `sip`, `sips`, `snews`, `svn`, `svn+ssh`, `telnet`, `wais`, `ws`, `wss`.

`urllib.parse` 模块的功能可分为两大类: URL parsing 和 URL quoting. 

## Parsing

### urlparse()

🔨 urllib.parse.urlparse(*urlstring*, *scheme=*'', *allow_fragments=True*)

该函数会按照如下格式将 URL 解析为 6 个部分，其返回值是 ParseResult 对象。

```
scheme://netloc/path;parameters?query#fragment
```

#### Parameters

- *urlstring* - 用于设置待解析的 URL

  ```python
  from urllib.parse import urlparse
  url = 'http://netloc:80/path;param?query=arg#frag'
  print(urlparse(url))
  '''Out:
  ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='frag')
  '''
  ```

- *scheme* - 用于设置 `scheme` 的默认值，仅在 URL 中缺少 `scheme` 时会才会使用该值

  ```python
  from urllib.parse import urlparse
  url = 'http://netloc:80/path;param?query=arg#frag'
  print(urlparse(url, scheme='https'))
  #> ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='frag')
  url = '//netloc:80/path;param?query=arg#frag'
  print(urlparse(url, scheme='https'))
  #> ParseResult(scheme='https', netloc='netloc:80', path='/path', params='param', query='query=arg', fragment='frag')
  ```

- *allow_fragments* - 若 `allow_fragments=False` 则无法识别 `fragment`，并且会将 `fragment` 解析为 `path`, `parameters` 或 `query` 中的一部分

  ```python
  from urllib.parse import urlparse
  url = 'http://netloc:80/path;param?query=arg#frag'
  print(urlparse(url, allow_fragments=False))
  #> ParseResult(scheme='http', netloc='netloc:80', path='/path', params='param', query='query=arg#frag', fragment='')
  ```

#### Return

`urlparse` 的返回值是基于 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) 实现的 ParseResult 对象，所含属性如下:

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

ParseResult 对象与其它 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) 一样，拥有一些非常有用的特殊方法，比如 `_replace()`:

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

`urlparse` 遵循 [RFC 1808](https://tools.ietf.org/html/rfc1808.html) 中给定的语法规范，只有在使用 `'//'` 引入 netloc 时，`urlparse` 才会识别 netloc；否则 `urlparse` 会假定正在使用相对 URL:

```python
from urllib.parse import urlparse
urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
#> ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
urlparse('www.cwi.nl/%7Eguido/Python.html')
#> ParseResult(scheme='', netloc='', path='www.cwi.nl/%7Eguido/Python.html', params='', query='', fragment='')
urlparse('help/Python.html')
#> ParseResult(scheme='', netloc='', path='help/Python.html', params='', query='', fragment='')
```

Reading the `port` attribute will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) if an invalid port is specified in the URL. See section[Structured Parse Results](https://docs.python.org/3/library/urllib.parse.html#urlparse-result-object) for more information on the result object.

Unmatched square brackets in the `netloc` attribute will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError).

Characters in the `netloc` attribute that decompose under NFKC normalization (as used by the IDNA encoding) into any of `/`, `?`, `#`, `@`, or `:` will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError). If the URL is decomposed before parsing, no error will be raised.

*Changed in version 3.2:* Added IPv6 URL parsing capabilities.

*Changed in version 3.3:* The fragment is now parsed for all URL schemes (unless *allow_fragment* is false), in accordance with [**RFC 3986**](https://tools.ietf.org/html/rfc3986.html). Previously, a whitelist of schemes that support fragments existed.

*Changed in version 3.6:* Out-of-range port numbers now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError), instead of returning [`None`](https://docs.python.org/3/library/constants.html#None).

*Changed in version 3.7.3:* Characters that affect netloc parsing under NFKC normalization will now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError).

### urlsplit()

🔨 urllib.parse.urlsplit(*urlstring*, *scheme*='', *allow_fragments*=True)

`urlsplit()` 和 `urlparse()` 的区别在于前者不会将 `path` 和 `parameters` 分开。

```
scheme://netloc/path;parameters?query#fragment
```

`urlsplite()` 对于遵循 [**RFC 2396**](https://tools.ietf.org/html/rfc2396.html) 的 URL 非常有用，因为这些 URL 支持为每段路径配置参数。

```python
from urllib.parse import urlsplit
url = 'http://user:pwd@NetLoc:80/p1;para/p2;para?query=arg#frag'
print(urlsplit(url))
#> SplitResult(scheme='http', netloc='user:pwd@NetLoc:80', path='/p1;para/p2;para', query='query=arg', fragment='frag')
```

#### Parameters

`urlsplit()` 各参数的用法与 `urlparse()` 相同

#### Return

`urlparse()` 的返回值是基于 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) 实现的 SplitResult 对象，所含属性如下:

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

#### Notes

Reading the `port` attribute will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) if an invalid port is specified in the URL. See section[Structured Parse Results](https://docs.python.org/3/library/urllib.parse.html#urlparse-result-object) for more information on the result object.

Unmatched square brackets in the `netloc` attribute will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError).

Characters in the `netloc` attribute that decompose under NFKC normalization (as used by the IDNA encoding) into any of `/`, `?`, `#`, `@`, or `:` will raise a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError). If the URL is decomposed before parsing, no error will be raised.

*Changed in version 3.6:* Out-of-range port numbers now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError), instead of returning [`None`](https://docs.python.org/3/library/constants.html#None).

*Changed in version 3.7.3:* Characters that affect netloc parsing under NFKC normalization will now raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError).

### urldefrag()

🔨 urllib.parse.urldefrag(*url*)

该函数会按照如下格式将 URL 解析为 6 个部分，其返回值是 ParseResult 对象。

该函数会将 *url* 解析为 2 个部分:

- 第一个部分包含 `scheme://netloc/path;parameters?query` 
- 第二个部分包含 `fragment`

```python
from urllib.parse import urldefrag

original = 'http://netloc/path;param?query=arg#frag'
d = urldefrag(original)
print(d.url) #> http://netloc/path;param?query=arg
print(d.fragment) #> frag
print(d.geturl()) #> http://netloc/path;param?query=arg#frag
```

#### Return

`urldefrag()` 的返回值是基于 [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) 实现的 DefragResult 对象，所含属性如下:

| Attribute  | Index | Value                | Value if not present |
| :--------- | :---- | :------------------- | :------------------- |
| `url`      | 0     | URL with no fragment | empty string         |
| `fragment` | 1     | Fragment identifier  | empty string         |

## Unparsing

把分解后的 URL 重新组合为一个完整的 URL 的过程被成为逆解析(*unparsing*)

### .geturl()

ParseResult 对象(由 `urlparse()` 产生)、SplitResult 对象(由 `urlsplite()` 产生)和 DefragResult 对象(由 `urldefrag` 产生)均具备 `geturl()` 方法，该方法用于逆解析 URL:

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

该函数用于从可迭代对象 *parts* 逆解析 URL，

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

该函数用于从可迭代对象 *parts* 逆解析 URL，

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

## Joining

### urljoin()

🔨 urllib.parse.urljoin(*base*, *url*, *allow_fragments*=True)

`urljoin()` 用于将 *base* (base URL) 和 *url* 拼接为一个完整的 URL，该函数会分析 *base* 的 `scheme`, `netloc` 和 `path` 

```
scheme://netloc/path;parameters?query#fragment
```

若 `allow_fragments=False` 则无法识别 `fragment`，并且会将 `fragment` 解析为 `path`, `parameters` 或 `query` 中的一部分，这与 `urlparse()` 相同。

如果 *url* 使用相对路径，效果如下:

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

如果 *url* 使用非相对路径，处理方式与 `os.path.join()` 相同:

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

如果 *url* 是绝对 URL (以 `//` 或  `scheme://` 开头的 URL)，那么 *url* 的 netloc 和/或 scheme 将出现在结果中:

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

Changed in version 3.5:* Behaviour updated to match the semantics defined in [**RFC 3986**](https://tools.ietf.org/html/rfc3986.html).

## Encoding Query Arguments

### parse_qs()

urllib.parse.parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)

### parse_qsl()

urllib.parse.parse_qsl(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)









