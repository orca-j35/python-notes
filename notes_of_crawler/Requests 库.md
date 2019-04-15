# Requests 库
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

相关资源:

- PyPI: https://pypi.org/project/requests/
- GitHub: https://github.com/kennethreitz/requests
- Docs-EN: http://docs.python-requests.org/en/master/ 🍰
- Docs-CN: http://docs.python-requests.org/zh_CN/latest/
- 教程 - [测试教程网](http://www.testclass.net/all): http://www.testclass.net/requests

安装:

```shell
conda install requests
```

## httpbin

可使用 [httpbin](http://httpbin.org/) 来观察 HTTP 请求和响应的内容。由于众所周知的问题，直接访问 [httpbin](http://httpbin.org/) 可能会比较缓慢，因此建议在本地运行 httppin，详见 [httpbin - GitHub](https://github.com/postmanlabs/httpbin) 。

```python
docker pull kennethreitz/httpbin
docker run -p 80:80 kennethreitz/httpbin
```

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

