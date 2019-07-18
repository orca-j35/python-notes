# complex
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记：
>
> - 『数值类型(int,float,complex).md』
> - 『2. Lexical analysis.md.md』-> 2.4.7. 虚数字面值
> - 『numbers - Numeric abstract base classes.md』

该函数是 complex 类型的构造函数，用于创建复数。

有关 complex 类型的详细描述，可阅读 [Numeric Types — int, float, complex](https://docs.python.org/3.7/library/stdtypes.html#typesnumeric) 。

Changed in version 3.6: Grouping digits with underscores as in code literals is allowed.

## 🔨 complex( )

🔨 *class* complex( )

如果实参为空，由于 *imag* 的默认值为 `0`，所以将返回 `0j`：

```python
complex() #> 0j
```

## 🔨 complex(*real*)

🔨 *class* complex(*real*)

在仅使用 *real* 参数时，可分为以下几种情况：

- *real* 是一个表示数值的字符串(不能是 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 或 [`bytearray`](https://docs.python.org/3.7/library/stdtypes.html#bytearray)，且绝对不能使用第二参数)，此时会将 *real* 解释为一个复数：

  ```python
  complex('6+1j') #> (6+1j)
  complex('6') #> (6+0j)
  complex('1j') #> 1j
  ```

  当 *real* 是一个表示复数的字符串时，在 `+` (或 `-`)的周围不能包含空白符：

  ```python
  complex('1+2j') #> (1+2j)
  complex('1 + 2j') #> ValueError: complex() arg is a malformed string
  ```

  可在字符串中的数值前使用前导符号( `+` 或 `-` ) ，数值和 `+` (或 `-`)之间不允许有空格(*space*)，但在数值和 `+` (或 `-`)的外围允许存在空白符(*whitespace*)：

  ```python
  complex(' \t-1+1j\t \n') #> (-1+1j)
  ```

- *real* 是数值类型对象(可以是任意数值类型，包括 complex)，此时默认 *imag* 为 `0`，会将数值 *real* 转换为 complex 类型的对象：

  ```python
  complex(6+1j),complex(6.1),complex(3j)
  #> ((6+1j), (6.1+0j), 3j)
  
  from fractions import Fraction
  complex(Fraction(1,2)) #> (0.5+0j)
  
  from decimal import *
  complex(Decimal('1.4')) #> (1.4+0j)
  # Decimal不能与complex相加，否则会抛出异常
  complex(Decimal('1.4')+3j) 
  #> TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'complex'
  ```

- *real* 还可以是实现了 `__complex__()` 方法的对象，此时默认 *imag* 为 `0`：

  ```python
  class Sample:
      def __complex__(self):
          return 6+6j
  complex(Sample()) #> (6+6j)
  ```

  如果 *real* 对象没有实现 `__complex__()`，则会尝试调用 `__float__()`，并默认 *imag* 为 `0`：

  ```python
  class Sample:
      def __float__(self):
          return 3.3
  complex(Sample()) #> (3.3+0j)
  ```

  如果在 *real* 对象中并没有实现  `__complex__()` 或 `__float__()`，则会抛出 `TypeError` 异常。

## 🔨 complex(*real*, *imag*)

🔨 *class* complex(*real*, *imag*)

如果提供了第二参数 *imag* (绝对不能将字符串用作第二参数)，*real* 可分为以下几种情况：

- *real* 是数值类型对象(可以是任意数值类型，包括 complex)，此时 `complex(real, imag)`  等效于 `real+imag*1j `：

  ```python
  complex(6+1j,1j) #> (5+1j)
  ```

- *real* 是实现了 `__complex__()` 方法的对象，此时 `complex(real, imag)`  等效于 `real.__complex__()+imag*1j `：

  ```python
  class Sample:
      def __complex__(self):
          return 6+6j
  complex(Sample(),3),complex(Sample(),3j)
  #> ((6+9j), (3+6j))
  ```

  如果 *real* 对象没有实现 `__complex__()`，则会尝试调用 `__float__()`，此时 `complex(real, imag)`  等效于 `real.__float__()+imag*1j `：

  ```python
  class Sample:
      def __float__(self):
          return 3.5
  complex(Sample(),3),complex(Sample(),3j)
  #> ((3.5+3j), (0.5+0j))
  ```

  如果在 *real* 对象中并没有实现  `__complex__()` 或 `__float__()`，则会抛出 `TypeError` 异常。

如果提供了第二参数 *imag* (绝对不能将字符串用作第二参数)，*imag* 可分为以下几种情况：

- *imag* 是数值类型对象(可以是任意数值类型，包括 complex)，此时 `complex(real, imag)`  等效于 `real+imag*1j `：

  ```python
  complex(6+1j,1+1j) #> (5+2j) 
  ```

- *imag* 是实现了 `__float__()` 方法的对象，此时 `complex(real, imag)`  等效于 `real.+imag.__float__()*1j `：

  ```python
  class Sample:
      def __float__(self):
          return 3.5
  complex(6+6j,Sample()) #> (6+9.5j)
  ```

  如果在 *imag* 对象中并没有实现 `__float__()`，则会抛出 `TypeError` 异常。

## 支持的操作

complex 类型支持以下操作：

- 支持 [`complex`](https://docs.python.org/3.7/library/functions.html#complex) 和 [`bool`](https://docs.python.org/3.7/library/functions.html#bool) 转换
- 支持 [`real`](https://docs.python.org/3.7/library/numbers.html#numbers.Complex.real), [`imag`](https://docs.python.org/3.7/library/numbers.html#numbers.Complex.imag), `+`, `-`, `*`, `/`, [`abs()`](https://docs.python.org/3.7/library/functions.html#abs), [`conjugate()`](https://docs.python.org/3.7/library/numbers.html#numbers.Complex.conjugate) 等
- 支持 `==` 和 ``!=` 

以上所有操作，除 `-` 和 `!=` 外均为抽象属性。

- `real` - 抽象方法，用于检索数字的实部
- `imag` - 抽象方法，用于检索数字的虚部
- *abstractmethod* `conjugate`() - 抽象方法，用于返回共轭(*conjugate*)复数，例如 `(1+3j).conjugate() ==(1-3j)`.

```python
bool(0j) #> False
(1+2j).real #> 1.0
(1+2j).imag #> 2.0
(1+3j).conjugate() #> (1-3j)
abs(3+4j) #> 5.0
(2+1j) ** 2 #> (3+4j)
```

更多细节，请参考笔记『numbers - Numeric abstract base classes.md』

## \_\_complex\_\_

🔨 object.[`__complex__`](https://docs.python.org/3.7/reference/datamodel.html#object.__complex__)(*self*)

该方法用于实现 `complex(real)`。

如果未实现 `__complex__`， `complex(real)` 则会尝试调用 `__float__`，详见 「🔨 complex(*real*)」和「🔨 complex(*real*, *imag*)」小节。