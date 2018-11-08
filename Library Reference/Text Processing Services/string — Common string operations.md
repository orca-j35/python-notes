# string — 通用字符串操作

Common string operations

> 本笔记介绍了 string 模块的各项功能，提供了更丰富的示例，但并没有逐字翻译原文档中的内容。
> 在阅读笔记时，可同时参考下述资料：
> 
> - [string — Common string operations](https://docs.python.org/3.7/library/string.html#module-string) 
> 
> - [string — 字符串常量和模板](https://pythoncaff.com/docs/pymotw/string-string-constants-and-templates/76)
> 
> - string 模块源代码

`string` 模块始于最早的 Python 版本，早先在该模块中实现的许多功能大多已被转移到了 `str` 中。

## String constants

```python
# Some strings for ctype-style character classification
whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace
```

## Custom String Formatting

通过继承 `string.Formatter` 类，我们可使用与 `str.format` 相同的实现方式来创建自定义的字符创格式化行为。[`str.format()`](https://docs.python.org/3.7/library/stdtypes.html#str.format) 和 `string.Formatter` 类采用同一套语法来格式化字符串，即格式化字符串语法(请阅读下一小节)，但可通过 `string.Formatter` 的子类来自定义格式化行为。

tips: `str.format` 与 `string.Formatter` 拥有相同的实现方式，如果想了解 `str.format` 的实现方式 ，可以参考上本节。

**class string.Formatter**

- **format**(*format_string*, \**args*, \*\**kwargs*) - 主 API 方法，用于获取参数并返回 `vformat` 方法的调用，相当于 `vformat` 方法的包装器(wrapper)。

  ```python
  >>> from string import Formatter
  >>> f = Formatter()
  >>> f.format('format_string：{0}_{1}', 'Orca', 'J35')
  'format_string：Orca_J35'
  >>> f.format('format_string：{0}_{1}', *('Orca', 'J35'))
  'format_string：Orca_J35'
  ```

  Changed in version 3.7: A format string argument is now [positional-only](https://docs.python.org/3.7/glossary.html#positional-only-parameter).

- **vformat**(*format_string*, *args*, *kwargs*) - 该方法是实际执行格式化操作的地方。将该方法作为一个独立方法的原因是：当实参已被打包到某种数据结构中时，可跳过对实参进行解包的步骤 —— 免去需要先拆封参数到 `format` 方法，然后通过 `format` 方法再次打包参数，然后再调用 `vformat` 方法的重复操作。`vformat` 会将 `format_string` 拆分为字符数据和替换字段。

  ```python
  >>> f.vformat('format_string：{0}_{1}', ('Orca', 'J35'),{})
  'format_string：Orca_J35'
  ```

  `vformat` 会调用下面的方法来完成格式化操作：(下面这些方法均可被子类覆写，从而达到自定义格式操作的目的)

- **parse**(*format_string*) - 将 *field_name* 解析为一个元组，元组中的每一项包含四个元素(*literal_text*, *field_name*, *format_spec*, *conversion*)。源代码如下：

  ```python
  # returns an iterable that contains tuples of the form:
  # (literal_text, field_name, format_spec, conversion)
  # literal_text can be zero length
  # field_name can be None, in which case there's no
  #  object to format and output
  # if field_name is not None, it is looked up, formatted
  #  with format_spec and conversion and then used
  def parse(self, format_string):
      return _string.formatter_parser(format_string)
  ```

  示例 - 展示 `_string.formatter_parser` 的解析结构，以了解 `format_string` 被解析后的状态：

  ```python
  >>> import _string
  >>> for x in _string.formatter_parser('{0!s:<}_{1} is {hero!r:>}'):print(x)
  
  ('', '0', '<', 's')
  ('_', '1', '', None)
  (' is ', 'hero', '>', 'r')
  ```

- **get_field**(*field_name*, *args*, *kwargs*) - 源代码如下：

  ```python
  ​```python
    # given a field_name, find the object it references.
    #  field_name:   the field being looked up, e.g. "0.name"
    #                 or "lookup[3]"
    #  used_args:    a set of which args have been used
    #  args, kwargs: as passed in to vformat
    def get_field(self, field_name, args, kwargs):
        first, rest = _string.formatter_field_name_split(field_name)
  
        obj = self.get_value(first, args, kwargs)
  
        # loop through the rest of the field_name, doing
        #  getattr or getitem as needed
        for is_attr, i in rest:
            if is_attr:
                obj = getattr(obj, i)
                else:
                    obj = obj[i]
  
         return obj, first
  ```

  *field_name* 可以是复合字段名(如，`"0.name"`、`"lookup[3]"`、`"key.attr"` )，但 `get_value` 方法只会使用复合字段名的第一部分(如，`0`、`"lookup"`、`"key"` )来寻找 *args* 和 *kwargs* 中的匹配项。符合字段名的后续部分会通过 `getattr` 或索引来获取。比如，对于复合字段名 `"0.name"`，会将 `0` 用作 [`get_value()`](https://docs.python.org/3.7/library/string.html#string.Formatter.get_value) 的 *key* 参数，而 `name` 字段则会在 `get_field` 方法中通过 `getattr` 获取。

  示例 - 演示复合字段名的分拆方式：

  ```python
    >>> first, rest =_string.formatter_field_name_split('hero[1].help')
    >>> for i,j in rest:print(i,j)
  
    False 1
    True help
  ```

   示例 - 演示了复合字段名的使用方法

  ```python
    >>> f = Formatter()
    >>> f.format(
        '{0[1]}_{num.__class__}',
        'Orca',
        num='J35',
    )
    "r_<class 'str'>"
  ```

- **get_value**(*key*, *args*, *kwargs*)

  ```python
  def get_value(self, key, args, kwargs):   
      if isinstance(key, int):
          return args[key]
      else:
          return kwargs[key]
  ```

- **check_unused_args**(*used_args*, *args*, *kwargs*) - 检查未使用的参数

  ```python
  def check_unused_args(self, used_args, args, kwargs):
      pass
  ```

- **format_field**(*value*, *format_spec*)

  ```python
  def format_field(self, value, format_spec):
      return format(value, format_spec)
  ```

- **convert_field**(*value*, *conversion*) - 用于转换 `get_field()` 的返回值，*conversion* 位于 `parse` 返回的数组中。

  ```python
  def convert_field(self, value, conversion):
      # do any conversion on the resulting object
      if conversion is None:
          return value
      elif conversion == 's':
          return str(value)
      elif conversion == 'r':
          return repr(value)
      elif conversion == 'a':
          return ascii(value)
      raise ValueError("Unknown conversion specifier {0!s}".format(conversion))
  ```

### 嵌套的替换字段

顶层替换字段可能会包含嵌套的替换字段(如 `{value:{width}}`)。这些嵌套的替换字段可能会包含它们自己的转换字段和格式化序列，但是不能包含更深层次的嵌套字段，否则会抛出 `ValueError` 异常。

```python
>>> from string import Formatter
>>> f = Formatter()
>>> f.format("result: {value:{width}}",width=10, value=12.34567)
'result:   12.34567'
>>> "result: {value:{width}}".format(
    width=10, precision=4, value=12.34567)
'result:   12.34567'
```

在这个示例中，顶层替换替换字段是 `"result: {value:{width}}"` ，第二层替换字段是 `"{value:{width}}"`，第三层嵌套字段是 `"{width}"`。

## Format String Syntax

`str.format()` 和 `string.Formatter()` 类均采用格式化字符串语法(*Format String Syntax*)，该该语法和 *f-string* 的语法相似，但存在一些区别。

tips: `str.format` 与 `string.Formatter` 拥有相同的实现方式，如果想了解 `str.format` 的实现方式 ，可以参考上 Custom String Formatting 小节。

在格式化字符串语法中，替换字段(*replacement fields*)被置于花括号中。任何被置于花括号之外的内容均被视为文本字面值，会被直接复制到输出结果中。双层花括号( `'{{'`  或  `'}}'` )会被替换为对应的单个花括号。

大多数情况下，用于格式化字符串的新式语法和旧式语法拥有相似的规则。在新式语法中使用 `{}` 和 `%` 替换了旧式语法中的 `%`。比如旧式语法中的 `'%03.2f'` 可被翻译为 `'{:03.2f}'`。另外，新式语法还支持一些新选项。

替换字段的语法如下：

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
field_name        ::=  arg_name ("." attribute_name | "[" element_index "]")*
arg_name          ::=  [identifier | digit+]
attribute_name    ::=  identifier
element_index     ::=  digit+ | index_string
index_string      ::=  <any source character except "]"> +
conversion        ::=  "r" | "s" | "a"
format_spec       ::=  <described in the next section>
```

### arg_name

🔨 Formatter.format(*format_string*, \**args*, \*\**kwargs*) 

🔨 str.format(\**args*, \*\**kwargs*)

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
field_name        ::=  arg_name ("." attribute_name | "[" element_index "]")*
arg_name          ::=  [identifier | digit+]
```

利用 `arg_name` 获得相应实参的过程等效于以下源代码：

```python
def get_value(self, arg_name, args, kwargs):
    '''args,kwargs:是str.format(或Formatter.format)的var-positional和var-keyword'''
    if isinstance(arg_name, int):
        return args[arg_name]
    else:
        return kwargs[arg_name]
```

`arg_name` 可引用位置实参和关键字实参：

- 当 `arg_name` 是数值时，便会引用 *args* 中相应位置的实参

  ```python
  >>> '{0}, {1}, {2}'.format('a', 'b', 'c', 'd') # 可存在未使用的参数
  'a, b, c'
  >>> '{2}, {1}, {0}'.format('a', 'b', 'c')
  'c, b, a'
  >>> '{2}, {1}, {0}'.format(*'abc')      # 解包参数序列
  'c, b, a'
  >>> '{0}{1}{0}'.format('abra', 'cad')   # 参数可被重复引用
  'abracadabra'
  ```

- 当 `arg_name` 为空时，便会自动依次引用 *args* 中的位置实参

  ```python
  >>> '{}, {}, {}'.format('a', 'b', 'c')  # 3.1+ only
  'a, b, c'
  >>> '{}_{1}'.format('orca','j35','extra_value') # 不能混用自动模式和手动模式
  Traceback (most recent call last):
    File "<pyshell#30>", line 1, in <module>
      '{}_{1}'.format('orca','j35','extra_value')
  ValueError: cannot switch from automatic field numbering to manual field specification
  ```

  Changed in version 3.1: The positional argument specifiers can be omitted for [`str.format()`](https://docs.python.org/3.7/library/stdtypes.html#str.format), so `'{} {}'.format(a, b)` is equivalent to `'{0} {1}'.format(a, b)`.

  Changed in version 3.4: The positional argument specifiers can be omitted for [`Formatter`](https://docs.python.org/3.7/library/string.html#string.Formatter).

- 当 `arg_name` 是关键字时，便会引用 *kwargs* 中相应的关键字实参。

  ```python
  >>> '{whale}_{sn}'.format(whale='orca',sn='j35')
  'orca_j35'
  >>> coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
  >>> 'Coordinates: {latitude}, {longitude}'.format(**coord)
  'Coordinates: 37.24N, -115.81W'
  >>> '{}_{sn}'.format('orca',sn='j35') # 可以和手动数值模式混用
  'orca_j35'
  >>> '{0}_{sn}'.format('orca',sn='j35') # 可以和自动数值模式混用
  'orca_j35'
  ```

### field_name

🔨 Formatter.format(*format_string*, \**args*, \*\**kwargs*) 

🔨 str.format(\**args*, \*\**kwargs*)

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
field_name        ::=  arg_name ("." attribute_name | "[" element_index "]")*
```

利用 `field_name` 获得"替换对象"的过程等效于以下源代码：

```python
# given a field_name, find the object it references.
#  field_name:   the field being looked up, e.g. "0.name"
#                 or "lookup[3]" or "loopup[index_string]"
#  args,kwargs:是str.format(或Formatter.format)的var-positional和var-keyword
def get_field(self, field_name, args, kwargs):
    arg_name, rest = _string.formatter_field_name_split(field_name)
    obj = self.get_value(arg_name, args, kwargs)

    # loop through the rest of the field_name, doing
    #  getattr or getitem as needed
    for is_attr, i in rest:
        if is_attr:
            obj = getattr(obj, i)
            else:
                obj = obj[i]
     return obj, arg_name
```

`arg_name` 后可接任意数量的索引或属性表达式：

```python
>>> # 访问参数的索引位置
>>> d = dict(whale='orca',sn='j35')
>>> s=('orca','j35')
>>> '{key[whale]}_{0[1]}'.format(s,key=d)
'orca_j35'
>>> # 访问参数的属性
>>> class Orca:
    def __init__(self):
        self.whale='orca'
        self.sn='j35'


>>> '{0.whale}_{0.sn}'.format(Orca())
'orca_j35'
```

### conversion

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
conversion        ::=  "r" | "s" | "a"
```

`conversion` 用于将通过 `field_name` 获得的"替换对象"进行强制类型转换，利用 `conversion` 进行强制转换的过程等效于以下源代码：

```python
def convert_field(self, obj, conversion):
    # do any conversion on the resulting object
    if conversion is None:
        return obj
    elif conversion == 's':
        return str(obj)
    elif conversion == 'r':
        return repr(obj)
    elif conversion == 'a':
        return ascii(obj)
    raise ValueError("Unknown conversion specifier {0!s}".format(conversion))
```

示例

```python
>>> "repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2')
"repr() shows quotes: 'test1'; str() doesn't: test2"
```

### format_spec

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
format_spec       ::=  <described in the next section>
```

`format_spec` 字段用于配合 [`format()`](https://docs.python.org/3.6/library/functions.html#format) 协议对"替换对象" (或是经转换后的结果) 进行格式化。`format_spec` 会被传递到表达式的"替换对象"的  [`__format__()`](https://docs.python.org/3.6/reference/datamodel.html#object.__format__) 方法中，或是被传递到经转换后的结果的 [`__format__()`](https://docs.python.org/3.6/reference/datamodel.html#object.__format__) 方法中。当格式说明符被省略时，会传递一个空字符串。然后将格式化之后的最终结果插入到整个字符串的最终值中。利用 `format_spec` 进行格式化的过程等效于以下源代码：

```python
def format_field(self, value, format_spec):
    return format(value, format_spec)
```

`format_spec` 字段描述了"替换对象" (或是经转换后的结果)的格式化规则，详细的格式化规则会在 Format Specification Mini-Language 小节中讲解。

### 嵌套替换字段

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
```

顶层替换字段可能会包含嵌套的替换字段(如 `{value:{width}}`)。这些嵌套的替换字段可能会包含它们自己的转换字段和格式化序列，但是不能包含更深层次的嵌套字段，否则会抛出 `ValueError` 异常。

```python
>>> from string import Formatter
>>> f = Formatter()
>>> f.format("result: {value:{width}}",width=10, value=12.34567)
'result:   12.34567'

>>> "result: {value:{width}}".format(
    width=10, precision=4, value=12.34567)
'result:   12.34567'
```

在这个示例中，顶层替换替换字段是 `"result: {value:{width}}"` ，第二层替换字段是 `"{value:{width}}"`，第三层嵌套字段是 `"{width}"`—— 最多也只能包含三层，否则会抛出异常

### Format Specification Mini-Language

以下均采用了本节讲述的格式化规范：

- `str.format()`  
- `string.Formatter` 
- *f-string*
- [`format()`](https://docs.python.org/3.7/library/functions.html#format) 内置函数

实际上 `str.format()`、`string.Formatter`、*f-string* 最终均是通过内置函数 `format()` 来完成替换字段的格式化操作的。

格式化说明符的标准形式如下(部分格式化选项仅支持数值类型)：

```
format_spec     ::=  [[fill]align][sign][#][0][width][grouping_option][.precision][type]
fill            ::=  <any character>
align           ::=  "<" | ">" | "=" | "^"
sign            ::=  "+" | "-" | " "
width           ::=  digit+
grouping_option ::=  "_" | ","
precision       ::=  digit+
type            ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"
```

#### fill & align

```
format_spec::=[[fill]align][sign][#][0][width][grouping_option][.precision][type]
fill            ::=  <any character>
align           ::=  "<" | ">" | "=" | "^"
```

`fill` 字段表示填充字符，在 `str.format()`、`string.Formatter`、*f-string* 中不能使用花括号 `{}` 作为填充字符，但在内置函数 `format()` 中可使用花括号作为填充字符。如果 `align` 是一个有效值，则会使用 `fill` 字符进行填充。

```python
>>> '{0:_>10},{1:_<10}'.format('orca','j35')
'______orca,j35_______'
>>> format('orca','{>10')
'{{{{{{orca'
```

tips: 除非定义了最小宽度，否则替换字段的宽度始终与填充它的数据的宽度相同。因此，在没有定义最小宽度情况下，使用 `align` 字段是没有意义的。

`align` 的可选值如下：

| Option | Meaning                                                                                                |
| ------ | ------------------------------------------------------------------------------------------------------ |
| `'<'`  | 强制替换字段在可用空间内左对齐(大多数对象的默认对齐方式)                                                                          |
| `'>'`  | 强制替换字段在可用空间内右对齐(数值对象的默认对齐方式)                                                                           |
| `'='`  | 强制将 `fill` 填充到 `sign` 和数字之间，用于打印形如 `+000000120` 的字段。该对齐选项仅对数值类型有效。当 `'0'` 紧邻 `width` 字段之前时，会默认使用本对齐方式。 |
| `'^'`  | 强制替换字段在可用空间内居中                                                                                         |

```python
>>> '{0:10},{1:<10}'.format('orca','j35') # 字符串默认<
'orca      ,j35       '
>>> '{0:10},{1:>10}'.format(61,35) # 数值对象默认>
'        61,        35'
>>> '{:^30}'.format('centered')
'           centered           '
>>> '{:*^30}'.format('centered')  # use '*' as a fill char
'***********centered***********'
>>> '{0:0=+10},{1:0=10}'.format(+61,-35)
'+000000061,-000000035'
>>> '{0:+010},{1:010}'.format(+61,-35)
'+000000061,-000000035'
```

#### sign

```
format_spec::=[[fill]align][sign][#][0][width][grouping_option][.precision][type]
sign            ::=  "+" | "-" | " "
```

`sign` 字段只能用于数值类型，可选值如下：

| Option | Meaning                     |
| ------ | --------------------------- |
| `'+'`  | 表示正数和负数都会使用符号               |
| `'-'`  | 表示只有负数会使用符号(默认行为)           |
| space  | 表示会在正数前面使用一个前导空格，会在负数前面使用负号 |

```python
>>> '{0},{1}'.format(10,-1) # 默认-
'10,-1'
>>> '{0:+},{1:+}'.format(10,-1)
'+10,-1'
>>> '{0:-},{1:-}'.format(10,-1)
'10,-1'
>>> '{0: },{1: }'.format(10,-1)
' 10,-1'
```

#### \#

```
format_spec::=[[fill]align][sign][#][0][width][grouping_option][.precision][type]
```

 `'#'` 的意思是使用"替代形式(*alternate form*) "表示转换后的内容。该选项仅对整数、浮点数、复数和 Decimal 类型有效，并且每种类型的"替代形式"均不相同。

对于整数，"替代形式"是指为不同的进制添加相应的前缀：

```python
>>> # format also supports binary numbers
>>> "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(42)
'int: 42;  hex: 2a;  oct: 52;  bin: 101010'
>>> # with 0x, 0o, or 0b as prefix:
>>> "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(42)
'int: 42;  hex: 0x2a;  oct: 0o52;  bin: 0b101010'
```

对于浮点数、复数和 Decimal，"替代形式"会使得转换结果中始终包含小数点，即便没有小数位也会如此：

```python
>>> # 如果精度为0，由于没有小数位，则不会保留小数点
>>> "float: {0:.0f}".format(6)
'float: 6'
>>> # 如果使用替代形式，则始终保留小数点
>>> "float: {0:#.0f}".format(6)
'float: 6.'
```

对于 `'g'` 和 `'G'` 转换，"替代形式"则会导致结果始终包含小数点，并且不会从结果中删除尾随零。

```python
>>> "{:g}".format(0.00002) # 如果结果没小数部分，则只保留整数部分
'2e-05'
>>> "{:#g}".format(0.00002) # 会保留小数点和尾随零
'2.00000e-05'
>>> "{:#.0g}".format(0.00002) # 强行压缩精度，也会保留小数点
'2.e-05'
```

#### grouping_option

```
format_spec::=[[fill]align][sign][#][0][width][grouping_option][.precision][type]
grouping_option ::=  "_" | ","
```

`','` 表示将逗号用作千位分隔符。如果需要使用与当前区域匹配的分隔符，使用 `'n'` 作为 `type` 的值。

```python
>>> "{0:,}".format(100000)
'100,000'
>>> "{0:,d}".format(100000)
'100,000'
>>> "{0:,f}".format(100000)
'100,000.000000'
```

Changed in version 3.1: Added the `','` option (see also [**PEP 378**](https://www.python.org/dev/peps/pep-0378)).

`'_'` 表示将下划线用作浮点数和十进制整数 (`'d'`) 的千位分隔符，对于其它进制的整数，则会四个数字一组进行分隔。不支持 `type` 中的其它值，会抛出异常。

```python
>>> "{0:_}".format(100000)
'100_000'
>>> "{0:_d}".format(100000)
'100_000'
>>> "{0:_f}".format(100000)
'100_000.000000'
```

Changed in version 3.6: Added the `'_'` option (see also [**PEP 515**](https://www.python.org/dev/peps/pep-0515)).

#### width

```
format_spec::=[[fill]align][sign][#][0][width][grouping_option][.precision][type]
```

`width` 是一个十进制整数，表示替换字段的**最小宽度**。如果没有给出 `width` 的值，则替换字段长度由数据内容自身的长度决定。

对于数值类型，如果没有显式给出对齐方式，并且当 `width` 紧接在 `'0'`  之后时，会在结果中会使用 `0` 填充输出结果的左侧。等效于  `fill` 值为 `"0"` 且 `align` 值为 `"="` 。

```python
>>> '{0:+010},{1:010}'.format(+61,-35)
'+000000061,-000000035'
>>> '{0:0=+10},{1:0=10}'.format(+61,-35)
'+000000061,-000000035'
```

#### .precision

```
format_spec::=[[fill]align][sign][#][0][width][grouping_option][.precision][type]
```

当使用 `'f'` 和 `'F'` 对浮点数进行格式化时，`precision` 表示浮点数的小数位数；：

```python
>>> '{0:.4f}'.format(2)
'2.0000'
>>> '{0:.4f}'.format(0.000021111111)
'0.0000'
```

当使用 `'g'` 和 `'G'` 对浮点数进行格式化时，`precision` 表示小数点前后总的有效位数：

```python
>>> '{0:.4g}'.format(0.00021111111)
'0.0002111'key
>>> '{0:.4g}'.format(0.000021111111)
'2.111e-05'
```

对于非数值类型，`precision` 表示替换字段的最大长度

```python
>>> '{0:.4}'.format('abcdef')
'abcd'
```

tips: `precision` 不能用于整数类型

#### type

```
format_spec::=[[fill]align][sign][#][0][width][grouping_option][.precision][type]
```

"替换对象"的呈现方式由 `type` 决定。

可用于字符串的 `type` 值如下：

| Type  | Meaning                                          |
| ----- | ------------------------------------------------ |
| `'s'` | 字符串格式，这是字符串的默认 `type` 值，可以省略 |
| None  | 等效于 `'s'`                                     |

可用于整数的 `type` 值如下：

| Type  | Meaning                                                      |
| ----- | ------------------------------------------------------------ |
| `'b'` | 二进制格式                                                   |
| `'c'` | 字符，将整数转换为对应的 Unicode 字符。                      |
| `'d'` | 十进制格式                                                   |
| `'o'` | 八进制格式                                                   |
| `'x'` | 十六进制格式，使用小写字母                                   |
| `'X'` | 十六进制格式，使用大写字母                                   |
| `'n'` | 数字，与 `'d' ` 相同，但会根据当前语言环境插入来恰当的数字分隔符 |
| None  | 等效于 `'d'`                                                 |

```python
>>> "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(42)
'int: 42;  hex: 2a;  oct: 52;  bin: 101010'
>>> # with 0x, 0o, or 0b as prefix:
>>> "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(42)
'int: 42;  hex: 0x2a;  oct: 0o52;  bin: 0b101010'
>>> '{0:c}'.format(10)
'\n'
```

另外，适用于浮点数的 `type` 值(`'n'` 和 `None` 除外)也可用于整数。当对整数使用浮点数的 `type` 值时，会使用 `float()` 函数将整数转换为浮点数。

可用于浮点数的 `type` 值如下：

| Type  | Meaning                                                      |
| ----- | ------------------------------------------------------------ |
| `'e'` | 指数表示法。使用字母 'e' 表示指数，并以科学计数法打印数值。默认精度是 `6` |
| `'E'` | 指数表示法。除了改用 'E' 表示指数外，其余效果与 `'e'` 相同。 |
| `'f'` | 定点表示法。将数值显式为一个定点数。默认精度是 `6`           |
| `'F'` | 定点表示法，与 `'f'` 相同，但是会将 `nan` 转换为 `NAN` ，将 `inf` 转换为 `INF`. |
| `'g'` | 通用格式，会先依照给定精度`p >= 1`，将数值舍入为 `p` 位有效数值，然后根据舍入结果的数量级选择"定点表示法"或"科学计数法"。简单来讲，如果指数小于 -4 或大于等于精度时，会采用 `'e'` 格式；否则采用小数格式的浮点数。<br />精度规则：首先会尝试采用"科学计数法"进行格式化，并假定精度是 `p-1` (留一位给个位使用)，此时经格式化后的指数值是 `exp`。如果 `-4 <= exp < p`，则会采用"定点表示法"格式化原数值，精度为`p-1-exp`；否则会采用"科学计数法"格式化原数值，精度为`p-1` 。在者两种情况下都会从有效数字中删除不重要的尾随零，如果小数点后没有数字，则会一并删除小数点。<br />正无穷和负无穷被格式化为`inf`和 `-inf`；正零和负零被格式化为 `0` 和 `-0`；nans 被格式化为 `nan`。以上三者和精度无关。<br />精度 `0` 被视为等于精度 `1`；默认精度是 `6`. |
| `'G'` | 通用格式，除了使用大写 `'E'` 之外，和 `'g'` 完全相同。另外，无穷数和 nans 也会被记作大写。 |
| `'n'` | 数字，与 `'g' ` 相同，但会根据当前语言环境插入来恰当的数字分隔符 |
| `'%'` | 百分比，将数字乘以 100 并以固定(`'f'`)格式显示，同时将百分号作为后缀。 |
| None  | 与 `'g'` 类似，除了在使用"定点表示法"时，小数点后至少有一位数字。默认精度与需要被表示的值一样高。整体效果与调用 `str()` 的相同，并会更具有其它格式化修饰符进行调整。 |

示例 - 展示和浮点数相关的 `type` 值：

```python
>>> points = 19
>>> total = 22
>>> 'Correct answers: {:.2%}'.format(points/total)
'Correct answers: 86.36%'
>>> format(0.00003141566) #和g相同
'3.141566e-05'
```

tips: 在保留精度时会进行舍入，而非直接截断。

```python
>>> '{0:.3f}'.format(0.6666)
'0.667'
```

### 复杂示例

```python
>>> for align, text in zip('<^>', ['left', 'center', 'right']):
...     '{0:{fill}{align}16}'.format(text, fill=align, align=align)
...
'left<<<<<<<<<<<<'
'^^^^^center^^^^^'
'>>>>>>>>>>>right'
>>>
>>> octets = [192, 168, 0, 1]
>>> '{:02X}{:02X}{:02X}{:02X}'.format(*octets)
'C0A80001'
>>> int(_, 16)
3232235521
>>>
>>> width = 5
>>> for num in range(5,12): 
...     for base in 'dXob':
...         print('{0:{width}{base}}'.format(num, base=base, width=width), end=' ')
...     print()
...
    5     5     5   101
    6     6     6   110
    7     7     7   111
    8     8    10  1000
    9     9    11  1001
   10     A    12  1010
   11     B    13  1011
```

### 特定的格式化方式

有些类型拥有特定的格式化方式：

```python
>>> import datetime
>>> d = datetime.datetime(2010, 7, 4, 12, 15, 58)
>>> '{:%Y-%m-%d %H:%M:%S}'.format(d)
'2010-07-04 12:15:58'
```

## Template strings

模板字符串只负责执行替换操作，不支持格式化语法(例如，无法控制浮点数的精度)。

### 初级用法

在初级用法中，直接使用 Template 类即可，下面是可用的实例属性：

> class string.Template(template)
> 
> - substitute(mapping, **kwds) # 替换占位符
> 
> - safe_substitute(mapping, **kwds) # 安全替换占位符
> 
> - template # 查看或修改字符串模板

默认情况下，模板字符串支持基于 `$` 的替换规则，具体如下：(注意：占位符区分大小写)

> - `$$` is an escape; it is replaced with a single `$`.
> 
> - `$identifier` names a substitution placeholder matching a mapping key of`"identifier"`. By default, `"identifier"` is restricted to any case-insensitive ASCII alphanumeric string (including underscores) that starts with an underscore or ASCII letter. The first non-identifier character after the `$` character terminates this placeholder specification.
> 
> - `${identifier}` is equivalent to `$identifier`. It is required when valid identifier characters follow the placeholder but are not part of the placeholder, such as `"${noun}ification"`.

示例 - 展示初级用法，`$var` 是占位符

```python
>>> from string import Template
>>> values = {'var': 'foo'}
>>> t=Template("""\
Escape          : $$
Variable        : $var
Variable in text: ${var}iable""")
>>> print(t.substitute(values))
Escape          : $
Variable        : foo
Variable in text: fooiable
>>> # 如果只提供了部分关键字参数，可利用safe_substitute避免KeyError
>>> print(t.safe_substitute(dict()))
Escape          : $
Variable        : $var
Variable in text: ${var}iable
```

### 高级用法

通过在 Template 的子类中覆盖类属性，从而自定义占位符(*placeholder*)语法、分隔(*delimiter*)符，甚至可以自定义用于解析模板字符串的整个正则表达式。可覆盖的类属性如下：

- *delimiter* - 定义分隔符样式，默认值是 `$` 

- *idpattern* - 定义标识符的模板，用于匹配占位符，默认值是 ` r'(?a:[_a-z][_a-z0-9]*)'` 

- *braceidpattern* - 定义带花括号的标识符的模板，用于匹配带括号的占位符，默认值与 *idpattern* 相同

- *flags* - 定义正则表达式标记，默认值是 `re.IGNORECASE`

- *pattern* -  定义整个正则表达式模板，包含以下 4 个分组：

  - *escaped* - 匹配转义序列
  - *named* - 匹配名称，用于匹配占位符
  - *braced* - 匹配被置于大括号中名称，用于匹配带括号的占位符，通常与 *named* 保持一致
  - *invalid* - 匹配任何分隔符模板，，用于无效的占位符

在创建子类时，元类 `_TemplateMetaclass` 会将*delimiter*, *idpattern*, *braceidpattern*, *flags* 添加到 *pattern* 中，同时会将 *pattern* 编译为一个正则表达式，并使用 *pattern* 对模板字符串进行匹配。所以，在子类已被创建的情况下，即使对子类的上述四个属性重新赋值，也不会影响匹配过程。详情况请查看 `_TemplateMetaclass` 类的源代码。

示例 - 直接在子类中覆盖类属性：

```python
# string_template_advanced.py
import string

class MyTemplate(string.Template):
    delimiter = '%' # 修改分隔符
    idpattern = '[a-z]+_[a-z]+' # 修改标识符模板

template_text = '''
  Delimiter : %%
  Replaced  : %with_underscore
  Ignored   : %notunderscored
'''
# %notunderscored 被匹配为无效占位符
d = {
    'with_underscore': 'replaced',
    'notunderscored': 'not replaced',
}

t = MyTemplate(template_text)
print('Modified ID pattern:')
print(t.safe_substitute(d))
"""Out:
Modified ID pattern:

  Delimiter : %
  Replaced  : replaced
  Ignored   : %notunderscored
"""
```

示例 - 修改正则表达式模板 *pattern*：

```python
# string_template_newsyntax.py
import re
import string

class MyTemplate(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''

t = MyTemplate('''
{{{{
{{var}}
''')

print('MATCHES:', t.pattern.findall(t.template))
print('SUBSTITUTED:', t.safe_substitute(var='replacement'))
"""Out
MATCHES: [('{{', '', '', ''), ('', 'var', '', '')]
SUBSTITUTED:
{{
replacement
"""
```

## Helper functions

🔨 string.capwords(*s*, *sep=None*)

Source code:

```python
def capwords(s, sep=None):
    """capwords(s [,sep]) -> string"""
    return (sep or ' ').join(x.capitalize() for x in s.split(sep))
```

Split the argument into words using [`str.split()`](https://docs.python.org/3.7/library/stdtypes.html#str.split), capitalize each word using [`str.capitalize()`](https://docs.python.org/3.7/library/stdtypes.html#str.capitalize), and join the capitalized words using [`str.join()`](https://docs.python.org/3.7/library/stdtypes.html#str.join). 

```python
>>> import string
>>> s = 'The quick brown fox jumped over the lazy dog.'
>>> string.capwords(s)
'The Quick Brown Fox Jumped Over The Lazy Dog.'
```

If the optional second argument *sep* is absent or `None`, runs of whitespace characters are replaced by a single space and leading and trailing whitespace are removed, otherwise *sep* is used to split and join the words.

```python
>>> s_ = 'The-quick-brown-fox-jumped-over-the-lazy-dog.'
>>> string.capwords(s_,sep='-')
'The-Quick-Brown-Fox-Jumped-Over-The-Lazy-Dog.'
```

## 术语

### 替换字段

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
```

`replacement_field` 是替换字段

### 转换字段

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
```

`["!" conversion]` 是转换字段

### 格式化序列

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
```

`[":" format_spec]` 是格式化序列
