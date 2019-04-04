# HTTPResponse 对象
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - ﹝[urllib.request - Extensible library for opening URLs.md](./urllib.request - Extensible library for opening URLs.md)﹞
> - [HTTPResponse Objects](https://docs.python.org/3/library/http.client.html#httpresponse-objects) 

## 概述

> An [`HTTPResponse`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) instance wraps the HTTP response from the server. It provides access to the request headers and the entity body. The response is an iterable object and can be used in a `with` statement.
>
> *Changed in version 3.5:* The [`io.BufferedIOBase`](https://docs.python.org/3/library/io.html#io.BufferedIOBase) interface is now implemented and all of its reader operations are supported.
>
> —— [HTTPResponse Objects](https://docs.python.org/3/library/http.client.html#httpresponse-objects) 

```python
from urllib import request
with request.urlopen('https://pymotw.com') as response:
    print(f'{response}\n')
    for line in response:
        print(line)
'''Out:
<http.client.HTTPResponse object at 0x000001E76D330C88>

b'<html xmlns="http://www.w3.org/1999/xhtml">\n'
b'<head>\n'
b'    <title>PyMOTW</title>\n'
b'    <meta http-equiv="refresh" content="0;URL=\'https://pymotw.com/3/\'" />\n'
b'  </head>\n'
b'  <body>\n'
b'    <p>Redirecting to <a href="https://pymotw.com/3/">Python 3 examples</a>.</p>\n'
b'  </body>\n'
b'</html>\n'
'''
```

`HTTPResponse` 对象除了包含以下常用属性外，还实现了 [`io.BufferedIOBase`](https://docs.python.org/3/library/io.html#io.BufferedIOBase) 接口。为了保证正常关闭 `HTTPResponse` 对象，最好使用 `with` 语句。

本笔记针对 `urllib.request.urlopen()` 返回的 `http.client.HTTPResponse` 对象展开，由于 `urlopen()` 会对 `http.client.HTTPResponse` 做出修改，所有本笔记不适用于原始的 `http.client.HTTPResponse` 对象。

无论使用何种 URL，`urlopen()` 返回的对象始终可用于上下文管理器，并且总会包含以下方法:

- `geturl()` — 返回检索到的资源的 URL，通常用于确定是否遵循重定向
- `info()` — 以 [`email.message_from_string()`](https://docs.python.org/3/library/email.parser.html#email.message_from_string) 实例的形式返回页面的元信息(*meta*-*information*)，比如 hearder (见 [Quick Reference to HTTP Headers](http://jkorpela.fi/http.html)) 
- `getcode()` – 返回响应的 HTTP 状态代码

```python
from urllib import request
with request.urlopen('http://127.0.0.1/get?id=orca-j35') as rp:
    print(f'geturl-->\n{rp.geturl()}')
    print(f'info-->\n{rp.info()}')
    print(f'getcode-->\n{rp.getcode()}')
'''Out:
geturl-->
http://127.0.0.1/get?id=orca-j35
info-->
Server: gunicorn/19.9.0
Date: Wed, 03 Apr 2019 03:47:50 GMT
Connection: close
Content-Type: application/json
Content-Length: 263
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true


getcode-->
200
'''
```

对于 HTTP 和 HTTPS URL，`urlopen()` 将返回经过修改的 `http.client.HTTPResponse` 对象，并且会将前面提到的三个方法添加到该对象中。另外该对象的 `msg` 属性不再包含响应头(由 [`HTTPResponse`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) 文档规定)，而是与 [`reason`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse.reason) 包含相同的信息(服务器返回的 reason 短语)。

另外，可利用 `vars()` 和 `dir()` 来观察 `HTTPResponse` 对象的属性:(远比本文列举的内容丰富):

```python
from pprint import pprint
from urllib import request
url = 'https://pymotw.com'
with request.urlopen(url, data=b'a=1') as rp:
    # print(f'{rp}\n')
    # for line in rp:
    #     print(line)
    pprint(vars(rp))
    print(dir(rp))
'''Out:
{'_method': 'POST',
 'chunk_left': 'UNKNOWN',
 'chunked': False,
 'code': 200,
 'debuglevel': 0,
 'fp': <_io.BufferedReader name=608>,
 'headers': <http.client.HTTPMessage object at 0x0000018DF4AE09B0>,
 'length': 269,
 'msg': 'OK',
 'reason': 'OK',
 'status': 200,
 'url': 'https://pymotw.com',
 'version': 11,
 'will_close': True}
['__abstractmethods__', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_abc_impl', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_check_close', '_close_conn', '_get_chunk_left', '_method', '_peek_chunked', '_read1_chunked', '_read_and_discard_trailer', '_read_next_chunk_size', '_read_status', '_readall_chunked', '_readinto_chunked', '_safe_read', '_safe_readinto', 'begin', 'chunk_left', 'chunked', 'close', 'closed', 'code', 'debuglevel', 'detach', 'fileno', 'flush', 'fp', 'getcode', 'getheader', 'getheaders', 'geturl', 'headers', 'info', 'isatty', 'isclosed', 'length', 'msg', 'peek', 'read', 'read1', 'readable', 'readinto', 'readinto1', 'readline', 'readlines', 'reason', 'seek', 'seekable',
'status', 'tell', 'truncate', 'url', 'version', 'will_close', 'writable', 'write', 'writelines']
'''
```



## read()🔨

🔨HTTPResponse.read([*amt*])
Reads and returns the response body, or up to the next amt bytes.

```python
from urllib import request
with request.urlopen('https://pymotw.com') as response:
    # 读取响应体中的内容
	print(response.read())
'''Out:
b'<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n    <title>PyMOTW</title>\n    <meta http-equiv="refresh" content="0;URL=\'https://pymotw.com/3/\'" />\n  </head>\n  <body>\n    <p>Redirecting to <a href="https://pymotw.com/3/">Python 3 examples</a>.</p>\n  </body>\n</html>\n'
'''
```

直接迭代 `HTTPResponse` 对象，也可获得相同的内容。

## readinto()🔨

🔨HTTPResponse.readinto(*b*)
Reads up to the next len(b) bytes of the response body into the buffer b. Returns the number of bytes read.

New in version 3.3.

```python
from urllib import request
with request.urlopen('https://pymotw.com') as response:
    b = bytearray(20)
    # 读取响应体中的内容
    response.readinto(b)
    print(b)
	#> bytearray(b'<html xmlns="http://')
```

## getheader()🔨

🔨HTTPResponse.getheader(*name*, *default*=None)
Return the value of the header *name*, or *default* if there is no header matching *name*. If there is more than one header with the name *name*, return all of the values joined by ‘, ‘. If ‘default’ is any iterable other than a single string, its elements are similarly returned joined by commas.

```python
from urllib import request
with request.urlopen('https://pymotw.com') as response:
    # 获取响应头中的内容
	print(response.getheader('Content-Type'))
#> text/html
```

## getheaders()🔨

🔨HTTPResponse.getheaders()
Return a list of (header, value) tuples.

```python
from urllib import request
with request.urlopen('https://pymotw.com') as response:
    # 获取响应头中的全部内容
	print(response.getheaders())
#> [('Date', 'Mon, 01 Apr 2019 07:19:19 GMT'), ('Server', 'Apache'), ('Last-Modified', 'Sat, 02 Jan 2016 16:34:42 GMT'), ('ETag', '"10d-5285c770209dc"'), ('Accept-Ranges', 'bytes'), ('Content-Length', '269'), ('Connection', 'close'), ('Content-Type', 'text/html')]
```

## fileno()🔨

🔨HTTPResponse.fileno()
Return the fileno(文件描述符) of the underlying socket.

```python
from urllib import request
with request.urlopen('https://pymotw.com') as response:
    # 获取HTTPResponse实例的文件描述符
	print(response.fileno())
#> 632
```

## msg🔧

🔧HTTPResponse.msg
A http.client.HTTPMessage instance containing the response headers. http.client.HTTPMessage is a subclass of email.message.Message.

Note: `urlopen()` 返回的 `http.client.HTTPResponse` 实例已经过修改，其 `msg` 属性不再包含响应头(如上述英文)，而是与 [`reason`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse.reason) 包含相同的信息(服务器返回的 reason 短语)。

```python
with request.urlopen('https://pymotw.com') as response:
    print(response.msg) #> OK
    print(response.version) #> 11
    print(response.status) #> 200
    print(response.reason) #> OK
    print(response.debuglevel) #> 0
    print(response.closed) #> False
```

## version🔧

🔧HTTPResponse.version
HTTP protocol version used by server. 10 for HTTP/1.0, 11 for HTTP/1.1.

## status🔧

🔧HTTPResponse.status
Status code returned by server.

## reason🔧

🔧HTTPResponse.reason
Reason phrase returned by server.

## debuglevel🔧

🔧HTTPResponse.debuglevel
A debugging hook. If debuglevel is greater than zero, messages will be printed to stdout as the response is read and parsed.

## closed🔧

🔧HTTPResponse.closed
Is True if the stream is closed.