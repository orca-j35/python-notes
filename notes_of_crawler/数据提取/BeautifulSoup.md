# BeautifulSoup
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

## 概述

如需了解 Beautiful Soup 的使用方法，建议将本笔记与官方文档配合食用。

[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) 是一个用来从 HTML 或 XML 文件中提取数据的 Python 库。在使用 BeautifulSoup 时，我们选择自己喜欢的解析器，从而以自己熟悉的方式来导航、查找和修改解析树。

相关资源:

- Home: https://www.crummy.com/software/BeautifulSoup/
- PyPI: https://pypi.org/project/beautifulsoup4/
- Docs-EN: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Docs-CN: https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

安装:

```shell
conda install beautifulsoup4
```

如果能顺利执行以下代码，则说明安装成功:

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup('<p>Hello</p>', 'lxml')
print(soup.p.string) #> Hello
```

⚠在安装 BeautifulSoup4 时，使用的名称是 `beautifulsoup4`；在导入时，使用的名称是 `bs4` (路径为 `~\Python\Lib\site-packages\bs4`)。由此可见，在安装库和导入库时使用的名称并不一定相同。

Beautiful Soup 支持 Python 标准库中的 HTML [解析器](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id9)，同时还支持一些第三方的解析器(如 [lxml](http://lxml.de/))。详见:

- <https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id9>
- <https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id49>

如需了解 CSS 选择器，可参考:

- <http://www.w3school.com.cn/css/css_selector_type.asp>
- http://www.w3school.com.cn/cssref/css_selectors.asp
- https://www.runoob.com/cssref/css-selectors.html

## 示例文档

下面这段 HTML 文档是本文的示例代码(官方文档中也用的这段代码):

```html
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
```

这段 HTML 文档存在"tag soup"，需要我们选择恰当的解析器，否则不能自动修复"tag soup"

## Output

BeautifulSoup 兼容 Py2 和 Py3 ，但 Py2 和 Py3 中的 `str` 对象并不相同，这会导出输出结果并不相同。

### prettify()🔨

> 参考: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#pretty-printing

🔨prettify(self, encoding=None, formatter="minimal")

`encoding` 参数的值为 `None` 时，`prettify()` 会将 BeautifulSoup 解析树转换为格式良好的 Unicode 字符串，每个 HTML/XML tag 和 字符串都会独占一行；`encoding` 参数的值为不是 `None` 时，`prettify()` 会将 BeautifulSoup 解析树编码为格式良好的 `bytes` 字符串。

源代码如下:

```python
# prettify()的源代码
def prettify(self, encoding=None, formatter="minimal"):
    if encoding is None:
        return self.decode(True, formatter=formatter)
    else:
        return self.encode(encoding, True, formatter=formatter)
```

示例 - in Py3:

```python
# in Python3
from bs4 import BeautifulSoup
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'lxml')
print(type(soup.prettify()))
#> <class 'str'>
print(soup.prettify())
'''Out:
<html>
 <body>
  <a href="http://example.com/">
   I linked to
   <i>
    example.com
   </i>
  </a>
 </body>
</html>
'''
```

在 `BeautifulSoup` 对象和 `Tag` 对象上均可调用 `prettify()` 方法:

```python
print(soup.a.prettify())
'''Out:
<a href="http://example.com/">
 I linked to
 <i>
  example.com
 </i>
</a>
'''
```

示例 - in Py2:

```python
# in Python2
from bs4 import BeautifulSoup
markup = u'<a href="http://example.com/">连接到<i>example.com</i></a>'
soup = BeautifulSoup(markup, 'lxml')
print(soup.prettify())
'''Out:
<html>
 <body>
  <a href="http://example.com/">
   I linked to
   <i>
    example.com
   </i>
  </a>
 </body>
</html>
'''
```



### Non-pretty printing

如果只想得到结果字符串并不在意格式，则可以在 `BeautifulSoup` 对象和 `Tag` 对象上调用以下方法: 

- `__unicode__()` - 对应内置函数 `unicode()`，适用于 Py2
- `__str__()` - 对应内置函数 `str()`，由于 Py2 中的 `str` 对象不是 Unicode 字符串，所以 `str()` 在 Py2 和 Py3 中的输出并不相同
- `__repr__()` - 对应于内置函数 `repr()`，由于 Py2 中的 `str` 对象不是 Unicode 字符串，所以 `repr()` 在 Py2 和 Py3 中的输出并不相同

这三个方法的源代码如下:

```python
def __repr__(self, encoding="unicode-escape"):
    """Renders this tag as a string."""
    if PY3K:
        # "The return value must be a string object", i.e. Unicode
        return self.decode()
    else:
        # "The return value must be a string object", i.e. a bytestring.
        # By convention, the return value of __repr__ should also be
        # an ASCII string.
        return self.encode(encoding)

def __unicode__(self):
    return self.decode()

def __str__(self):
    if PY3K:
        return self.decode()
    else:
        return self.encode()

if PY3K:
    __str__ = __repr__ = __unicode__
```

对 Py3 而言，以上三个方法完全等效，均返回 `str` 对象(Unicode 字符串):

```python
# in Python3
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'lxml')
print(soup) # 
#> <html><body><a href="http://example.com/">I linked to <i>example.com</i></a></body></html>
```

对 Py2 而言，`str()` 将返回以 UTF-8 编码的 `str` 对象(如果需要了解与编码相关的内容，可以参考 [Encodings](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#encodings) )

```python
# in Python2
>>> markup = u'<a href="http://example.com/">I linked to 示例<i>example.com</i></a>'
>>> soup = BeautifulSoup(markup, 'lxml')
>>> str(soup)
'<html><body><a href="http://example.com/">I linked to \xe7\xa4\xba\xe4\xbe\x8b<i>example.com</i></a></body></html>'
```

对 Py2 而言，`repr()` 将返回以 unicode-escape 编码(详见 [Text Encodings](https://docs.python.org/3.7/library/codecs.html#text-encodings))的 `str` 对象:

```python
# in Python2
>>> markup = u'<a href="http://example.com/">I linked to 示例<i>example.com</i></a>'
>>> soup = BeautifulSoup(markup, 'lxml')
>>> repr(soup) # 以ASCII编码,并将Unicode字面值表示为quote形式
'<html><body><a href="http://example.com/">I linked to \\u793a\\u4f8b<i>example.com</i></a></body></html>'
```

### encode()🔨

该方法会先将数据结构转换为 Unicode 字符串，再按照指定编码对 Unicode 字符串进行编码，默认采用 UTF-8 编码。源代码如下:

```python
def encode(self, encoding=DEFAULT_OUTPUT_ENCODING,
           indent_level=None, formatter="minimal",
           errors="xmlcharrefreplace"):
    # Turn the data structure into Unicode, then encode the
    # Unicode.
    u = self.decode(indent_level, encoding, formatter)
    return u.encode(encoding, errors)
```

对 Py3 而言，`encode()` 将返回以 `encoding` 编码的 `bytes` 对象:

```python
# in Python3
from bs4 import BeautifulSoup
markup = '<a href="http://example.com/">连接到<i>example.com</i></a>'
soup = BeautifulSoup(markup, 'lxml')
print(type(soup.encode()))
#> <class 'bytes'>
print(soup.encode())
#> b'<html><body><a href="http://example.com/">\xe8\xbf\x9e\xe6\x8e\xa5\xe5\x88\xb0<i>example.com</i></a></body></html>'
```

对 Py2 而言，`encode()` 将返回以 `encoding` 编码的 `str` 对象(注意，Py2 和 Py3 中的 `str` 对象并不相同):

```python
# in Python2
>>> markup = u'<a href="http://example.com/">连接到<i>example.com</i></a>'
>>> soup = BeautifulSoup(markup, 'lxml')
>>> print(soup.encode())
<html><body><a href="http://example.com/">连接到<i>example.com</i></a></body></html>
>>> soup.encode()
'<html><body><a href="http://example.com/">\xe8\xbf\x9e\xe6\x8e\xa5\xe5\x88\xb0<i>example.com</i></a></body></html>'
>>> type(soup.encode())
<type 'str'>
```

### decode()🔨

该方法会将 `BeautifulSoup` 对象和 `Tag` 对象中的内容转换为 Unicode，源代码中的注释如下:

```python
def decode(self, indent_level=None,
           eventual_encoding=DEFAULT_OUTPUT_ENCODING,
           formatter="minimal"):
    """Returns a Unicode representation of this tag and its contents.

        :param eventual_encoding: The tag is destined to be
           encoded into this encoding. This method is _not_
           responsible for performing that encoding. This information
           is passed in so that it can be substituted in if the
           document contains a <META> tag that mentions the document's
           encoding.
        """
```

对 Py3 而言，`decode()` 将返回 `str` 对象(Uncode 字符串):

```python
# in Python3
from bs4 import BeautifulSoup
markup = '<a href="http://example.com/">连接到<i>example.com</i></a>'
soup = BeautifulSoup(markup, 'lxml')
print(type(soup.decode()))
#> <class 'str'>
print(soup.decode())
#> <html><body><a href="http://example.com/">连接到<i>example.com</i></a></body></html>
```

对 Py2 而言，`decode()` 将返回 `Unicode` 对象(Uncode 字符串):

```python
# in Python2
>>> markup = u'<a href="http://example.com/">连接到<i>example.com</i></a>'
>>> soup = BeautifulSoup(markup, 'lxml')
>>> print(type(soup.decode()))
<type 'unicode'>
>>> print(soup.decode())
<html><body><a href="http://example.com/">连接到<i>example.com</i></a></body></html>
```

### formatter

> 参考: [Output formatters](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#output-formatters)(适用于 Py2，本小节适用于 Py3)

如果传递给 `BeautifulSoup()` 的文档中包含 HTML 实体(*entities*)，那么在输出文档时，这些 HTML 实体将被转换为 Unicode 字符:

```python
# in Python3
from bs4 import BeautifulSoup
soup = BeautifulSoup("&ldquo;Dammit!&rdquo; he said.", 'lxml')
print(soup)
#> <html><body><p>“Dammit!” he said.</p></body></html>
```

如果将文档编码为 `bytes` 对象，则会对通过 HTML 实体获得 Unicode 字符进行编码:

```python
# in Python3
from bs4 import BeautifulSoup
soup = BeautifulSoup("&ldquo;Dammit!&rdquo; he said.", 'lxml')
print(soup.encode())
#> b'<html><body><p>\xe2\x80\x9cDammit!\xe2\x80\x9d he said.</p></body></html>'

print('“'.encode('utf-8'))
#> b'\xe2\x80\x9c'
```

默认情况下，在输出的 Unicode 字符串中，独立的 `&`(*ampersand*)和尖括号会以 HTML 实体显示。从而保证 BeautifulSoup 不会在无意中生成无效的 HTML 或 XML。

```python
# 独立的&会显示为&amp;   &amp;会保持原样
# 独立的<会显示为&lt;    &lt;会保持原样
# 独立的>会显示为&gt;    &gt;会保持原样

# in Python3
from bs4 import BeautifulSoup
soup = BeautifulSoup(
    "<p>The law firm of Dewey, Cheatem, > &gt; < &lt; & &amp; Howe</p>",
    'lxml')
p = soup.p
print(p)
#> <p>The law firm of Dewey, Cheatem, &gt; &gt; &lt; &lt; &amp; &amp; Howe</p>
soup = BeautifulSoup(
    '<a href="http://example.com/?foo=val1&bar=val2">A link</a>', 'lxml')
print(soup.a)
#> <a href="http://example.com/?foo=val1&amp;bar=val2">A link</a>
```

通过 `prettify()` , `encode()` , `decode()` 获取输出时，可利用 `formatter` 参数来改变上述行为。`formatter` 的值有 6 种情况，默认 `formatter="minimal"`。`__str__()` , `__unicode__()` , `__repr__()` 在输出时只能采用默认行为，不可修改。

当 `formatter="minimal"` 时，会按照前面叙述的规则来处理字符串，以确保生成有效的 HTML/XML:

```python
# in Python3
from bs4 import BeautifulSoup
french = "<p>Il a dit &lt;&lt;Sacr&eacute; bleu!&gt;&gt;</p>"
soup = BeautifulSoup(french, 'lxml')
print(soup.prettify(formatter="minimal"))
'''Out:
<html>
 <body>
  <p>
   Il a dit &lt;&lt;Sacré bleu!&gt;&gt;
  </p>
 </body>
</html>'''
```

当 `formatter="html"` 时，BeautifulSoup 会尽可能的将 Unicode 字符传唤为 HTML 实体:

```python
# in Python3
from bs4 import BeautifulSoup
french = "<p>Il a dit &lt;&lt;Sacr&eacute; bleu!&gt;&gt; é</p>"
soup = BeautifulSoup(french, 'lxml')
print(soup.prettify(formatter="html"))
'''Out:
<html>
 <body>
  <p>
   Il a dit &lt;&lt;Sacr&eacute; bleu!&gt;&gt;&eacute;
  </p>
 </body>
</html>'''

# If you pass in ``formatter="html5"``, it's the same as
```

当 `formatter="html5"` 时，BeautifulSoup 会省略 HTML 空 tag 种的结束斜杠，例如:

```python
# in Python3
from bs4 import BeautifulSoup
soup = BeautifulSoup("<br>", 'lxml')
print(soup.encode(formatter="html"))
# <html><body><br/></body></html>
print(soup.encode(formatter="html5"))
# <html><body><br></body></html>
```

当 `formatter=None` 时，BeautifulSoup 将不会在输出中修改字符串。此时可以最快的速度来获得输出，但可能会导致 BeautifulSoup 生成无效的 HTML/XML，例如:

```python
# in Python3
from bs4 import BeautifulSoup
french = "<p>Il a dit &lt;&lt;Sacr&eacute; bleu!&gt;&gt;</p>"
soup = BeautifulSoup(french, 'lxml')
print(soup.prettify(formatter=None))
'''Out:
<html>
 <body>
  <p>
   Il a dit <<Sacré bleu!>>
  </p>
 </body>
</html>
'''

link_soup = BeautifulSoup('<a href="http://example.com/?foo=val1&bar=val2">A link</a>')
print(link_soup.a.encode(formatter=None))
# <a href="http://example.com/?foo=val1&bar=val2">A link</a>
```

还可以向 `formatter` 传递一个函数，BeautifulSoup 会为文档中的每个字符串和属性值调用一次该函数。你可以在这个函数中做任何你想做的事情。下面这个 formatter 函数会将字符串转换为大写，但不执行其它操作:

```python
# in Python3
from bs4 import BeautifulSoup

def uppercase(str):
    return str.upper()

french = "<p>Il a dit &lt;&lt;Sacr&eacute; bleu!&gt;&gt;</p>"
soup = BeautifulSoup(french, 'lxml')
print(soup.prettify(formatter=uppercase))
'''Out:
<html>
 <body>
  <p>
   IL A DIT <<SACRÉ BLEU!>>
  </p>
 </body>
</html>'''

link_soup = BeautifulSoup(
    '<a href="http://example.com/?foo=val1&bar=val2">A link</a>', 'lxml')
print(link_soup.a.prettify(formatter=uppercase))
'''Out:
<a href="HTTP://EXAMPLE.COM/?FOO=VAL1&BAR=VAL2">
 A LINK
</a>
'''
```









