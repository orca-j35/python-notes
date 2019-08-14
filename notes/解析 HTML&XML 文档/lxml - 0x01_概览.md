# lxml
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考: 
>
> - [`xml.etree.ElementTree`](https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree) — The ElementTree XML API
> - [lxml 学习笔记](https://www.jianshu.com/p/e084c2b2b66d)
> - [Python爬虫利器——lxml 和 xpath 表达式](http://yifei.me/note/464)
>
> 扩展阅读:
>
> - [Python HTML Parser Performance](http://www.ianbicking.org/blog/2008/03/python-html-parser-performance.html)
> - [HTML DOM 节点](http://www.w3school.com.cn/htmldom/dom_nodes.asp)
> - [How ElementTree represents XML](https://infohost.nmt.edu/tcc/help/pubs/pylxml/web/etree-view.html)

## 概述

> The lxml XML toolkit is a Pythonic binding for the C libraries [libxml2](http://xmlsoft.org/) and [libxslt](http://xmlsoft.org/XSLT/). 
>
> The lxml is the most feature-rich and easy-to-use library for processing XML and HTML in the Python language.

lxml 提供各种操作 XML 的方式，比如读取、生成、修改、解析等操作。

💾相关资源:

- Home: https://lxml.de/
- PyPI: https://pypi.org/project/lxml/
- GitHub: https://github.com/lxml/lxml
- Docs-EN: https://lxml.de/index.html#documentation
- Tutorials:
  - the [lxml.etree tutorial for XML processing](https://lxml.de/tutorial.html)
  - John Shipman's tutorial on [Python XML processing with lxml](http://www.nmt.edu/tcc/help/pubs/pylxml/) 🧀
  - Fredrik Lundh's [tutorial for ElementTree](http://effbot.org/zone/element.htm)
    - [`xml.etree.ElementTree`](http://docs.python.org/library/xml.etree.elementtree.html) is now an official part of the Python library. 
      `lxml.etree` 兼容并优于标准库中的 `xml.etree.ElementTree`， `lxml.etree` 还扩展了一些功能
  - [xml.etree.ElementTree‘s tutorial in the Python library](https://docs.python.org/3/library/xml.etree.elementtree.html#tutorial)

🧩安装:

```shell
conda install lxml
```

Tips: 如果在使用 `pip` 安装时，提示缺少依赖库(如 libxml2)，可采用 wheel 方式安装缺少库。在 https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml 中下载需要的版本(如 Win64、Python3.6 需选择 lxml‑3.8.0‑cp36‑cp36m‑win_amd64.whl)，然后在本地安装 `.whl` 文件即可。

Note: lxml 库不仅包含 `etree` 模块，还包含 `html`、`cssselect` 等模块。另外，我们还可以在 `lxml.html` 的文档中看到 BeautifulSoup 和 html5lib 的身影:

> [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) is a Python package for working with real-world and broken HTML, just like [lxml.html](https://lxml.de/lxmlhtml.html). As of version 4.x, it can use [different HTML parsers](http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser), each of which has its advantages and disadvantages (see the link).
>
> lxml can make use of BeautifulSoup as a parser backend, just like BeautifulSoup can employ lxml as a parser. 
>
> lxml interfaces with BeautifulSoup through the `lxml.html.soupparser` module. 
>
> -- 详见 https://lxml.de/elementsoup.html
>
> lxml can benefit from the parsing capabilities of html5lib through the lxml.html.html5parser module. In order to make use of the HTML5 parser of [html5lib](https://pypi.python.org/pypi/html5lib) instead, it is better to go directly through the [html5parser module](https://lxml.de/html5parser.html) in `lxml.html`.
>
> -- 详见 https://lxml.de/html5parser.html

如需了解 lxml 库的层次结构，可参考 https://lxml.de/api/index.html

## Element vs. ElementTree

> 参考:
>
> - https://docs.python.org/3/library/xml.etree.elementtree.html#xml-tree-and-elements
>
> 需要了解 Element 类?
>
> - [`etree._Element`](https://lxml.de/api/lxml.etree._Element-class.html) API
> - <https://lxml.de/tutorial.html#the-element-class>
> - <https://infohost.nmt.edu/tcc/help/pubs/pylxml/web/etree-Element.html>
> - <https://docs.python.org/3/library/xml.etree.elementtree.html#element-objects>
>
> 需要了解 ElementTree 类?
>
> - [`etree._ElementTree`](https://lxml.de/api/lxml.etree._ElementTree-class.html) API
> - <https://lxml.de/tutorial.html#the-elementtree-class>
> - <https://infohost.nmt.edu/tcc/help/pubs/pylxml/web/etree-ElementTree.html>
> - <https://docs.python.org/3/library/xml.etree.elementtree.html#elementtree-objects>

由于 XML 是一种层次化的数据格式，因此使用树(*tree*)来表示 XML 是最自然的方式。在 `lxml.etree` 模块中有两个用于此目的类: `ElementTree` 和 `Element`。`ElementTree` 类用于将整个 XML 文档表示为树，`Element` 用于表示树中的单个节点。在与整个文档进行交互(读写文件)时，通常会在 `ElementTree` 级别上完成；在与单个 XML 元素及其子元素交互时，通常会在 `Element` 级别上完成。

`ElementTree` 和 `Element` 的构造函数如下:

- 🔨Element(\_tag, attrib=None, nsmap=None, \*\*\_extra)

  > Element factory. This function returns an object implementing the Element interface.
  >
  > Also look at the [_Element.makeelement()](https://lxml.de/api/lxml.etree._Element-class.html#makeelement) and `_BaseParser.makeelement()` methods, which provide a faster way to create an Element within a specific document or parser context.

  `etree.Element()` 函数用于构造 [`etree._Element`](https://lxml.de/api/lxml.etree._Element-class.html) 实例。

  ```python
  from lxml import etree
  root = etree.Element("root")
  type(root)
  #> lxml.etree._Element
  ```

- 🔨ElementTree(*element=None*, file=None, parser=None) 

  > ElementTree wrapper class.
  
  `etree.ElementTree()` 函数用于构造 [`etree._ElementTree`](https://lxml.de/api/lxml.etree._ElementTree-class.html) 实例。

### 相互转换

如需要将 Element 转换为 ElementTree，可使用 [_Element](https://lxml.de/api/lxml.etree._Element-class.html).[getroottree](https://lxml.de/api/lxml.etree._Element-class.html#getroottree)(self) 方法:

> [getroottree](https://lxml.de/api/lxml.etree._Element-class.html#getroottree)(self)
> Return an ElementTree for the root node of the document that contains this element.

如需要将 ElementTree 转换为 Element，可使用 [_ElementTree](https://lxml.de/api/lxml.etree._ElementTree-class.html).getroot(self) 方法:

> **getroot**(self)
> Gets the root element for this tree.

### Element Object

如果需要了解 Element 对象的接口，可参考以下内容:

- [Element Objects - 标准库文档](https://docs.python.org/3/library/xml.etree.elementtree.html#element-objects)
- [The Element class](https://lxml.de/tutorial.html#the-element-class)
- [Python爬虫利器——lxml 和 xpath 表达式](http://yifei.me/note/464)
- [lxml 学习笔记](https://www.jianshu.com/p/e084c2b2b66d)
- <https://lxml.de/api/lxml.etree._Element-class.html>

### ElementTree Object

如果需要了解 ElementTree 对象的接口，可参考以下内容:

- [ElementTree Objects - 标准库文档](https://docs.python.org/3/library/xml.etree.elementtree.html#elementtree-objects)
- [The ElementTree class](https://lxml.de/tutorial.html#the-elementtree-class)
- <https://lxml.de/api/lxml.etree._ElementTree-class.html>

 Note: Element 和 ElementTree 之间没有继承关系

## Element tree vs. DOM tree 

> 参考:
>
> - [How ElementTree represents XML](https://infohost.nmt.edu/tcc/help/pubs/pylxml/web/etree-view.html)
> - <https://lxml.de/api/lxml.etree._Element-class.html>
> - <https://docs.python.org/3/library/xml.etree.elementtree.html#element-objects>
>
> 扩展阅读:
>
> - [XML DOM 教程](http://www.w3school.com.cn/xmldom/index.asp)
> - [HTML DOM 教程](http://www.w3school.com.cn/htmldom/index.asp)

XML Element tree 和 XML DOM tree 的树状结构并不相同。
DOM 树由[节点(*Node*)](http://www.w3school.com.cn/xmldom/dom_nodes.asp)组成，XML 文档中的每个部分均被视为一个节点:

- 整个文档是一个文档节点
- 每个 XML 标签是一个元素节点
- 包含在 XML 元素中的文本是文本节点
- 每一个 XML 属性是一个属性节点
- 注释属于注释节点

示例 - DOM tree:

```xml
<p>To find out
    <em>more</em>, see the
    <a href="http://www.w3.org/XML">standard</a>.
</p>
```

![dom-view](lxml - 0x01_概览.assets/dom-view.png)

`lxml.etree` 仅使用元素([`etree._Element`](https://lxml.de/api/lxml.etree._Element-class.html))节点来构建树，[`etree._Element`](https://lxml.de/api/lxml.etree._Element-class.html) 对象包含如下属性:

- `attrib`
  Element attribute dictionary. Where possible, use get(), set(), keys(), values() and items() to access element attributes. 
  For example, for the element “`<h2 class="arch" id="N15">`”, that element's `.attrib` would be the dictionary “`{"class": "arch", "id": "N15"}`”.

- [`base`](https://lxml.de/api/lxml.etree._Element-class.html#base) 
  The base URI of the Element (xml:base or HTML base URL). None if the base URI is unknown. 

- [`nsmap`](https://lxml.de/api/lxml.etree._Element-class.html#nsmap) 
  Namespace prefix->URI mapping known in the context of this Element. This includes all namespace declarations of the parents. 

- `prefix` 
  Namespace prefix or None. 

- `sourceline` 
  Original line number as found by the parser or None if unknown.

- `tag` 
  Element tag. The name of the element, such as `"p"` for a paragraph or `"em"` for emphasis.

- `tail` 
  Text after this element's end tag, but before the next sibling element's start tag. This is either a string or the value None, if there was no text. 
  In the DOM model, any text following an element `*E*` is associated with the parent of `*E*`; in `lxml`, that text is considered the “tail” of `*E*`.

- `text` 
  Text before the first subelement. This is either a string or the value None, if there was no text.

- (element children)

  To access sub-elements, treat an element as a list. For example, if `node` is an `Element` instance, `node[0]` is the first sub-element of `node`. If `node` doesn't have any sub-elements, this operation will raise an `IndexError` exception.

  You can find out the number of sub-elements using the `len()` function. For example, if `node` has five children, `len(node)`will return a value of 5.

One advantage of the `lxml` view is that a tree is now made of only one type of node: each node is an `Element` instance. 

示例 - Element tree:

```xml
<p>To find out
    <em>more</em>, see the
    <a href="http://www.w3.org/XML">standard</a>.
</p>
```

![et-view](lxml - 0x01_概览.assets/et-view.png)

Notice that in the `lxml` view, the text `", see the\n"` (which includes the newline) is contained in the `.tail` attribute of the `em`element, not associated with the `p` element as it would be in the DOM view. Also, the `"."` at the end of the paragraph is in the `.tail` attribute of the `a` (link) element.

