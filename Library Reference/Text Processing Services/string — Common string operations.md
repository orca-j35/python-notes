# string — 通用字符串操作

Common string operations

> 本文介绍了 string 模块的各项功能，目的是提供更多的展示示例，但并没有逐字翻译原文档中的内容。
> 有关 string 模块的更多细节，需阅读下述资料：
>
> - [string — Common string operations](https://docs.python.org/3.7/library/string.html#module-string) 
> - [string — 字符串常量和模板](https://pythoncaff.com/docs/pymotw/string-string-constants-and-templates/76)
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

通过运用 `string.Formatter` 类，我们可使用与 `str.format` 方法相同的实现来创建自定义的字符创格式化行为。

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

- **vformat**(*format_string*, *args*, *kwargs*) - 该方法是实际执行格式化操作的地方。将该方法暴露为一个独立方法的原因是：当实参已被打包到某种数据结构中时，可跳过对实参进行解包的步骤 —— 免去需要先拆封参数到 `format` 方法，然后通过 `format` 方法再次打包参数，然后再调用 `vformat` 方法的重复操作。`vformat` 会将 `format_string` 拆分为字符数据和替换字段。

  ```python
  >>> f.vformat('format_string：{0}_{1}', ('Orca', 'J35'),{})
  'format_string：Orca_J35'
  ```

  `vformat` 会调用下述方法来完成格式化操作：(下面这些方法均可被子类覆写，从而达到自定义格式操作的目的)

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
    >>> for x in _string.formatter_parser('{0!s:<}_{1} is {hero!r:>}'):
    	print(x)
    
    	
    ('', '0', '<', 's')
    ('_', '1', '', None)
    (' is ', 'hero', '>', 'r')
    ```

  - **get_field**(*field_name*, *args*, *kwargs*)

    ```python
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

    示例 - 演示复合字段名的分拆方式：

    ```python
    >>> first, rest =_string.formatter_field_name_split('hero[1].help')
    >>> for i,j in rest:print(i,j)
    
    False 1
    True help
    ```

    *field_name* 可以是复合字段名(如，`"0.name"`、`"lookup[3]"`、`"key.attr"` )，但 `get_value` 方法只会使用复合字段名的第一部分(如，`0`、`"lookup"`、`"key"` )来寻找 *args* 和 *kwargs* 中的匹配项。符合字段名的后续部分会通过 `getattr` 或索引来获取。比如，对于复合字段名 `"0.name"`，会将 `0` 用作 [`get_value()`](https://docs.python.org/3.7/library/string.html#string.Formatter.get_value) 的 *key* 参数，而 `name` 字段则会在 `get_field` 方法中通过 `getattr` 获取。

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

  - **convert_field**(*value*, *conversion*) - 用于转换 `get_field()` 的返回值，*conversion* 在 `parse` 方法中

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

### 嵌套替换字段

顶层替换字段可能会包含嵌套的替换字段(如 `{value:{width}}`)。这些嵌套的替换字段可能会包含它们自己的转换字段和格式化序列，但是不能包含更深层次的嵌套字段，否则会抛出 `ValueError` 异常。

```python
>>> "result: {value:{width}}".format(
    width=10, precision=4, value=12.34567)
'result:   12.34567'
```

在这个示例中，顶层替换替换字段是 `"result: {value:{width}}"` ，第二层替换字段是 `"{value:{width}}"`，第三层嵌套字段是 `"{width}"`。

## Format String Syntax

[`str.format()`](https://docs.python.org/3.7/library/stdtypes.html#str.format) 和 `string.Formatter` 类采用同一套语法来格式化字符串，即格式化字符串语法。该语法和 *f-string* 的语法相似，但存在一些区别。

在格式化字符串语法中，替换字段(*replacement fields*)被置于花括号中。任何被置于花括号之外的内容均被视为文本字面值，会被直接复制到输出结果中。双层花括号( `'{{'`  或  `'}}'` )会被替换为对应的单个花括号。

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

*arg_name* 可以是数值或关键字，

`arg_name` 可引用位置实参和关键字实参：

- 当 `arg_name` 是数值时，则会引用位置实参





The *field_name* itself begins with an *arg_name* that is either a number or a keyword. If it’s a number, it refers to a positional argument, and if it’s a keyword, it refers to a named keyword argument. If the numerical arg_names in a format string are 0, 1, 2, … in sequence, they can all be omitted (not just some) and the numbers 0, 1, 2, … will be automatically inserted in that order. Because *arg_name* is not quote-delimited, it is not possible to specify arbitrary dictionary keys (e.g., the strings `'10'` or `':-]'`) within a format string. The *arg_name* can be followed by any number of index or attribute expressions. An expression of the form `'.name'` selects the named attribute using [`getattr()`](https://docs.python.org/3.7/library/functions.html#getattr), while an expression of the form `'[index]'` does an index lookup using [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__).

Changed in version 3.1: The positional argument specifiers can be omitted for [`str.format()`](https://docs.python.org/3.7/library/stdtypes.html#str.format), so `'{} {}'.format(a, b)` is equivalent to `'{0} {1}'.format(a, b)`.

Changed in version 3.4: The positional argument specifiers can be omitted for [`Formatter`](https://docs.python.org/3.7/library/string.html#string.Formatter).





f-string* 和 `string .format()` 使用相同的格式化说明符——[format specifier mini-language](https://docs.python.org/3.7/library/string.html#formatspec)。

### 嵌套替换字段



### 复合字段名

```python
>>> f = Formatter()
>>> f.format(
    '{0[1]}_{num.__class__}',
    'Orca',
    num='J35',
)
"r_<class 'str'>"
```

## Template strings

模板字符串只负责执行替换操作，不支持格式化语法(例如，无法控制浮点数的精度)。

### 初级用法

在初级用法中，直接使用 Template 类即可，下面是可用的实例属性：

> class string.Template(template)
>
> - substitute(mapping, **kwds) # 替换占位符
> - safe_substitute(mapping, **kwds) # 安全替换占位符
> - template # 查看或修改字符串模板

默认情况下，模板字符串支持基于 `$` 的替换规则，具体如下：(注意：占位符区分大小写)

> - `$$` is an escape; it is replaced with a single `$`.
> - `$identifier` names a substitution placeholder matching a mapping key of`"identifier"`. By default, `"identifier"` is restricted to any case-insensitive ASCII alphanumeric string (including underscores) that starts with an underscore or ASCII letter. The first non-identifier character after the `$` character terminates this placeholder specification.
> - `${identifier}` is equivalent to `$identifier`. It is required when valid identifier characters follow the placeholder but are not part of the placeholder, such as `"${noun}ification"`.
>

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



### 替换字段

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
```

### 转换字段

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
```

### 格式化序列

```
replacement_field ::=  "{" [field_name] ["!" conversion] [":" format_spec] "}"
```







