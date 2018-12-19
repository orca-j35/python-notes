# numbers - Numeric abstract base classes
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本笔记概述了 [`numbers`](https://docs.python.org/3.7/library/numbers.html#module-numbers) — Numeric abstract base classes 中的内容

[`numbers`](https://docs.python.org/3.7/library/numbers.html#module-numbers) 模块 ([**PEP 3141**](https://www.python.org/dev/peps/pep-3141)) 定义了数值(*numeric*)抽象基类([*abstract* *base* *classes*](https://docs.python.org/3.7/glossary.html#term-abstract-base-class))的层次结构，并逐步定义了许多操作。在此模块中定义的所有类型都不能进行实例化。

```python
__all__ = ["Number", "Complex", "Real", "Rational", "Integral"]
```

### 🔨 Number

🔨 *class* numbers.Number

Number 类是数值层次结构的根类。如果需要检测参数 *x* 是否是一个数字，并且不关心 *x* 的类型，则可以使用  `isinstance(x, Number)`：

```python
from numbers import *
assert isinstance(1,Number) is True
assert isinstance(1.2,Number) is True
assert isinstance(1+1j,Number) is True
# 分数
from fractions import Fraction
assert isinstance(Fraction(1,2),Number)is True
# 十进制小数
from decimal import *
assert isinstance(Decimal('1.4'),Number) is True
```

## The numeric tower

数值抽象基类的层次结构如下：

```
Number
|---Complex # int, float, Complex, Fraction
	|---Real # int, float, Fraction
		|---Rational # int, Fraction
			|---Integral # int
```

bool 是 int 的子类型

### 🔨 Complex

🔨 *class* numbers.Complex

Complex 抽象基类的子类用于描述复数(*complex*)，并包含对内置 [`complex`](https://docs.python.org/3.7/library/functions.html#complex) 类型起作用的操作：

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

int, float, Complex, Fraction 属于 Complex 类型：

```python
from numbers import *
assert isinstance(1,Complex) is True
assert isinstance(1.2,Complex) is True
assert isinstance(1+1j,Complex) is True
from fractions import Fraction
assert isinstance(Fraction(1,2),Complex)is True
from decimal import *
assert isinstance(Decimal('1.4'),Complex) is False
```

### 🔨 Real

🔨 *class* numbers.Real

相较于 [`Complex`](https://docs.python.org/3.7/library/numbers.html#numbers.Complex) ，[`Real`](https://docs.python.org/3.7/library/numbers.html#numbers.Real) 添加了对实数有效的操作。
简单来讲，扩增了以下方法：

- 支持 [`float`](https://docs.python.org/3.7/library/functions.html#float), [`math.trunc()`](https://docs.python.org/3.7/library/math.html#math.trunc), [`round()`](https://docs.python.org/3.7/library/functions.html#round), [`math.floor()`](https://docs.python.org/3.7/library/math.html#math.floor), [`math.ceil()`](https://docs.python.org/3.7/library/math.html#math.ceil),
- 支持 [`divmod()`](https://docs.python.org/3.7/library/functions.html#divmod), `//`, `%`, `<`, `<=`, `>`, `>=`

Real 同样支持 [`complex()`](https://docs.python.org/3.7/library/functions.html#complex), [`real`](https://docs.python.org/3.7/library/numbers.html#numbers.Complex.real), [`imag`](https://docs.python.org/3.7/library/numbers.html#numbers.Complex.imag), [`conjugate()`](https://docs.python.org/3.7/library/numbers.html#numbers.Complex.conjugate)。

Decimal 和 [`complex`](https://docs.python.org/3.7/library/functions.html#complex) 不属于 Real 类型：

int, float, Fraction 属于 Real 类型：

```python
from numbers import *
assert isinstance(1,Real) is True
assert isinstance(1.2,Real) is True
assert isinstance(1+1j,Real) is False
from fractions import Fraction
assert isinstance(Fraction(1,2),Real)is True
from decimal import *
assert isinstance(Decimal('1.4'),Real) is False
```

### 🔨 Rational

🔨 *class* numbers.Rational

Rational 是 Real 的子类型，并添加了两个属性：[`numerator`](https://docs.python.org/3.7/library/numbers.html#numbers.Rational.numerator) 和 [`denominator`](https://docs.python.org/3.7/library/numbers.html#numbers.Rational.denominator)。

- `numerator` - 抽象属性，分子

- `denominator` - 抽象属性，分母

Rational 同样支持 [`float()`](https://docs.python.org/3.7/library/functions.html#float)：

```python
float(Fraction(2,3)) #> 0.6666666666666666
float(Fraction(1,2)) #> 0.5
```

只有 int 和 Fraction 属于 Rational 类型：

```python
from numbers import *
assert isinstance(1,Rational) is True
assert isinstance(1.2,Rational) is False
assert isinstance(1+1j,Rational) is False
from fractions import Fraction
assert isinstance(Fraction(1,2),Rational)is True
from decimal import *
assert isinstance(Decimal('1.4'),Rational) is False
```

### 🔨 Integral

🔨 *class* numbers.Integral

Integral 是 [`Rational`](https://docs.python.org/3.7/library/numbers.html#numbers.Rational) 的子类，支持 [`int`](https://docs.python.org/3.7/library/functions.html#int) 转换，支持 [`float()`](https://docs.python.org/3.7/library/functions.html#float), [`numerator`](https://docs.python.org/3.7/library/numbers.html#numbers.Rational.numerator), [`denominator`](https://docs.python.org/3.7/library/numbers.html#numbers.Rational.denominator)，还为  `**` 和 bit-string 操作（`<<`, `>>`, `&`, `^`, `|`, `~`）添加了抽象方法。

只有 int 属于 Integral 类型：

```python
from numbers import *
assert isinstance(1,Integral) is True
assert isinstance(1.2,Integral) is False
assert isinstance(1+1j,Integral) is False
from fractions import Fraction
assert isinstance(Fraction(1,2),Integral)is False
from decimal import *
assert isinstance(Decimal('1.4'),Integral) is False
```

## 术语

### abstract base class

[Abstract base classes](https://docs.python.org/3.7/glossary.html#term-abstract-base-class) complement [duck-typing](https://docs.python.org/3.7/glossary.html#term-duck-typing) by providing a way to define interfaces when other techniques like [`hasattr()`](https://docs.python.org/3.7/library/functions.html#hasattr) would be clumsy or subtly wrong (for example with[magic methods](https://docs.python.org/3.7/reference/datamodel.html#special-lookup)). ABCs introduce virtual subclasses, which are classes that don’t inherit from a class but are still recognized by [`isinstance()`](https://docs.python.org/3.7/library/functions.html#isinstance) and [`issubclass()`](https://docs.python.org/3.7/library/functions.html#issubclass); see the [`abc`](https://docs.python.org/3.7/library/abc.html#module-abc)module documentation. Python comes with many built-in ABCs for data structures (in the [`collections.abc`](https://docs.python.org/3.7/library/collections.abc.html#module-collections.abc) module), numbers (in the [`numbers`](https://docs.python.org/3.7/library/numbers.html#module-numbers) module), streams (in the [`io`](https://docs.python.org/3.7/library/io.html#module-io) module), import finders and loaders (in the [`importlib.abc`](https://docs.python.org/3.7/library/importlib.html#module-importlib.abc) module). You can create your own ABCs with the [`abc`](https://docs.python.org/3.7/library/abc.html#module-abc) module.

