# 文本序列类型(str)

> 本文涵盖了 [str](https://docs.python.org/3.7/library/stdtypes.html#str) 中的第一部分的知识点，并进行了扩展，后面两部的笔记如下：
> - [String Methods](https://docs.python.org/3.7/library/stdtypes.html#string-methods) 小节位于笔记『字符串方法.md』中
> - `printf`-[style String Formatting](https://docs.python.org/3.7/library/stdtypes.html#printf-style-string-formatting) 小节位于笔记『格式化操作.md』中

Python 通过字符(*string*) 来处理文本数据(*textual data*)，字符串是由 Unicode 码点(*code point*)组成的不可变[序列](https://docs.python.org/3.7/glossary.html#term-sequence)(*sequence*)。

在 Python 中并没有单独的"字符(*character*)"类型，因此当我们索引一个非空字符串 `s` 时，将产生一个长度为 1 的字符串，即 `s[0] == s[0:1]`。

如果需要深入了解各种形式的字符串字面值，可阅读 [String and Bytes literals](https://docs.python.org/3.7/reference/lexical_analysis.html#strings)。在笔记『2. Lexical analysis.md』中已翻译了这部分文档，并且在文档中还介绍了转义序列，以及如何使用 `r` (*raw*) 前缀来禁用大多数转义序列。

[`-b`](https://docs.python.org/3.7/using/cmdline.html#cmdoption-b) 命令行选项会在比较 `str` 对象和 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes)(或 [`bytearray`](https://docs.python.org/3.7/library/stdtypes.html#bytearray))对象时发出警告。

**Changed in version 3.3:** 为了向后兼容 Python 2 系列，重新允许在字符串中使用 `u` 前缀。`u` 前缀对字符串的含义没有任何影响，但是不能和 `r` 前缀共存。

> 扩展阅读：
>
> - 『2. Lexical analysis.md』->「2.4. 字面值」
> - 『格式化操作.md』
> - [Text Processing Services](https://docs.python.org/3.7/library/text.html#stringservices)

## 1. 构建字符串

字符串字面量有以下三种定义方式：

- Single quotes: `'allows embedded "double" quotes'`
- Double quotes: `"allows embedded 'single' quotes"` 
- Triple quoted: `'''Three single quotes'''` 或 `"""Three double quotes"""`

三重引号 (*triple-quoted*) 字符串可以跨越多行，此时在字符串字面值中会保留所有相应的空白符(*whitespace*)，不过在这种情况下不可以添加注释：

```python
>>> '''first line
second line'''
'first line\nsecond line'
```

如果想要避免三重引号字符串在行尾自动添加换行符，可在行尾使用反斜线 `\`：

```python
>>> print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
```

如果在单引号(或双引号)字符串的行末添加反斜线 `\`，则表示该字符串在下一行继续，并且不会添加换行符：

```
>>> "This is the first sentence. \
This is the second sentence."
'This is the first sentence. This is the second sentence.'
```

还可使用 `str()` 构造函数从其它对象创建字符串。

### 1.1 str()

详见笔记 『str.md』，还可以阅读笔记『repr.md』

## 2. 字符串支持的操作

字符串实现了所有[通用序列操作](https://docs.python.org/3/library/stdtypes.html#typesseq-common)，详见笔记『序列类型支持的操作.md』

字符串还实现了很多附加方法，详见笔记『字符串方法.md』

字符串支持两种方式的格式化操作：

- 格式化字符串语法(*Format String Syntax*) - 具备更大灵活性和更强的定制性，详见：
  - 『string — Common string operations.md』
  - 『格式化操作.md』
  -  [`str.format()`](https://docs.python.org/3.7/library/stdtypes.html#str.format)
  - [Format String Syntax](https://docs.python.org/3.7/library/string.html#formatstrings)
  - [Custom String Formatting](https://docs.python.org/3.7/library/string.html#string-formatting)
- 基于 C  `printf` 风格的格式化操作，可处理的类型比上一种方式少，但是通常更快，详见：
  - 『格式化操作.md』
  - [printf-style String Formatting](https://docs.python.org/3.7/library/stdtypes.html#old-string-formatting)

标准库中的 [Text Processing Services](https://docs.python.org/3.7/library/text.html#textservices) 部分提供了与处理文本相关的许多内置模块。比如，在  [`re`](https://docs.python.org/3.7/library/re.html#module-re) 模块中提供了与正则表达式相关的操作。

## 3. 提示

### 2.1 字符串字面值的连接

在对序列进行连接时通常会使用连接操作符(`+`)，但在连接字符串时甚至可以省略 `+`。直接将字符串并置在一起，便可完成连接操作：

```python
>>> 'orca'"_"'j35'
'orca_j35'
```

当单个表达式中存在被空白符分隔的多个字符串字面值时，这些字符串也将被隐式连接为一个单独的字符串。在连接字面值时，对于每个组成部分可以使用不同的引用风格(甚至可以将原始字符串和三重引号字符串进行混用)，还可以将格式化字符串字面值与纯(*plain*)字符串字面值连接。但是，这种连接方法只适用于字符串字面值，不能包含变量或表达式——包含变量或表达式时，必须使用连接操作符(`+`)。

```python
>>> sn='j35'
>>> print('orca' # 允许对每段字符串添加注释
	  """_"""
	  f'{sn}'
	  r'\n')
orca_j35\n
>>> 'orca' sn # 不能隐式连接字面值和变量
SyntaxError: invalid syntax
>>> ('orca'*3) 'j35' # 不能隐式连接字面值和表达式
SyntaxError: invalid syntax
```

注意，上述特性是在语法层次上定义的，但在编译时实现。在运行时必须使用 '+' 运算符连接字符串表达式。

在 Python 中没有可变字符串类型，当需要将多个字符串片段连接为一个字符串时，可使用 [`str.join()`](https://docs.python.org/3.7/library/stdtypes.html#str.join)( 或 [`io.StringIO`](https://docs.python.org/3.7/library/io.html#io.StringIO)) 。与连接操作符 `+` 的区别是，这两个方法的时间复杂度为线性。

### 2.2 反转字符串

将切片的第三参数为 `-1`，便可反转字符串

```python
>>> word = 'Python'
>>> word[::-1]
'nohtyP'
```

### 2.3 比较字符串

当我们利用"值比较运算符"来比较不同的字符串时，会依次比较两个字符串中的各个字符，并将字符的 Unicode 码点作为判定依据。

```python
>>> ord('鲸')
40120
>>> ord('熊')
29066
>>> '鲸' > '熊'
True
```

注意，字符串的长度与比较结果无关。

```python
>>> 'abcd' < 'abd'
True
```




























