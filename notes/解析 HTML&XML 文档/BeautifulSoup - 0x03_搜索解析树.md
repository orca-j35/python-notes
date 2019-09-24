# BeautifulSoup - 搜索解析树

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree



## 概述

BeautifulSoup 中定义了许多搜索解析树的方法，但这些方法都非常类似，它们大多采用与 `find_all()` 相同的参数: *name*、*attrs*、*string*、*limit* 和 \*\*kwargs，但是仅有 `find()` 和 `find_all()` 支持 *recursive* 参数。

这里着重介绍 `find()` 和 `find_all()`，其它"搜索方法"也这两个类似。



### Three sisters

本节会以 "three sister" 作为示例:

```python
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
        and they lived at the bottom of a well.
    </p>

    <p class="story">...</p>
"""
from pprint import pprint
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(html_doc, 'html.parser')
```



## 过滤器

过滤器(*filter*)用于在解析树中筛选目标节点，被用作"搜索方法"的实参。



### 字符串

字符串可用作过滤器，BeautifulSoup 可利用字符串来筛选节点，并保留符合条件节点:

- 使用字符串筛选 tag 时，会保留与字符串同名 tag 节点，且总会过滤掉 HTML 文本节点
- 使用字符串筛选 HTML 属性时，会保留属性值与字符串相同的 tag 节点，且总会过滤掉 HTML 文本节点
- 使用字符串筛选 HTML 文本时，会保留与字符串相同的文本节点

与 `str` 字符串类似，我们还可将 `bytes` 对象用作过滤器，区别在于 BeautifulSoup 会假定编码模式为 UTF-8。

示例:

```python
soup = BeautifulSoup(html_doc, 'html.parser')
# 查找名为b的tag节点
print([f"{type(i)}::{i.name}" for i in soup.find_all('b')])
print([f"{type(i)}::{i.name}" for i in soup.find_all(b'b')])
# 查找id值为link1的tag节点
print([f"{type(i)}::{i.name}" for i in soup.find_all(id='link1')])
# 查找文本值为Elsie的文本节点
print([f"{type(i)}::{i.name}" for i in soup.find_all(text='Elsie')])
```

输出:

```
["<class 'bs4.element.Tag'>::b"]
["<class 'bs4.element.Tag'>::b"]
["<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.NavigableString'>::None"]
```



### 正则表达式

正则表达式对象可用作过滤器，BeautifulSoup 会利用正则表达式对象的 `search()` 方法来筛选节点，并保留符合条件节点:

- 使用正则表达式对象筛选 tag 时，会利用正则表达式的 `search()` 方法来筛选 tag 节点的名称，并保留符合条件的 tag 节点。因为文本节点的 `.name` 属性值为 `None`，因此总会过滤掉 HTML 文本节点
- 使用正则表达式对象筛选 HTML 属性时，会利用正则表达式的 `search()` 方法来筛选指定属性的值，并保留符合条件的 tag 节点。因为文本节点不包含任何 HTML 属性，因此总会过滤掉 HTML 文本节点
- 使用正则表达式对象筛选 HTML 文本时，会利用正则表达式的 `search()` 方法来筛选文本节点，并保留符合条件的文本节点。

示例:

```python
import re

soup = BeautifulSoup(html_doc, 'html.parser')
# 查找名称中包含字母b的节点
print([f"{type(i)}::{i.name}" for i in soup.find_all(re.compile(r'b'))])
# 查找class值以t开头的tag
print(
    [f"{type(i)}::{i.name}" for i in soup.find_all(class_=re.compile(r'^t'))])
# 查找文本值以E开头的文本节点
print([f"{type(i)}::{i.name}" for i in soup.find_all(text=re.compile(r'^E'))])
```

输出:

```
["<class 'bs4.element.Tag'>::body", "<class 'bs4.element.Tag'>::b"]
["<class 'bs4.element.Tag'>::p"]
["<class 'bs4.element.NavigableString'>::None"]
```



### 列表

列表 `list` 可用作过滤器，列表中的项可以是:

- 字符串
- 正则表达式对象
- 可调用对象，详见 [函数](#函数)

BeautifulSoup 会利用列表中的项来筛选节点，并保留符合条件节点:

- 使用列表筛选 tag 时，若 tag 名与列表中的某一项匹配，则会保留该 tag 节点，且总会过滤掉 HTML 文本节点
- 使用列表筛选 HTML 属性时，若属性值与列表中的某一项匹配，则会保留该 tag 节点，且总会过滤掉 HTML 文本节点
- 使用列表筛选 HTML 文本时，若文本与列表中的某一项匹配，则会保留该文本节点

示例

```python
import re
def func(tag):
    return tag.get('id') == "link1"

soup = BeautifulSoup(html_doc, 'html.parser')
# 查找与列表匹配的tag节点
tag = soup.find_all(['title', re.compile('b$'), func])
pprint([f"{type(i)}::{i.name}" for i in tag])
pprint(
    [f"{type(i)}::{i.name}" for i in soup.find_all(text=["Elsie", "Tillie"])])
```

输出:

```
["<class 'bs4.element.Tag'>::title",
 "<class 'bs4.element.Tag'>::b",
 "<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None"]
```



### True

布尔值 `True` 可用作过滤器:

- 使用 `True` 筛选 tag 时，会保留所有 tag 节点，且过滤掉所有 HTML 文本节点
- 使用 `True` 筛选 HTML 属性时，会保留所有具备该属性的 tag 节点，且过滤掉所有 HTML 文本节点
- 使用 `True` 筛选 HTML 文本时，会保留所有文本节点

```python
soup = BeautifulSoup(html_doc, 'html.parser')
pprint([f"{type(i)}::{i.name}" for i in soup.find_all(True)])
pprint([f"{type(i)}::{i.name}" for i in soup.find_all(id=True)])
pprint([f"{type(i)}::{i.name}" for i in soup.find_all(text=True)])
```

输出:

```
["<class 'bs4.element.Tag'>::html",
 "<class 'bs4.element.Tag'>::head",
 "<class 'bs4.element.Tag'>::title",
 "<class 'bs4.element.Tag'>::body",
 "<class 'bs4.element.Tag'>::p",
 "<class 'bs4.element.Tag'>::b",
 "<class 'bs4.element.Tag'>::p",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::p"]
["<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None",
 "<class 'bs4.element.NavigableString'>::None"]
```



### 函数

过滤器可以是某个函数(或任何可调用对象):

- 以 tag 节点为筛选对象时，过滤器函数需以 tag 节点作为参数，如果函数返回 `True`，则保留该 tag 节点，否则抛弃该节点。

  示例 - 筛选出含 `class` 属性，但不含 `id` 属性的 tag 节点:

  ```python
  def has_class_but_no_id(tag):
      # Here’s a function that returns True if a tag defines the “class” attribute but doesn’t define the “id” attribute
      return tag.has_attr('class') and not tag.has_attr('id')
  
  
  soup = BeautifulSoup(html_doc, 'html.parser')
  tag = soup.find_all(has_class_but_no_id)
  pprint([f"{type(i)}::{i.name}" for i in tag])
  ```

  输出:

  ```
  ["<class 'bs4.element.Tag'>::p",
   "<class 'bs4.element.Tag'>::p",
   "<class 'bs4.element.Tag'>::p"]
  ```

- 针对 HTML 属性进行筛选时，过滤函数需以属性值作为参数，而非整个 tag 节点。如果 tag 节点包含目标属性，则会向过滤函数传递 `None`，否则传递实际值。如果函数返回 `True`，则保留该 tag 节点，否则抛弃该节点。

  ```python
  def not_lacie(href):
      # Here’s a function that finds all a tags whose href attribute does not match a regular expression
      return href and not re.compile("lacie").search(href)
  
  
  soup = BeautifulSoup(html_doc, 'html.parser')
  tag = soup.find_all(href=not_lacie)
  for i in tag:
      print(f"{type(i)}::{i.name}::{i}")
  ```

  输出:

  ```
  <class 'bs4.element.Tag'>::a::<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
  <class 'bs4.element.Tag'>::a::<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
  ```
  
- 针对 HTML 文本进行筛选时，过滤需以文本值作为参数，而非整个 tag 节点。如果函数返回 `True`，则保留该 tag 节点，否则抛弃该节点。

  ```python
  def func(text):
      return text == "Lacie"
  
  soup = BeautifulSoup(html_doc, 'html.parser')
  print([f"{type(i)}::{i}" for i in soup.find_all(text=func)])
  ```

  输出:

  ```
  ["<class 'bs4.element.NavigableString'>::Lacie"]
  ```

  

过滤函数可以被设计的非常复杂，比如:

```python
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

def surrounded_by_strings(tag):
    # returns True if a tag is surrounded by string objects
    return (isinstance(tag.next_element, NavigableString)
            and isinstance(tag.previous_element, NavigableString))

soup = BeautifulSoup(html_doc, 'html.parser')
tag = soup.find_all(surrounded_by_strings)
pprint([f"{type(i)}::{i.name}" for i in tag])
# 注意空白符对输出结果的影响
```

输出:

```
["<class 'bs4.element.Tag'>::body",
 "<class 'bs4.element.Tag'>::p",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::p"]
```



## find_all()🔨

🔨find_all(*name*=None, *attrs*={}, *recursive*=True, *text*=None, *limit*=None, *\*\*kwargs*)

该方法会检索当前 tag 对象的所有子孙节点，并提取与给定条件匹配的所有节点对象，然后返回一个包含这些**节点对象**的列表。

### name 参数

*name* 是用来筛选 tag 名称的"过滤器"，`find_all()` 会保留与 *name* 过滤器匹配的 tag 对象。使用 *name* 参数时，会自动过滤 HTML 文本节点，因为文本节点的 `.name` 字段为 `None`。

前面提到的五种过滤器均可用作 *name* 参数，即字符串、正则表达式、列表、`True`、函数(可调用对象)。

```python
soup = BeautifulSoup(html_doc, 'html.parser')
print([f"{type(i)}::{i.name}" for i in soup.find_all('title')])
#> ["<class 'bs4.element.Tag'>::title"]
```



### \*\*kwargs 参数

函数定义中未包含的关键字参数将被视作 HTML 属性"过滤器"，`find_all()` 会保留属性值与 var-keyword 匹配的 tag 对象。使用 var-keyword 时，会自动过滤 HTML 文本节点，因为文本节不含有 HTML 属性。

前面提到的五种过滤器均可用作 var-keyword 的值，即字符串、正则表达式、列表、`True`、函数(可调用对象)。

```python
soup = BeautifulSoup(html_doc, 'html.parser')
# 搜索id值为link2的tag节点
print([f"{type(i)}::{i.name}" for i in soup.find_all(id='link2')])
# 搜索href值以字母'e'结尾的tag节点
print([f"{type(i)}::{i.name}" for i in soup.find_all(href=re.compile(r"e$"))])
# 搜索具备id属性的tag节点
print([f"{type(i)}::{i.name}" for i in soup.find_all(id=True)])
# 过滤多个HTML属性
print([
    f"{type(i)}::{i.name}"
    for i in soup.find_all(class_="sister", href=re.compile(r"tillie"))
])
```

输出:

```
["<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.Tag'>::a", "<class 'bs4.element.Tag'>::a", "<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.Tag'>::a", "<class 'bs4.element.Tag'>::a", "<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.Tag'>::a"]
```

#### string

var-keyword 参数 *string* 与 *text* 参数等效:

```python
soup = BeautifulSoup(html_doc, 'html.parser')
print([f"{type(i)}::{i}" for i in soup.find_all(string=re.compile("sisters"))])
#> ["<class 'bs4.element.NavigableString'>::Once upon a time there were three little sisters; and their names were\n        "]
print([f"{type(i)}::{i}" for i in soup.find_all(text=re.compile("sisters"))])
#> ["<class 'bs4.element.NavigableString'>::Once upon a time there were three little sisters; and their names were\n        "]
```

*string* 是在 Beautiful Soup 4.4.0 中新加入的，在之前的版本中只能使用 *text* 参数。

#### 例外

HTML 5 中的部分属性并不符合 Python 的命名规则，不能用作 var-keyword 参数，此时需要使用 *attrs* 参数来过滤这些属性: 

```python
data_soup = BeautifulSoup('<div data-foo="value">foo!</div>')
data_soup.find_all(data-foo="value")
#> SyntaxError: keyword can't be an expression

print([
    f"{type(i)}::{i.name}"
    for i in data_soup.find_all(attrs={"data-foo": "value"})
])
#> ["<class 'bs4.element.Tag'>::div"
```

 var-keyword 参数不能用于过滤 HTML tag 的 name 属性，因为在 `find_all()` 的函数定义中已占用了变量名 *name*。如果要过滤 name 属性，可使用 *attrs* 参数来完成。

```python
soup = BeautifulSoup(html_doc, 'html.parser')
name_soup = BeautifulSoup('<input name="email"/>', 'html.parser')
print([f"{type(i)}::{i.name}" for i in name_soup.find_all(name="email")])
print([
    f"{type(i)}::{i.name}" for i in name_soup.find_all(attrs={"name": "email"})
])
```

输出:

```
[]
["<class 'bs4.element.Tag'>::input"]
```

#### 按 CSS 类搜索

CSS 的 class 属性是 Python 的保留关键字，从 BeautifulSoup 4.1.2 开始，可使用 var-keyword 参数 *class_* 来筛选 CSS 的 class 属性。使用 var-keyword 时，会自动过滤 HTML 文本节点，因为文本节不含有 HTML 属性。

前面提到的五种过滤器均可用作 *class_* 的值，即字符串、正则表达式、列表、`True`、函数(可调用对象)。

```python
# 搜索class时sister的a标签
soup = BeautifulSoup(html_doc, 'html.parser')
pprint([f"{type(i)}::{i.name}" for i in soup.find_all("a", class_="sister")])

# 搜索class中包含itl字段的标签
pprint(
    [f"{type(i)}::{i.name}" for i in soup.find_all(class_=re.compile("itl"))])

def has_six_characters(css_class):
    return css_class is not None and len(css_class) == 6
# 搜索class值长度为6的标签
pprint(
    [f"{type(i)}::{i.name}" for i in soup.find_all(class_=has_six_characters)])

pprint(
    [f"{type(i)}::{i.name}" for i in soup.find_all(class_=['title', "story"])])
```

输出:

```
["<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.Tag'>::p"]
["<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.Tag'>::p",
 "<class 'bs4.element.Tag'>::p",
 "<class 'bs4.element.Tag'>::p"]
```

CSS 的 class 属性可能会包含[多个值](#Multi-valued attributes)，如果 *class_* 仅匹配单个值，则会筛选出所有包含此 CSS class 的 tag 标签；如果 *class_* 匹配多个值时，会严格按照 CSS class 的顺序进行匹配，即使内容完全一样，但顺序不一致也会匹配失败:

```python
css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')
print(css_soup.find_all(class_='body'))
#> [<p class="body strikeout"></p>]
print(css_soup.find_all(class_='strikeout'))
#> [<p class="body strikeout"></p>]

print(css_soup.find_all("p", class_="body strikeout"))
#> [<p class="body strikeout"></p>]
print(css_soup.find_all("p", class_="strikeout body"))
#> []
```

因此，当你想要依据多个 CSS class 来搜索需要的 tag 标签时，为了不免因顺序不一致而搜索失败，应使用 CSS 选择器:

```python
print(css_soup.select("p.strikeout.body"))
#> [<p class="body strikeout"></p>]
```

在 BeautifulSoup 4.1.2 之前不能使用 *class_* 参数，此时可通过 *attrs* 参数来完成搜索:

```python
soup = BeautifulSoup(html_doc, 'html.parser')
pprint(
    [f"{type(i)}::{i.name}" for i in soup.find_all(attrs={"class": "sister"})])

pprint([f"{type(i)}::{i.name}" for i in soup.find_all(attrs="sister")])
```

输出:

```
["<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a"]
["<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a",
 "<class 'bs4.element.Tag'>::a"]
```



### attrs 参数

可以向 *attrs* 传递以下两种类型的实参值:

- 过滤器 - 此时 `.find_all()` 会查找 CSS class 的值与该过滤器匹配的 tag 标签，前面提到的五种过滤器均可使用。

  ```python
  soup = BeautifulSoup(html_doc, 'html.parser')
  print(soup.find_all("p", "title"))
  #> [<p class="title"><b>The Dormouse's story</b></p>]
  
  print([f"{type(i)}::{i.name}" for i in soup.find_all(attrs="sister")])
  #> ["<class 'bs4.element.Tag'>::a", "<class 'bs4.element.Tag'>::a", "<class 'bs4.element.Tag'>::a"]
  ```

- 映射对象 - `.find_all()` 会把映射对象中的键值对视作 HTML 属性名和属性值，并找出拥有配匹属性的 tag 标签，前面提到的五种过滤器均可用作映射对象的值。

  ```python
  soup = BeautifulSoup(html_doc, 'html.parser')
  
  pprint([
      f"{type(i)}::{i.name}" for i in soup.find_all(attrs={
          "class": "sister",
          "id": "link1",
      })
  ])
  #> ["<class 'bs4.element.Tag'>::a"]
  ```

### text/string 参数

> The `string` argument is new in Beautiful Soup 4.4.0. In earlier versions it was called `text`

*text* 是用来筛选文本标签的过滤器，`find_all()` 会保留与 *text* 过滤器匹配的文本标签，前面提到的五种过滤器均可用作 *text* 的实参。

```python
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.find_all(string="Elsie"))
print(soup.find_all(string=["Tillie", "Elsie", "Lacie"]))
print(soup.find_all(string=re.compile("Dormouse")))


def is_the_only_string_within_a_tag(s):
    """Return True if this string is the only child of its parent tag."""
    return (s == s.parent.string)


print(soup.find_all(string=is_the_only_string_within_a_tag))
```

输出:

```
['Elsie']
['Elsie', 'Lacie', 'Tillie']
["The Dormouse's story", "The Dormouse's story"]
["The Dormouse's story", "The Dormouse's story", 'Elsie', 'Lacie', 'Tillie', '...']
```

在查找 tag 标签时，*text* 被视作筛选条件，`find_all()` 会筛选出 `.string` 字段与 *text* 过滤器匹配的 tag 标签:

```python
soup = BeautifulSoup(html_doc, 'html.parser')

print([f'{type(i)}::{i}' for i in soup.find_all("a", string="Elsie")])
#> ['<class \'bs4.element.Tag\'>::<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>']
```



### limit 参数

默认情况下 `find_all()` 会返回所有匹配到的标签对象，如果并不需要获取全部标签对象，可使用 *limit* 参数来控制对象的数量，此时 BeautifulSoup 会在搜索到 *limit* 个标签对象后停止搜索。

```python
soup = BeautifulSoup(html_doc, 'html.parser')
# There are three links in the “three sisters” document,
# but this code only finds the first two
print([f'{type(i)}::{i.name}' for i in soup.find_all("a", limit=2)])
#> ["<class 'bs4.element.Tag'>::a", "<class 'bs4.element.Tag'>::a"]
```



### recursive 参数

默认情况下 `find_all()` 会检索当前 tag 对象的所有子孙节点，并提取与给定条件匹配的所有节点对象，然后返回一个包含这些**节点对象**的列表。如果不想递归检索所有子孙节点，可使用 *recursive* 进行限制: 当 `recursive=False` 时，只会检索直接子节点:

```python
soup = BeautifulSoup(html_doc, 'html.parser')

print([f'{type(i)}::{i.name}' for i in soup.find_all("title")])
#> ["<class 'bs4.element.Tag'>::title"]
print(
    [f'{type(i)}::{i.name}' for i in soup.find_all("title", recursive=False)])
#> []
```



## 调用 `Tag` 对象

在使用 BeautifulSoup 时，`find_all()` 是最常用的检索方法，因此开发人员为 `find_all()` 提供了更简便的调用方法——我们在调用 `Tag` 对象时，便是在调用其 `find_all()` 方法，源代码如下:

```python
def __call__(self, *args, **kwargs):
    """Calling a tag like a function is the same as calling its
        find_all() method. Eg. tag('a') returns a list of all the A tags
        found within this tag."""
    return self.find_all(*args, **kwargs)
```

示例 :

```python
soup("a") # 等效于soup.find_all("a")
soup.title(string=True) # 等效于soup.title.find_all(string=True)
```

## find()🔨

🔨find([name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id11), [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attrs), [recursive](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#recursive), [string](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id12), [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kwargs))

`find()` 方法会只会返回第一个被匹配到的标签对象，如果没有与之匹配的标签则会返回 `None`。在解析树中[使用节点名称导航](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#navigating-using-tag-names)时，实际上就是在使用 `find()` 方法。

## 其它搜索方法

> 在理解下面这些方法时，请交叉参考笔记﹝BeautifulSoup - 解析树.md﹞中的"在解析树中导航"一节，以便理解解析树的结构。
>
> 本节中不会详细解释各个方法的含义，只会给出函数签名和文档参考连接。

### find_parents()&find_parent()🔨

🔨find_parents([name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id11), [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attrs), [string](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id12), [limit](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#limit), [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kwargs))

🔨find_parent([name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id11), [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attrs), [string](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id12), [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kwargs))

详见: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-parents-and-find-parent



### find_next_siblings()&find_next_sibling()🔨

🔨find_next_siblings([name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id11), [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attrs), [string](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id12), [limit](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#limit), [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kwargs))

🔨find_next_sibling([name](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id11), [attrs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attrs), [string](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#id12), [**kwargs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kwargs))

详见: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-next-siblings-and-find-next-sibling



### find_previous_siblings()&find_previous_sibling()🔨

🔨find_previous_siblings(name, attrs, string, limit, **kwargs)

🔨find_previous_sibling(name, attrs, string, **kwargs)

详见: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-previous-siblings-and-find-previous-sibling



### find_all_next()&find_next()🔨

🔨find_all_next(name, attrs, string, limit, **kwargs)

🔨find_next(name, attrs, string, **kwargs)

详见: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all-next-and-find-next



### find_all_previous()&find_previous()🔨

🔨find_all_previous(name, attrs, string, limit, **kwargs)

🔨find_previous(name, attrs, string, **kwargs)

详见: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all-previous-and-find-previous



## CSS 选择器

从 4.7.0 版本开始，BeautifulSoup 将通过 [SoupSieve](https://facelessuser.github.io/soupsieve/) 项目支持大多数 CSS4 选择器。如果你通过 `pip` 来安装 BeautifulSoup，则会自动安装 SoupSieve。

[SoupSieve](https://facelessuser.github.io/soupsieve/) 的官方文档中详细介绍了 API 和目前已支持的 CSS 选择器，API 不只包含本节介绍的 `.select()`，还包含以下方法:

- `.select_one()`
- `.iselect()`
- `.closest()`
- `.match()`
- `.filter()`
- `.comments()`
- `.icomments()`
- `.escape()`
- `.compile()`
- `.purge()`

总之，如需全面了解 [SoupSieve](https://facelessuser.github.io/soupsieve/) 相关信息，请参考其官方文档。

在了解 CSS 时，推荐使用"[jQuery 选择器检测器](https://www.runoob.com/try/trysel.php)"来观察不同的选择器的效果，还可交叉参考笔记﹝PyQuery.md﹞和以下连接:

- <http://www.w3school.com.cn/css/css_selector_type.asp>
- http://www.w3school.com.cn/cssref/css_selectors.asp
- https://www.runoob.com/cssref/css-selectors.html



### select()🔨

`.select()` 方法适用于 `BeautifulSoup` 对象和 `Tag` 对象。

在 4.7.0 版本之后， `.select()` 会使用 SoupSieve 来提取与 CSS 选择器匹配的所有节点对象，然后返回一个包含这些**节点对象**的列表。

在 4.7.0 版本之前，虽然也可以使用 `.select()`，但是在旧版本中仅支持最常见的 CSS 选择器。

元素选择器:

```python
print(soup.select("title"))
#> [<title>The Dormouse's story</title>]

print(soup.select("p:nth-of-type(3)"))
#> [<p class="story">...</p>]
```

嵌套选择器:

```python
print(soup.select("body a"))
#> [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#>  <a class="sister" href="http://example.com/lacie"  id="link2">Lacie</a>,
#>  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

print(soup.select("html head title"))
#> [<title>The Dormouse's story</title>]
```

CSS 选择器会选取所有符合条件 tag

更多示例详见: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors