# XPath
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

## 概述

> XML Path Language (XPath)
>
> XPath is an expression language that allows the processing of values conforming to the data model defined in the XQuery and Xpath Data Model.

相关资源:

- [XPath 教程 - W3school](http://www.w3school.com.cn/xpath/index.asp)
- [XPath 教程 - 菜鸟教程](http://www.runoob.com/xpath/xpath-tutorial.html)
- [XML Path Language (XPath) - W3C 标准](https://www.w3.org/TR/xpath/all/)
- [XPath and XQuery Functions and Operators 3.1](https://www.w3.org/TR/xpath-functions-31)
- [4. XPath reference](https://infohost.nmt.edu/tcc/help/pubs/xslt/xpath-sect.html) 🍰
- [微软 XPath 语法页面](https://docs.microsoft.com/en-us/previous-versions/dotnet/netframework-4.0/ms256471(v=vs.100)?redirectedfrom=MSDN) 

XPath 是一门在 XML 文档中查找信息的语言(也适用于 HTML)。XPath 的功能十分强大，主要体现在以下两方面:

- XPath 路径表达式 - 可使用路径表达式来选取 XML 文档中的节点或者节点集。XPath 路径表达式和我们在常规的电脑文件系统中看到的表达式非常相似。
- XPath 标准函数 - XPath 含有超过 100 个内建的函数。这些函数用于字符串值、数值、日期和时间比较、节点和 QName 处理、序列处理、逻辑值等等。

## 语法

XML 实例文档 - 在本节的示例将使用此 XML 文档:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>

<bookstore>

<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>

<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>

</bookstore>
```



### 选取节点

XPath 使用路径表达式(绝对路径或相对路径)来选取 XML 文档中的节点或节点集:

- 绝对路径以正斜杠( `/` )开头:

  ```
  /step/step/...
  ```

- 相对路径:

  ```
  step/step/...
  ```

下面列出了最常用的路径表达式：

| 表达式   | 描述                                                       |
| :------- | :--------------------------------------------------------- |
| nodename | 选取此节点的所有子节点                                     |
| /        | 从根节点选取，或从当前节点选取直接子节点                   |
| //       | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
| .        | 选取当前节点                                               |
| ..       | 选取当前节点的父节点                                       |
| @        | 属性限定，选取匹配属性的节点                               |

示例 - 在下面的表格中，我们已列出了一些路径表达式以及表达式的结果：

| 路径表达式      | 结果                                                         |
| :-------------- | :----------------------------------------------------------- |
| bookstore       | 选取 bookstore 元素的所有子节点。                            |
| /bookstore      | 选取根元素 bookstore。注释：假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！ |
| bookstore/book  | 选取属于 bookstore 的子元素的所有 book 元素。                |
| //book          | 选取所有 book 子元素，而不管它们在文档中的位置。             |
| bookstore//book | 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置。 |
| //@lang         | 选取名为 lang 的所有属性。                                   |



#### 步

路径由一个或多个步(*steps*)构成，每个步均根据当前节点集之中的节点来进行计算，在步中可以包含以下内容:

- 轴（axis）

  定义所选节点与当前节点之间的树关系

- 节点测试（node-test）

  识别某个轴内部的节点

- 零个或者更多谓语（predicate）

  更深入地提炼所选的节点集

步的语法：

```
轴名称::节点测试[谓语]
```

XML 文档:

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>

<bookstore>

<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>

<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>

</bookstore>
```

用例展示:

| 例子                   | 结果                                                         |
| :--------------------- | :----------------------------------------------------------- |
| child::book            | 选取所有属于当前节点的子元素的 book 节点。                   |
| attribute::lang        | 选取当前节点的 lang 属性。                                   |
| child::*               | 选取当前节点的所有子元素。                                   |
| attribute::*           | 选取当前节点的所有属性。                                     |
| child::text()          | 选取当前节点的所有文本子节点。                               |
| child::node()          | 选取当前节点的所有子节点。                                   |
| descendant::book       | 选取当前节点的所有 book 后代。                               |
| ancestor::book         | 选择当前节点的所有 book 先辈。                               |
| ancestor-or-self::book | 选取当前节点的所有 book 先辈以及当前节点（如果此节点是 book 节点） |
| child::*/child::price  | 选取当前节点的所有 price 孙节点。                            |

### 谓语

谓语(*Predicates*)被嵌在方括号中，用来查找某个特定的节点或者包含某个指定的值的节点。

示例 - 在下面的表格中，列出了带有谓语的一些路径表达式，以及表达式的结果：

| 路径表达式                         | 结果                                                         |
| :--------------------------------- | :----------------------------------------------------------- |
| /bookstore/book[1]                 | 选取属于 bookstore 子元素的第一个 book 元素。                |
| /bookstore/book[last()]            | 选取属于 bookstore 子元素的最后一个 book 元素。              |
| /bookstore/book[last()-1]          | 选取属于 bookstore 子元素的倒数第二个 book 元素。            |
| /bookstore/book[position()<3]      | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。    |
| //title[@lang]                     | 选取所有拥有名为 lang 的属性的 title 元素。                  |
| //title[@lang='eng']               | 选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。   |
| /bookstore/book[price>35.00]       | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。 |
| /bookstore/book[price>35.00]/title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

### 轴

> 参考: <https://infohost.nmt.edu/tcc/help/pubs/xslt/axis-sect.html>

轴用于定义相对于当前节点的节点集。

| 轴名称             | 结果                                                     |
| :----------------- | :------------------------------------------------------- |
| ancestor           | 选取当前节点的所有先辈（父、祖父等）。                   |
| ancestor-or-self   | 选取当前节点的所有先辈（父、祖父等）以及当前节点本身。   |
| attribute          | 选取当前节点的所有属性，等效于 `@`                       |
| child              | 选取当前节点的所有子元素。                               |
| descendant         | 选取当前节点的所有后代元素（子、孙等）。                 |
| descendant-or-self | 选取当前节点的所有后代元素（子、孙等）以及当前节点本身。 |
| following          | 选取文档中当前节点的结束标签之后的所有节点。             |
| following-sibling  | 获取当前节点之后的所有同级节点                           |
| namespace          | 选取当前节点的所有命名空间节点。                         |
| parent             | 选取当前节点的父节点，等效于 `../`                       |
| preceding          | 选取文档中当前节点的开始标签之前的所有节点。             |
| preceding-sibling  | 选取当前节点之前的所有同级节点。                         |
| self               | 选取当前节点，等效于 `./`                                |

![img](XPath.assets/axes.jpg)



### 选取未知节点

XPath 通配符可用来选取未知的 XML 元素。

| 通配符 | 描述                 |
| :----- | :------------------- |
| *      | 匹配任何元素节点。   |
| @*     | 匹配任何属性节点。   |
| node() | 匹配任何类型的节点。 |

示例 - 在下面的表格中，列出了一些路径表达式，以及这些表达式的结果：

| 路径表达式   | 结果                              |
| :----------- | :-------------------------------- |
| /bookstore/* | 选取 bookstore 元素的所有子元素。 |
| //*          | 选取文档中的所有元素。            |
| //title[@*]  | 选取所有带有属性的 title 元素。   |

### 选取若干路径

通过在路径表达式中使用 “|” 运算符，您可以选取若干个路径。

示例 - 在下面的表格中，列出了一些路径表达式，以及这些表达式的结果：

| 路径表达式                       | 结果                                                         |
| :------------------------------- | :----------------------------------------------------------- |
| //book/title \| //book/price     | 选取 book 元素的所有 title 和 price 元素。                   |
| //title \| //price               | 选取文档中的所有 title 和 price 元素。                       |
| /bookstore/book/title \| //price | 选取属于 bookstore 元素的 book 元素的所有 title 元素，以及文档中所有的 price 元素。 |

### 节点测试

Most XPath expressions are used to select zero or more nodes from the document. For example, the XPath expression **cue** selects all `<cue>` child elements of the context node.

These functions are used to select certain special node sets:

- text()

  This function selects all the text children of the context node.

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
  print(elem.xpath('/html/body/book/author/text()'))
  #> ['Tom ', ' cat', 'Tom_ ', ' cat_']
  print(elem.xpath('/html/body/book/author//text()'))
  #> ['Tom ', 'John', ' cat', 'Tom_ ', 'John_', ' cat_']
  ```

- comment()

  Selects all comments that are children of the context node.

- processing-instruction()

  Selects all children of the context node that are processing instructions.

### XPath 运算符

下面列出了可用在 XPath 表达式中的运算符：

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



## 节点类型

These types of nodes are used to represent a document as a tree:

- A *document* node roots the tree. It will always have as its child an element node for the outermost element of the document. It may also have comment or processing instruction nodes as children, if those nodes appear outside the document.

  如果使用文档节点， `Element.xpath()` 将返回元素列表

- Each *element node* represents one XML tag and its children, if any.

  如果使用元素节点， `Element.xpath()` 将返回元素列表

- *Attribute nodes* represent attributes of an element. Such nodes have element nodes as a parent, but are not considered ordinary children of the parent element.

  如果使用属性节点， `Element.xpath()` 将返回字符串列表

- Chunks of text inside an element become *text nodes*.

  如果使用文本节点， `Element.xpath()` 将返回字符串列表

- Comments in the document are represented as *comment nodes*.

- *Processing instructions* come from XML's **<?...?>** construct.

### 节点关系

#### Parent 父

每个元素以及属性都有一个父。

在下面的例子中，book 元素是 title、author、year 以及 price 元素的父：

```
<book>
  <title>Harry Potter</title>
  <author>J K. Rowling</author>
  <year>2005</year>
  <price>29.99</price>
</book>
```

#### Children 子

元素节点可有零个、一个或多个子。

在下面的例子中，title、author、year 以及 price 元素都是 book 元素的子：

```
<book>
  <title>Harry Potter</title>
  <author>J K. Rowling</author>
  <year>2005</year>
  <price>29.99</price>
</book>
```

#### Sibling 同胞

拥有相同的父的节点

在下面的例子中，title、author、year 以及 price 元素都是同胞：

```
<book>
  <title>Harry Potter</title>
  <author>J K. Rowling</author>
  <year>2005</year>
  <price>29.99</price>
</book>
```

#### Ancestor 先辈

某节点的父、父的父，等等。

在下面的例子中，title 元素的先辈是 book 元素和 bookstore 元素：

```
<bookstore>

<book>
  <title>Harry Potter</title>
  <author>J K. Rowling</author>
  <year>2005</year>
  <price>29.99</price>
</book>

</bookstore>
```

#### Descendant 后代

某个节点的子，子的子，等等。

在下面的例子中，bookstore 的后代是 book、title、author、year 以及 price 元素：

```
<bookstore>

<book>
  <title>Harry Potter</title>
  <author>J K. Rowling</author>
  <year>2005</year>
  <price>29.99</price>
</book>

</bookstore>
```

## XPath、XQuery 以及 XSLT 函数

详见:

- <http://www.w3school.com.cn/xpath/xpath_functions.asp>
- [XPath and XQuery Functions and Operators 3.1](https://www.w3.org/TR/xpath-functions-31)

## text() | string() | data()

> issue: 在文档中看到 `text()` 和 `string()`，但 `text()` 并不是函数，那么这两者有什么区别喃?
>
> 参考: 
>
> - [MarkLogic学习——XPath中的text()和string()区别](https://blog.csdn.net/jiangchao858/article/details/63314426)
> - <https://blog.csdn.net/jiangchao858/article/details/63314426>
> - [XPath and XQuery Functions and Operators 3.1](https://www.w3.org/TR/xpath-functions-31/#func-adjust-dateTime-to-timezone)
> - [XML Path Language (XPath) 3.1](https://www.w3.org/TR/2017/REC-xpath-31-20170321/)
> - [XPath、XQuery 以及 XSLT 函数](http://www.w3school.com.cn/xpath/xpath_functions.asp)

`text()` 是 [node test](https://www.w3.org/TR/2017/REC-xpath-31-20170321/#node-tests)，而 `string()` 是[函数](https://www.w3.org/TR/xpath-functions-31)，`data()` 是函数且可以保留数据类型。此外，还有点号 `.` 表示当前节点。

在 W3C 文档中给出的解释如下:

- `text()` - matches any text node.
- `string()` - Returns the value of `$arg` represented as an `xs:string`.

- `data()` - Returns the result of atomizing a sequence. This process flattens arrays, and replaces nodes by their typed values.

XML 示例: `<book><author>Tom John</author></book>`

| 用例     | 举例                 |
| -------- | -------------------- |
| text()   | book/author/text()   |
| string() | book/author/string() |
| data()   | book/author/data()   |
| .        | book/author/.        |

`text()` 不是函数，XML结构的细微变化，可能会使得结果与预期不符，应该尽量少用，`data()` 作为特殊用途的函数，可能会出现性能问题，如无特殊需要尽量不用，`string()` 函数可以满足大部分的需求。

### 示例

XML 示例:

```xml
<book>
    <author>Tom <em>John</em> cat</author>
    <pricing>
        <price>20</price>
        <discount>0.8</discount>
    </pricing>
</book>
```

- `text()` - 经常在 XPath 表达式的最后看到 `text()`，它仅仅返回所指元素的文本内容。

  ```
  let $x := book/author/text()
  return $x
  ```

  返回的结果是 "Tom cat"，其中的 John 不属于 `author` 直接的节点内容。

  

- `string()` - `string()` 函数会得到所指元素的所有节点文本内容，这些文本讲会被拼接成一个字符串。

  ```
  let $x := book/author/string()
  return $x
  ```

  返回的内容是 "Tom John cat"

- `data()` - 大多数时候，data()函数和string()函数通用，而且不建议经常使用 data() 函数，有数据表明，该函数会影响 XPath 的性能。

  ```
  let $x := book/pricing/string()
  return $x
  ```

  返回的是 "200.8"

  ```
  let $x := book/pricing/data()
  return $x
  ```

  这样将返回分开的 "20" 和 "0.8"，他们的类型并不是字符串而是 xs:anyAtomicType，于是就可以使用数学函数做一定操作。

  ```
  let $x := book/pricing/price/data()
  let $y := book/pricing/discount/data()
  return $x*$y
  ```

  比如上面这个例子，就只能使用data()，不能使用text()或 string()，因为XPath不支持字符串做数学运算。

