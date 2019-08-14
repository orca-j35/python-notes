# PyQuery
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

## 概述

> a jquery-like library for python
>
> pyquery allows you to make jquery queries on xml documents. The API is as much as possible the similar to jquery. pyquery uses lxml for fast xml and html manipulation.

相关资源:

- PyPI: https://pypi.org/project/pyquery/
- GitHub: https://github.com/gawel/pyquery
- Docs-EN: https://pyquery.readthedocs.io/en/stable/
- PyQuery complete API: https://pyquery.readthedocs.io/en/stable/api.html

安装:

```python
conda install pyquery
```



### 示例文档

下面是本文档中作为示例使用的 HTML 文档:

```HTML
html_doc = """
<html>
<head>
    <title>The Dormouse's story</title>
</head>
<body>
    <p class="title"><b>The Dormouse's story</b></p>
    <p class="story">Once upon a time there were three little sisters; and their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>

    <p class="story">...</p>
"""
```



## PyQuery 对象

> 有关 PyQuery API 的完整信息，请参考:
>
> - [`pyquery`](https://pyquery.readthedocs.io/en/stable/api.html#module-pyquery.pyquery) – PyQuery complete API
> - https://api.jquery.com/

### 概览

PyQuery 类继承自 list，PyQuery 实例是由 xml 解析器的元素(`etree._Element`)对象构成的列表(元素集):

```python
from pyquery import PyQuery
# html_doc是前文给出的示例文档
d_html = PyQuery(html_doc,parser='html')
type(d_html)
#> pyquery.pyquery.PyQuery

# 注意对比repr和str的输出效果
repr(d_html)
#> '[<span>]'
str(d_html)
#> '<html>\n<head>\n    <title>The Dormouse\'s story</title>\n</head>\n<body>\n    <p class="title"><b>The Dormouse\'s story</b></p>\n    <p class="story">Once upon a time there were three little sisters; and their names were\n        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,\n        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and\n        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;\n        and they lived at the bottom of a well.</p>\n\n    <p class="story">...</p>\n</body></html>'

a = d_html('a') # 选择器查询结果也是PyQuery对象
type(a)
#> pyquery.pyquery.PyQuery
repr(a)
#> '[<a#link1.sister>, <a#link2.sister>, <a#link3.sister>]'
str(a)
#> '<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,\n<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and\n<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;\n'

for i in a: # a是包含etree._Element对象的列表
    print(f"{type(i)}:{i.xpath('@href')}")
'''Out:
<class 'lxml.html.HtmlElement'>:['http://example.com/elsie']
<class 'lxml.html.HtmlElement'>:['http://example.com/lacie']
<class 'lxml.html.HtmlElement'>:['http://example.com/tillie']
'''
```

### 输出

`PyQuery.__repr__()` 会以列表形式描述 PyQuery 实例中的元素:

```python
    def __repr__(self):
        r = []
        try:
            for el in self:
                c = el.get('class')
                c = c and '.' + '.'.join(c.split(' ')) or ''
                id = el.get('id')
                id = id and '#' + id or ''
                r.append('<%s%s%s>' % (el.tag, id, c))
            return '[' + (', '.join(r)) + ']'
        except AttributeError:
            if PY3k:
                return list.__repr__(self)
            else:
                for el in self:
                    if isinstance(el, text_type):
                        r.append(el.encode('utf-8'))
                    else:
                        r.append(el)
                return repr(r)
```

`PyQuery.__str__()` 会将 PyQuery 实例中各个 `etree._Element` 元素中的内容整合到一个字符串中:

```python
def __str__(self):
    """xml representation of current nodes::

            >>> xml = PyQuery(
            ...   '<script><![[CDATA[ ]></script>', parser='html_fragments')
            >>> print(str(xml))
            <script>&lt;![[CDATA[ ]&gt;</script>

        """
    encoding = str if PY3k else None
    return ''.join([etree.tostring(e, encoding=encoding) for e in self])
```



### 构造函数

> 参考:
>
> - <https://pyquery.readthedocs.io/en/latest/index.html>
> - <https://pyquery.readthedocs.io/en/latest/scrap.html#scraping>
> - 源代码

🛠class pyquery.pyquery.PyQuery(\*args, \*\*kwargs)

PyQuery 类的构造函数 `PyQuery(*args, **kwargs)` 可以从字符串、`bytes` 对象、lxml 文档、文件和 url 中加载 xml 文档:

```python
>>> from pyquery import PyQuery as pq
>>> from lxml import etree
>>> import urllib
>>> d = pq("<html></html>")
>>> d = pq(etree.fromstring("<html></html>"))
>>> d = pq(url=your_url)
>>> d = pq(url=your_url,
...        opener=lambda url, **kw: urlopen(url).read())
>>> d = pq(filename=path_to_html_file) # 需使用关键字参数
```

在使用 xml 解析器时，建议使用 `bytes` 类型的文本，详见笔记﹝lxml.etree.md﹞->Python Unicode 字符串

#### bytes 数据和编码问题

使用 xml 解析器解析 bytes 数据时，通常情况下我们应避免在将 XML/HTML 数据传递到解析器之前，将其转换为 Unicode (这样做既慢又容易出错，虽然可以避免编码问题)。也就是说，被解析的文本最好是 `bytes` 类型，通常情况下解析器会根据 HTML  `mate` 标记来识别编码方式。当我们需要将 `bytes` 类型的数据解码为 Unicode 字符串(或转换为其它编码方式的 `bytes` 字符串)时，便会以 `mate` 标记给出的编码方案为准。

如果 xml 文档中声明了编码方案( 如，`<meta charset="gb2312">`)，则会使用此编码方案来处理 `bytes` 对象。`.encode` 字段与能否成功解码并没有必然联系。如果缺少 HTML `mate` 标记，则会默认采用  `ascii` 编码方式。此时可以创建 `HTMLParser` (或 `XMLParser`) 实例，并在构造函数中传入所需的编码方案。

详见笔记﹝lxml.etree.md﹞->Python Unicode 字符串

```python
from pyquery import PyQuery as pq
html_unicode1 = """
<html><head>
<meta charset="gb2312">
<title>鲸鱼</title>
</head>
"""
html_gb2312 = html_unicode1.encode('gb2312') # 将unicode字符串编码为gb2312字节码
doc = pq(html_gb2312)
print(doc('title')) #> <title>鲸鱼</title>
print(doc.encoding) #> gb2312

html_unicode2 = """
<html><head>
<title>鲸鱼</title>
</head>
"""
html_gb2312 = html_unicode2.encode('gb2312')
doc = pq(html_gb2312)
print(doc('title')) #> <title>¾¨Óã</title>
print(doc.encoding) #> UTF-8


html_utf8 = html_unicode2.encode('utf-8')
doc = pq(html_utf8)
print(doc('title')) #> <title>é²¸é±¼</title>
print(doc.encoding) #> UTF-8

# 如果在 bytes 包含 BOM 信息，也可以处理
html_utf_8_sig = html_unicode2.encode('utf_8_sig') 
doc = pq(html_utf_8_sig)
print(doc('title')) #> <title>鲸鱼</title>
print(doc.encoding) #> UTF-8
```

从 url 中加载 xml 文档时，由请求库对收到的内容进行解码，返回 Unicode 字符串。最好还是自己先使用请求库获取内容，并把内容解码为 Unicode 字符串后，再传递给构造函数 `PyQuery()`



#### `*args`

`*args` 参数支持以下几种使用方法:

- 可将 url 和 data 用作 `*args` 参数，详见 `PyQuery.__init__` 的源代码。使用示例:

  ```python
  from pyquery import PyQuery as pq
  # 默认采用get请求
  doc1 = pq('https://httpbin.org/get')
  print(doc1)
  '''Out:
  <p>{
    "args": {},
    --snip--
  </p>
  '''
  # 可以为请求方法添加参数
  payload = {'key1': 'value1', 'key2': 'value2'}
  doc2 = pq('https://httpbin.org/get', payload)
  print(doc2)
  '''Out:
  <p>{
    "args": {
      "key1": "value1",
      "key2": "value2"
    },
    --snip--
  }
  </p>
  '''
  # 可手动设置请求类型
  doc3 = pq('https://httpbin.org/post', payload, method='post')
  print(doc3)
  '''Out:
  <p>{
    "args": {},
    "data": "",
    "files": {},
    "form": {
      "key1": "value1",
      "key2": "value2"
    },
    --snip--
  </p>
  '''
  ```

- 可将 selector 和/或 context (可以是文本, PyQuery 对象, list 对象, etree._Element 对象) 用作 `*args` 参数，详见 `PyQuery.__init__` 的源代码。使用示例:

  ```python
  from pyquery import PyQuery as pq
  # 仅使用context(html_doc是示例文档)
  doc1 = pq(html_doc)
  print(doc1)
  '''Out:
  <html>
  <head>
      <title>The Dormouse's story</title>
  </head>
  <body>
      <p class="title"><b>The Dormouse's story</b></p>
      <p class="story">Once upon a time there were three little sisters; and their names were
          <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
          <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
          <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
          and they lived at the bottom of a well.</p>
  
      <p class="story">...</p>
  </body></html>
  '''
  # 同时使用selector和context
  doc2 = pq('#link1', html_doc)
  print(doc2)
  '''Out:
  <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
  '''
  ```

#### `**kwargs`

`PyQuery(*args, **kwargs)` 支持通过 `**kwargs` 自定义如下内容:

- `parser` 用于设置 XML/HTML 文档的解析器
- `url` 用于设置 url 连接
- `data` 设置 GET 请求和 POST 请求的数据
- `parent` 似乎是用于设置父节点，目前不清楚具体效果
- `css_translator` 似乎是用于设置 css 翻译器，目前不清楚具体效果
- `namespaces` 用于为 XML 设置命名空间，目前不清楚具体效果
- `filename` 用于指定 XML/HTML 文件，
- `opener` 设置用于请求 url 的工具，比如 `requests`

剩余的 `**kwargs` 会被传递给 `opener` 使用，例如:

```python
# headers会被传递给requests使用
>>> pq(your_url, headers={'user-agent': 'pyquery'})
[<html>]
# method和verify会被传递给requests使用
>>> pq(your_url, {'q': 'foo'}, method='post', verify=True)
[<html>]
```



#### 解析器的选择

> 参考: <https://pyquery.readthedocs.io/en/stable/tips.html#using-different-parsers>

建议在构造函数 `PyQuery()` 中手动设置解析器。🧀

默认情况下，PyQuery 会优先使用 lxml 的 xml 解析器进行解析。如果 xml 解析器解析失败，才会尝试使用 lxml.html 的 html 解析器进行解析。在解析 xhtml 页面时，xml 解析器有时出现问题，虽然解析器不会抛出异常，但由解析器提供的树将不可用。

构造函数 `PyQuery()` 在解析文档时，解析库的选择遵循以下规则(详见源代码):

- 如果没有在 `**kwargs` 中提供 `parser` 参数，则会先使用 `lxml.etree` 进行解析，如果失败则会使用 `lxml.html` 进行解析
- 还可通过 `**kwargs` 的 `parser` 参数手动设置解析器，`parser` 的可选实参值如下:
  - `'xml'` - 对应 `lxml.etree`
  - `'html'` - 对应 `lxml.html`
  - `'html5'` - 对应 `lxml.html.html5parser`
  - `'soup'` - 对应 `lxml.html.soupparser`
  - `'html_fragments'` - 对应 `lxml.html.fragments_fromstring`

```python
>>> pq('<html><body><p>toto</p></body></html>', parser='xml')
[<html>]
>>> pq('<html><body><p>toto</p></body></html>', parser='html')
[<html>]
>>> pq('<html><body><p>toto</p></body></html>', parser='html_fragments')
[<p>]
```



#### 请求库的选择

构造函数 `PyQuery()` 从 url 中加载 html 文档时，请求库的选择遵循以下规则(详见源代码):

- 默认情况下，PyQuery 会使用 urllib 库，此时可使用与 urllib 相关的请求参数。
- 如果安装了 [requests](http://docs.python-requests.org/en/latest/) 库，则会使用 requests 库，此时可使用与 requests 库相关的请求参数。
- 还可通过 `**kwargs` 的 `opener` 参数手动设置请求工具，比如 `requests`

```python
>>> pq(your_url, headers={'user-agent': 'pyquery'})
[<html>]

>>> pq(your_url, {'q': 'foo'}, method='post', verify=True)
[<html>]
```



#### 超时

> 参考: <https://pyquery.readthedocs.io/en/latest/scrap.html#timeout>

超时的默认时长是 60 秒，如果需要修改超时时长可通过 `**kwargs` 向 urllib 或 requests 传递相应的关键字参数。



#### 会话

> 参考: <https://pyquery.readthedocs.io/en/latest/scrap.html#session>

> When using the requests library you can instantiate a Session object which keeps state between http calls (for example - to keep cookies). You can set the session parameter to use this session object.

在使用 requests 时，你可以实例化一个 Session 对象，以便在 htpp 调用之间保持状态(例如，保留 cookies)。

我看了看源代码，似乎不能直接向构造函数 `PyQuery()` 传递 Session 对象。我们需要先创建一个 Session 对象，然后通过此 Session 对象来请求数据，再使用 `PyQuery()` 来加载这些数据，类似于:

```python
import requests
from pyquery import PyQuery as pq
s = requests.Session()

s.get('http://httpbin.org/cookies/set/sessioncookie/123456789') # 设置cookies
r = s.get("http://httpbin.org/cookies")

print(r.text)
#> '{"cookies": {"sessioncookie": "123456789"}}'
doc = pq(r.text)
print(doc)
'''Out:
<p>{
  "cookies": {
    "sessioncookie": "123456789"
  }
}
</p>
'''
```





## jQuery vs. PyQuery

> 参考:
>
> - jQuery 教程:
>   - <https://www.runoob.com/jquery/jquery-tutorial.html>
>   - <http://www.w3school.com.cn/jquery/index.asp>
> - jQuery API: <https://api.jquery.com/>
> - jQuery Home: <http://jquery.com/>
> - jQuery Learning Center: <https://learn.jquery.com/>

### 基础语法

> 参考:
>
> - [pyquery: a jquery-like library for python](https://pyquery.readthedocs.io/en/stable/index.html)
> - https://www.runoob.com/jquery/jquery-syntax.html
> - http://www.w3school.com.cn/jquery/jquery_syntax.asp

jQuery 可用于查询(*query*) HTML 元素，并对 HTML 元素进行操作(*action*)，基础语法是 `$(selector).action()`:

- `$` 是 jQuery 的别名 - The jQuery library exposes its methods and properties via two properties of the `window` object called `jQuery` and `$`. `$` is simply an alias for `jQuery` and it's often employed because it's shorter and faster to write.
- `(selector)` 用于查询 HTML 元素
- `action()` 用于对元素执行操作。

Note: jQuery 的选择器是 CSS 1-3，XPath 的结合物。jQuery 提取这二种查询语言最好的部分，融合后创造出了最终的 jQuery 表达式查询语言。实例展示:

```javascript
$(this).hide() # 隐藏当前元素
$("p").hide() # 隐藏所有 <p> 元素
$("p.test").hide() # 隐藏所有 class="test" 的 <p> 元素
$("#test").hide() # 隐藏所有 id="test" 的元素
```

🐍PyQuery 实例相当于 jQuery 中的 `$`，选择器 `PyQuery(selector)` 的返回值也是 `PyQuery` 对象。例如:

```python
from pyquery import PyQuery as pq
# html_doc是前文给出的示例文档
d_html = pq(html_doc, parser='html')
print(type(d_html))
#> <class 'pyquery.pyquery.PyQuery'>
print(repr(d_html))
#> [<html>]
print(d_html)
"""Out:
<html>
<head>
    <title>The Dormouse's story</title>
</head>
<body>
 --snip--
</body></html>
"""
```

上面这段代码中的 `d_html` 相当于 jQuery 中的 `$`。我们可以通过 `$(selector).action()` 来查询和操作 HTML 元素。与此类似，我们也可以通过 `d_html(selector).action()` 来查询和操作 HTML 元素，查询结果仍然是 `PyQuery` 对象:

```python
from pyquery import PyQuery as pq
# html_doc是前文给出的示例文档
d_html = pq(html_doc, parser='html')
print(repr(d_html('#link1')))  # 选择id为"link1"的元素
#> [<a#link1.sister>]
print(d_html('#link1'))
#> <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
link = d_html('#link1')
print(type(link)) # 查询结果是PyQuery对象
#> <class 'pyquery.pyquery.PyQuery'>

print(d_html('#link1').html())  # 获取子节点的HTML表示
#> Elsie
d_html('#link1').html("orca-j35")  # 设置子节点的HTML表示
print(d_html('#link1').html())
#> orca-j35

print(d_html('#link1').text())  # 获取子节点的文本表示
#> orca-j35
d_html('#link1').text('hello')  # 设置子节点的文本表示
print(d_html('#link1').text())
#> hello
```



### 选择器

jQuery 选择器(`$(selector)`)用于查询 HTML 元素，选择器基于已经存在的 CSS 选择器，因此可依据 id、class、属性和属性值等条件来查询 HTML 元素。除了已有的 CSS 选择器，jQuery 还提供了一些自定义选择器。

如果需要进一步了解选择器的使用方法，可从以下三个部分入手:

- jQuery 选择器，可参考:
  - <https://api.jquery.com/category/selectors/> 🧀
  - http://www.w3school.com.cn/jquery/jquery_selectors.asp
  - https://www.runoob.com/jquery/jquery-selectors.html
  - http://www.w3school.com.cn/jquery/jquery_ref_selectors.asp
  - https://www.runoob.com/jquery/jquery-ref-selectors.html 🧀
  - https://www.runoob.com/try/trysel.php 🧀
- CSS 选择器，可参考:
  - <http://www.w3school.com.cn/cssref/css_selectors.asp>
  - <http://www.w3school.com.cn/css/css_selector_type.asp>
  - <https://www.runoob.com/cssref/css-selectors.html>
- XPath，可参考笔记 ﹝XPath.md﹞

选择器实例展示:

| 语法                     | 描述                                                        |
| :----------------------- | :---------------------------------------------------------- |
| $("*")                   | 选取所有元素                                                |
| $(this)                  | 选取当前 HTML 元素                                          |
| $("p")                   | 选取所有 `<p>` 元素                                         |
| $("p.intro")             | 选取 class 为 intro 的 `<p>` 元素                           |
| $(".intro")              | 选取所有 class 为 intro 的元素                              |
| $("p:first")             | 选取第一个 `<p>` 元素                                       |
| $("ul li:first")         | 选取第一个 `<ul>` 元素的第一个 `<li>` 元素                  |
| $("ul li:first-child")   | 选取每个 `<ul>` 元素的第一个 `<li>` 元素                    |
| $("[href]")              | 选取带有 href 属性的元素                                    |
| $("a[target='_blank']")  | 选取所有 target 属性值等于 "_blank" 的 `<a>` 元素           |
| $("a[target!='_blank']") | 选取所有 target 属性值不等于 "_blank" 的 `<a>` 元素         |
| $(":button")             | 选取所有 type="button" 的 `<input>` 元素 和 `<button>` 元素 |
| $("tr:even")             | 选取偶数位置的 `<tr>` 元素                                  |
| $("tr:odd")              | 选取奇数位置的 `<tr>` 元素                                  |



#### 元素选择器

"jQuery 元素选择器"基于元素名选取元素(CSS 选择器语法)，比如在页面中选取所有 `<p>` 元素:

```javascript
$("p")
```

🐍 PyQuery:

```python
html_doc = """
<html id='hello' class='hello'><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">...
</body></html>
"""
d = pq(html_doc)
print(d('p'))
'''Out:
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">...
</p>
'''
d('p'),type(d('p'))
#> ([<p.title>, <p.story>], pyquery.pyquery.PyQuery)
```



#### id 选择器 `#`

"jQuery id 选择器"基于元素的 id 属性来选取元素(CSS 选择器语法):

```javascript
$("#test")
```

🐍 PyQuery:

```python
from pyquery import PyQuery as pq
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
d = pq(html_doc)
print(d('#link2'))
#> <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
d('#link2'),type(d('#link2'))
#> ([<a#link2.sister>], pyquery.pyquery.PyQuery)
```

如果需要选择带点号 `.` 的 id，则需要对点号进行转义:

```python
>>> d = pq('<p id="hello.you"><a/></p><p id="test"><a/></p>')
>>> d('#hello\.you')
[<p#hello.you>]
```



#### 类选择器 `.`

"jQuery 类选择器"基于元素的 class 属性来选取元素(CSS 选择器语法):

```javascript
$(".test")
```

🐍 PyQuery:

```python
html_doc = """
<html id='hello' class='hello'><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">...
</body></html>
"""
d = pq(html_doc)
print(d('.title'))
#> <p class="title"><b>The Dormouse's story</b></p>
d('.title'),type(d('.title'))
#> ([<p.title>], pyquery.pyquery.PyQuery)
```



#### 属性选择器 `[]`

"jQuery 属性选择器"基于元素的属性来选取元素(有点像 XPath 中的谓语):

```javascript
$("[href]") # 选取所有带有 href 属性的元素。
$("[href='#']") # 选取所有带有 href 值等于 "#" 的元素。
$("[href!='#']") # 选取所有带有 href 值不等于 "#" 的元素。
$("[href$='.jpg']") # 选取所有 href 值以 ".jpg" 结尾的元素。
```

🐍 PyQuery:

```python
d = pq("<option id='A' value='1'><option id='B' value='2'>")
d('option[value="1"]')
#> [<option#A>]
```



#### 伪类选择器 `:`

除了可使用 CSS 标准中的伪类之外，还可以使用一些在 jQuery 中可以用，但不属于 CSS 标准的伪类，例如: `:first`, `:last`, `:even`, `:odd`, `:eq`, `:lt`, `:gt`, `:checked`, `:selected`, `:file`:

```
>>> d('p:first')
[<p#hello.hello>]
```

有关伪类(*pseudo* *classes*)的详细信息请交叉参考:

- [Using pseudo classes](https://pyquery.readthedocs.io/en/stable/pseudo_classes.html) - PyQuery 官方文档，似乎存在一些错误
- https://api.jquery.com/category/selectors/

CSS 标准中的伪类:

- https://www.runoob.com/css/css-pseudo-classes.html
- http://www.w3school.com.cn/css/css_pseudo_classes.asp
- http://www.w3school.com.cn/css/css_pseudo_elements.asp

#### 组合选择器

每个选择器并不是独立存在的，它们可以被组合使用，从而表示复杂查询条件:

```python
from pyquery import PyQuery
html_doc = '''
<ul>
  <li id='1'>list item 1</li>
  <li id='2'>list item 2</li>
  <li id='3' class="third-item">list item 3</li>
  <li id='4'>list item 4</li>
  <li id='5'>list item 5</li>
</ul>
'''
doc = PyQuery(html_doc)
a = doc("li.third-item") # 表示查询class为third-item的li元素
print(repr(a))
print(repr(a.siblings()))
print(repr(a.siblings('#5')))
```

输出:

```
[<li#3.third-item>]
[<li#2>, <li#1>, <li#4>, <li#5>]
[<li#5>]
```



#### 嵌套选择器

可使用由空格分隔的一组选择器来表示层层递进的嵌套选择:

```python
from pyquery import PyQuery as pq
html_doc = """
<html>
<head>
    <title>The Dormouse's story</title>
</head>
<body>
    <div id="container">
        <p class="title"><b>The Dormouse's story</b></p>
        <p class="title1"><b>The Dormouse's story</b></p>
        <p class="story">Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
            and they lived at the bottom of a well.
        </p>
    </div>
"""
doc = pq(html_doc)
a = doc('#container .story a')
print(repr(a))
print(type(a))
```

选择器 `'#container .story a'` 表示先选取 id 为 `container` 的节点，然后在该节点内部选取 class 为 `story` 的节点，并在 `class=story` 的节点内部选取所有 `a` 元素节点。输出如下:

```
[<a#link1.sister>, <a#link2.sister>, <a#link3.sister>]
<class 'pyquery.pyquery.PyQuery'>
```

在选择器组中用于分隔每个选择器的空格是必须的。

### jQuery 选择器概览

> 参考:
>
> - https://www.runoob.com/jquery/jquery-ref-selectors.html
> - http://www.w3school.com.cn/jquery/jquery_ref_selectors.asp
>
> 推荐使用"jQuery 选择器检测器"来了解不同的选择器:
>
> - https://www.runoob.com/try/trysel.php



| 选择器                                                       | 实例                          | 选取                                                         |
| :----------------------------------------------------------- | :---------------------------- | :----------------------------------------------------------- |
| [*](https://www.runoob.com/jquery/jq-sel-all.html)           | $("*")                        | 所有元素                                                     |
| [#*id*](https://www.runoob.com/jquery/jq-sel-id.html)        | $("#lastname")                | id="lastname" 的元素                                         |
| [.*class*](https://www.runoob.com/jquery/jq-sel-class.html)  | $(".intro")                   | class="intro" 的所有元素                                     |
| [.*class,*.*class*](https://www.runoob.com/jquery/sel-multiple-classes.html) | $(".intro,.demo")             | class 为 "intro" 或 "demo" 的所有元素                        |
| [*element*](https://www.runoob.com/jquery/jq-sel-element.html) | $("p")                        | 所有 `<p>` 元素                                              |
| [*el1*,*el2*,*el3*](https://www.runoob.com/jquery/sel-multiple-elements.html) | $("h1,div,p")                 | 所有 `<h1>`、`<div>` 和 `<p>` 元素                           |
|                                                              |                               |                                                              |
| [:first](https://www.runoob.com/jquery/sel-first.html)       | $("p:first")                  | 第一个 `<p>` 元素                                            |
| [:last](https://www.runoob.com/jquery/sel-last.html)         | $("p:last")                   | 最后一个 `<p>` 元素                                          |
| [:even](https://www.runoob.com/jquery/sel-even.html)         | $("tr:even")                  | 所有偶数 `<tr>` 元素，索引值从 0 开始，第一个元素是偶数 (0)，第二个元素是奇数 (1)，以此类推。 |
| [:odd](https://www.runoob.com/jquery/sel-odd.html)           | $("tr:odd")                   | 所有奇数 <tr> 元素，索引值从 0 开始，第一个元素是偶数 (0)，第二个元素是奇数 (1)，以此类推。 |
|                                                              |                               |                                                              |
| [:first-child](https://www.runoob.com/jquery/jq-sel-firstchild.html) | $("p:first-child")            | 属于其父元素的第一个子元素的所有 `<p>` 元素                  |
| [:first-of-type](https://www.runoob.com/jquery/sel-firstoftype.html) | $("p:first-of-type")          | 属于其父元素的第一个 `<p>` 元素的所有 `<p>` 元素             |
| [:last-child](https://www.runoob.com/jquery/sel-lastchild.html) | $("p:last-child")             | 属于其父元素的最后一个子元素的所有 `<p>` 元素                |
| [:last-of-type](https://www.runoob.com/jquery/sel-lastoftype.html) | $("p:last-of-type")           | 属于其父元素的最后一个 `<p>` 元素的所有 `<p>` 元素           |
| [:nth-child(*n*)](https://www.runoob.com/jquery/sel-nthchild.html) | $("p:nth-child(2)")           | 属于其父元素的第二个子元素的所有 `<p>` 元素                  |
| [:nth-last-child(*n*)](https://www.runoob.com/jquery/sel-nthlastchild.html) | $("p:nth-last-child(2)")      | 属于其父元素的第二个子元素的所有 `<p>` 元素，从最后一个子元素开始计数 |
| [:nth-of-type(*n*)](https://www.runoob.com/jquery/sel-nthoftype.html) | $("p:nth-of-type(2)")         | 属于其父元素的第二个 `<p>` 元素的所有 `<p>` 元素             |
| [:nth-last-of-type(*n*)](https://www.runoob.com/jquery/sel-nthlastoftype.html) | $("p:nth-last-of-type(2)")    | 属于其父元素的第二个 `<p>` 元素的所有 `<p>` 元素，从最后一个子元素开始计数 |
| [:only-child](https://www.runoob.com/jquery/sel-onlychild.html) | $("p:only-child")             | 属于其父元素的唯一子元素的所有 `<p>` 元素                    |
| [:only-of-type](https://www.runoob.com/jquery/sel-onlyoftype.html) | $("p:only-of-type")           | 属于其父元素的特定类型的唯一子元素的所有 `<p>` 元素          |
|                                                              |                               |                                                              |
| [parent > child](https://www.runoob.com/jquery/sel-parent-child.html) | $("div > p")                  | `<div>` 元素的直接子元素的所有 `<p>` 元素                    |
| [parent descendant](https://www.runoob.com/jquery/sel-parent-descendant.html) | $("div p")                    | `<div>` 元素的后代的所有 `<p>` 元素                          |
| [element + next](https://www.runoob.com/jquery/sel-previous-next.html) | $("div + p")                  | 每个 `<div>` 元素相邻的下一个 `<p>` 元素                     |
| [element ~ siblings](https://www.runoob.com/jquery/sel-previous-siblings.html) | $("div ~ p")                  | `<div>` 元素同级的所有 `<p>` 元素                            |
|                                                              |                               |                                                              |
| [:eq(*index*)](https://www.runoob.com/jquery/sel-eq.html)    | $("ul li:eq(3)")              | 列表中的第四个元素（index 值从 0 开始）                      |
| [:gt(*no*)](https://www.runoob.com/jquery/sel-gt.html)       | $("ul li:gt(3)")              | 列举 index 大于 3 的元素                                     |
| [:lt(*no*)](https://www.runoob.com/jquery/sel-lt.html)       | $("ul li:lt(3)")              | 列举 index 小于 3 的元素                                     |
| [:not(*selector*)](https://www.runoob.com/jquery/jq-sel-not.html) | $("input:not(:empty)")        | 所有不为空的输入元素                                         |
|                                                              |                               |                                                              |
| [:header](https://www.runoob.com/jquery/sel-header.html)     | $(":header")                  | 所有标题元素 `<h1>`, `<h2>` ...                              |
| [:animated](https://www.runoob.com/jquery/sel-animated.html) | $(":animated")                | 所有动画元素                                                 |
| [:focus](https://www.runoob.com/jquery/jq-sel-focus.html)    | $(":focus")                   | 当前具有焦点的元素                                           |
| [:contains(*text*)](https://www.runoob.com/jquery/sel-contains.html) | $(":contains('Hello')")       | 所有包含文本 "Hello" 的元素                                  |
| [:has(*selector*)](https://www.runoob.com/jquery/sel-has.html) | $("div:has(p)")               | 所有包含有 `<p>` 元素在其内的 `<div>` 元素                   |
| [:empty](https://www.runoob.com/jquery/jq-sel-empty.html)    | $(":empty")                   | 所有空元素                                                   |
| [:parent](https://www.runoob.com/jquery/sel-parent.html)     | $(":parent")                  | 匹配所有含有子元素或者文本的父元素。                         |
| [:hidden](https://www.runoob.com/jquery/sel-hidden.html)     | $("p:hidden")                 | 所有隐藏的 `<p>` 元素                                        |
| [:visible](https://www.runoob.com/jquery/sel-visible.html)   | $("table:visible")            | 所有可见的表格                                               |
| [:root](https://www.runoob.com/jquery/jq-sel-root.html)      | $(":root")                    | 文档的根元素                                                 |
| [:lang(*language*)](https://www.runoob.com/jquery/jq-sel-lang.html) | $("p:lang(de)")               | 所有 lang 属性值为 "de" 的 `<p>` 元素                        |
|                                                              |                               |                                                              |
| [[*attribute*\]](https://www.runoob.com/jquery/jq-sel-attribute.html) | $("[href]")                   | 所有带有 href 属性的元素                                     |
| [[*attribute*=*value*\]](https://www.runoob.com/jquery/sel-attribute-equal-value.html) | $("[href='default.htm']")     | 所有带有 href 属性且值等于 "default.htm" 的元素              |
| [[*attribute*!=*value*\]](https://www.runoob.com/jquery/sel-attribute-notequal-value.html) | $("[href!='default.htm']")    | 所有带有 href 属性且值不等于 "default.htm" 的元素            |
| [[*attribute*$=*value*\]](https://www.runoob.com/jquery/sel-attribute-end-value.html) | $("[href$='.jpg']")           | 所有带有 href 属性且值以 ".jpg" 结尾的元素                   |
| [[*attribute*\|=*value*\]](https://www.runoob.com/jquery/sel-attribute-prefix-value.html) | $("[title\|='Tomorrow']")     | 所有带有 title 属性且值等于 'Tomorrow' 或者以 'Tomorrow' 后跟连接符作为开头的字符串 |
| [[*attribute*^=*value*\]](https://www.runoob.com/jquery/sel-attribute-beginning-value.html) | $("[title^='Tom']")           | 所有带有 title 属性且值以 "Tom" 开头的元素                   |
| [[*attribute*~=*value*\]](https://www.runoob.com/jquery/sel-attribute-contains-value.html) | $("[title~='hello']")         | 所有带有 title 属性且值包含单词 "hello" 的元素               |
| [[*attribute**=*value*\]](https://www.runoob.com/jquery/sel-attribute-contains-string-value.html) | $("[title*='hello']")         | 所有带有 title 属性且值包含字符串 "hello" 的元素             |
| [[*name*=*value*\][*name2*=*value2*]](https://www.runoob.com/jquery/sel-multipleattribute-equal-value.html) | $( "input[id][name$='man']" ) | 带有 id 属性，并且 name 属性以 man 结尾的输入框              |
|                                                              |                               |                                                              |
| [:input](https://www.runoob.com/jquery/sel-input.html)       | $(":input")                   | 所有 input 元素                                              |
| [:text](https://www.runoob.com/jquery/sel-input-text.html)   | $(":text")                    | 所有带有 type="text" 的 input 元素                           |
| [:password](https://www.runoob.com/jquery/sel-input-password.html) | $(":password")                | 所有带有 type="password" 的 input 元素                       |
| [:radio](https://www.runoob.com/jquery/sel-input-radio.html) | $(":radio")                   | 所有带有 type="radio" 的 input 元素                          |
| [:checkbox](https://www.runoob.com/jquery/sel-input-checkbox.html) | $(":checkbox")                | 所有带有 type="checkbox" 的 input 元素                       |
| [:submit](https://www.runoob.com/jquery/sel-input-submit.html) | $(":submit")                  | 所有带有 type="submit" 的 input 元素                         |
| [:reset](https://www.runoob.com/jquery/sel-input-reset.html) | $(":reset")                   | 所有带有 type="reset" 的 input 元素                          |
| [:button](https://www.runoob.com/jquery/sel-input-button.html) | $(":button")                  | 所有带有 type="button" 的 input 元素                         |
| [:image](https://www.runoob.com/jquery/sel-input-image.html) | $(":image")                   | 所有带有 type="image" 的 input 元素                          |
| [:file](https://www.runoob.com/jquery/sel-input-file.html)   | $(":file")                    | 所有带有 type="file" 的 input 元素                           |
|                                                              |                               |                                                              |
| [:enabled](https://www.runoob.com/jquery/sel-input-enabled.html) | $(":enabled")                 | 所有启用的元素                                               |
| [:disabled](https://www.runoob.com/jquery/sel-input-disabled.html) | $(":disabled")                | 所有禁用的元素                                               |
| [:selected](https://www.runoob.com/jquery/sel-input-selected.html) | $(":selected")                | 所有选定的下拉列表元素                                       |
| [:checked](https://www.runoob.com/jquery/sel-input-checked.html) | $(":checked")                 | 所有选中的复选框选项                                         |
| .selector                                                    | $(selector).selector          | 在jQuery 1.7中已经不被赞成使用。返回传给jQuery()的原始选择器 |
| [:target](https://www.runoob.com/jquery/jq-sel-target.html)  | $( "p:target" )               | 选择器将选中ID和URI中一个格式化的标识符相匹配的<p>元素       |

## 操作 PyQuery 对象

> 参考: <https://pyquery.readthedocs.io/en/stable/manipulating.html>
>
> 如果需要了解更多操作 PyQuery 对象的方法，可阅读:
>
> - https://api.jquery.com/category/manipulation/

You can also add content to the end of tags:

```python
>>> from pyquery import PyQuery as pq
>>> d = pq('<p class="hello" id="hello">you know Python rocks</p>')
>>> d('p').append(' check out <a href="http://reddit.com/r/python"><span>reddit</span></a>')
[<p#hello.hello>]
>>> print(d)
<p class="hello" id="hello">you know Python rocks check out <a href="http://reddit.com/r/python"><span>reddit</span></a></p>
```

Or to the beginning:

```python
>>> p = d('p')
>>> p.prepend('check out <a href="http://reddit.com/r/python">reddit</a>')
[<p#hello.hello>]
>>> print(p)
<p class="hello" id="hello">check out <a href="http://reddit.com/r/python">reddit</a>you know Python rocks</p>
>>> print(p.html())
check out <a href="http://reddit.com/r/python">reddit</a>you know Python rocks
```

Prepend or append an element into an other:

```python
>>> d = pq('<html><body><div id="test"><a href="http://python.org">python</a> !</div></body></html>')
>>> p.prependTo(d('#test'))
[<p#hello.hello>]
>>> print(d('#test').html())
<p class="hello" ...
```

Insert an element after another:

```python
>>> p.insertAfter(d('#test'))
[<p#hello.hello>]
>>> print(d('#test').html())
<a href="http://python.org">python</a> !
```

Or before:

```python
>>> p.insertBefore(d('#test'))
[<p#hello.hello>]
>>> print(d('body').html())
<p class="hello" id="hello">...
```

Doing something for each elements:

```python
>>> p.each(lambda i, e: pq(e).addClass('hello2'))
[<p#hello.hello.hello2>]
```

Remove an element:

```python
>>> d = pq('<html><body><p id="id">Yeah!</p><p>python rocks !</p></div></html>')
>>> d.remove('p#id')
[<html>]
>>> d('p#id')
[]
```

Remove what’s inside the selection:

```python
>>> d('p').empty()
[<p>]
```

And you can get back the modified html:

```python
>>> print(d)
<html><body><p/></body></html>
```

You can generate html stuff:

```python
>>> from pyquery import PyQuery as pq
>>> print(pq('<div>Yeah !</div>').addClass('myclass') + pq('<b>cool</b>'))
<div class="myclass">Yeah !</div><b>cool</b>
```

Remove all namespaces:

```python
>>> d = pq('<foo xmlns="http://example.com/foo"></foo>')
>>> d
[<{http://example.com/foo}foo>]
>>> d.remove_namespaces()
[<foo>]
```

### .text()🔨

🔨`text(value=<NoDefault>, **kwargs)`

获取元素集中每个元素(包括子孙节点)的文本，并将这些文本组合到一起。如果传递了 value 参数，则重设元素集中每个元素的文本，并抹去这些元素的子节点。

> Description in api.jquery.com:
>
> - Get the combined text contents of each element in the set of matched elements, including their descendants, or set the text contents of the matched elements.
> - https://api.jquery.com/text/
>
> In PyQuery API:
>
> - Get or set the text representation of sub nodes.
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.text

Get the text value:

```python
>>> doc = PyQuery('<div><span>toto</span><span>tata</span></div>')
>>> print(doc.text())
tototata
>>> doc = PyQuery('''<div><span>toto</span>
...               <span>tata</span></div>''')
>>> print(doc.text())
toto tata
```

Set the text value:

```python
>>> doc = PyQuery('<div><span>toto</span><span>tata</span></div>')
>>> doc.text('Youhou !')
[<div>]
>>> print(doc) # 在设置文本的同时，子节点会被抹去
<div>Youhou !</div>
```



### .html()🔨

🔨`html(value=<NoDefault>, **kwargs)`

获取元素集中第一个元素的 HTML 内容。如果传递了 value 参数，则重设元素集中每个元素的 HTML 内容，并抹去这些元素的子节点。

> Description in api.jquery.com:
>
> - Get the HTML contents of the first element in the set of matched elements or set the HTML contents of every matched element.
> - https://api.jquery.com/html/
>
> In PyQuery API:
>
> - Get or set the html representation of sub nodes.
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.html

Get the text value:

```python
>>> d = PyQuery('<div><span>toto</span></div>')
>>> print(d.html())
<span>toto</span>
```

Extra args are passed to `lxml.etree.tostring`:

```python
>>> d = PyQuery('<div><span></span></div>')
>>> print(d.html())
<span/>
>>> print(d.html(method='html'))
<span></span>
```

Set the text value:

```python
>>> d.html('<span>Youhou !</span>')
[<div>]
>>> print(d)
<div><span>Youhou !</span></div>
```

### .empty()🔨

🔨empty()

从 DOM 中移除元素集中每个元素的所有子节点

> Description in api.jquery.com:
>
> - Remove all child nodes of the set of matched elements from the DOM.
> - https://api.jquery.com/empty/
>
> In PyQuery API:
>
> - remove nodes content
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.empty

```python
html_doc = '''
<div class="container">
  <div class="hello">Hello</div>
  <div class="hello">world</div>
  <div class="goodbye">Goodbye</div>
</div>
'''
doc = PyQuery(html_doc)
x = doc('.hello').empty()
print(doc)
```

输出:

```python
<div class="container">
  <div class="hello"/>
  <div class="hello"/>
  <div class="goodbye">Goodbye</div>
</div>
```



### .remove()🔨

🔨`remove(expr=<NoDefault>)`
如果未提供 expr 参数，则会从 DOM 中移除当前元素集；如果提供了 `expr` 参数，则会从元素集中的每个元素中移除 `expr` 选定的内容。

> Description in api.jquery.com:
>
> - Remove the set of matched elements from the DOM.
> - https://api.jquery.com/remove/
>
> In PyQuery API:
>
> - remove nodes
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.remove

```python
html_doc = '''
<div>
  <ul class="level-1">
    <li id='1'>list item 1</li>
  </ul>
  <ul class="level-2">
    <li id='2'>list item 2</li>
  </ul>
</di>'''
doc = PyQuery(html_doc)
print(repr(doc('ul')), end='\n-------\n')
doc('ul').remove('li')
print(doc, end='\n-------\n')
doc('ul').remove()
print(doc)
```

输出:

```
[<ul.level-1>, <ul.level-2>]
-------
<div>
  <ul class="level-1">

  </ul>
  <ul class="level-2">

  </ul>
</div>
-------
<div>


</div>
```

示例 - 假设需要提取字符串 `"Hello, World"`，如果直接使用 `text()` 方法，则会提取到 `<p>` 节点中的内容。需要先移除 `<p>` 节点，然后在调用 `text()`  方法。

```python
html = '''
<div class="wrap">
    Hello, World
    <p>This is a paragraph.</p>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
wrap = doc('.wrap').remove('p')
print(wrap.text())
#> Hello, World
```



### 改用绝对连接

> 参考: <https://pyquery.readthedocs.io/en/stable/tips.html#making-links-absolute>

🔨make_links_absolute(base_url=None)

将元素集中的所有相对连接改为绝对连接。

```python
from pyquery import PyQuery
d = PyQuery('https://cn.bing.com/', parser='html')
d('form').attr('action')
#> '/search'
d.base_url
#> 'https://cn.bing.com/'
d.make_links_absolute()
d('form').attr('action')
#> 'https://cn.bing.com/search'

html_doc = """
<html>
<head> 
<meta charset="utf-8"> 
<title></title> 
</head>
<body>

<form action="/search">
First name: <input type="text" name="FirstName" value="Mickey"><br>
Last name: <input type="text" name="LastName" value="Mouse"><br>
<input type="submit" value="提交">
</form>
<a href="/orca_j35.jpg">picture</a>

</body>
</html>
"""
d_html = PyQuery(html_doc,parser='html')
d_html('form').attr('action')
#> '/search'
d_html.make_links_absolute('https://cn.bing.com')
d_html('form').attr('action')
#> 'https://cn.bing.com/search'
d_html('a').attr('href')
#> 'https://cn.bing.com/orca_j35.jpg'
d_html.base_url
#> None
```



## 操作属性

> 参考: https://pyquery.readthedocs.io/en/stable/attributes.html
>
> 如果需要了解更多与属性相关的操作，可阅读:
>
> - https://api.jquery.com/category/attributes/

可以在属性选择器中使用属性来选择需要的元素:

```python
d = pq("<option id='A' value='1'><option id='B' value='2'>")
d('option[value="1"]')
#> [<option#A>]
```

### .attr()🔨

🔨attr(attributeName, [value])

获取元素集中第一个元素的 attributeName 属性的值，或为元素集中的每一个元素(不包含子节点)设置名为 attributeName 的属性。

> Description in api.jquery.com:
>
> - Get the value of an attribute for the first element in the set of matched elements or set one or more attributes for every matched element.
> - https://api.jquery.com/attr/#attr-attributeName-function
>
> In PyQuery API: 没有此条目

You can play with the attributes with the jquery API:

```python
>>> p = pq('<p id="hello" class="hello"></p>')('p')
>>> p.attr("id") # 获取属性
'hello'
>>> p.attr("id", "plop") # 设置属性
[<p#plop.hello>]
>>> p.attr("id", "hello")
[<p#hello.hello>]
```

Or in a more pythonic way:

```python
>>> p.attr.id = "plop" # 设置属性
>>> p.attr.id # 查看属性
'plop'
>>> p.attr["id"] = "ola" # 设置属性
>>> p.attr["id"] # 查看属性
'ola'
>>> p.attr(id='hello', class_='hello2') # 设置属性
[<p#hello.hello2>]
>>> p.attr.class_
'hello2'
>>> p.attr.class_ = 'hell
```

示例:

```python
html_doc = '''
<form>
<input type="radio" name="sex" value="male">Male<br>
<input type="radio" name="sex" value="female">Female
</form>
'''
doc = PyQuery(html_doc)
print(doc('input').attr('value')) # 只会获取第一个元素的value属性值
doc('input').attr('name', '??')
print(doc)
doc.attr('kk', '??')
print(doc)
```

输出:

```
male
<form>
<input type="radio" name="??" value="male"/>Male<br/>
<input type="radio" name="??" value="female"/>Female
</form>

<form kk="??">
<input type="radio" name="??" value="male"/>Male<br/>
<input type="radio" name="??" value="female"/>Female
</form>
```

如果想要获取元素集中每个元素的属性，则需要配合 `items()` 使用:

```python
html_doc = '''
<form>
<input type="radio" name="sex" value="male">Male<br>
<input type="radio" name="sex" value="female">Female
</form>
'''
doc = PyQuery(html_doc)
print([i.attr('value') for i in doc('input').items()])
#> ['male', 'female']
```



### .remove_attr()🔨

🔨remove_attr(name) - Alias for `removeAttr(name)`

从元素集的每个元素中移除指定元素

> Description in api.jquery.com:
>
> - Remove an attribute from each element in the set of matched elements.
> - https://api.jquery.com/removeAttr/
>
> In PyQuery API:
>
> - Remove an attribute
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.remove_attr

```python
html_doc = '''
<form>
<input type="radio" name="sex" value="male">Male<br>
<input type="radio" name="sex" value="female">Female
</form>
'''
doc = PyQuery(html_doc)
print(repr(doc('input')), end='\n\n')
doc('input').remove_attr('value')
print(doc)
```

输出:

```
[<input>, <input>]

<form>
<input type="radio" name="sex"/>Male<br/>
<input type="radio" name="sex"/>Female
</form>
```



### .val()🔨

🔨`val(*value=<NoDefault>*)`

获取元素集中第一个元素的 value 属性，或设置元素集中每个元素(不包含子节点)的 value 属性。

> Description in api.jquery.com:
>
> - Get the current value of the first element in the set of matched elements or set the value of every matched element.
> - https://api.jquery.com/val/
>
> In PyQuery API:
>
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.val



```python
html_doc = '''
<form>
<input type="radio" name="sex" value="male">Male<br>
<input type="radio" name="sex" value="female">Female
</form>
'''
doc = PyQuery(html_doc)
print(repr(doc('input')), end='\n\n')
print(doc('input').val(), end='\n\n')
doc('input').val('??')
print(doc)
doc.val('!!')
print(doc)
```

输出:

```
[<input>, <input>]

male

<form>
<input type="radio" name="sex" value="??"/>Male<br/>
<input type="radio" name="sex" value="??"/>Female
</form>

<form value="!!">
<input type="radio" name="sex" value="??"/>Male<br/>
<input type="radio" name="sex" value="??"/>Female
</form>
```



## 操作 CSS

> 参考: https://pyquery.readthedocs.io/en/stable/css.html
>
> 如果需要了解更多与 CSS 操作相关的方法，可以阅读:
>
> - https://api.jquery.com/category/css/

jQuery 拥有若干进行 CSS 操作的方法，比如下面这些:

- `addClass()` - 向被选元素添加一个或多个类
- `removeClass()` - 从被选元素删除一个或多个类
- `has_class()` - 测试是否包含某个 class
- `toggleClass()` - 对被选元素进行添加/删除类的切换操作
- `css()` - 设置或返回样式(*style*)属性

```javascript
# 把所有p元素的背景颜色更改为红色
$("p").css("background-color","red");
```

下面是一些使用 🐍PyQuery 进行 CSS 操作的示例:

You can play with css classes:

```python
>>> p = pq('<p id="hello" class="hello"></p>')('p')
>>> p.addClass("toto") # add_class()方法的别名，用于为class添加值
[<p#hello.hello.toto>]
>>> print(p)
<p id="hello" class="hello toto"/>
>>> p.toggleClass("titi toto") # 切换class的值
[<p#hello.hello.titi>]
>>> print(p)
<p id="hello" class="hello titi"/>
>>> p.removeClass("titi") # 移除class的值
[<p#hello.hello>]
```

Or the css style:

```python
>>> p = pq('<p id="hello" class="hello"></p>')('p')
>>> p.css("font-size", "15px")
[<p#hello.hello>]
>>> print(p.css("font-size", "15px"))
<p id="hello" class="hello" style="font-size: 15px"/>
>>> p.attr("style")
'font-size: 15px'
>>> p.css({"font-size": "17px"})
[<p#hello.hello>]
>>> p.attr("style")
'font-size: 17px'
```

Same thing the pythonic way (‘_’ characters are translated to ‘-‘):

```python
>>> p.css.font_size = "16px"
>>> p.attr.style
'font-size: 16px'
>>> p.css['font-size'] = "15px"
>>> p.attr.style
'font-size: 15px'
>>> p.css(font_size="16px")
[<p#hello.hello>]
>>> p.attr.style
'font-size: 16px'
>>> p.css = {"font-size": "17px"}
>>> p.attr.style
'font-size: 17px'
```

### .add_class()🔨

🔨add_class(value) - Alias for `addClass(value)`

> Description in api.jquery.com:
>
> - Adds the specified class(es) to each element in the set of matched elements.
> - https://api.jquery.com/addClass/
>
> In PyQuery API:
>
> - Add a css class to elements:
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.add_class

```python
>>> d = PyQuery('<div></div>')
>>> d.add_class('myclass')
[<div.myclass>]
>>> d.addClass('myclass')
[<div.myclass>]
```



### .remove_class()🔨

🔨remove_class(className) - Alias for `removeClass(className)`

从元素集的每个元素的 class 属性中移除 className

> Description in api.jquery.com:
>
> - Remove a single class, multiple classes, or all classes from each element in the set of matched elements.
> - https://api.jquery.com/removeClass/
>
> In PyQuery API:
>
> - Remove an attribute
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.remove_class

```python
html_doc = '''
<div class="level-1 level-2">
  <div class="level-1 level-2">
  </div>
</div>
'''
doc = PyQuery(html_doc)
doc.remove_class('level-2 level-1')
print(doc)
```

输出:

```
<div class="">
  <div class="level-1 level-2">
  </div>
</div>
```



## 遍历 PyQuery 对象

> 参考: 
>
> - <https://pyquery.readthedocs.io/en/latest/traversing.html>
> - [`pyquery`](https://pyquery.readthedocs.io/en/stable/api.html#module-pyquery.pyquery) – PyQuery complete API 🧀
> - <https://api.jquery.com/category/traversing/> 🧀
> - [jQuery 遍历函数](http://www.w3school.com.cn/jquery/jquery_ref_traversing.asp)

PyQuery 支持一些 jQuery 中的遍历方法，本小节仅介绍一些常用的方法，如果需要了解更多内容，请阅读参考中给出的连接。

### .items()🔨

🔨items(selector=None)

会构造一个生成器，通过生成器可逐一获取元素集中的每个元素，生成器返回的条目也是 PyQuery 对象，但是在这些 PyQuery 对象中仅包含一个元素。

> Description in api.jquery.com: 没有该条目
>
> In PyQuery API:
>
> - Iter over elements. Return PyQuery objects:
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.items

示例 1:

```python
>>> d = PyQuery('<div><span>foo</span><span>bar</span></div>')
>>> [i.text() for i in d.items('span')]
['foo', 'bar']
>>> [i.text() for i in d('span').items()]
['foo', 'bar']
>>> list(d.items('a')) == list(d('a').items())
True

d = PyQuery('<div><span>foo</span><span>bar</span></div>')
print(repr(d('span')))
print(d('span').items())
print(list(d('span').items()))
print([i.text() for i in d('span').items()])
print([i.text() for i in d.items('span')])
print(list(d.items('a')) == list(d('a').items()))
```

输出:

```
[<span>, <span>]
<generator object PyQuery.items at 0x000001B456FEB570>
[[<span>], [<span>]]
['foo', 'bar']
['foo', 'bar']
True
```



### Tree Traversal

#### .children()🔨

🔨children(selector=None)

获取直接子节点

> Description in api.jquery.com:
>
> - Get the children of each element in the set of matched elements, optionally filtered by a selector.
> - https://api.jquery.com/children/
>
> In PyQuery API:
>
> - Filter elements that are direct children of self using optional selector:
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.children

```python
# children()用于获取元素集中每个元素的直接子节点,可使用selector过滤结果
>>> d = PyQuery('<span><p class="hello">Hi</p><p>Bye</p></span>')
>>> d
[<span>]
>>> d.children()
[<p.hello>, <p>]
>>> d.children('.hello')
[<p.hello>]

>>> m = '<p><span><em>Whoah!</em></span>\n</p><p><em> there</em></p>'
>>> d = PyQuery(m)
>>> d('p')
[<p>, <p>]
>>> d('p').children()
[<span>, <em>]
>>> print(d('p').children())
<span><em>Whoah!</em></span>
<em> there</em>
```



#### .find()🔨

🔨find(selector)

获取所有后代节点

> Description in api.jquery.com:
>
> - Get the descendants of each element in the current set of matched elements, filtered by a selector, jQuery object, or element.
> - <https://api.jquery.com/find/>
>
> In PyQuery API:
>
> - Find elements using selector traversing down from self:
> - <https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.find>

```python
# find()的功能是通过选择器、jQuery对象或元素筛选元素集中每个元素的所有后代
>>> m = '<p><span><em>Whoah!</em></span></p><p><em> there</em></p>'
>>> d = PyQuery(m)
>>> d('p').find('em')
[<em>, <em>]
>>> d('p').eq(1).find('em')
[<em>]
```

查找嵌套元素

```python
>>> d = pq('<p id="hello" class="hello"><a/></p><p id="test"><a/></p>')
>>> d('p').find('a')
[<a>, <a>]
>>> d('p').eq(1).find('a')
[<a>]
```



#### .parent()🔨

🔨parent([selector])

获取直接父节点

> Description in api.jquery.com:
>
> - Get the parent of each element in the current set of matched elements, optionally filtered by a selector.
> - https://api.jquery.com/parent/
>
> In PyQuery API: 在官方文档 [PyQuery API](https://pyquery.readthedocs.io/en/stable/api.html) 中没有提到 `parent()` 方法

```python
# parent()用于获取元素集中每个元素的直接父节点,可使用selector过滤结果
from pyquery import PyQuery
html_doc = '''
<ul class="level-1">
  <ul class="entry-1">
    <li class="item-a" id="1">A1</li>
  </ul>
  <ul class="entry-2">
    <li class="item-a" id="2">A2</li>
    <li class="item-a" id="3">A3</li>
  </ul>
  <ul class="level-2">
    <ul class="entry-i">
      <li class="item-a" id="4">A1</li>
    </ul>
  </ul>
</ul>
'''
doc = PyQuery(html_doc)
a = doc("li.item-a")
print(repr(a))
print(repr(a.parent()))
```

输出:

```
[<li#1.item-a>, <li#2.item-a>, <li#3.item-a>, <li#4.item-a>]
[<ul.entry-1>, <ul.entry-2>, <ul.entry-i>]
```



#### .parents()🔨

🔨parents(selector=None)

获取所有祖先节点

> Description in api.jquery.com:
>
> - Get the ancestors of each element in the current set of matched elements, optionally filtered by a selector.
> - https://api.jquery.com/parents/
>
> In PyQuery API:
>
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.parents

```python
# parent()用于获取元素集中每个元素的所有祖先节点,可使用selector过滤结果
from pyquery import PyQuery
html_doc = '''
<ul class="level-1">
  <ul class="entry-1">
    <li class="item-a" id="1">A1</li>
  </ul>
  <ul class="entry-2">
    <li class="item-a" id="2">A2</li>
    <li class="item-a" id="3">A3</li>
  </ul>
  <ul class="level-2">
    <ul class="entry-i">
      <li class="item-a" id="4">A1</li>
    </ul>
  </ul>
</ul>
'''
doc = PyQuery(html_doc)
a = doc("li.item-a")
print(repr(a))
print(repr(a.parents()))
print(repr(a.parents(".level-2")))
```

输出:

```
[<li#1.item-a>, <li#2.item-a>, <li#3.item-a>, <li#4.item-a>]
[<ul.level-1>, <ul.entry-1>, <ul.entry-2>, <ul.level-2>, <ul.entry-i>]
[<ul.level-2>]
```

#### .siblings()🔨

🔨siblings(selector=None)

获取兄弟节点

> Description in api.jquery.com:
>
> - Get the siblings of each element in the set of matched elements, optionally filtered by a selector.
> - https://api.jquery.com/siblings/
>
> In PyQuery API:
>
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.siblings

```python
# siblings()用于获取元素集中每个元素的所有兄弟节点,可使用selector过滤结果
from pyquery import PyQuery
html_doc = '''
<ul>
  <ul class="level-1">
    <li id='1'>list item 1</li>
    <li id='2'>list item 2</li>
    <li id='3' class="third-item">list item 3</li>
    <li id='4'>list item 4</li>
    <li id='5'>list item 5</li>
  </ul>
  <ul class="level-2">
    <li id='6' class="third-item">list item 6</li>
    <li id='7'>list item 7</li>
  </ul>
</ul>
'''
doc = PyQuery(html_doc)
a = doc("li.third-item")
print(repr(a))
print(repr(a.siblings()))
print(repr(a.siblings('#5')))
```

输出:

```
[<li#3.third-item>, <li#6.third-item>]
[<li#2>, <li#1>, <li#4>, <li#5>, <li#7>]
[<li#5>]
```



### Filtering

#### .filter()🔨

🔨filter(selector)

过滤元素集

> Description in api.jquery.com:
>
> - Reduce the set of matched elements to those that match the selector or pass the function's test.
> - <https://api.jquery.com/filter/>
>
> In PyQuery API:
>
> - Filter elements in self using selector (string or function):
> - <https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.filter>

```python
# filter()对元素集进行过滤,仅保留匹配的元素
>>> d = PyQuery('<p class="hello">Hi</p><p>Bye</p>')
>>> d('p')
[<p.hello>, <p>]
>>> d('p').filter('.hello')
[<p.hello>]
>>> d('p').filter(lambda i: i == 1) # i表示索引
[<p>]
>>> d('p').filter(lambda i: PyQuery(this).text() == 'Hi')
[<p.hello>]
>>> d('p').filter(lambda i, this: PyQuery(this).text() == 'Hi')
[<p.hello>]
```

#### .eq()🔨

🔨eq(index)

> Description in api.jquery.com:
>
> - Reduce the set of matched elements to the one at the specified index.
> - <https://api.jquery.com/eq/>
>
> In PyQuery API:
>
> - Return PyQuery of only the element with the provided index:
> - <https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.eq>

```python
# eq()用于选择特定索引位置的元素
>>> d = PyQuery('<p class="hello">Hi</p><p>Bye</p><div></div>')
>>> d('p').eq(0)
[<p.hello>]
>>> d('p').eq(1)
[<p>]
>>> d('p').eq(2)
[]
```

#### is_()🔨

🔨is_(selector)

> Description in api.jquery.com:
>
> - Check the current matched set of elements against a selector, element, or jQuery object and return `true` if at least one of these elements matches the given arguments.
> - <https://api.jquery.com/is/>
>
> In PyQuery API:
>
> - Returns True if selector matches at least one current element, else False:
> - https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.is_

```python
>>> d = PyQuery('<p class="hello"><span>Hi</span></p><p>Bye</p>')
>>> d('p').eq(0).is_('.hello')
True
>>> d('p').eq(0).is_('span')
False
>>> d('p').eq(1).is_('.hello')
False
```

### Miscellaneous Traversing

#### .end()🔨

🔨end()

> Description in api.jquery.com:
>
> - End the most recent filtering operation in the current chain and return the set of matched elements to its previous state.
> - <https://api.jquery.com/end/>
>
> In PyQuery API:
>
> - Break out of a level of traversal and return to the parent level.
> - <https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.end>

```python
# 跳出一个遍历层，回到父层的状态
>>> m = '<p><span><em>Whoah!</em></span></p><p><em> there</em></p>'
>>> d = PyQuery(m)
>>> d('p').eq(1).find('em').end().end()
[<p>, <p>]
```









