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



## 示例文档

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



## 构造函数

> 参考:
>
> - <https://pyquery.readthedocs.io/en/latest/index.html>
> - <https://pyquery.readthedocs.io/en/latest/scrap.html#scraping>
> - 源代码

🛠class pyquery.pyquery.PyQuery(\*args, \*\*kwargs)

PyQuery 类的构造函数 `PyQuery(*args, **kwargs)` 可以从字符串、lxml 文档、文件和 url 中加载 xml 文档:

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



### `*args`

构造函数 `PyQuery(*args, **kwargs)` 的 `*args` 参数支持以下几种使用方法:

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

- 可将 selector 和 context (可以是文本, PyQuery 对象, list 对象, etree._Element 对象) 用作 `*args` 参数，详见 `PyQuery.__init__` 的源代码。使用示例:

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

### `**kwargs`

构造函数 `PyQuery(*args, **kwargs)` 支持通过 `**kwargs` 参数自定义如下内容:

- `parser` 用于设置 XML/HTML 文档的解析器
- `url` 用于设置 url 连接
- `data` 设置 GET 请求和 POST 请求的数据
- `parent` 似乎是用于设置父节点，目前不清楚具体效果
- `css_translator` 似乎是用于设置 css 翻译器，目前不清楚具体效果
- `namespaces` 用于为 XML 设置命名空间，目前不清楚具体效果
- `filename` 用于指定 XML/HTML 文件
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



### 解析器的选择

> 参考: <https://pyquery.readthedocs.io/en/stable/tips.html#using-different-parsers>

默认情况下，PyQuery 使用 lxml 的 xml 解析器进行解析。如果 xml 解析器解析失败，则会尝试使用 lxml.html 中的 html 解析器进行解析。在解析 xhtml 页面时，xml 解析器有时出现问题，虽然解析器不会抛出异常，但由解析器提供的树将不可用(on w3c.org for example)。

构造函数 `PyQuery()` 在解析文档时，解析库的选择遵循以下规则(详见源代码):

- 如果没有在 `**kwargs` 中提供 `parser` 参数，则会先使用 `lxml.etree` 进行解析，如果失败则会使用 `lxml.html` 进行解析
- 还可通过 `**kwargs` 的 `parser` 参数手动设置解析器，`parser` 的可选实参值如下:
  - `'xml'` - 对应 `lxml.etree`
  - `'html'` - 对应 `lxml.html`
  - `'html5'` - 对应 `lxml.html.html5parser`
  - `'soup'` - 对应 `lxml.html.soupparser`
  - `'html_fragments'` - 对应 `lxml.html.fragments_fromstring`

建议为 `PyQuery()` 手动设置解析器。

```python
>>> pq('<html><body><p>toto</p></body></html>', parser='xml')
[<html>]
>>> pq('<html><body><p>toto</p></body></html>', parser='html')
[<html>]
>>> pq('<html><body><p>toto</p></body></html>', parser='html_fragments')
[<p>]
```



### 请求库的选择

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



### 超时

> 参考: <https://pyquery.readthedocs.io/en/latest/scrap.html#timeout>

超时的默认时长是 60 秒，如果需要修改超时时长可通过 `**kwargs` 向 urllib 或 requests 传递相应的关键字参数。



### 会话

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





## PyQuery 对象

PyQuery 类继承自 list，可将 PyQuery 实例视作由 xml 解析器的元素对象构成的列表:

```python
from pyquery import PyQuery
html_doc = """
<body>
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
</body>
"""
d_html = PyQuery(html_doc,parser='html')
a = d_html('a')
type(a)
#> pyquery.pyquery.PyQuery
a
#> [<a#link1.sister>, <a#link2.sister>, <a#link3.sister>]

for i in a:
    print(f"{type(i)}:{i.xpath('@href')}")
'''Out:
<class 'lxml.html.HtmlElement'>:['http://example.com/elsie']
<class 'lxml.html.HtmlElement'>:['http://example.com/lacie']
<class 'lxml.html.HtmlElement'>:['http://example.com/tillie']
'''
```

### 操作 PyQuery 对象

> 参考: <https://pyquery.readthedocs.io/en/stable/manipulating.html>

You can also add content to the end of tags:

```python
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
>>> print(p.html())
check out <a href="http://reddit.com/r/python">reddit</a>you know ...
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



## 改用绝对连接

> 参考: <https://pyquery.readthedocs.io/en/stable/tips.html#making-links-absolute>

通过 PyQuery 对象可将相对连接改为绝对连接，这在爬虫中非常有用:

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

## 遍历

> 参考: 
>
> - <https://pyquery.readthedocs.io/en/latest/traversing.html>
> - <https://api.jquery.com/category/traversing/>

PyQuery 支持一些 jQuery 中的遍历方法，下面是一些示例。

### .filter(selector)

> Description in api.jquery.com:
>
> - Reduce the set of matched elements to those that match the selector or pass the function's test.
>
> - <https://api.jquery.com/filter/>
>
> In PyQuery API：
>
> - Filter elements in self using selector (string or function):
>
> - <https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.filter>

```python
# filter()用于过滤选择列表，仅保留匹配的元素
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

### .eq(index)

> Description in api.jquery.com:
>
> - Reduce the set of matched elements to the one at the specified index.
>
> - <https://api.jquery.com/eq/>
>
> In PyQuery API：
>
> - Return PyQuery of only the element with the provided index:
>
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

### .find(selector)

> Description in api.jquery.com:
>
> - Get the descendants of each element in the current set of matched elements, filtered by a selector, jQuery object, or element.
>
> - <https://api.jquery.com/find/>
>
> In PyQuery API：
>
> - Find elements using selector traversing down from self:
>
> - <https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.find>

```python
# find()的功能是通过选择器、jQuery对象或元素筛选当前匹配元素集中每个元素的后代。
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



### .end()

> Description in api.jquery.com:
>
> - End the most recent filtering operation in the current chain and return the set of matched elements to its previous state.
>
> - <https://api.jquery.com/end/>
>
> In PyQuery API：
>
> - Break out of a level of traversal and return to the parent level.
>
> - <https://pyquery.readthedocs.io/en/stable/api.html#pyquery.pyquery.PyQuery.end>

```python
# 跳出一个遍历层，回到父层的状态
>>> m = '<p><span><em>Whoah!</em></span></p><p><em> there</em></p>'
>>> d = PyQuery(m)
>>> d('p').eq(1).find('em').end().end()
[<p>, <p>]
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

我们可以通过 jQuery 来选取(查询、query) HTML 元素，并对这些元素执行操作(*action*)

jQuery 的基础语法是 `$(selector).action()`:

- `$` 是 jQuery 的别名 - The jQuery library exposes its methods and properties via two properties of the `window` object called `jQuery` and `$`. `$` is simply an alias for `jQuery` and it's often employed because it's shorter and faster to write.
- `(selector)` 用于查询 HTML 元素
- `action()` 用于对元素执行操作。

Note: jQuery 使用的语法是 XPath 与 CSS 选择器语法的组合。

实例展示:

```javascript
$(this).hide() # 隐藏当前元素
$("p").hide() # 隐藏所有 <p> 元素
$("p.test").hide() # 隐藏所有 class="test" 的 <p> 元素
$("#test").hide() # 隐藏所有 id="test" 的元素
```

🐍PyQuery:

```python
from pyquery import PyQuery as pq
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">...</p>
</body></html>
"""
d = pq(html_doc)
d, type(d)
#> ([<html>], pyquery.pyquery.PyQuery)
print(d)
'''Out:
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">...</p>
</body></html>
'''
```

上面这段代码中的 `d` 相当于 jQuery 中的 `$`，因此可以通过 `d(selector).action()` 来选择和操作元素:

```python
d("#hello") # 选择id="hello"的元素
#> [<html#hello.hello>]

# Get the html representation of sub nodes.
print(d("#hello").html())
"""Out:
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">...</p>
</body>
"""

# set the html representation of sub nodes.
d("#hello").html("you know <a href='http://python.org/'>Python</a> rocks") 
#> [<html#hello.hello>]

print(d("#hello").html())
# you know <a href="http://python.org/">Python</a> rocks

# Get the text representation of sub nodes.
print(d("#hello").text()) 
# you know Python rocks

print(d)
#> <html id="hello" class="hello">you know <a href="http://python.org/">Python</a> rocks</html>
```

### 选择器

jQuery 选择器的语法是 `$(selector)`，我们可利用 jQuery 选择器来选取(或查找)一组 HTML 元素。jQuery 选择器基于已经存在的 CSS 选择器，可依据 id、class、属性和属性值等选取(或查找) HTML 元素。除了已有的 CSS 选择器，jQuery 还提供了一些自定义选择器。

Note: jQuery 使用的语法是 XPath 与 CSS 选择器语法的组合。

如需了解 jQuery 选择器的 API，可参考:

- <https://api.jquery.com/category/selectors/> 🍰

如需了解 CSS 选择器，可参考:

- <http://www.w3school.com.cn/cssref/css_selectors.asp>
- <http://www.w3school.com.cn/css/css_selector_type.asp>
- <https://www.runoob.com/cssref/css-selectors.html>

如需了解 XPath，可参考笔记 ﹝XPath.md﹞

下面是一些选择器实例

| 语法                     | 描述                                                        |
| :----------------------- | :---------------------------------------------------------- |
| $("*")                   | 选取所有元素                                                |
| $(this)                  | 选取当前 HTML 元素                                          |
| $("p")                   | 选取所有 `<p>` 元素                                         |
| $("p.intro")             | 选取 class 为 intro 的 `<p>` 元素                           |
| $(".intro")              | 选取所有 class 为 intro 的元素                              |
| $("p:first")             | 选取第一个 `<p>` 元素                                       |
| $("ul li:first")         | 选取第一个 `<ul>` 元素的第一个 <li> 元素                    |
| $("ul li:first-child")   | 选取每个 `<ul>` 元素的第一个 `<li>` 元素                    |
| $("[href]")              | 选取带有 href 属性的元素                                    |
| $("a[target='_blank']")  | 选取所有 target 属性值等于 "_blank" 的 `<a>` 元素           |
| $("a[target!='_blank']") | 选取所有 target 属性值不等于 "_blank" 的 `<a>` 元素         |
| $(":button")             | 选取所有 type="button" 的 `<input>` 元素 和 `<button>` 元素 |
| $("tr:even")             | 选取偶数位置的 `<tr>` 元素                                  |
| $("tr:odd")              | 选取奇数位置的 `<tr>` 元素                                  |

🐍 PyQuery:

在 PyQuery 中选择器的返回值是 PyQuery 对象，同样只能用于选取(或查找)一组 HTML 元素。

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



#### id 选择器

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



#### 类选择器

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

#### 属性选择器

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

#### 伪类选择器

You can use some of the pseudo classes that are available in jQuery but that are not standard in css such as :first :last :even :odd :eq :lt :gt :checked :selected :file:

```
>>> d('p:first')
[<p#hello.hello>]
```

有关伪类(*pseudo* *classes*)的详细信息请交叉参考 [Using pseudo classes](https://pyquery.readthedocs.io/en/stable/pseudo_classes.html) 和 <https://api.jquery.com/category/selectors/>，前者虽属于 PyQuery 的官方文档，但是我发现存在错误。

#### 嵌套选择

选择器还支持嵌套选择:

- 使用空格分隔的一组选择器表示层层递进的嵌套选择



各个选择器之间加上空格分隔开便可以代表嵌套关系，

## 属性

可以在属性选择器中使用属性来选择需要的 tag，该值应是一个有效的 CSS 标识符或引用为字符串:

```python
d = pq("<option id='A' value='1'><option id='B' value='2'>")
d('option[value="1"]')
#> [<option#A>]
```

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

## CSS

> 参考:
>
> - <https://api.jquery.com/category/css/>

jQuery 拥有若干进行 CSS 操作的方法，比如下面这些:

- addClass() - 向被选元素添加一个或多个类
- removeClass() - 从被选元素删除一个或多个类
- toggleClass() - 对被选元素进行添加/删除类的切换操作
- css() - 设置或返回样式(*style*)属性

```javascript
# 把所有p元素的背景颜色更改为红色
$("p").css("background-color","red");
```

🐍 PyQuery

You can play with css classes:

```python
>>> p = pq('<p id="hello" class="hello"></p>')('p')
>>> p.addClass("toto") # add_class()方法的别名，用于为class添加值
[<p#hello.hello.toto>]
>>> p.toggleClass("titi toto") # 切换class的值
[<p#hello.hello.titi>]
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









