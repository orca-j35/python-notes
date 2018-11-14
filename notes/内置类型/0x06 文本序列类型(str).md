# 文本序列类型(str)

> 本文涵盖了 [str](https://docs.python.org/3.7/library/stdtypes.html#str) 中的所有知识点，并进行了扩展。

Python 通过 [`str`](https://docs.python.org/3/library/stdtypes.html#str) 对象来处理文本数据(*textual data*)。

字符串是由 Unicode 码点(*code point*)组成的不可变[序列](https://docs.python.org/3.7/glossary.html#term-sequence)(*sequence*)。

如果需要深入了解各种形式的字符串字面值，可阅读 [String and Bytes literals](https://docs.python.org/3.7/reference/lexical_analysis.html#strings)。在笔记『2. Lexical analysis.md』中已翻译了这部分文档，并且在文档中还讲述了转义序列，以及如何使用 `r` (*raw*) 前缀来禁用大多数转义序列。

在 Python 中并没有单独的"字符(*character*)"类型，因此当我们索引一个非空字符串 `s` 时，将产生一个长度为 1 的字符串，即 `s[0] == s[0:1]`。

在 Python 中没有可变字符串类型，当需要将多个字符串片段连接为一个字符串时，可使用 [`str.join()`](https://docs.python.org/3.7/library/stdtypes.html#str.join)( 或 [`io.StringIO`](https://docs.python.org/3.7/library/io.html#io.StringIO)) 。与连接操作符 `+` 的区别是，这两个方法的时间复杂度为线性。

[`-b`](https://docs.python.org/3.7/using/cmdline.html#cmdoption-b) 命令行选项会在比较 `str` 对象和 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes)(或 [`bytearray`](https://docs.python.org/3.7/library/stdtypes.html#bytearray))对象时发出警告。

**Changed in version 3.3:** 为了向后兼容 Python 2 系列，重新允许在字符串字面中使用 `u` 前缀。`u` 前缀对字符串的含义没有任何影响，但是不能和 `r` 前缀共存。

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

还可使用 `str()` 构造函数从其它对象创建字符串，具体使用方法如下：

### 1.1 str(*object*)

🔨 *class* str(*object=''*)

此时，该函数将返回 *object* 的字符串版本，使用方法如下：

```
str(object='') -> str
 | str() -> empty string ''
 | str(object) -> type(object).__str__()
 | str(bytes_or_buffer) -> type(bytes_or_buffer).__str__()
```

*object* 可以是任意的对象，包括 `bytes` 和 `buffer` 的实例。

```python
>>> str("orca_j35") # 字符串实例，将返回其自身
'orca_j35'
>>> str(b'abs') # bytes实例
"b'abs'"
```

`type(object).__str__()` 方法会返回一个用于描述 *object* 的字符串，且该字符串会以适于打印的(或非正式的)形式来描述 *object*。如果 `type(object)` 没有 `__str__()` 方法，则会返回 [`repr(object)`](https://docs.python.org/3.7/library/functions.html#repr)：

```python
class Cls():
    def __repr__(self):
        return 'in __repr__'
print(str(Cls())) # Out: in __repr__
```

注意：`str(object)` 会返回 `type(object).__str__()`，也就是说 `str()` 会利用类字典中的 `__str__` 方法对 *object* 进行格式化，这样做的目的是跳过实例字典中的方法。如果仅考虑类和实例，这好像并没有什么意义，因为不会有人在实例字典中重新绑定 `__str__` 方法。但是，如果考虑到元类和类，这就很有意义了，因为类是元类的实例，并且通常会在类字典中绑定 `__str__` 方法。当 *object* 是一个类时，实际上需要调用元类中的 `__str__` 方法，此时我们便需要跳过类字典中 `__str__` 方法，使用元类中的同名方法。

```python
class Cls():
    def __str__(self):
        return 'Cls 类的实例对象'
obj = Cls()
from types import MethodType
obj.__str__ = MethodType(lambda self: '绑定到实例的__str__方法', obj)
print(str(obj))
"""Out:
Cls 类的实例对象
"""
```

### 1.2 str(*object*, *encoding*, *errors*)

🔨 *class* str(*object=b''*, *encoding='utf-8'*, *errors='strict'*)

此时会按照给定编码方式对 *object* 进行**解码**，并返回解码后的字符串，使用方法如下：

```
str(bytes_or_buffer[, encoding[, errors]]) -> str
 | str(bytes_or_buffer, encoding='...') -> bytes_or_buffer.decode(encoding='...')
 | str(bytes_or_buffer, errors='...') -> bytes_or_buffer.decode(errors='...')
 | str(bytes_or_buffer, encoding='...', errors='...') -> bytes_or_buffer.decode(encoding='...', errors='...')
```

各参数的含义如下：

- *object* 用于设置解码对象，要求其属于 [bytes-like](https://docs.python.org/3.7/glossary.html#term-bytes-like-object) 对象，可分为以下两种情况：
  - 如果 *object* 是 `bytes`(或 `bytearray`)对象，那么 `str(object, encoding, errors)`会直接返回 [`object.decode(encoding, errors)`](https://docs.python.org/3.7/library/stdtypes.html#bytes.decode)；
  - 否则，需要在返回 `object.decode()` 之前，先获取缓冲器对象下的字节对象。

- *encoding* 用于设置编码方案，将被传递给 `bytes_or_buffer.decode()`，其默认值是 `sys.getdefaultencoding()`，可在 [Standard Encodings](https://docs.python.org/3.7/library/codecs.html#standard-encodings) 中可查看编码方案列表。

- *errors* 用于设置[错误处理方案](https://docs.python.org/3.7/library/codecs.html#error-handlers)，也会被传递给 `bytes_or_buffer.decode()`，其默认值是 `'strict'`。*errors* 可以是 `'ignore'`, `'replace'`, `'xmlcharrefreplace'`, `'backslashreplace'` 或任何已通过 [`codecs.register_error()`](https://docs.python.org/3.7/library/codecs.html#codecs.register_error) 注册的名称。

```python
>>> a_bytes = bytes('鲸','utf-8')
>>> a_bytes
b'\xe9\xb2\xb8'
>>> str(a_bytes,'utf-8')
'鲸'
>>> str(a_bytes,'ascii')
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    str(a_bytes,'ascii')
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 0: ordinal not in range(128)
>>> str(a_bytes,'ascii','ignore')
''
```

有关缓冲区对象的详细信息，可阅读 [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3.7/library/stdtypes.html#binaryseq) 和 [Buffer Protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects)。

Tips: 在 Python 文档中，"编码(*encoding*)"是指将 Unicode 字符串转换为字节序列的规则，也就是说"编码"包含了从"抽象字符序列"到"字节序列"的全部过程，"解码"则包含了从"字节序列"到"抽象字符序列"的全部过程。

## 2. 字符串支持的操作

字符串实现了所有[通用序列操作](https://docs.python.org/3/library/stdtypes.html#typesseq-common)，以及下列附加方法：

Strings implement all of the [common](https://docs.python.org/3.7/library/stdtypes.html#typesseq-common) sequence operations, along with the additional methods described below.

Strings also support two styles of string formatting, one providing a large degree of flexibility and customization (see [`str.format()`](https://docs.python.org/3.7/library/stdtypes.html#str.format), [Format String Syntax](https://docs.python.org/3.7/library/string.html#formatstrings) and [Custom String Formatting](https://docs.python.org/3.7/library/string.html#string-formatting)) and the other based on C `printf` style formatting that handles a narrower range of types and is slightly harder to use correctly, but is often faster for the cases it can handle ([printf-style String Formatting](https://docs.python.org/3.7/library/stdtypes.html#old-string-formatting)).

The [Text Processing Services](https://docs.python.org/3.7/library/text.html#textservices) section of the standard library covers a number of other modules that provide various text related utilities (including regular expression support in the [`re`](https://docs.python.org/3.7/library/re.html#module-re) module).



### 2.1 字符串字面值的连接

在对序列进行连接时通常会使用连接操作符(`+`)，但在连接字符串时甚至可以省略 `+`。直接将字符串并置在一起，便可完成连接操作：

```python
>>> 'orca'"_"'j35'
'orca_j35'
```

当单个表达式中存在被空白符分隔的多个字符串字面值时，这些字符串也将被隐式连接为一个单独的字符串。在连接字面值时，对于每个组成部分可以使用不同的引用风格(甚至可以将原始字符串和三重引号字符串进行混用)，还可以将格式化字符串字面值与纯(*plain*)字符串字面值连接。

```python
>>> sn='j35'
>>> print('orca' # 允许对每段字符串添加注释
	  """_"""
	  f'{sn}'
	  r'\n')
orca_j35\n
```

注意，上述特性是在语法层次上定义的，但在编译时实现。在运行时必须使用 '+' 运算符连接字符串表达式。







由于字符串是[不可变的](https://docs.python.org/3/glossary.html#term-immutable)对象，因此不能对字符串本身做出修改。这意味着我们虽然可以查看字符串中的项，但并不能对其进行修改：

```python
>>> a_str = "Orca_J35"
>>> a_str[1]
'r'
>>> a_str[1]='R'
Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    a_str[1]='R'
TypeError: 'str' object does not support item assignment
```

字符串对象还拥有很多方法，但这些方法同样不会修改原字符串对象，而是会返回新的对象。

```python
>>> a_str = "Orca_J35"
>>> a_str.lower()
'orca_j35'
>>> a_str
'Orca_J35'
```

`str.lower()` 方法会将原字符串中的字母全部转化为小写，并返回转换后的结果，但不会修改原字符串。

tips: Python 中没有用于表示一个单一字符的数据类型(如 `char` )，因此我们应将一个单一字符视作长度为 1 的字符串。





See [String and Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#strings) for more about the various forms of string literal, including supported escape sequences, and the `r` (“raw”) prefix that disables most escape sequence processing.

## 1. 操作字符串

字符串作为一种不可变[序列](https://docs.python.org/3.7/glossary.html#term-sequence)，它支持各种[通用序列操作](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)：

| Operation              | Result                                                       |
| ---------------------- | ------------------------------------------------------------ |
| `x in s`               | `True` if an item of *s* is equal to *x*, else `False`       |
| `x not in s`           | `False` if an item of *s* is equal to *x*, else `True`       |
| `s + t`                | the concatenation of *s* and *t*                             |
| `s * n` or `n * s`     | equivalent to adding *s* to itself *n* times                 |
| `s[i]`                 | *i* th item of *s*, origin 0                                 |
| `s[i:j]`               | slice of *s* from *i* to *j*                                 |
| `s[i:j:k]`             | slice of *s* from *i* to *j* with step *k*                   |
| `len(s)`               | length of *s*                                                |
| `min(s)`               | smallest item of *s*                                         |
| `max(s)`               | largest item of *s*                                          |
| `s.index(x[, i[, j]])` | index of the first occurrence of *x* in *s* (at or after index *i* and before index *j*) |
| `s.count(x)`           | total number of occurrences of *x* in *s*                    |

更多细节请阅读笔记 "序列类型(list,tuple,range).md" 和 "[Common Sequence Operations](https://docs.python.org/3/library/stdtypes.html#common-sequence-operations)" 

### s[ i ]

`i` 被称为索引(*index*)，表示相对于序列中第一个元素的偏移量(*offset*)。因此，序列中的第一个元素的索引为 0，且索引只能是整数。索引可以是一个**负整数**，负索引表示相对于序列中最后一个元素的偏移量。序列对象会将负索引与序列长度相加，从而得到一个正索引。因此，负索引的绝对值不能大于序列的长度。

```
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
   0   1   2   3   4   5
  -6  -5  -4  -3  -2  -1
```

示例：

```python
>>> word = 'Python'
>>> word[0]
'P'
>>> word[5]
'n'
```

在 `s[i]` 中使用超过序列的长度的索引，便会抛出 IndexError 异常。

### s[ i : j ]

从序列中获取位于两个索引( `i` 和 `j`)间的子序列，子序列中包含索引为 `i` 的元素，但不包含索引为 `j` 的元素。

```
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
   0   1   2   3   4   5
  -6  -5  -4  -3  -2  -1
```

示例：

```python
>>> word = 'Python'
>>> word[2:5]
'tho'
>>> word[:2] + word[2:]
'Python'
```

如果 `i` 被省略，则将其视为 0，即 `s[:j] = s[0:j]` ；如果 `j` 被省略，则将其视为序列的长度，即 `s[:] = s[0:len(s)]` 。

在 `s[i:j]` 中，若 `i` 或 `j` 超出了序列长度，则会被自动替换为序列长度：

```python
>>> word[len(word)+1:]
''
>>> word[:len(word)+1]
'Python'
```

在 `s[i:j]` 中，若 `i` 的值大于等于 `j` ，则会返回空字符串：

```python
>>> word[2:2]
''
>>> word[3:2]
''
```

### 反转字符串

通过在切片中添加第三参数，可对切片进行反转

```python
>>> word = 'Python'
>>> word[::-1]
'nohtyP'
```

### 比较字符串对象

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





----

### 引号

#### 单引号/双引号

单引号和双引号完全相同，没有任何区别。
引号内所有的 space (spaces and tabs) 都照原样保留。 

如果`'`本身也是一个字符，那就可以用`""`括起来，如`"I'm OK"`

#### 三重引号 Triple Quotes

三重引号用于指定多行字符串 - (`"""` or `'''`)。
可在三重引号中自由使用单引号和双引号。例如：

```
'''This is a multi-line string. This is the first line.
This is the second line.
"What's your name?," I asked.
He said "Bond, James Bond."
'''
```

也可在多行字符串 `'''...'''` 前面加上 `r` 使用。

##### 行尾换行符

行尾换行符会被自动包含到字符串中，但是可以在行尾加上 `\` 来避免这个行为。下面的示例： 

```
print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
""")
```

输出如下（注意，不包括初始换行符）：

```
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to
```

### 转义序列

Escape Sequences

`\` 字符用于将非图形化的字符(如 换行符 `\n`, 制表符 `\t` 或 反斜杠 `\` )进行转义。

```
>>> print('I\'m learning\nPython.')
I'm learning
Python.
>>> print('\\\n\\')
\
\
```

如果字符串内部既包含`'`又包含`"`，可以用转义字符 `\` 来标识，比如：(注意有无 `print()` 语句的区别。)

```
>>> 'I\'m \"OK\"!'
'I\'m "OK"!'
>>> print('I\'m \"OK\"!')
I'm "OK"!
```

在行末的一个反斜杠 `\` 表示该字符串在下一行继续，此处不会添加换行符。
例如：

```
"This is the first sentence. \
This is the second sentence."
```

等效于：

```
"This is the first sentence. This is the second sentence."
```

### 原始字符串

Raw String

如果字符串里面有很多字符都需要转义，便会加入很多`\` 。
此时，为了简化操作，Python 允许使用 `r'...'` 表示 `'...'` 内部的字符串默认不转义：

```
>>> print('\\\t\\')
\       \
>>> print(r'\\\t\\')
\\\t\\
```

**注意：正则表达式用户**

当处理正则表达式时通常会使用原始字符串。否则会需要使用很多的反斜杠。例如，反向引用符可以写成 `'\\1'` or `r'\1'`.

### 将值转化为字符串

convert values to strings

 [`repr()`](https://docs.python.org/3/library/functions.html#repr) 或 [`str()`](https://docs.python.org/3/library/stdtypes.html#str) 函数，可将值转换为字符串。

#### repr(obj, /)

Return the canonical标准 string representation of the object.
For many object types, including most builtins, eval(repr(obj)) == obj.

Return a string containing a printable representation of an object. For many types, this function makes an attempt to return a string that would yield an object with the same value when passed to [`eval()`](https://docs.python.org/3/library/functions.html#eval), otherwise the representation is a string enclosed in angle brackets that contains the name of the type of the object together with additional information often including the name and address of the object. A class can control what this function returns for its instances实例 by defining a [`__repr__()`](https://docs.python.org/3/reference/datamodel.html#object.__repr__) method.

```
In [49]: eval(repr('12'))
Out[49]: '12'

In [50]: eval(str('12'))
Out[50]: 12
```

#### \_\_repr\_\_

> object. `__repr__` (*self*) 
>
> Called by the [`repr()`](../library/functions.html#repr) built-in function to compute the **“official”** string representation of an object. 
>
> If at all possible, this should look like a valid Python expression that could be used to recreate an object with the same value (given an appropriate environment). 
>
> If this is not possible, a string of the form `<...some useful description...>` should be returned. 
>
> The **return** value must be a string object. 
>
> If a class defines [`__repr__()`](#object.__repr__) but not [`__str__()`](#object.__str__), then [`__repr__()`](#object.__repr__) is also used when an “informal” string representation of instances of that class is required.
>
> This is typically used for **debugging**, so it is important that the representation is information-rich and unambiguous清晰.

```
class Student():
    def __init__(self, name):
        self.name = name

    def __repr__(self): # 返回值必须是字符串
        return 'Student object (name = {})'.format(self.name)


stu = Student('Bob')

#通过repr调用
stu_repr = repr(stu)
print(stu_repr)
print()

#print会请求 __str__
print(stu_repr)
```

输出：

```
Student object (name = Bob)

Student object (name = Bob)
```

- 若不定义 `__repr__` 方法：

```
class Student():
    def __init__(self, name):
        self.name = name

#    def __repr__(self):
#        return 'Student object (name = {})'.format(self.name)


stu = Student('Bob')
stu_repr = repr(stu)
print(stu_repr)
print()

#print会请求 __str__
print(stu_repr)
```

输出：

```
<__main__.Student object at 0x000002DE34B2D3C8>

<__main__.Student object at 0x000002DE34B2D3C8>
```

如果 `__str__` 和 `__repr__` 相同，可直接写作 `__repr__ = __str__` 。

```
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name=%s)' % self.name
    __repr__ = __str__
```



#### str(object='')

class str(object='')
class str(object=b'', encoding='utf-8', errors='strict')

Return a string version of object. If object is not provided, returns the empty string. Otherwise, the behavior of str() depends on whether encoding or errors is given, as follows.

#### \_\_str_\_

[`type(object).__str__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__str__)

> `object.` `__str__`(*self*)  
>
> Called by [`str(object)`](../library/stdtypes.html#str) and the built-in functions [`format()`](../library/functions.html#format) and [`print()`](../library/functions.html#print) to compute the “informal” or nicely printable string representation of an object. The return value must be a [string](../library/stdtypes.html#textseq) object.
>
> This method differs from [`object.__repr__()`](#object.__repr__) in that there is no expectation期望 that [`__str__()`](#object.__str__) return a valid Python expression: a more convenient or concise representation can be used.
>
> The default implementation defined by the built-in type [`object`](../library/functions.html#object) calls [`object.__repr__()`](#object.__repr__).

```
class Student():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Student object (name = {})'.format(self.name)


stu = Student('Bob')
stu_str = str(stu)
print(stu_str)
print()
print(stu_str)
```

输出：

```
Student object (name = Bob)

Student object (name = Bob)
```

如果没有定义 `__str__`

```
class Student():
    def __init__(self, name):
        self.name = name

#    def __str__(self):
#        return 'Student object (name = {})'.format(self.name)


stu = Student('Bob')
stu_str = str(stu)
print(stu_str)
print()
print(stu_str)
```

输出：

```
class Student():
    def __init__(self, name):
        self.name = name

#    def __str__(self):
#        return 'Student object (name = {})'.format(self.name)


stu = Student('Bob')
stu_str = str(stu)
print(stu_str)
print()
print(stu_str)
```



#### repr() vs str()

> The [`str()`](https://docs.python.org/3/library/stdtypes.html#str) function is meant to return representations of values which are fairly human-readable, while [`repr()`](https://docs.python.org/3/library/functions.html#repr) is meant to generate representations which can be read by the interpreter (or will force a [`SyntaxError`](https://docs.python.org/3/library/exceptions.html#SyntaxError) if there is no equivalent syntax). For objects which don’t have a particular representation for human consumption, [`str()`](https://docs.python.org/3/library/stdtypes.html#str) will return the same value as [`repr()`](https://docs.python.org/3/library/functions.html#repr). Many values, such as numbers or structures like lists and dictionaries, have the same representation using either function. Strings, in particular, have two distinct representations.

 [`str()`](https://docs.python.org/3/library/stdtypes.html#str) 函数意味着返回一个用于易读的表达形式，而 `repr()` 则意味着产生一个可以被解释器读取的形式( 如果没有等效语法，将会强制出现 [`SyntaxError`](https://docs.python.org/3/library/exceptions.html#SyntaxError) 异常 )。对于那些没有适于人类阅读的特定形式的对象， [`str()`](https://docs.python.org/3/library/stdtypes.html#str) 将会返回与 [`repr()`](https://docs.python.org/3/library/functions.html#repr) 相同的值。许多值，如数字；或结构，如列表和字典，使用这两个函数时会给出相同的形式。字符串比较特殊，会给出两种不同的展现形式。

一些示例：

```
>>> s = 'Hello, world.'
>>> str(s)
'Hello, world.'
>>> repr(s)
"'Hello, world.'"
>>> str(1/7)
'0.14285714285714285'
>>> x = 10 * 3.25
>>> y = 200 * 200
>>> s = 'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
>>> print(s)
The value of x is 32.5, and y is 40000...
>>> # The repr() of a string adds string quotes and backslashes 
	# 在repr()中的字符添加引号和反斜线:
... hello = 'hello, world\n'
>>> hellos = repr(hello)
>>> print(hellos)
'hello, world\n'
>>> # 传递给repr()的参数可以是任何 Python对象 
# The argument to repr() may be any Python object:
... repr((x, y, ('spam', 'eggs')))
"(32.5, 40000, ('spam', 'eggs'))"
```

示例，用于计算平方和立方：

```
>>> for x in range(1, 11):
...     print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
...     # Note use of 'end' on previous line 
...     print(repr(x*x*x).rjust(4))
...
 1   1    1
 2   4    8
 3   9   27
 4  16   64
 5  25  125
 6  36  216
 7  49  343
 8  64  512
 9  81  729
10 100 1000

>>> for x in range(1, 11):
...     print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))
...
 1   1    1
 2   4    8
 3   9   27
 4  16   64
 5  25  125
 6  36  216
 7  49  343
 8  64  512
 9  81  729
10 100 1000
```

示例中，每列之间的第一个空格有 `print()` 自动添加。`print()` 会自动将两个参数间的逗号替换为空格。

 [`str.rjust()`](https://docs.python.org/3/library/stdtypes.html#str.rjust) 右对齐字符串，同样也可以使用切片 如  `x.ljust(n)[:n]` 
 [`str.ljust()`](https://docs.python.org/3/library/stdtypes.html#str.ljust) 左对齐
 [`str.center()`](https://docs.python.org/3/library/stdtypes.html#str.center)中心对齐
 [`str.zfill()`](https://docs.python.org/3/library/stdtypes.html#str.zfill) 在数值字符串的左侧填充 0
字符串方法会返回一个新的字符串。
因此也可以直接使用切片功能，如：`str.ljust(n)[:n]`





### 操作字符串的方法

- [String Methods](https://docs.python.org/3/library/stdtypes.html#string-methods) 

  Strings support a large number of methods for basic transformations and searching. 
  字符串支持大量的基本转换和搜索方法。

Python 中的字符串都是 `str` 类的对象。
此处演示`str` 类中的的一些方法。
完整方法列表，可查看 `help(str)` 。

Example (save as `ds_str_methods.py`):

```python
# This is a string object
name = 'Swaroop'

if name.startswith('Swa'):
    print('Yes, the string starts with "Swa"')

if 'a' in name:
    print('Yes, it contains the string "a"')
#不存在，返回-1。在if语句中-1也为真，0为假
if name.find('war') != -1:
    print('Yes, it contains the string "war"')

delimiter = '_*_'
mylist = ['Brazil', 'Russia', 'India', 'China']
print(delimiter.join(mylist))
```

Output:

```python
$ python ds_str_methods.py
Yes, the string starts with "Swa"
Yes, it contains the string "a"
Yes, it contains the string "war"
Brazil_*_Russia_*_India_*_China
```

- `startswith` 方法被用于检测原字符串是否以给定的字符串开头。
- `in` 操作符用于检测给定字符串是否是当前字符串的一部分。
- `find` 方法用于定位给定字符串在原字符串中的位子，如果没有找到子字符串 `find` 返回 -1。
- `str` 类拥有一个优雅的`join`方法，该方法将一个字符串序列项作为另序列中各个项目之间的分隔符，从该字符串中生成并返回一个更大的字符串。

### 字符串运算符

1. `+`  表示连接两个字符串； `*` 表示重复某字符串。
   可用于操作变量。

```
>>> # 3 times 'un', followed by 'ium'
>>> 3 * 'un' + 'ium'
'unununium'
>>> prefix + 'thon'
'Python'
```

1. 彼此相邻的字符串字面量，会自动连接在一起：

   注意：该方法只适用于字面量，不能包含表达式和变量。

```
>>> 'Py''thon'
'Python'

>>> prefix = 'Py'
>>> prefix 'thon'  # can't concatenate a variable and a string literal
  ...
SyntaxError: invalid syntax
>>> ('un' * 3) 'ium'
  ...
SyntaxError: invalid syntax
```

```
当想要断开很长的字符串时，此功能特别有用：
```

```
>>> text = ('Put several strings within parentheses '
...         'to have them joined together.')
>>> text
'Put several strings within parentheses to have them joined together.'
```

1. 

