# int
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记:
>
> - 『数值类型(int,float,complex)』
> - 『2. Lexical analysis.md.md』-> 2.4.5. 整型字面值
> - 『numbers - Numeric abstract base classes.md』

该函数是 int 类型的构造函数，用于将 *x* (数字或字符串)转换为一个整数。

有关整数类型的详细描述，可阅读 [Numeric Types — int, float, complex](https://docs.python.org/3.7/library/stdtypes.html#typesnumeric) 。

Changed in version 3.4: If *base* is not an instance of [`int`](https://docs.python.org/3.7/library/functions.html#int) and the *base* object has a [`base.__index__`](https://docs.python.org/3.7/reference/datamodel.html#object.__index__) method, that method is called to obtain an integer for the base. Previous versions used [`base.__int__`](https://docs.python.org/3.7/reference/datamodel.html#object.__int__) instead of [`base.__index__`](https://docs.python.org/3.7/reference/datamodel.html#object.__index__).

Changed in version 3.6: Grouping digits with underscores as in code literals is allowed.

Changed in version 3.7: *x* is now a positional-only parameter.

## 🔨 int([*x*])

🔨 *class* int([*x*])

如果参数为空，则会返回 `0`：

```python
int() #> 0
```

如果 *x* 定义了 [`__int__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__int__)，则 `int(x)` 会调用 `x.__int__()`：

```python
class Sample:
    def __init__(self,value):
        self._value = value
    def __int__(self):
        return self._value
int(Sample(6)) #> 6
```

如果 *x* 未定义 `__int__()` ，那么 `int()` 将会调用 [`x.__trunc__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__trunc__) (如果存在该方法的话)：

```python
class Sample:
    def __init__(self,value):
        self._value = value
    def __trunc__(self):
        return self._value**2
int(Sample(6)) #> 36
```

如果 `__int__` 和 `__trunc__` 都未定义，则会抛出 `TypeError`：

```python
class Sample:
    def __init__(self,value):
        self._value = value
int(Sample(6))
#> TypeError: int() argument must be a string, a bytes-like object or a number, not 'Sample'
```

如果 *x* 是[实数(*Real*)](https://docs.python.org/3.7/library/numbers.html#numbers.Real)，则会向着 0 的方向进行截断，直接抛弃小数部分：

```python
# numbers.Real 包含 int, float, Fraction
int(2.9),int(-2.9) 
#> (2, -2)

from fractions import Fraction
int(Fraction(29,10)),int(Fraction(-29,10))
#> (2, -2)
```

## 🔨 int(*x*, *base=10*)

🔨 *class* int(*x*, *base=10*)

*x* 还可以是以 *base* 为基数的整型字面值([*integer* *literal*](https://docs.python.org/3.7/reference/lexical_analysis.html#integers))的字符串(或 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [`bytearray`](https://docs.python.org/3.7/library/stdtypes.html#bytearray))形式，*base* 的默认值是 `10`。此时，会按照给定进制将 *x* 转换为对应的整数。

可在整型字面值字符串的前方添加 `+` (或 `-`)，字面值和 `+` (或 `-`)之间不允许有空格(*space*)，但在字面值和 `+` (或 `-`)的外围允许存在空白符(*whitespace*)。

```python
int(' \t -10 \n') #> -10
```

Base-n 的字面值由数字 `0` ~ `n-1` 组成——字母 `a` ~ `z` (或 `A` ~ `Z`)对应于 `10` ~ `35`。

```python
int('z',base=36) #> 35
```

*base* 有效的取值范围是 0 和 2~36，其默认值是 10。

Base-2, -8, -16 的字面值可使用相应的前缀：`0b`/`0B`, `0o`/`0O`,  `0x`/`0X`。

```python
int('0b10',base=2) #> 2
int('0o10',base=8) #> 8
int('0x10',base=16) #> 16
```

Base-0 表示完全由整型字面值自身来决定如何解释基数，此时只能使用以 2, 8, 10, 16 作为基数的整型字面值。

```python
int('0b10',0) #> 2
int('0o10',0) #> 8
int('0x10',0) #> 16
int('10',0) #> 10
```

在基数非零的情况下，可以在整型字面值中使用前导 `0`，但前导 `0` 只能位于 `+` (或 `-`)内侧，否则会抛出异常。

```python
int('+010'),int('-010'),int('010')
#> (10, -10, 10)
int('+010', 8),int('-010', 8),int('010', 8)
#> (8, -8, 8)
```

在 Base-0 的情况下，不允许在整型字面值中使用前导 `0`：

```python
int('010', 0)
#> ValueError: invalid literal for int() with base 0: '010'
```

## 支持的操作

详见笔记：

- 『数值类型(int,float,complex).md』
- 『numbers - Numeric abstract base classes.md』

## \_\_int\_\_

🔨 object.[`__int__`](https://docs.python.org/3.7/reference/datamodel.html#object.__int__)(*self*)

该方法用于实现 `int()`。 

## \_\_trunc\_\_

🔨 object.`__trunc__`(*self*)

该方法用于实现 [`math.trunc()`](https://docs.python.org/3.7/library/math.html#math.trunc)，会将[实数(*Real*)](https://docs.python.org/3.7/library/numbers.html#numbers.Real) *x* 截断为一个整数。

如果未定义 `__int__()` ，那么 `int()` 将会调用 [`__trunc__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__trunc__) (如果存在该方法的话)。

