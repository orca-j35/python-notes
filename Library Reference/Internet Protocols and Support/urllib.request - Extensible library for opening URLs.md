# urllib.request - Extensible library for opening URLs
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) — Extensible library for opening URLs
> - [urllib.request — Network Resource Access](https://pymotw.com/3/urllib.request/index.html#module-urllib.request)
> - [13.3. urllib.request — 访问网络资源](https://learnku.com/docs/pymotw/urllibrequest-network-resource-access/3433)
> - [HOWTO Fetch Internet Resources Using The urllib Package](https://docs.python.org/3/howto/urllib2.html)

该模块中包含用于打开 URL(主要是 HTTP) 的函数和类 — basic and digest authentication, redirections, cookies and more. 

> See also: The [Requests package](http://docs.python-requests.org/) is recommended for a higher-level HTTP client interface.

## 相关工具

本笔记会使用 [httpbin](http://httpbin.org/) 来观察 HTTP 请求和响应的内容，为了提高 httpbin 的响应速度，会在本地运行 httpbin，详见 [httpbin - GitHub](https://github.com/postmanlabs/httpbin) 。

```python
docker pull kennethreitz/httpbin
docker run -p 80:80 kennethreitz/httpbin
```

httpbin 用于提供 HTTP 请求测试，当 httpbin 服务器获得请求消息后，它会将请求消息转换为 JSON 格式并将其置于响应体中。

## functions

[`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) 模块提供了如下函数

### urlopen()🔨

🔨urllib.request.urlopen(*url*, *data=None*, [*timeout*, ]*, *cafile*=None, *capath*=None, *cadefault*=False, *context*=None)

该函数用于请求 *url*。`urllib.request` 模块使用的 HTTP 协议为 HTTP/1.1，并且会在 HTTP 请求的头中包含 `Connection:close`。

Note: 如果没有处理程序处理请求，则可能会返回 `None` (尽管默认安装的全局 [`OpenerDirector`](https://docs.python.org/3/library/urllib.request.html#urllib.request.OpenerDirector) 会使用 [`UnknownHandler`](https://docs.python.org/3/library/urllib.request.html#urllib.request.UnknownHandler) 处理程序来确保永远不会发生这种情况)。

此外，如果检测到代理设置(例如，当设置了像 `http_proxy` 这样的 `*_proxy` 环境变量时)，则会默认安装 [`ProxyHandler`](https://docs.python.org/3/library/urllib.request.html#urllib.request.ProxyHandler) 并确保通过代理处理请求。

来自 Python 2.6 及更早版本的遗留函数 `urllib.urlopen` 已停止使用；[`urllib.request.urlopen()`](https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen) 对应于旧的 `urllib.urlopen`。Proxy handling, which was done by passing a dictionary parameter to `urllib.urlopen`, can be obtained by using [`ProxyHandler`](https://docs.python.org/3/library/urllib.request.html#urllib.request.ProxyHandler) objects.

*Changed in version 3.2:* *cafile* and *capath* were added.

*Changed in version 3.2:* HTTPS virtual hosts are now supported if possible (that is, if[`ssl.HAS_SNI`](https://docs.python.org/3/library/ssl.html#ssl.HAS_SNI) is true).

*New in version 3.2:* *data* can be an iterable object.

*Changed in version 3.3:* *cadefault* was added.

*Changed in version 3.4.3:* *context* was added.

*Deprecated since version 3.6:* *cafile*, *capath* and *cadefault* are deprecated in favor of *context*. Please use [`ssl.SSLContext.load_cert_chain()`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_cert_chain) instead, or let[`ssl.create_default_context()`](https://docs.python.org/3/library/ssl.html#ssl.create_default_context) select the system’s trusted CA certificates for you.

#### 参数说明

- *url* - 被请求的 URL，可以是字符串或 [`Request`](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request) 对象。

- *data* - 需要发送给服务器的附加数据，*data* 必须是 `bytes` 类型的数据。如果不需要附加数据，将其设为 `None` 即可，详见﹝[Request()📦](#Request()📦)﹞小节。如果没有提供 *data* 参数，便会使用 GET 方法；如果提供了 *data* 参数，则会使用 POST 方法:

  ```python
  from urllib import request, parse
  url_post = 'http://127.0.0.1/post'
  data = parse.urlencode({'id': 'orca-j35', '鲸': '鱼'})
  print(data)
  with request.urlopen(url_post, data=data.encode('ascii')) as rp:
      # 'ascii'或'utf8'均可
      print(f'==={rp._method}===')
      for line in rp:
          print(line)
  ```

  运行效果如下，`form` 字段中的数据便是我们通过 *data* 传递的参数:

  ```python
  id=orca-j35&%E9%B2%B8=%E9%B1%BC
  ===POST===
  b'{\n'
  b'  "args": {}, \n'
  b'  "data": "", \n'
  b'  "files": {}, \n'
  b'  "form": {\n'
  b'    "id": "orca-j35", \n'
  b'    "\\u9cb8": "\\u9c7c"\n'
  b'  }, \n'
  b'  "headers": {\n'
  b'    "Accept-Encoding": "identity", \n'
  b'    "Connection": "close", \n'
  b'    "Content-Length": "31", \n'
  b'    "Content-Type": "application/x-www-form-urlencoded", \n'
  b'    "Host": "127.0.0.1", \n'
  b'    "User-Agent": "Python-urllib/3.7"\n'
  b'  }, \n'
  b'  "json": null, \n'
  b'  "origin": "172.17.0.1", \n'
  b'  "url": "http://127.0.0.1/post"\n'
  b'}\n'
  ```

- *timeout* - 设置阻塞操作(如连接尝试)超时的时长(以秒为单位)，如果在 *timeout* 时长内未获得响应，便会抛出异常。如果未设置，则会使用全局默认超时设置。*timoeout* 仅适用于 HTTP、HTTPS 和 FTP 连接。

  ```python
  from urllib import request
  with request.urlopen("https://www.google.com/", timeout=1) as rp:
      print(f'==={rp._method}===')
      for line in rp:
          print(line)
  '''Out:
  Traceback (most recent call last):
  --snip--
      sock.connect(sa)
  socket.timeout: timed out
  
  During handling of the above exception, another exception occurred:
  Traceback (most recent call last):
    --snip--
      raise URLError(err)
  urllib.error.URLError: <urlopen error timed out>
  '''
  ```

  以下代码可用于处理超时异常

  ```python
  import socket
  import urllib.error
  from urllib import request
  try:
      with request.urlopen(url, timeout=0.1) as rp:
          print(f'==={rp._method}===')
          for line in rp:
              print(line)
  except urllib.error.URLError as e:
      if isinstance(e.reason, socket.timeout):
          print('time out')
  ```

- *context* - 用于配置 SSL，其值必须是用于描述 SSL 选项的 [`ssl.SSLContext`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext) 实例，详见 [`HTTPSConnection`](https://docs.python.org/3/library/http.client.html#http.client.HTTPSConnection)。

- *cafile* & *capath* - 用于为 HTTPS 请求指定一组可信的 CA 证书(*certificates*)，在 Python 3.6 中已被弃用

  - *cafile* should point to a single file containing a bundle of CA certificates
  - *capath* should point to a directory of hashed certificate files

  如果了解更多信息，可参考 [`ssl.SSLContext.load_verify_locations()`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_verify_locations)

- *cadefault* - 在 Python 3.6 中已被弃用

Note: 自 Python 3.6 起，已弃用 *cafile*、*capath*、*cadefault*，请改用 *context* 来完成相关操作，比如使用 [`ssl.SSLContext.load_cert_chain()`](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_cert_chain)，还可让 [`ssl.create_default_context()`](https://docs.python.org/3/library/ssl.html#ssl.create_default_context) 为你选择系统可信任的 CA 证书。

如果使用了错误的协议，将抛出 [`URLError`](https://docs.python.org/3/library/urllib.error.html#urllib.error.URLError)。

#### 返回值

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

如果 *url* 是 HTTP 和 HTTPS，`urlopen()` 将返回经过修改的 [`http.client.HTTPResponse`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) 对象，并且会将前面提到的三个方法添加到该对象中。另外该对象的 `msg` 属性不再包含响应头(由 [`HTTPResponse`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) 文档规定)，而是与 [`reason`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse.reason) 包含相同的信息(服务器返回的 reason 短语)。有关 [`http.client.HTTPResponse`](https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse) 对象的信息，详见笔记﹝[HTTPResponse 对象.md](./HTTPResponse 对象.md)﹞

对于 FTP、file 和 data URL，以及利用 Python2 中遗留的 [`URLopener`](https://docs.python.org/3/library/urllib.request.html#urllib.request.URLopener) 和 [`FancyURLopener`](https://docs.python.org/3/library/urllib.request.html#urllib.request.FancyURLopener) 显示处理的请求，`urlopen()` 将返回 `urllib.response.addinfourl` 对象。

#### 坑

脚本文件:

```python
# learn.py
from urllib import request, parse
url = 'https://pymotw.com'
with request.urlopen(url) as rp:
    print(rp)
```

我在 `conda` 环境中(或独立安装的 Python 中)可正常执行以上脚本:

```shell
# 在名为base的conda环境中执行脚本
(base) C:\Users\iwhal\Desktop\PyTest>C:/Anaconda3/python.exe c:/Users/iwhal/Desktop/PyTest/learn.py
<http.client.HTTPResponse object at 0x0000023DAF1B15C0>
# 在独立安装的Python3.5中执行脚本
C:\Users\iwhal>C:\Python35\python.exe c:/Users/iwhal/Desktop/PyTest/learn.py
<http.client.HTTPResponse object at 0x000001B72B777320>
```

但是如果我在没有激活 conda 环境情况下，使用 conda 中的 Python 来运行上述脚本，便会抛出异常:

```shell
C:\Users\iwhal>C:/Anaconda3/python.exe c:/Users/iwhal/Desktop/PyTest/learn.py
Traceback (most recent call last):
--snip--
    raise URLError('unknown url type: %s' % type)
urllib.error.URLError: <urlopen error unknown url type: https>
```

目前怀疑是在这种情况下无法导入 `ssl` 模块造成的，但并不知道是什么原因导致无法导入 `ssl` 模块，我看到 `_ssl` 文件确实躺在它应在的路径上 `~\Anaconda3\DLLs\_ssl.pyd` 。

```shell
C:\Users\iwhal>C:\Python35\python.exe
Python 3.5.4 (v3.5.4:3f56838, Aug  8 2017, 02:17:05) 
>>> import ssl
>>> ^Z

C:\Users\iwhal>C:/Anaconda3/python.exe
Python 3.7.1 (default, Dec 10 2018, 22:54:23) 
>>> import ssl
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Anaconda3\lib\ssl.py", line 98, in <module>
    import _ssl             # if we can't import it, let the error propagate
ImportError: DLL load failed: 找不到指定的模块。
```

这个问题会导致在 PyChram 中无法使用 conda 环境中的 Python 解释器，因为 PyChram 在运行脚本时不会激活 conda 环境，它会直接使用解释器运行脚本，如果脚本中调用了 `request.urlopen()` 便会抛出异常。VScode 在运行脚本时会先激活选定的 conda 环境，因此能正常调用  `request.urlopen()`。

## classes

[`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) 模块提供了如下类

### Request()📦



