# lxml.html
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考: 
>
> - <https://lxml.de/lxmlhtml.html>
> - [Python爬虫利器——lxml 和 xpath 表达式](http://yifei.me/note/464)
> - [lxml 学习笔记](https://www.jianshu.com/p/e084c2b2b66d)
> - <https://lxml.de/api/lxml.html-module.html>
> - [Source Code for Package lxml.html](https://lxml.de/api/lxml.html-pysrc.html)
> - [Class HtmlElement](https://lxml.de/api/lxml.html.HtmlElement-class.html)

从 2.0 版本开始，lxml 附带了一个用于处理 HTML 的专用 Python 包 `lxml.html`。该包基于 lxml 的 HTML 解析器，但为 HTML elements 提供了一个特殊的 API，以及一些用于 HTML 处理任务的使用程序。

主 API 基于 [lxml.etree](https://lxml.de/tutorial.html) API，因此也基于 [ElementTree](http://effbot.org/zone/element-index.htm)API。

## 解析 HTML

### parse()🔨

🔨parse(filename_url_or_file, parser=None, base_url=None, **kw)

◀return lxml.etree._ElementTree object

> Parse a filename, URL, or file-like object into an HTML document tree.  if the object has a `.read()` method, `parse()` can parses from that.
>
> Note: this returns a tree, not an element. Use `parse(...).getroot()` to get the document root.
>
> If you give a URL, or if the object has a `.geturl()` method (as file-like objects from `urllib.urlopen()` have), then that URL is used as the base URL. You can also provide an explicit `base_url` keyword argument.
>
> You can override the base URL with the `base_url` keyword. This is most useful when parsing from a file-like object.

```python
 # 源代码
 928 -def parse(filename_or_url, parser=None, base_url=None, **kw): 
 937      if parser is None: 
 938          parser = html_parser 
 939      return etree.parse(filename_or_url, parser, base_url=base_url, **kw)
 --snip--
 1925  html_parser = HTMLParser() 
```

示例代码:

```python
from lxml import etree
from lxml import html
from io import StringIO
broken_html = "<html><head><title>test<body><h1>page title</h3>"
tree = html.parse(StringIO(broken_html))
root = tree.getroot() # 获得_ElementTree的根元素
etree.dump(root)
'''Out:
<html>
  <head>
    <title>test</title>
  </head>
  <body>
    <h1>page title</h1>
  </body>
</html>
'''
```

### document_fromstring🔨

🔨document_fromstring(html, parser=None, ensure_head_body=False, \*\*kw)

◀return lxml.html.[HtmlElement](https://lxml.de/api/lxml.html.HtmlElement-class.html) object

> Parses a document from the given string(or bytes). This always creates a correct HTML document, which means the parent node is `<html>`, and there is a body and possibly a head.

```python
 758 -def document_fromstring(html, parser=None, ensure_head_body=False, **kw): 
 759      if parser is None: 
 760          parser = html_parser 
 761      value = etree.fromstring(html, parser, **kw) 
 762      if value is None: 
 763          raise etree.ParserError( 
 764              "Document is empty") 
 765      if ensure_head_body and value.find('head') is None: 
 766          value.insert(0, Element('head')) 
 767      if ensure_head_body and value.find('body') is None: 
 768          value.append(Element('body')) 
 769      return value 
```

示例代码:

```python
from lxml import etree
from lxml import html
broken_html = "<html><head><title>test<body><h1>page title</h3>"
root = html.document_fromstring(broken_html)
etree.dump(root)
'''Out:
<html>
  <head>
    <title>test</title>
  </head>
  <body>
    <h1>page title</h1>
  </body>
</html>
'''
```

### fragment_fromstring()🔨

🔨fragment_fromstring(html, create_parent=False, base_url=None, parser=None, \*\*kw)

◀return lxml.html.[HtmlElement](https://lxml.de/api/lxml.html.HtmlElement-class.html) object

> Parses a single HTML element; it is an error if there is more than one element unless `create_parent` is given, or if anything but whitespace precedes or follows the element.
>
> If `create_parent` is true (or is a tag name) then a parent node will be created to encapsulate the HTML in a single element. In this case, leading or trailing text is also allowed, as are multiple elements as result of the parsing.
>
> Passing a `base_url` will set the document's `base_url` attribute (and the tree's docinfo.URL).

示例代码:

```python
from lxml import etree
from lxml import html
broken_html = "<html><head><title>test<body><h1>page title</h3>"
fragment = html.fragment_fromstring(broken_html)
etree.dump(fragment)
#> <h1>page title</h1>

fragment = html.fragment_fromstring(broken_html,create_parent='div')
etree.dump(fragment)
'''Out:
<div>
  <h1>page title</h1>
</div>'''

html.fragment_fromstring("<h1>page title</h1><h2>page")
#> ParserError: Multiple elements found (h1, h2)

etree.dump(html.fragment_fromstring("<h1>page title</h1><h2>page",create_parent='div'))
'''Out:
<div>
  <h1>page title</h1>
  <h2>page</h2>
</div>'''
```

### fragments_fromstring()🔨

🔨fragments_fromstring(html, no_leading_text=False, base_url=None, parser=None, **kw)

◀return list of lxml.html.[HtmlElement](https://lxml.de/api/lxml.html.HtmlElement-class.html) object

> Parses several HTML elements, returning a list of elements.
>
> The first item in the list may be a string. If no_leading_text is true, then it will be an error if there is leading text, and it will always be a list of only elements.
>
> base_url will set the document's base_url attribute (and the tree's docinfo.URL).

示例代码:

```python
from lxml import html
from lxml import etree
broken_html = "<h1>page title</h1><h2>page"
fragments = html.fragments_fromstring(broken_html)
for frg in fragments:
    etree.dump(frg)
'''Out:
<h1>page title</h1>
<h2>page</h2>
'''
```

### fromstring()🔨

🔨fromstring(html, base_url=None, parser=None, \*\*kw)

◀return list of lxml.html.[HtmlElement](https://lxml.de/api/lxml.html.HtmlElement-class.html) object

> Parse the html(string or bytes), returning a single element/document, based on whether the string looks like a full document, or just a fragment.
>
> This tries to minimally parse the chunk of text, without knowing if it is a fragment or a document.
>
> base_url will set the document's base_url attribute (and the tree's docinfo.URL)

示例代码:

```python
etree.dump(html.fromstring("test<body><h1>page title</h3>"))
print()
etree.dump(html.fromstring("<html><head><title>test<body><h1>page title</h3>"))
'''Out:
<div>
  <p>test</p>
  <h1>page title</h1>
</div>

<html>
  <head>
    <title>test</title>
  </head>
  <body>
    <h1>page title</h1>
  </body>
</html>
'''
```



## 序列化

### tostring()🔨

🔨tostring(doc, pretty_print=False, include_meta_content_type=False, encoding=None, method='html', with_tail=True, doctype=None)

> Return an HTML string representation of the document.
>
> Note: if include_meta_content_type is true this will create a <meta http-equiv="Content-Type" ...> tag in the head; regardless of the value of include_meta_content_type any existing <meta http-equiv="Content-Type" ...> tag will be removed
>
> The encoding argument controls the output encoding (defauts to ASCII, with &#...; character references for any characters outside of ASCII). Note that you can pass the name 'unicode' as encoding argument to serialise to a Unicode string.
>
> The method argument defines the output method. It defaults to 'html', but can also be 'xml' for xhtml output, or 'text' to serialise to plain text without markup.
>
> To leave out the tail text of the top-level element that is being serialised, pass with_tail=False.
>
> The doctype option allows passing in a plain string that will be serialised before the XML tree. Note that passing in non well-formed content here will make the XML output non well-formed. Also, an existing doctype in the document tree will not be removed when serialising an ElementTree instance.

```python
# 源代码:
1844      html = etree.tostring(doc, method=method, pretty_print=pretty_print, 
1845                            encoding=encoding, with_tail=with_tail, 
1846                            doctype=doctype) 
1847      if method == 'html' and not include_meta_content_type: 
1848          if isinstance(html, str): 
1849              html = __str_replace_meta_content_type('', html) 
1850          else: 
1851              html = __bytes_replace_meta_content_type(bytes(), html) 
1852      return html 
```

示例代码:

```python
>>> from lxml import html
>>> root = html.fragment_fromstring('<p>Hello<br>world!</p>')

>>> html.tostring(root)
'<p>Hello<br>world!</p>'
>>> html.tostring(root, method='html')
'<p>Hello<br>world!</p>'

>>> html.tostring(root, method='xml')
'<p>Hello<br/>world!</p>'

>>> html.tostring(root, method='text')
'Helloworld!'

>>> html.tostring(root, method='text', encoding='unicode')
u'Helloworld!'

>>> root = html.fragment_fromstring('<div><p>Hello<br>world!</p>TAIL</div>')
>>> html.tostring(root[0], method='text', encoding='unicode')
u'Helloworld!TAIL'

>>> html.tostring(root[0], method='text', encoding='unicode', with_tail=False)
u'Helloworld!'

>>> doc = html.document_fromstring('<p>Hello<br>world!</p>')
>>> html.tostring(doc, method='html', encoding='unicode')
u'<html><body><p>Hello<br>world!</p></body></html>'

>>> print(html.tostring(doc, method='html', encoding='unicode',
...          doctype='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"'
...                  ' "http://www.w3.org/TR/html4/strict.dtd">'))
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><body><p>Hello<br>world!</p></body></html>
```

## tag soup

> The normal HTML parser is capable of handling broken HTML, but for pages that are far enough from HTML to call them 'tag soup', it may still fail to parse the page in a useful way. A way to deal with this is [ElementSoup](https://lxml.de/elementsoup.html), which deploys the well-known [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) parser to build an lxml HTML tree.
>
> However, note that the most common problem with web pages is the lack of (or the existence of incorrect) encoding declarations. It is therefore often sufficient to only use the encoding detection of BeautifulSoup, called UnicodeDammit, and to leave the rest to lxml's own HTML parser, which is several times faster.

## Other

在 <https://lxml.de/lxmlhtml.html> 中还包含以下内容:

- [HTML Element Methods](https://lxml.de/lxmlhtml.html#html-element-methods)
- [Running HTML doctests](https://lxml.de/lxmlhtml.html#running-html-doctests)
- [Creating HTML with the E-factory](https://lxml.de/lxmlhtml.html#creating-html-with-the-e-factory)
  - [Viewing your HTML](https://lxml.de/lxmlhtml.html#viewing-your-html)
- [Working with links](https://lxml.de/lxmlhtml.html#working-with-links)
  - [Functions](https://lxml.de/lxmlhtml.html#functions)
- [Forms](https://lxml.de/lxmlhtml.html#forms)
  - [Form Filling Example](https://lxml.de/lxmlhtml.html#form-filling-example)
  - [Form Submission](https://lxml.de/lxmlhtml.html#form-submission)
- [Cleaning up HTML](https://lxml.de/lxmlhtml.html#cleaning-up-html)
  - [autolink](https://lxml.de/lxmlhtml.html#autolink)
  - [wordwrap](https://lxml.de/lxmlhtml.html#wordwrap)
- [HTML Diff](https://lxml.de/lxmlhtml.html#html-diff)
- [Examples](https://lxml.de/lxmlhtml.html#examples)
  - [Microformat Example](https://lxml.de/lxmlhtml.html#microformat-example)