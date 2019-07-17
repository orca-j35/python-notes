# Requests 库
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

相关资源:

- PyPI: https://pypi.org/project/requests/
- GitHub: https://github.com/kennethreitz/requests
- Docs-EN: http://docs.python-requests.org/en/master/ 🧀
- Docs-CN: http://docs.python-requests.org/zh_CN/latest/
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

