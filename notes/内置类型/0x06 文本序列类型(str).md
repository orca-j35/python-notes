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

还可使用 `str()` 构造函数从其它对象创建字符串，具体使用方法如下：

### 1.1 str(*object*)

🔨 *class* str(*object=''*)

此时，该函数将返回 *object* 的字符串版本，使用方法如下：

```
str(object='') -> str
 | str() -> empty string ''
 | str(object) -> type(object).__str__()
 |
 | object 可以是任意对象，包括 bytes 和 buffer 的实例
```

`type(object).__str__()` 会返回一个字符串——该字符串会以适于打印的(或非正式的)形式来描述 *object*。

```python
>>> str("orca_j35") # 字符串实例，将返回其自身
'orca_j35'
>>> str(b'abs') # bytes实例
"b'abs'"
>>> str(list)				  
"<class 'list'>"
>>> str([1,2])					  
'[1, 2]'
```

如果 `type(object)` 没有 `__str__()` 方法，则会返回 [`repr(object)`](https://docs.python.org/3.7/library/functions.html#repr)：

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
str(object[, encoding[, errors]]) -> str
 | str(object, encoding='...') -> object.decode(encoding='...')
 | str(object, errors='...') -> object.decode(errors='...')
 | str(object, encoding='...', errors='...') -> object.decode(encoding='...', errors='...')
 | 
 | object 必须是 bytes 和 buffer 的实例
```

各参数的含义如下：(这三个参数均是 *positional-or-keyword*)

- *object* 是被解码的 [bytes-like](https://docs.python.org/3.7/glossary.html#term-bytes-like-object) 对象：
  - 如果 *object* 是 `bytes`(或 `bytearray`)对象， `str(object, encoding, errors)`会调用 [`object.decode(encoding, errors)`](https://docs.python.org/3.7/library/stdtypes.html#bytes.decode) 并返回其结果
  - 否则，`str(object, encoding, errors)` 会先获取缓冲器对象下的字节对象，然后再调用 `object.decode()` 并返回其结果
- *encoding* 用于设置编码方案，会被传递给 `bytes_or_buffer.decode()`，其默认值是 `sys.getdefaultencoding()`，可在 [Standard Encodings](https://docs.python.org/3.7/library/codecs.html#standard-encodings) 中可查看编码方案列表。
- *errors* 用于设置[错误处理方案](https://docs.python.org/3.7/library/codecs.html#error-handlers)，也会被传递给 `bytes_or_buffer.decode()`，其默认值是 `'strict'`。*errors* 可以是 `'ignore'`, `'replace'`, `'xmlcharrefreplace'`, `'backslashreplace'` 或任何已通过 [`codecs.register_error()`](https://docs.python.org/3.7/library/codecs.html#codecs.register_error) 注册的名称。

```python
>>> a_bytes = bytes('鲸','utf-8') # 对Unicode码点按照UTF8编码
>>> a_bytes
b'\xe9\xb2\xb8'
>>> str(a_bytes,'utf-8') # 对bytes对象进行解码
'鲸'
>>> str(a_bytes,'ascii') # 提供错误的编码方案会抛出异常
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    str(a_bytes,'ascii')
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 0: ordinal not in range(128)
>>> str(a_bytes,'ascii','ignore') # 修改错误处理方案
''
```

有关缓冲区对象的详细信息，可阅读 [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3.7/library/stdtypes.html#binaryseq) 和 [Buffer Protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects)。

Tips: 在 Python 文档中，"编码(*encoding*)"是指将 Unicode 字符串转换为字节序列的规则，也就是说"编码"包含了从"抽象字符序列"到"字节序列"的全部过程；反之，"解码"则包含了从"字节序列"到"抽象字符序列"的全部过程。

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

## 4. 参考





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

https://docs.python.org/3.7/reference/datamodel.html#object.__str__

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

### 



