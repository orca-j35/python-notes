# urllib.error - Exception classes raised by urllib.request
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [HOWTO Fetch Internet Resources Using The urllib Package](https://docs.python.org/3/howto/urllib2.html)

[`urllib.error`](https://docs.python.org/3/library/urllib.error.html#module-urllib.error) 模块定义了由 [`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) 模块产生的异常，如果在使用 `urllib.request` 时出现了问题，便会抛出 `urllib.error` 中定义的异常。最基本的异常类型是 [`URLError`](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError)。

🔨*exception* urllib.error.URLError

The handlers raise this exception (or derived exceptions) when they run into a problem. It is a subclass of [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError).

- `reason` - 引发错误的原因，可以是一个消息字符串，或者是另一个异常实例。

```python
from urllib import parse, error, request
url_error = 'https://www.google.com/'
try:
    with request.urlopen(url_error, timeout=1) as rp:
        print(rp)
except error.URLError as ex:
    if isinstance(ex.reason, socket.timeout):
        print(type(ex.reason))
```

输出:

```python
<class 'socket.timeout'>
```

*Changed in version 3.3:* [`URLError`](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError) has been made a subclass of [`OSError`](https://docs.python.org/3/library/exceptions.html#OSError) instead of [`IOError`](https://docs.python.org/3/library/exceptions.html#IOError).

🔨*exception* urllib.error.HTTPError

虽然 [`HTTPError`](https://docs.python.org/3/library/urllib.error.html#urllib.error.HTTPError) 属于异常类型([`URLError`](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError) 的子类)，但是我们还可以将其视作 non-exceptional 的 file-like 返回值(类似于 [`urlopen()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) 的返回值)——这在处理部分 HTTP 错误时非常有用，比如身份验证(*authentication*)请求。

- `code`

  An HTTP status code(e.g. `404`) as defined in [**RFC 2616**](https://tools.ietf.org/html/rfc2616.html). This numeric value corresponds to a value found in the dictionary of codes as found in [`http.server.BaseHTTPRequestHandler.responses`](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler.responses).

- `reason`

  This is usually a string explaining the reason for this error.

- `headers`

  The HTTP response headers for the HTTP request that caused the [`HTTPError`](https://docs.python.org/3/library/urllib.error.html#urllib.error.HTTPError).

  *New in version 3.4.*

```python
from urllib import parse, error, request
url_error = 'http://127.0.0.1/hello'
try:
    with request.urlopen(url_error, timeout=1) as rp:
        print(rp)
except error.HTTPError as ex:
    print(type(ex))
    print(ex.code, ex.reason, ex.headers, sep='\n')
```

输出:

```python
<class 'urllib.error.HTTPError'>
404
NOT FOUND
Server: gunicorn/19.9.0
Date: Mon, 08 Apr 2019 08:00:21 GMT
Connection: close
Content-Type: text/html
Content-Length: 233
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

🔨*exception* urllib.error.ContentTooShortError(*msg*, *content*)

This exception is raised when the [`urlretrieve()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlretrieve) function detects that the amount of the downloaded data is less than the expected amount (given by the *Content-Length*header). The `content` attribute stores the downloaded (and supposedly truncated) data.