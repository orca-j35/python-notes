# urllib.robotparser - Parser for robots.txt
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`urllib.robotparser`](https://docs.python.org/3/library/urllib.robotparser.html#module-urllib.robotparser) — Parser for robots.txt
> - [urllib.robotparser — Internet Spider Access Control](https://pymotw.com/3/urllib.robotparser/index.html)
> - [13.4. urllib.robotparser — 互联网爬虫访问控制](https://learnku.com/docs/pymotw/urllibrobotparser-internet-spider-access-control/3434)
> - https://en.wikipedia.org/wiki/Robots_exclusion_standard

该模块提供了一个用于分析 [`robots.txt`](https://en.wikipedia.org/wiki/Robots_exclusion_standard) 文件的 `RobotFileParser` 的类。

## robots.txt

`robots.txt` 是一种基于文本的访问控制系统，Web 站点可利用根目录下的 `robots.txt` 文件来约定可被爬取的范围，例如:

```
# robots.txt
User-agent: *
Allow: /public/
Disallow: /
```

上面这个 `/robots.txt` 只允许爬虫爬取 `/public/` 目录中的内容。`Allow` 需和 `Disallow ` 一起使用，并位于 `Disallow ` 前面，表示允许访问 `Disallow` 中的某些目录。

`User-agent: *` 表示对所有爬虫程序有效，如果设置为 `User-agent: Baiduspider`，则表示所设置的规则仅对百度爬虫有效。大公司的爬虫都有固定的 user-agent 标识符，例如:

| user-agent  | companies         |
| ----------- | ----------------- |
| BaiduSpider | www.baidu.com     |
| Googlebot   | www.google.com    |
| 360Spider   | www.so.com        |
| YodaoBot    | www.youdao.com    |
| ia_archiver | www.alexa.cn      |
| Scooter     | www.altavista.com |

有关 `robots.txt` 结构的详细信息，请参考: 

- http://www.robotstxt.org/orig.html
- http://www.robotstxt.org/robotstxt.html
- https://en.wikipedia.org/wiki/Robots_exclusion_standard

## RobotFileParser

🔨class urllib.robotparser.RobotFileParser(*url*='')

该类提供读取和解析 `/robots.txt` 文件的方法。

- set_url(*url*) - 用于设置 `robots.txt` 的 URL，如果在创建 `RobotFileParser` 实例时没有传入 URL，则需调用 `set_url()` 进行设置。

- read() - 读取 `robots.txt` 的 URL 并将其提供给解析器 `parse()`。

- parse(*lines*) - 解析 *lines* 列表中的 robots 规则

  ```python
  '''https://pymotw.com/robots.txt
  Sitemap: https://pymotw.com/sitemap.xml
  User-agent: *
  Disallow: /admin/
  Disallow: /downloads/
  Disallow: /media/
  Disallow: /static/
  Disallow: /codehosting/
  '''
  from urllib import request
  from urllib import robotparser
  
  parser = robotparser.RobotFileParser()
  parser.parse(request.urlopen('https://pymotw.com/robots.txt').read().decode('utf-8').splitlines())
  print(parser.can_fetch('*', 'https://pymotw.com/media/'))
  #> False
  print(parser.can_fetch('*', 'https://pymotw.com/3/urllib.robotparser'))
  #> True
  ```

- can_fetch(*useragent*, *url*) - 根据 `robots.txt` 中设定的规则来判断 *useragent* 是否能够抓取 *url*。在调用 `can_fetch()` 前需要先调用 `read()` 或 `parse()` 来解析 `robots.txt` 中的内容，否则  `can_fetch()` 始终会返回 `False`。

- mtime() - 返回上次获取 `robots.txt` 的时间。这对于需要定期检查 `robots.txt` 的 Web 爬虫非常有用。

- modified() - 将上一次抓取 `robots.txt` 的时间设置为当前时间

- crawl_delay(*useragent*) - 返回 `robts.txt` 中为 *useragent* 配置 `Crawl-delay` 参数。如果出现以下情况，将返回 `None`:

  - 没有在 `robots.txt` 中配置 `Crawl-delay` 参数
  - `Crawl-delay` 参数不适用于 *useragent*
  - `Crawl-delay` 具备无效语法。

  *New in version 3.6.*

  Hint: 可利用 `robots.txt` 中 `Crawl-delay` 规则来约定爬虫的抓取延迟，例如:

  ```python
  User-agent: *
  Crawl-delay: 10
  ```

  详见: https://en.wikipedia.org/wiki/Robots_exclusion_standard#Crawl-delay_directive

- request_rate(*useragent*) - 获取 `robts.txt` 中为 *useragent* 配置 `Request-rate` 参数，返回值是  [named tuple](https://docs.python.org/3/glossary.html#term-named-tuple) `RequestRate(requests, seconds)`。如果出现以下情况，将返回 `None`:

  - 没有在 `robots.txt` 中配置 `Request-rate` 参数
  - `Request-rate` 参数不适用于 *useragent*
  - `Request-rate` 具备无效语法。

  *New in version 3.6.*

## Example

示例 - 演示了 [`RobotFileParser`](https://docs.python.org/3/library/urllib.robotparser.html#urllib.robotparser.RobotFileParser) 类的基本使用方法:

```python
>>> import urllib.robotparser
>>> rp = urllib.robotparser.RobotFileParser()
>>> rp.set_url("http://www.musi-cal.com/robots.txt")
>>> rp.read()
>>> rrate = rp.request_rate("*")
>>> rrate.requests
3
>>> rrate.seconds
20
>>> rp.crawl_delay("*")
6
>>> rp.can_fetch("*", "http://www.musi-cal.com/cgi-bin/search?city=San+Francisco")
False
>>> rp.can_fetch("*", "http://www.musi-cal.com/")
True
```

示例 - 利用 `mtime()` 方法定期检查 `robots.txt` 的更新:

```python
from urllib import robotparser
from urllib import parse
import time

AGENT_NAME = 'PyMOTW'
URL_BASE = 'https://pymotw.com/'
parser = robotparser.RobotFileParser()
parser.set_url(parse.urljoin(URL_BASE, 'robots.txt'))
parser.read()
parser.modified()

PATHS = [
    '/',
    '/PyMOTW/',
    '/admin/',
    '/downloads/PyMOTW-1.92.tar.gz',
]

for path in PATHS:
    age = int(time.time() - parser.mtime())
    print('age:', age, end=' ')
    if age > 1:
        print('rereading robots.txt')
        parser.read()
        parser.modified()
    else:
        print()
    print('{!r:>6} : {}'.format(parser.can_fetch(AGENT_NAME, path), path))
    # Simulate a delay in processing
    time.sleep(1)
    print('.')
'''Out:
age: 0
  True : /
.
age: 1
  True : /PyMOTW/
.
age: 2 rereading robots.txt
 False : /admin/
.
age: 1
 False : /downloads/PyMOTW-1.92.tar.gz
.
'''
```

