# lxml.etree
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考: 
>
> - <https://lxml.de/tutorial.html>
> - https://lxml.de/tutorial.html#parsing-from-strings-and-files>
> - <https://lxml.de/parsing.html>
> - <https://lxml.de/api/lxml.etree-module.html>
> - [lxml 学习笔记](https://www.jianshu.com/p/e084c2b2b66d)
> - [`xml.etree.ElementTree`](https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree) — The ElementTree XML API
> - [Python爬虫利器——lxml 和 xpath 表达式](http://yifei.me/note/464)



## 解析函数

### fromstring()🔨...

🔨fromstring(text, parser=None, base_url=None)

◀return lxml.etree._Element object

> Parses an XML document or fragment from a string(or bytes). Returns the root node (or the result returned by a parser target).
>
> To override the default parser with a different parser you can pass it to the `parser` keyword argument.
>
> The `base_url` keyword argument allows to set the original base URL of the document to support relative Paths when looking up external entities (DTD, XInclude, ...).

```python
# 该函数用于从字符串中解析XML
# 返回值是lxml.etree._Element类型
some_xml_data = "<root>data</root>"

root = etree.fromstring(some_xml_data)
type(root)
#> lxml.etree._Element

root.tag
#> root
etree.tostring(root)
#> b'<root>data</root>'
```

使用 HTML 解析器来解析 HTML:

```python
some_xml_data = "<root>data"
root = etree.fromstring(some_xml_data,etree.HTMLParser())
etree.tounicode(root)
#> '<html><body><root>data</root></body></html>'
```

> If you want to parse from memory and still provide a base URL for the document (e.g. to support relative paths in an XInclude), you can pass the `base_url` keyword argument:

```python
xml = '<a xmlns="test"><b xmlns="test"/></a>'
root = etree.fromstring(xml, base_url="http://where.it/is/from.xml")
root.base
#> 'http://where.it/is/from.xml'
```



------

🔨fromstringlist(strings, parser=None)

return lxml.etree._Element object

```python
# 该函数用于从字符串序列中解析XML
# 返回值是lxml.etree._Element类型
xml_list=["<root>","data","</root>"]

root = etree.fromstringlist(xml_list)
type(root)
#> lxml.etree._Element
```

> Parses an XML document from a sequence of strings. Returns the root node (or the result returned by a parser target).
>
> To override the default parser with a different parser you can pass it to the `parser` keyword argument.

### XML()🔨...

🔨XML(text, parser=None, base_url=None)

◀return lxml.etree._Element object

`XML()` 默认使用 XMLParser 解析器，其功能类似于 `fromstring()`，但通常用于解析 XML。

> The `XML()` function behaves like the `fromstring()` function, but is commonly used to write XML literals right into the source:
>
> Parses an XML document or fragment from a string constant. Returns the root node (or the result returned by a parser target). This function can be used to embed "XML literals" in Python code, like in

```python
# 该函数用于从字符串中解析XML
# 返回值是lxml.etree._Element类型
root = etree.XML("<root>data</root>")
type(root)
#> lxml.etree._Element
root.tag
#> root
etree.tostring(root)
b'<root>data</root>'
```

> To override the parser with a different `XMLParser` you can pass it to the `parser` keyword argument.
>
> The `base_url` keyword argument allows to set the original base URL of the document to support relative Paths when looking up external entities (DTD, XInclude, ...).

------

🔨XMLDTDID(text, parser=None, base_url=None)

retrun tuple

Parse the text and return a tuple (root node, ID dictionary). The root node is the same as returned by the XML() function. The dictionary contains string-element pairs. The dictionary keys are the values of ID attributes as defined by the DTD. The elements referenced by the ID are stored as dictionary values.

Note that you must not modify the XML tree if you use the ID dictionary. The results are undefined.

------

🔨XMLID(text, parser=None, base_url=None)

retrun tuple

```python
some_xml_data = "<root>data</root>"

root = etree.XMLID("<root id='1'>data</root>")
type(root)
#> <class 'tuple'>
root
#> (<Element root at 0x193dfcfb708>, {'1': <Element root at 0x193dfcfb708>})
```

> Parse the text and return a tuple (root node, ID dictionary). The root node is the same as returned by the XML() function. The dictionary contains string-element pairs. The dictionary keys are the values of 'id' attributes. The elements referenced by the ID are stored as dictionary values.

### HTML()🔨

🔨HTML(text, parser=None, base_url=None)

◀return lxml.etree._Element object

默认使用 HTMLParser 解析器，用于从字符串(或 bytes)中解析 HTML 文档。

```python
# 该函数用于从字符串中解析HTML
# 返回值是lxml.etree._Element类型
root = etree.HTML("<p>data</p>")
type(root)
#> lxml.etree._Element
etree.tostring(root)
b'<html><body><p>data</p></body></html>'
```

> Parses an HTML document from a string constant. Returns the root node (or the result returned by a parser target). This function can be used to embed "HTML literals" in Python code.
>
> To override the parser with a different `HTMLParser` you can pass it to the `parser` keyword argument.
>
> The `base_url` keyword argument allows to set the original base URL of the document to support relative Paths when looking up external entities (DTD, XInclude, ...).

### parse()🔨...

🔨parse(source, parser=None, base_url=None)

◀return lxml.etree._ElementTree object

`parse()` 函数用于解析文件和类文件对象，`fromstring()` 用于解析字符串。

```python
# As an example of such a file-like object, the following code uses the BytesIO class for reading from a string instead of an external file. 

from io import BytesIO
some_file_or_file_like_object = BytesIO(b"<root>data</root>")

tree = etree.parse(some_file_or_file_like_object)
type(tree)
#> lxml.etree._ElementTree
etree.tostring(tree)
#> b'<root>data</root>'
root = tree.getroot()
root.tag, etree.tostring(root)
#> ('root', b'<root>data</root>')
```

Note: `parse()` 的返回值是 ElementTree 对象(lxml.etree.\_ElementTree)，而非 Element 对象( lxml.etree.\_Element)。因为 `parse()` 被用于解析文件(或类文件对象)，它会获得并返回一个完整的文档，而 `fromstring()` 通常用于解析 XML 片段。

可以向 *source* 传递 HTTP 或 FTP 字符串，但不能使用 HTTPS 字符串

```python
from io import BytesIO
some_file_or_file_like_object = BytesIO(b"<root>data</root>")

tree = etree.parse('http://httpbin.org/get?a=b',parser=etree.HTMLParser())
etree.tounicode(tree)
#> '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">\n<html><body><p>{\n  "args": {\n    "a": "b"\n  }, \n  "headers": {\n    "Accept-Encoding": "gzip", \n    "Host": "httpbin.org"\n  }, \n  "origin": "118.114.245.159, 118.114.245.159", \n  "url": "https://httpbin.org/get?a=b"\n}\n</p></body></html>'
```

> Return an ElementTree object loaded with source elements. If no parser is provided as second argument, the default parser is used.
>
> The `source` can be any of the following:
>
> - a file name/path string
> - an open file object (make sure to open it in binary mode)
> - a file-like object that has a `.read(byte_count)` method returning a byte string on each call
> - a URL using the HTTP or FTP protocol
>
> It also auto-detects and reads gzip-compressed XML files (.gz).
>
> To parse from a string, use the `fromstring()` function instead.
>
> Note that it is generally faster to parse from a file path or URL than from an open file object or file-like object. Transparent decompression from gzip compressed sources is supported (unless explicitly disabled in libxml2). However, the HTTP/FTP client in libxml2 is rather simple, so things like HTTP authentication require a dedicated URL request library, e.g. `urllib2` or `requests`. These libraries usually provide a file-like object for the result that you can parse from while the response is streaming in.
>
> The `base_url` keyword allows setting a URL for the document when parsing from a file-like object. This is needed when looking up external entities (DTD, XInclude, ...) with relative paths.

------

🔨parseid(source, parser=None)

Parses the source into a tuple containing an ElementTree object and an ID dictionary. If no parser is provided as second argument, the default parser is used.

Note that you must not modify the XML tree if you use the ID dictionary. The results are undefined.

## 解析器

> 参考:
>
> - <https://lxml.de/tutorial.html#parsing-from-strings-and-files>
> - <https://lxml.de/parsing.html
> - <https://lxml.de/api/lxml.etree-module.html>

解析器(parser)由解析器对象表示。支持解析 XML 和 (broken) HTML。最好使用 XML 解析器解析 XHTML，如果使用 HTML 解析器解析 XHTML，则有可能会出现意外结果，因为 HTML 解析不能识别命名空间。

如需了解解析器构造函数中各参数的含义，可参考解析器 API 文档和 <https://lxml.de/parsing.html#parser-options>

在默认情况下，`lxml.etree` 会使用具备默认设置的标准解析器。我们可使用 `get_default_parser()` 函数来获取默认解析器。

```python
etree.get_default_parser()
#> <lxml.etree.XMLParser at 0x26faf65f800>
```

如果需要对解释器进行配置，可以创建一个新实例:

```python
parser = etree.XMLParser(remove_blank_text=True) # lxml.etree only!
# This creates a parser that removes empty text between tags while parsing, which can reduce the size of the tree and avoid dangling tail text if you know that whitespace-only content is not meaningful for your data. An example:
root = etree.XML("<root>  <a/>   <b>  </b>     </root>", parser)
etree.tostring(root)
#> b'<root><a/><b>  </b></root>'

# Note that the whitespace content inside the <b> tag was not removed, as content at leaf elements tends to be data content (even if blank). You can easily remove it in an additional step by traversing the tree:
for element in root.iter("*"):
    if element.text is not None and not element.text.strip():
        element.text = None

etree.tostring(root)
#> b'<root><a/><b/></root>'

# See help(etree.XMLParser) to find out about the available parser options.
```



### ETCompatXMLParser🛠

[ETCompatXMLParser](https://lxml.de/api/lxml.etree.ETCompatXMLParser-class.html)(self, encoding=None, attribute_defaults=False, dtd_validation=False, load_dtd=False, no_network=True, ns_clean=False, recover=False, schema=None, huge_tree=False, remove_blank_text=False, resolve_entities=True, remove_comments=True, remove_pis=True, strip_cdata=True, target=None, compact=True)

> An XML parser with an ElementTree compatible default setup.

### HTMLParser🛠

[HTMLParser](https://lxml.de/api/lxml.etree.HTMLParser-class.html)(self, encoding=None, remove_blank_text=False, remove_comments=False, remove_pis=False, strip_cdata=True, no_network=True, target=None, schema: XMLSchema =None, recover=True, compact=True, collect_ids=True, huge_tree=False)

> The HTML parser.
>
> This parser allows reading HTML into a normal XML tree. By default, it can read broken (non well-formed) HTML, depending on the capabilities of libxml2. Use the 'recover' option to switch this off.

### XMLParser🛠

[XMLParser](https://lxml.de/api/lxml.etree.XMLParser-class.html)(self, encoding=None, attribute_defaults=False, dtd_validation=False, load_dtd=False, no_network=True, ns_clean=False, recover=False, schema: XMLSchema =None, huge_tree=False, remove_blank_text=False, resolve_entities=True, remove_comments=False, remove_pis=False, strip_cdata=True, collect_ids=True, target=None, compact=True)

> The XML parser.
>
> Parsers can be supplied as additional argument to various parse functions of the lxml API. A default parser is always available and can be replaced by a call to the global function 'set_default_parser'. New parsers can be created at any time without a major run-time overhead.

### get_default_parser()🔨

🔨get_default_parser()

获取默认解析器:

```python
etree.get_default_parser()
#> <lxml.etree.XMLParser at 0x26faf65f800>
```

### set_default_parser()🔨

🔨set_default_parser(parser=None)

> Set a default parser for the current thread. This parser is used globally whenever no parser is supplied to the various parse functions of the lxml API. If this function is called without a parser (or if it is None), the default parser is reset to the original configuration.
>
> Note that the pre-installed default parser is not thread-safe. Avoid the default parser in multi-threaded environments. You can create a separate parser for each thread explicitly or use a parser pool.

## 解析 HTML

[HTMLParser🛠](#HTMLParser🛠) 解析器支持解析(*broken*) HTML，它拥有一个名为 *recover* 关键字参数(默认值是 `True`)。当 `recover=True` 时，会产生如下效果:

- libxml2 会尽力返回一个有效的 HTML 树，在该树中包含了所有可解析的内容

  > You should use libxml2 version 2.6.21 or newer to take advantage of this feature.

- 在出现解析错误时不会抛出异常

```python
from io import StringIO
broken_html = "<html><head><title>test<body><h1>page title</h3>"

parser = etree.HTMLParser()
tree   = etree.parse(StringIO(broken_html), parser)

result = etree.tostring(tree.getroot(),
                        pretty_print=True, method="html")
print(result)
#> b'<html>\n<head><title>test</title></head>\n<body><h1>page title</h1></body>\n</html>\n'
```

HTML 解析器旨在解析 HTML 文档。如果要解析 XHTML 文档，请使用可识别命名空间的 XML 解析器。

`HTML()` 函数类似于 `XML()`，但被用于解析 HTML:

```python
broken_html = "<html><head><title>test<body><h1>page title</h3>"
html = etree.HTML(broken_html)
result = etree.tostring(html, pretty_print=True, method="html")
print(result)
#> b'<html>\n<head><title>test</title></head>\n<body><h1>page title</h1></body>\n</html>\n'
```

> The support for parsing broken HTML depends entirely on libxml2's recovery algorithm. It is *not* the fault of lxml if you find documents that are so heavily broken that the parser cannot handle them. There is also no guarantee that the resulting tree will contain all data from the original document. The parser may have to drop seriously broken parts when struggling to keep parsing. Especially misplaced meta tags can suffer from this, which may lead to encoding problems.
>
> Note that the result is a valid HTML tree, but it may not be a well-formed XML tree. For example, XML forbids double hyphens in comments, which the HTML parser will happily accept in recovery mode. Therefore, if your goal is to serialise an HTML document as an XML/XHTML document after parsing, you may have to apply some manual preprocessing first.



## Python Unicode 字符串

> 参考: [Python unicode strings](https://lxml.de/parsing.html#python-unicode-strings)
>
> 扩展阅读:
>
> - https://lxml.de/FAQ.html#why-can-t-lxml-parse-my-xml-from-unicode-strings
> - https://lxml.de/FAQ.html#can-lxml-parse-from-file-objects-opened-in-unicode-text-mode

`lxml.etree` 库与 `ElementTree` 库相比，前者对 Python Unicode 字符串提供了更广泛的支持。首先，在 `ElementTree` 因 Unicode 抛出异常的地方，`lxml.etree` 中的解析器可直接处理这些 Unicode。这对于使用 `XML()` 函数嵌入源代码中的 XML 片段最有帮助:

```python
root = etree.XML('<test>\u9cb8\u9c7c</test>' )
etree.tounicode(root)
```

但是，这要求 Unicode 字符串本身不指定冲突的编码:

```python
etree.XML( '<?xml version="1.0" encoding="ASCII"?>\n<test>\u9cb8\u9c7c</test>')
'''Out:
ValueError                                Traceback (most recent call last)
--snip--
ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
'''
```

类似的，当我们在 Unicode 字符串中尝试使用 HTML 数据(specifies a charset in a meta tag of the header)时，将会抛出异常。

```python
# 我不能用代码重现上面这句话，目前还不知道原因
text = '<html><head><meta charset="utf-8"><title>\u9cb8\u9c7c</title></head></html>'
r = etree.HTML(text)
etree.tounicode(r)
#> '<html><head><meta charset="utf-8"/><title>鲸鱼</title></head></html>'
```

### bytes 数据和编码问题

⚠通常情况下我们应避免在将 XML/HTML 数据传递到解析器之前，将其转换为 Unicode (这样做既慢又容易出错)。也就是说，被解析的文本最好是 `bytes` 类型，通常情况下解析器会根据 HTML  `mate` 标记来识别编码方式。当我们需要将 `bytes` 类型的数据解码为 Unicode 字符串(或转换为其它编码方式的 `bytes` 字符串)时，便会以 `mate` 标记给出的编码方案为准。

如果缺少 HTML `mate` 标记，则会默认采用  `ascii` 编码方式。此时可以创建 `HTMLParser` (或 `XMLParser`) 实例，并在构造函数中传入所需的编码方案，详见:

- https://lxml.de/FAQ.html#why-can-t-lxml-parse-my-xml-from-unicode-strings
- https://lxml.de/FAQ.html#can-lxml-parse-from-file-objects-opened-in-unicode-text-mode

```python
html_unicode = """
<html><head>
<title>鲸鱼</title>
</head>
"""
html_doc = html_unicode.encode('utf8') # 将unicode字符串编码为gb2312字节码
root = html.document_fromstring(html_doc,parser = etree.HTMLParser(encoding='utf8'))
print(etree.tounicode(root))
print(etree.tostring(root))
print(root.getroottree().docinfo.encoding)
```

输出

```
<html><head>
<title>鲸鱼</title>
</head>
</html>
b'<html><head>\n<title>&#40120;&#40060;</title>\n</head>\n</html>'
utf8
```

如果不设置编码方式，则会出现乱码:

```python
html_unicode = """
<html><head>
<title>鲸鱼</title>
</head>
"""
html_doc = html_unicode.encode('utf8')
root = html.document_fromstring(html_doc)
print(etree.tounicode(root))
print(etree.tostring(root))
print(root.getroottree().docinfo.encoding)
```

输出:

```
<html><head>
<title>é²¸é±¼</title>
</head>
</html>
b'<html><head>\n<title>&#233;&#178;&#184;&#233;&#177;&#188;</title>\n</head>\n</html>'
UTF-8
```



### 序列化为Unicode字符串

如果对结果进行序列化，通常会使用 `tostring()` 模块函数。默认情况下 `tostring()` 会将结果序列化为纯 ASCII:

```python
root = etree.XML( u'<test> \uf8d1 + \uf8d2 </test>' )
etree.tostring(root)
#> b'<test> &#63697; + &#63698; </test>'
etree.tostring(root, encoding='UTF-8', xml_declaration=False)
#> b'<test> \xef\xa3\x91 + \xef\xa3\x92 </test>'
```

如果需要为树构建 Python Unicode 表示，可将 `'unicode'` 作为 `encoding` 的实参:

```python
root = etree.XML( u'<test> \uf8d1 + \uf8d2 </test>' )
etree.tostring(root, encoding='unicode')
#> '<test> \uf8d1 + \uf8d2 </test>'
el = etree.Element("test")
etree.tostring(el, encoding='unicode')
#> '<test/>'
subel = etree.SubElement(el, "subtest")
etree.tostring(el, encoding='unicode')
#> '<test><subtest/><subtest/><subtest/></test>'
tree = etree.ElementTree(el)
etree.tostring(tree, encoding='unicode')
#> '<test><subtest/><subtest/><subtest/></test>'
```

> The result of `tostring(encoding='unicode')` can be treated like any other Python unicode string and then passed back into the parsers. However, if you want to save the result to a file or pass it over the network, you should use `write()` or `tostring()` with a byte encoding (typically UTF-8) to serialize the XML. The main reason is that unicode strings returned by `tostring(encoding='unicode')` are not byte streams and they never have an XML declaration to specify their encoding. These strings are most likely not parsable by other XML libraries.
>
> For normal byte encodings, the `tostring()` function automatically adds a declaration as needed that reflects the encoding of the returned string. This makes it possible for other parsers to correctly parse the XML byte stream. Note that using `tostring()` with UTF-8 is also considerably faster in most cases.



## 序列化 Element

> 参考: <https://lxml.de/api/lxml.etree-module.html>

### dump()🔨

> 🔨dump(elem, pretty_print=True, with_tail=True)
> Writes an element tree or element structure to sys.stdout. This function should be used for debugging only.

### tostring()🔨

🔨tostring(element_or_tree, encoding=None, method="xml", xml_declaration=None, pretty_print=False,with_tail=True, standalone=None, doctype=None, exclusive=False, with_comments=True,inclusive_ns_prefixes=None)

```python
>>> some_xml_data = "<root>data</root>"

>>> root = etree.fromstring(some_xml_data)
>>> print(root.tag)
root
>>> etree.tostring(root)
b'<root>data</root>'
```

Serialize an element to an encoded string representation of its XML tree.

Defaults to ASCII encoding without XML declaration. This behaviour can be configured with the keyword arguments '`encoding`' (string) and 'xml_declaration' (bool). Note that changing the encoding to a non UTF-8 compatible encoding will enable a declaration by default.

You can also serialise to a Unicode string without declaration by passing the name `'unicode'` as encoding (or the `str` function in Py3 or `unicode` in Py2). This changes the return value from a byte string to an unencoded unicode string.

The keyword argument '`pretty_print`' (bool) enables formatted XML.

The keyword argument '`method`' selects the output method: 'xml', 'html', plain 'text' (text content without tags) or 'c14n'. Default is 'xml'.

The `exclusive` and `with_comments` arguments are only used with C14N output, where they request exclusive and uncommented C14N serialisation respectively.

Passing a boolean value to the `standalone` option will output an XML declaration with the corresponding `standalone` flag.

The `doctype` option allows passing in a plain string that will be serialised before the XML tree. Note that passing in non well-formed content here will make the XML output non well-formed. Also, an existing doctype in the document tree will not be removed when serialising an ElementTree instance.

You can prevent the tail text of the element from being serialised by passing the boolean `with_tail` option. This has no impact on the tail text of children, which will always be serialised.

### tostringlist()🔨

🔨tostringlist(element_or_tree, *args, **kwargs)

Serialize an element to an encoded string representation of its XML tree, stored in a list of partial strings.

This is purely for ElementTree 1.3 compatibility. The result is a single string wrapped in a list.

### tounicode()🔨

🔨tounicode(element_or_tree, method="xml", pretty_print=False, with_tail=True, doctype=None)

Serialize an element to the Python unicode representation of its XML tree.

Note that the result does not carry an XML encoding declaration and is therefore not necessarily suited for serialization to byte streams without further treatment.

The boolean keyword argument 'pretty_print' enables formatted XML.

The keyword argument 'method' selects the output method: 'xml', 'html' or plain 'text'.

You can prevent the tail text of the element from being serialised by passing the boolean `with_tail` option. This has no impact on the tail text of children, which will always be serialised.

**Deprecated:** use `tostring(el, encoding='unicode')` instead.

### _ElementTree.write()🔨

[_ElementTree](https://lxml.de/api/lxml.etree._ElementTree-class.html).[write](https://lxml.de/api/lxml.etree._ElementTree-class.html#write)() 方法可将 ElementTree 序列化至文件中:

> 🔨write(self, file, encoding=None, method="xml", pretty_print=False, xml_declaration=None, with_tail=True, standalone=None, doctype=None, compression=0, exclusive=False, with_comments=True, inclusive_ns_prefixes=None)
>
> Write the tree to a filename, file or file-like object.
>
> Defaults to ASCII encoding and writing a declaration as needed.
>
> The keyword argument 'method' selects the output method: 'xml', 'html', 'text' or 'c14n'. Default is 'xml'.
>
> The `exclusive` and `with_comments` arguments are only used with C14N output, where they request exclusive and uncommented C14N serialisation respectively.
>
> Passing a boolean value to the `standalone` option will output an XML declaration with the corresponding `standalone` flag.
>
> The `doctype` option allows passing in a plain string that will be serialised before the XML tree. Note that passing in non well-formed content here will make the XML output non well-formed. Also, an existing doctype in the document tree will not be removed when serialising an ElementTree instance.
>
> The `compression` option enables GZip compression level 1-9.
>
> The `inclusive_ns_prefixes` should be a list of namespace strings (i.e. ['xs', 'xsi']) that will be promoted to the top-level element during exclusive C14N serialisation. This parameter is ignored if exclusive mode=False.
>
> If exclusive=True and no list is provided, a namespace will only be rendered if it is used by the immediate parent or one of its attributes and its prefix and values have not already been rendered by an ancestor of the namespace node's parent element.

## XPath with lxml

> 参考:
>
> - <https://lxml.de/xpathxslt.html>

lxml.etree 支持两种路径语言: 

- [ElementPath](https://lxml.de/tutorial.html#elementpath) - 一种 XPath-like 路径语言，属于 XPath 的简化版。Element 和 ElementTree 中的 `iterfind()`, `findall()`, `find()`, `findtext()` 方法支持 `ElementPath` 语法。

  > <https://lxml.de/tutorial.html#elementpath>
  >
  > The ElementTree library comes with a simple XPath-like path language called [ElementPath](http://effbot.org/zone/element-xpath.htm). The main difference is that you can use the `{namespace}tag`notation in ElementPath expressions. However, advanced features like value comparison and functions are not available.
  >
  > In addition to a [full XPath implementation](https://lxml.de/xpathxslt.html#xpath), `lxml.etree` supports the ElementPath language in the same way ElementTree does, even using (almost) the same implementation. The API provides four methods here that you can find on Elements and ElementTrees:
  >
  > - `iterfind()` iterates over all Elements that match the path expression
  > - `findall()` returns a list of matching Elements
  > - `find()` efficiently returns only the first match
  > - `findtext()` returns the `.text` content of the first match

  如需了解更多信息可参考:

  - [ElementPath](https://lxml.de/tutorial.html#elementpath)
  - [XPath Support in ElementTree](https://effbot.org/zone/element-xpath.htm)
  - [XPath support](https://docs.python.org/3/library/xml.etree.elementtree.html#finding-interesting-elements)

- 完整的 XPath - Element 和 ElementTree 的 `xpath()` 方法支持完整的 XPath 语法表达式和自定义扩展函数( [custom extension functions](https://lxml.de/extensions.html#xpath-extension-functions))。

  如需了解更多信息可参考:

  - [XPath and XSLT with lxml](https://lxml.de/xpathxslt.html)
  - [Using XPath to find text](https://lxml.de/tutorial.html#using-xpath-to-find-text)
  - [10. XPath processing](https://infohost.nmt.edu/tcc/help/pubs/pylxml/web/xpath.html)
  - 笔记﹝[XPath.md](./XPath.md)﹞
  
  注意，lxml 仅支持 [XML Path Language (XPath) Version 1.0](http://www.w3.org/TR/1999/REC-xpath-19991116/)

lxml.etree 还提供了的 XPath evaluator 类: lxml.etree.[XPath](https://lxml.de/api/lxml.etree.XPath-class.html) 和 lxml.etree.[XPathEvaluator](https://lxml.de/api/lxml.etree-module.html#XPathEvaluator)

> There are also specialized XPath evaluator classes that are more efficient for frequent evaluation: `XPath` and `XPathEvaluator`. See the [performance comparison](https://lxml.de/performance.html#xpath)to learn when to use which. Their semantics when used on Elements and ElementTrees are the same as for the `xpath()` method described here.
>
> 详见:
>
> - [The `XPath` class](https://lxml.de/xpathxslt.html#the-xpath-class)
> - [The `XPathEvaluator` classes](https://lxml.de/xpathxslt.html#the-xpathevaluator-classes)

### xpath()🔨

> 更多细节详见: 
>
> - <https://lxml.de/xpathxslt.html>
> - [9.21. Element.xpath(): Evaluate an XPath expression](https://infohost.nmt.edu/tcc/help/pubs/pylxml/web/Element-xpath.html)

🔨xpath(self, \_path, namespaces=None, extensions=None, smart_strings=True, \*\*\_variables)

在 ElementTree 对象上调用 `xpath()` 方法时，将针对该文档(如果是绝对路径)或根节点(如果是相对路径)执行全局 XPath 查询:

```python
from lxml import etree, html
from io import StringIO

broken_html = '''\
<foo>
    <bar>zero</bar>
    <bar>one\
</foo> '''

# 解析html
f = StringIO(broken_html)
tree = html.parse(f)
print(etree.tounicode(tree))
'''Out:
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html><body><foo>
    <bar>zero</bar>
    <bar>one</bar></foo> </body></html>'''
# 由于html.parse()会对HTML文档进行修正，因此绝对路径应以/html/body开头
r1 = tree.xpath('/html/body/foo/bar')
print([e.text for e in r1])
#> ['zero', 'one']
# 由于html.parse()会对HTML文档进行修正，因此根节点是html
r2 = tree.xpath('body/foo/bar')
print([e.text for e in r1])
#> ['zero', 'one']

# 解析xml
f = StringIO('<foo><bar>zero</bar><bar>one</bar></foo>')
tree_ = etree.parse(f)
print(etree.tounicode(tree_))
#> <foo><bar>zero</bar><bar>one</bar></foo>

r1_ = tree_.xpath('/foo/bar')
print([e.text for e in r1_])
#> ['zero', 'one']

r2_ = tree_.xpath('bar')
print([e.text for e in r2_])
#> ['zero', 'one']
```

在 Element 对象上调用 `xpath()` 方法时，将针对该元素(如果是相对路径)或根节点(如果是绝对路径)执行全局 XPath 查询:

```python
from lxml import etree, html
from io import StringIO

broken_html = '''\
<foo>
    <bar>zero</bar>
    <bar>one\
</foo> '''

# 解析html
f = StringIO(broken_html)
tree = html.parse(f)
root = tree.getroot()
print(etree.tounicode(root))
'''Out:
<html><body><foo>
    <bar>zero</bar>
    <bar>one</bar></foo> </body></html>'''
# 由于html.parse()会对HTML文档进行修正，因此绝对路径应以/html/body开头
r1 = root.xpath('/html/body/foo/bar')
print([e.text for e in r1])
#> ['zero', 'one']
# 由于html.parse()会对HTML文档进行修正，因此根节点是html
r2 = root.xpath('body/foo/bar')
print([e.text for e in r1])
#> ['zero', 'one']

# 解析xml
f = StringIO('<foo><bar>zero</bar><bar>one</bar></foo>')
tree_ = etree.parse(f)
root_ = tree_.getroot()
print(etree.tounicode(root_))
#> <foo><bar>zero</bar><bar>one</bar></foo>
r1_ = root_.xpath('/foo/bar')
print([e.text for e in r1_])
#> ['zero', 'one']
r2_ = root_.xpath('bar')
print([e.text for e in r2_])
#> ['zero', 'one']
```

`xpath()` 方法支持 XPath 变量:

```python
f = StringIO('<foo><bar>zero</bar><bar>one</bar></foo>')
tree_ = etree.parse(f)
root_ = tree_.getroot()
print(etree.tounicode(root_))
expr = "//*[local-name() = $name]" # fn:local-name()
print(root.xpath(expr, name="foo")[0].tag)
print(root.xpath(expr, name="bar")[0].tag)
print(root.xpath("$text", text="Hello World!"))
'''Out:
<foo><bar>zero</bar><bar>one</bar></foo>
foo
bar
Hello World!'''
```

#### 返回值

The returned value may be any of:

- A list of zero or more selected `Element` instances.
- A Python `bool` value for true/false tests.
- A Python `float` value for numeric results.
- A string for string results. 比如，文本节点和属性节点

详见: [XPath return values](https://lxml.de/xpathxslt.html#xpath-return-values)

### 获取后代节点

对于元素节点，`Element.xpath()` 将返回一个由元素构成的列表。

```python
from lxml import html, etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">1 item</a></li>
         <li class="item-1"><a href="link2.html">2 item</a></li>
         <li class="item-3"><a href="link3.html">3 item</a></li>
         <li class="item-1"><a href="link4.html">4 item</a></li>
         <li class="item-0"><a href="link5.html">5 item</a>
     </ul>
 </div>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

print(e.xpath('//*'))  # 选取所有后代节点
'''Out:
[<Element html at 0x253594d9728>, 
    <Element body at 0x2535b15bf48>, 
        <Element div at 0x2535b2bce08>, 
            <Element ul at 0x2535b4a8138>, 
                <Element li at 0x2535b4a8188>, 
                    <Element a at 0x2535b4a81d8>, 
                <Element li at 0x2535b4a8228>, 
                    <Element a at 0x2535b4a8278>, 
                <Element li at 0x2535b4a82c8>, 
                    <Element a at 0x2535b4a8318>, 
                <Element li at 0x2535b4a8368>, 
                    <Element a at 0x2535b4a83b8>, 
                <Element li at 0x2535b4a8408>, 
                    <Element a at 0x2535b4a8458>]
'''
print(e.xpath('//a'))  # 选取指定的后代节点
'''Out:
[<Element a at 0x2535b15bf48>, 
<Element a at 0x2535b2bce08>, 
<Element a at 0x2535b4a8138>, 
<Element a at 0x2535b4a8188>, 
<Element a at 0x2535b4a81d8>]
'''
```



### 获取子节点

对于元素节点，`Element.xpath()` 将返回一个由元素构成的列表。

```python
from lxml import html, etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">1 item</a></li>
         <li class="item-1"><a href="link2.html">2 item</a></li>
         <li class="item-3"><a href="link3.html">3 item</a></li>
         <li class="item-1"><a href="link4.html">4 item</a></li>
         <li class="item-0"><a href="link5.html">5 item</a>
     </ul>
 </div>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

print(e.xpath('//li/a'))  # 获取所有li元素节点的a元素子节点
'''Out:
[<Element a at 0x20b40bdbf48>, 
<Element a at 0x20b40d3ce08>, 
<Element a at 0x20b40f16188>, 
<Element a at 0x20b40f161d8>, 
<Element a at 0x20b40f16228>]'''
print(e.xpath('//ul/a')) # '/'只能获取子节点，不能用于获取全部后代
#> []
```



### 获取父节点

对于元素节点，`Element.xpath()` 将返回一个由元素构成的列表。
对于属性节点，`Element.xpath()` 将返回一个由字符串组成的列表。

```python
from lxml import html, etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">1 item</a></li>
         <li class="item-1"><a href="link2.html">2 item</a></li>
         <li class="item-3"><a href="link3.html">3 item</a></li>
         <li class="item-1"><a href="link4.html">4 item</a></li>
         <li class="item-0"><a href="link5.html">5 item</a>
     </ul>
 </div>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

print(e.xpath('//a[@href="link4.html"]/..'))
#> [<Element li at 0x24ad2cf6278>]
print(e.xpath('//a[@href="link4.html"]/parent::*'))
#> [<Element li at 0x24ad2cf6278>]
print(e.xpath('//a[@href="link4.html"]/../@class'))
#> ['item-1']
```



### 获取文本

对于文本节点，`Element.xpath()` 将返回一个由字符串组成的列表。

```python
text = '''
<book>
    <author>Tom <em>John</em> cat</author>
    <author>Tom_ <em>John_</em> cat_</author>
    <pricing>
        <price>20</price>
        <discount>0.8</discount>
    </pricing>
</book>
'''
elem = html.fromstring(text)
# 获取author的子文本节点
print(elem.xpath('/html/body/book/author/text()'))
#> ['Tom ', ' cat', 'Tom_ ', ' cat_']

# 获取author的所有后代的文本节点
print(elem.xpath('/html/body/book/author//text()'))
#> ['Tom ', 'John', ' cat', 'Tom_ ', 'John_', ' cat_']
```



### 筛选单值属性

在选取节点时，我们可使用 `[@xxx]` 进行属性筛选。
对于元素节点，`Element.xpath()` 将返回一个由元素构成的列表。
对于文本节点，`Element.xpath()` 将返回一个由字符串组成的列表。

```python
from lxml import html, etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">1 item</a></li>
         <li class="item-1"><a href="link2.html">2 item</a></li>
         <li class="item-3"><a href="link3.html">3 item</a></li>
         <li class="item-1"><a href="link4.html">4 item</a></li>
         <li class="item-0"><a href="link5.html">5 item</a>
     </ul>
 </div>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

print(e.xpath('//li[@class="item-1"]'))
#> [<Element li at 0x2a376e1bef8>, <Element li at 0x2a376f7ce08>]
print(e.xpath('//li[@class="item-1"]//text()'))
#> ['2 item', '4 item']
```

### 筛选多值属性

```python
from lxml import html, etree
text = '''
<li class="li li-first"><a href="link.html">1 item</a></li>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

# 如果属性包含多个值,如果要匹配其中的某个值,则需要使用contains()函数
print(e.xpath('//li[contains(@class, "li")]'))
#> [<Element li at 0x257acbabef8>]

# 如果不使用contains()函数,则无法筛选出多属性元素
print(e.xpath('//li[@class="li"]'))
#> []
```

此种选择方式在某个节点的某个属性有多个值的时候经常会用到，如某个节点的 class 属性通常有多个。

### 匹配多个属性

我们可以根据多个属性来确定一个节点:

```python
from lxml import html, etree
text = '''
<li class="li li-first" name="item"><a href="link.html">first item</a></li>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

# 使用and来同时匹配多个属性
print(e.xpath('//li[contains(@class, "li") and @name="item"]/a/text()'))
#> ['first item']
```

这里的 and 其实是 XPath 中的运算符，另外还有很多运算符，如 or、mod 等等，在此总结如下：

| 运算符 | 描述           | 实例                      | 返回值                                                       |
| :----- | :------------- | :------------------------ | :----------------------------------------------------------- |
| \|     | 计算两个节点集 | //book \| //cd            | 返回所有拥有 book 和 cd 元素的节点集                         |
| +      | 加法           | 6 + 4                     | 10                                                           |
| -      | 减法           | 6 - 4                     | 2                                                            |
| *      | 乘法           | 6 * 4                     | 24                                                           |
| div    | 除法           | 8 div 4                   | 2                                                            |
| =      | 等于           | price=9.80                | 如果 price 是 9.80，则返回 true。如果 price 是 9.90，则返回 false。 |
| !=     | 不等于         | price!=9.80               | 如果 price 是 9.90，则返回 true。如果 price 是 9.80，则返回 false。 |
| <      | 小于           | price<9.80                | 如果 price 是 9.00，则返回 true。如果 price 是 9.90，则返回 false。 |
| <=     | 小于或等于     | price<=9.80               | 如果 price 是 9.00，则返回 true。如果 price 是 9.90，则返回 false。 |
| >      | 大于           | price>9.80                | 如果 price 是 9.90，则返回 true。如果 price 是 9.80，则返回 false。 |
| >=     | 大于或等于     | price>=9.80               | 如果 price 是 9.90，则返回 true。如果 price 是 9.70，则返回 false。 |
| or     | 或             | price=9.80 or price=9.70  | 如果 price 是 9.80，则返回 true。如果 price 是 9.50，则返回 false。 |
| and    | 与             | price>9.00 and price<9.90 | 如果 price 是 9.80，则返回 true。如果 price 是 8.50，则返回 false。 |
| mod    | 计算除法的余数 | 5 mod 2                   | 1                                                            |

### 获取属性

可使用 `@xxx` 来获取属性节点。
对于属性节点，`Element.xpath()` 将返回一个由字符串组成的列表。

```python
from lxml import html, etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">1 item</a></li>
         <li class="item-1"><a href="link2.html">2 item</a></li>
         <li class="item-3"><a href="link3.html">3 item</a></li>
         <li class="item-1"><a href="link4.html">4 item</a></li>
         <li class="item-0"><a href="link5.html">5 item</a>
     </ul>
 </div>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

print(e.xpath('//li/a/@href'))
#> ['link1.html', 'link2.html', 'link3.html', 'link4.html', 'link5.html']
```

### 按位置筛选



```python
from lxml import html, etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">1 item</a></li>
         <li class="item-1"><a href="link2.html">2 item</a></li>
         <li class="item-3"><a href="link3.html">3 item</a></li>
         <li class="item-1"><a href="link4.html">4 item</a></li>
         <li class="item-0"><a href="link5.html">5 item</a>
     </ul>
 </div>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

# 注意，以1为起点
print(e.xpath('//li[1]/a/text()'))
#> ['1 item']
print(e.xpath('//li[last()]/a/text()'))
#> ['5 item']
print(e.xpath('//li[last()-2]/a/text()'))
#> ['3 item']
print(e.xpath('//li[position()<3]/a/text()'))
#> ['1 item', '2 item']
```

如果了解函数的含义，可参考 <http://www.w3school.com.cn/xpath/xpath_functions.asp>

### 使用轴

```python
from lxml import html, etree
text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html"><span>1 item</span></a></li>
         <li class="item-1"><a href="link2.html">2 item</a></li>
         <li class="item-3"><a href="link3.html">3 item</a></li>
         <li class="item-1"><a href="link4.html">4 item</a></li>
         <li class="item-0"><a href="link5.html">5 item</a>
     </ul>
 </div>
'''
# html解析器会对HTML文本进行自动修正
e = html.document_fromstring(text)

# 注意，以1为起点
print(e.xpath('//li[1]/ancestor::*'))
'''Out:
[<Element html at 0x185d69872c8>, 
<Element body at 0x185d87260e8>, 
<Element div at 0x185d877cea8>, 
<Element ul at 0x185d8936228>]'''
print(e.xpath('//li[1]/ancestor::div'))
#> [<Element div at 0x185d87260e8>]
print(e.xpath('//li[1]/attribute::*'))
#> ['item-0']
print(e.xpath('//li[1]/child::a[@href="link1.html"]'))
#> [<Element a at 0x185d87260e8>]
print(e.xpath('//li[1]/descendant::span'))
#> [<Element span at 0x185d87260e8>]
print(e.xpath('//li[1]/following::*[2]'))
#> [<Element a at 0x185d87260e8>]
print(e.xpath('//li[1]/following-sibling::*'))
'''Out:
[<Element li at 0x185d87260e8>, 
<Element li at 0x185d877cea8>, 
Element li at 0x185d8936228>, 
<Element li at 0x185d8936278>]
'''
```



## Others

在 [Parsing from strings and files](https://lxml.de/tutorial.html#parsing-from-strings-and-files) 中还包含以下内容:

- [Incremental parsing](https://lxml.de/tutorial.html#incremental-parsing) - 讲述了两种 step-by-step 解析 XML 内容的方法
- [Event-driven parsing](https://lxml.de/tutorial.html#event-driven-parsing) - 以事件驱动解析，目前仅支持 XML

在 [Parsing XML and HTML with lxml](https://lxml.de/parsing.html) 还包含以下内容:

- Parsers
  - [Parser options](https://lxml.de/parsing.html#parser-options)
  - [Error log](https://lxml.de/parsing.html#error-log)
  - [Doctype information](https://lxml.de/parsing.html#doctype-information)
- [The target parser interface](https://lxml.de/parsing.html#the-target-parser-interface)
- [The feed parser interface](https://lxml.de/parsing.html#the-feed-parser-interface)
- [Incremental event parsing](https://lxml.de/parsing.html#incremental-event-parsing)
  - [Event types](https://lxml.de/parsing.html#event-types)
  - [Modifying the tree](https://lxml.de/parsing.html#modifying-the-tree)
  - [Selective tag events](https://lxml.de/parsing.html#selective-tag-events)
  - [Comments and PIs](https://lxml.de/parsing.html#comments-and-pis)
  - [Events with custom targets](https://lxml.de/parsing.html#events-with-custom-targets)
- [iterparse and iterwalk](https://lxml.de/parsing.html#iterparse-and-iterwalk)
  - [iterwalk](https://lxml.de/parsing.html#iterwalk)



