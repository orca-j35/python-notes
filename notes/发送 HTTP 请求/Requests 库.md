# Requests 库
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

相关资源:

- PyPI: https://pypi.org/project/requests/
- GitHub: https://github.com/kennethreitz/requests
- Docs-EN: https://2.python-requests.org/en/master/ 🧀
- Docs-CN: https://2.python-requests.org/en/master/
- 教程 - [测试教程网](http://www.testclass.net/all): http://www.testclass.net/requests

安装:

```shell
conda install requests
```

延伸阅读:

-  [Python：requests：详解超时和重试](https://www.cnblogs.com/gl1573/p/10129382.html)

## 非 form 数据

如果需要发送非 form-encoded 数据，直接向 `data` 参数传递 `str` 对象即可，此时数据将被存放在 POST 请求的 data 字段中。例如:

```python
import json
import requests
payload = {'key1': 'value1', 'key2': 'value2'}
reps = requests.post('https://httpbin.org/post', data=json.dumps(payload))
print(reps.text)
```

输出:

```
{
  "args": {},
  "data": "{\"key1\": \"value1\", \"key2\": \"value2\"}",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "36",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.21.0"
  },
  "json": {
    "key1": "value1",
    "key2": "value2"
  },
  "origin": "171.210.195.197, 171.210.195.197",
  "url": "https://httpbin.org/post"
}
```

相同功能还可通过 `json` 参数(在 2.4.2 中添加)完成，此时无需手动编码 `dict` 对象:

```python
import requests
payload = {'key1': 'value1', 'key2': 'value2'}
reps = requests.post('https://httpbin.org/post', json=payload)
print(reps.text)
```

输出结果与前面完全一致。

## httpbin

可使用 [httpbin](http://httpbin.org/) 来观察 HTTP 请求和响应的内容。由于众所周知的原因，直接访问 [httpbin](http://httpbin.org/) 可能会比较缓慢，因此建议在本地运行 httppin，详见 [httpbin - GitHub](https://github.com/postmanlabs/httpbin) 。

```python
docker pull kennethreitz/httpbin
docker run -p 80:80 kennethreitz/httpbin
```

然后访问 <http://localhost:80/> 即可。

httpbin 用于提供 HTTP 请求测试，当 httpbin 服务器获得请求消息后，它会将请求消息转换为 JSON 格式并将其置于响应体中。

## 解码响应内容

> 参考: 
>
> - https://2.python-requests.org/en/master/api/#requests.Response
> - https://2.python-requests.org//zh_CN/latest/user/quickstart.html#id3

`Response` 对象中与解码过程相关的属性如下:

- `.apparent_encoding` - 利用 `chardet` 库猜测到的编码方案

- `.encoding = None` - 访问 `.text` 字段时使用的编码方案

- `.text` - 以 Unicode 字符串表示响应内容

  > If Response.encoding is None, encoding will be guessed using `chardet`.
  >
  > The encoding of the response content is determined based solely on HTTP headers, following RFC 2616 to the letter. If you can take advantage of non-HTTP knowledge to make a better guess at the encoding, you should set `r.encoding` appropriately before accessing this property.

如果需要获取 Unicode 形式的响应内容，可访问 `Response` 实例的 `.text` 字段。如果 `Response.encoding` 的值是 `None`，则会使用 `chardet` 库来猜测响应内容的编码方案。

响应内容的编码仅由 HTTP  header 确定，并严格遵循 RFC 2616 中给出的样式。如果你需要修改编码方案，请在访问 `.text` 前先设置 `.encoding` 字段。

```python
>>> import requests
>>> r = requests.get('https://api.github.com/events')
>>> r.text
u'[{"repository":{"open_issues":0,"url":"https://github.com/...
>>> r.encoding
'utf-8'
>>> r.encoding = 'ISO-8859-1'
```

Requests 会自动解码来自服务器的内容。大多数 unicode 字符集都能被无缝地解码。

请求发出后，Requests 会基于 HTTP 头部对响应的编码作出有根据的推测。当你访问 `r.text` 之时，Requests 会使用其推测的文本编码。你可以找出 Requests 使用了什么编码，并且能够使用 `r.encoding` 属性来改变它。

如果你改变了编码，每当你访问 `r.text` ，Request 都将会使用 `r.encoding` 的新值。你可能希望在使用特殊逻辑计算出文本的编码的情况下来修改编码。比如 HTTP 和 XML 自身可以指定编码。这样的话，你应该使用 `r.content` 来找到编码，然后设置 `r.encoding` 为相应的编码。这样就能使用正确的编码解析 `r.text` 了。

在你需要的情况下，Requests 也可以使用定制的编码。如果你创建了自己的编码，并使用 `codecs` 模块进行注册，你就可以轻松地使用这个解码器名称作为 `r.encoding` 的值， 然后由 Requests 来为你处理编码。



## Example

示例 - 获取 "知乎 - 发现" 页面中的条目:

```python
import requests
import re

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get("https://www.zhihu.com/explore", headers=headers)
# 目标HTML语句
# <div class="explore-feed feed-item" data-offset="1" data-za-module="AnswerItem" data-za-index="">
#     <h2><a class="question_link" href="/question/39835004/answer/644144243" target="_blank" data-id="8141376" data-za-element-name="Title">
#     从水龙头下落的水为何会越来越细？
#     </a></h2>
pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
titles = re.findall(pattern, r.text)
print(titles)
```

示例 - 抓取二进制数据

```python
# 抓取github.com的ico图标
import requests
url = "https://github.com/favicon.ico"
r = requests.get(url)

from urllib import parse
path = parse.urlparse(url).path.strip('/')
with open(path,'wb') as image:
    image.write(r.content)
```

