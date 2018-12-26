# float
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记：
>
> - 『数值类型(int,float,complex).md』
> - 『2. Lexical analysis.md.md』-> 2.4.6. 浮点字面值
> - 『numbers - Numeric abstract base classes.md』

🔨 *class* float([*x*])

该函数是 float 类型的构造函数，用于将 *x* (数字或字符串)转换为一个浮点数，如果实参为空，则会返回 `0.0` 。

有关浮点类型的详细描述，可阅读 [Numeric Types — int, float, complex](https://docs.python.org/3.7/library/stdtypes.html#typesnumeric) 。

Changed in version 3.6: Grouping digits with underscores as in code literals is allowed.

Changed in version 3.7: *x* is now a positional-only parameter.

## *x* is a string

如果 *x* 是一个字符串(或 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [`bytearray`](https://docs.python.org/3.7/library/stdtypes.html#bytearray))，那么 *x* 应表示一个十进制数整数或浮点数，并且可以在十进制数中使用前导符号( `+` 或 `-` ) —— `+` 号不会对值产生任何影响。数字和 `+` (或 `-`)之间不允许有空格(*space*)，但在数字和 `+` (或 `-`)的外围允许存在空白符(*whitespace*)：

```python
float(' \t 10 \n') #> 10.0
float(b' \t -10.11 \n') #> -10.11
float('+1.23') #> 1.23
float('   -12345\n') #> -12345.0
float('1e-003') #> 0.001
float('+1E6') #> 1000000.0
```

参数 *x* 还可以是表示 NaN (非数字)或 Infinity (正无穷和负无穷)的字符串，如：

```python
>>> float('-Infinity') #> -inf
```

对于字符串 *x* 而言，最准确的描述是：在剔除前导和尾随空白符后，输入必须符合以下语法：

```
sign           ::=  "+" | "-"
infinity       ::=  "Infinity" | "inf"
nan            ::=  "nan"
numeric_value  ::=  floatnumber | infinity | nan
numeric_string ::=  [sign] numeric_value
```

这里的 `floatnumber` 表示 Python 中的浮点字面值([*Floating point literals*](https://docs.python.org/3.7/reference/lexical_analysis.html#floating))。该语法对大小写不敏感，因此 “inf”, “Inf”, “INFINITY” 和 “iNfINity” 均是正无穷的合法表示。

## *x* is a number

参数 *x* 可以是某个整数或浮点数：

- 如果 *x* 是某个浮点数，则会返回相同的浮点值(在 Python 的浮点精度内)——假如 *x* 超出了 Pyhton 的 浮点范围，则会抛出 [`OverflowError`](https://docs.python.org/3.7/library/exceptions.html#OverflowError) 
- 如果 *x* 是某个整数，则会将其转换为浮点数

## *x* is a general object

如果 *x* 是某个普通的 Python 对象，`float(x)` 则会调用 `type(x).__float__(x)` 来将 *x* 转换为浮点数。`__float__()` 方法的返回值必须是浮点数，否则会抛出异常。

```python
class Sample:
    def __init__(self,value):
        self._value = value
    def __float__(self):
        return float(self._value)
float(Sample(6)) #> 6.0
```

## 支持的操作

详见笔记：

- 『数值类型(int,float,complex).md』
- 『numbers - Numeric abstract base classes.md』

## \_\_float\_\_

🔨 object.[`__float__`](https://docs.python.org/3.7/reference/datamodel.html#object.__float__)(*self*)

该方法用于实现 `float()`。 


