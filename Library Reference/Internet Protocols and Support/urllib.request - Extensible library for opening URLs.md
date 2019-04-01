# urllib.request - Extensible library for opening URLs
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

该模块中包含用于打开 URL(主要是 HTTP) 的函数和类 — basic and digest authentication, redirections, cookies and more. 

> See also: The [Requests package](http://docs.python-requests.org/) is recommended for a higher-level HTTP client interface.

## functions

在 [`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) 模块中定义了如下函数

### urlopen()🔨

🔨urllib.request.urlopen(*url*, *data=None*, [*timeout*, ]*, *cafile*=None, *capath*=None, *cadefault*=False, *context*=None)

参数说明

- *url* - 被打开的 URL，可以是字符串或 [`Request`](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request) 对象。
- *data* - `bytes` 类型的数据

该函数的返回值是 [`http.client.HTTPResponse`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) 对象，见﹝[HTTPResponse 对象](#HTTPResponse 对象)﹞小节

#### HTTPResponse 对象

> An [`HTTPResponse`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) instance wraps the HTTP response from the server. It provides access to the request headers and the entity body. The response is an iterable object and can be used in a `with` statement.
>
> *Changed in version 3.5:* The [`io.BufferedIOBase`](https://docs.python.org/3/library/io.html#io.BufferedIOBase) interface is now implemented and all of its reader operations are supported.
>
> —— HTTPResponse Objects](https://docs.python.org/3/library/http.client.html#httpresponse-objects) 

```python
from urllib import request
with request.urlopen('https://pymotw.com') as response:
	print(response)
#> <http.client.HTTPResponse object at 0x0000016EE40DAE10>
```

`HTTPResponse` 对象除了包含以下常用属性外，还实现了 [`io.BufferedIOBase`](https://docs.python.org/3/library/io.html#io.BufferedIOBase) 接口。为了保证正常关闭 `HTTPResponse` 对象，最好使用 `with` 语句。

- 🔨HTTPResponse.read([*amt*])
  Reads and returns the response body, or up to the next amt bytes.

  ```python
  from urllib import request
  with request.urlopen('https://pymotw.com') as response:
  	print(response.read())
  '''Out:
  b'<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n    <title>PyMOTW</title>\n    <meta http-equiv="refresh" content="0;URL=\'https://pymotw.com/3/\'" />\n  </head>\n  <body>\n    <p>Redirecting to <a href="https://pymotw.com/3/">Python 3 examples</a>.</p>\n  </body>\n</html>\n'
  '''
  ```

- 🔨HTTPResponse.readinto(*b*)
  Reads up to the next len(b) bytes of the response body into the buffer b. Returns the number of bytes read.

  New in version 3.3.

  ```python
  from urllib import request
  with request.urlopen('https://pymotw.com') as response:)
      b = bytearray(20)
      response.readinto(b)
      print(b)
  	#> bytearray(b'<html xmlns="http://')
  ```

- 🔨HTTPResponse.getheader(*name*, *default*=None)
  Return the value of the header *name*, or *default* if there is no header matching *name*. If there is more than one header with the name *name*, return all of the values joined by ‘, ‘. If ‘default’ is any iterable other than a single string, its elements are similarly returned joined by commas.

  ```python
  from urllib import request
  with request.urlopen('https://pymotw.com') as response:
  	print(response.getheader('Content-Type'))
  #> text/html
  ```

- 🔨HTTPResponse.getheaders()
  Return a list of (header, value) tuples.

  ```python
  from urllib import request
  with request.urlopen('https://pymotw.com') as response:
  	print(response.getheaders())
  #> [('Date', 'Mon, 01 Apr 2019 07:19:19 GMT'), ('Server', 'Apache'), ('Last-Modified', 'Sat, 02 Jan 2016 16:34:42 GMT'), ('ETag', '"10d-5285c770209dc"'), ('Accept-Ranges', 'bytes'), ('Content-Length', '269'), ('Connection', 'close'), ('Content-Type', 'text/html')]
  ```

- 🔨HTTPResponse.fileno()
  Return the fileno(文件描述符) of the underlying socket.

  ```python
  from urllib import request
  with request.urlopen('https://pymotw.com') as response:
  	print(response.fileno())
  #> 632
  ```

- 🔨HTTPResponse.msg
  A http.client.HTTPMessage instance containing the response headers. http.client.HTTPMessage is a subclass of email.message.Message.

  ```python
  with request.urlopen('https://pymotw.com') as response:
      print(response.msg) #> OK
      print(response.version) #> 11
      print(response.status) #> 200
      print(response.reason) #> OK
      print(response.debuglevel) #> 0
      print(response.closed) #> False
  ```

- 🔨HTTPResponse.version
  HTTP protocol version used by server. 10 for HTTP/1.0, 11 for HTTP/1.1.

- 🔨HTTPResponse.status
  Status code returned by server.

- 🔨HTTPResponse.reason
  Reason phrase returned by server.

- 🔨HTTPResponse.debuglevel
  A debugging hook. If debuglevel is greater than zero, messages will be printed to stdout as the response is read and parsed.

- 🔨HTTPResponse.closed
  Is True if the stream is closed.



