# format

🔨 format(*value*[, *format_spec*])

该函数会将 *value* 按照 *format_spec* 给定的规则进行格式化。*format_spec* 的含义与 *value* 的类型有关，不同类型的 *value* 会使 *format_spec* 拥有不同的解释方式。

大多数内置类型都遵循一套标准格式化语法：[Format Specification Mini-Language](https://docs.python.org/3.7/library/string.html#formatspec) (详见笔记『string — Common string operations.md』-> "Format Specification Mini-Language")。因此，如果 *value* 是内置类型，那么传递给 *format_spec* 的实参值需安装 Format Specification Mini-Language 中规定的格式编写：

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

示例 - 展示 `format()` 函数的使用方法：

```python
>>> format(97,'c') # 将整数转换为对应的Unicode字符
'a'
>>> format(11,'#x') # 以16进制"替代形式"显示整数
'0xb'
>>> format(314159267,'e') #科学计数法，默认保留6位小数
'3.141593e+08'
>>> format(3.14e+1000000,'F')  #小数点计数法，无穷大转换成大小字母
'INF'
```

*format_spec* 的默认值是一个空字符串，通常与调用 `str(value)` 的效果相同。

```python
>>> format([1,2,3])
'[1, 2, 3]'
>>> str([1,2,3])
'[1, 2, 3]'
```

## 实现细节

实际上 Python 会将 `format(value, format_spec)` 翻译为 `type(value).__format__(value, format_spec)`。也就是说在寻找 *value* 的 [`__format__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__format__) 方法时，会跳过实例字典：

```python
from types import MethodType
class Cls(object):
    def __format__(self, format_spec=''):
        # Cls.__dict__会收录该属性
        return 'in Cls.__dict__'
value = Cls()
# 为value绑定一个名为__format__的实例方法，value.__dict__会收录该属性
value.__format__ = MethodType(
    lambda self, format_spec='': 'in value.__dict__', value)

print(format(value)) # Out:in Cls.__dict__
print(value.__format__()) # Out:in value.__dict__
```

## TypeError

在调用 `format()` 方式时，有以下三种情况会抛出 [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError)：

- 在继承链中搜索 `__format__()` 方法时已抵达了 `object` 类，并且 *format_spec* 非空··

  ```python
  class Cls(object):
      # 该类中并没有覆写__format__方法，
      # 所以会调用继承自object的__format__方法
      pass
  print(format(Cls(), '>'))
  # 抛出 TypeError: unsupported format string passed to Cls.__format__
  ```

- 传递给 *format_spec* 的实参值并非字符串

  ```python
  class Cls(object):
      def __format__(self, format_spec=""):
          return 'orca_j35'
  format(Cls(), 11)
  # 抛出 TypeError: format() argument 2 must be str, not int
  ```

-  `__format__()` 方法的返回值并非字符串

  ```python
  class Cls(object):
      def __format__(self, format_spec=""):
          return True
  format(Cls()) 
  # 抛出 TypeError: __format__ must return a str, not bool
  ```

**Changed in version 3.4**: `object().__format__(format_spec)` raises [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError) if *format_spec* is not an empty string.

## \_\_format\_\_

🔨 object.\_\_format\_\_(*self*, *format_spec*)

该方法由内置函数 `format()` 调用。细节上来讲，`format(value, format_spec)` 会在内部调用 `type(value).__format__(value, format_spec)`，从而利用 `__format__` 而对 `value` 进行格式化。另外，在 [f-string](https://docs.python.org/3.7/reference/lexical_analysis.html#f-strings) 和 [`str.format()`](https://docs.python.org/3.7/library/stdtypes.html#str.format) 中都会使用 `format()` 来完成对象的格式化操作。

注意：`__format__` 方法的返回值必须是字符串对象。

*format_spec* 参数是由格式化选项组成的字符串。*format_spec* 的含义取决于 `type(value).__format__` 的实现方式，但是大多数类都会将格式化过程委托给某个内置类型，或是使用与 [Format Specification Mini-Language](https://docs.python.org/3.7/library/string.html#formatspec) 类似的语法。

有关标准格式化语法的说明，请阅读 [Format Specification Mini-Language ](https://docs.python.org/3.7/library/string.html#formatspec)，大多数内置类型都遵循该语法如下：(详见笔记『string — Common string operations.md』-> "Format Specification Mini-Language")

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

示例 - 展示 `format()` 和 `__format__()`：

```python
>>> format(97,'c') # 将整数转换为对应的Unicode字符
'a'
>>> type(10).__format__(10,'x')
'a'
```

**Changed in version 3.4**: The `__format__` method of `object` itself raises a [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError) if passed any non-empty string.

```python
>>> object().__format__('s')
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    object().__format__('s')
TypeError: unsupported format string passed to object.__format__
```

**Changed in version 3.7**: `object.__format__(x, '')` is now equivalent to `str(x)` rather than `format(str(self), '')`.

