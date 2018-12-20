# 数值类型(int,float,complex)

Numeric Types — [`int`](https://docs.python.org/3.7/library/functions.html#int), [`float`](https://docs.python.org/3.7/library/functions.html#float), [`complex`](https://docs.python.org/3.7/library/functions.html#complex)

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本文涵盖了 [Numeric Types — int, float, complex](https://docs.python.org/3.7/library/stdtypes.html#numeric-types-int-float-complex) 中的内容，并进行了扩展
>

## 1. 概述

> 相关笔记：
>
> - 『numbers - Numeric abstract base classes.md』
> - 『3.2. 标准类型层次.md』-> numbers.Number
> - 『2. Lexical analysis.md』-> 数值型字面值
>
> 扩展阅读：
>
> - [`decimal`](https://docs.python.org/3.7/library/decimal.html#module-decimal) — Decimal fixed point and floating point arithmetic
>   - [decimal — 高精度计算模块](https://pythoncaff.com/docs/pymotw/decimal-fixed-and-floating-point-math/101)
> - [`fractions`](https://docs.python.org/3.7/library/fractions.html#module-fractions) — Rational numbers
>   - [fractions — 分数运算](

Python 中有三种不同的数值(*numeric*)类型：整数(integers)，浮点数(*floating point numbers*)，复数(*complex numbers*)。另外，布尔值(*booleans*)是整数的子类。

通过数值型(*numeric*)字面值可创建相应类型的数值对象，算术运算符和内置算数函数的返回值也属于数值类型。

整数字面值（含 hex, octal, binary）将产生整数。包含小数点或指数符号的数值字面值将产生浮点数。在数值字面值中添加  `'j'` 或 `'J'` ，则会产生一个纯虚数（实部为 0 的复数）。详见『2. Lexical analysis.md』-> 数值型字面值。

Python 完全支持混合算术：当二元(*binary*)算数运算符拥有两个不同数值类型的操作数时，"较窄(*narrower*)"的数值类型将被拓宽——整数窄于浮点数，浮点数窄于复数。混合数值类型之间的比较，也遵守相同的规则。

```python
 [1, 2] == [1.0, 2.0],(1, 2) == (1.0, 2.0)
 #> (True, True)
```

构造器 [`int()`](https://docs.python.org/3.7/library/functions.html#int), [`float()`](https://docs.python.org/3.7/library/functions.html#float), [`complex()`](https://docs.python.org/3.7/library/functions.html#complex) 用于生成对应类型的数字。

当二进制算术运算符具有不同数值类型的操作数时，具有“较窄”类型的操作数被扩展为另一个的操作数，其中整数比浮点更窄，这比复数更窄。混合类型数字之间的比较使用相同的规则。

数值对象不可变；已创建的数值对象的值，不能被再次修改。Python 中的数值与数学中的数值密切相关。但是会受到计算机中数值表达能力的限制。

[数值抽象基类(ABC)](https://docs.python.org/3.7/library/numbers.html)的层次结构如下：

```
numbers.Number # 包含 int, float, Complex, Fraction, Decimal
|---numbers.Complex # 包含 int, float, Complex, Fraction
	|---numbers.Real # 包含 int, float, Fraction
		|---numbers.Rational # 包含 int, Fraction
			|---numbers.Integral # 包含 int
```

[numbers.Number](https://docs.python.org/3.7/library/numbers.html#numbers.Number)

- [numbers.Integral](https://docs.python.org/3.6/library/numbers.html#numbers.Integral)
  描述了数学的整数集合中的元素(正数和复数)。
  整数有两种类型：

  - 整数 ([`int`](https://docs.python.org/3.6/library/functions.html#int))

    整数具有无限精度，其表示的数值的范围是无限的，但会受到可用(虚拟)内存的限制。在进行位移(shift)和掩码(mask)运算时，可以假定整数以二进制表示。并且会以二进制补码的变体表示负数，从而给出符号位无限延伸到左侧的错觉。

  - 布尔值 ([`bool`](https://docs.python.org/3.6/library/functions.html#bool))
    表示真值 `False` 和 `True` 。这两个对象表示的值 `False` 和 `True` 是唯一的 Boolean 对象。Boolean 类型是整数类型的子类型，并且 Boolean 值 `False` 和 `True` 的行为分别类似于 0 和 1，这几乎适用于所有上下文。不过如果将 Boolean 值转换为字符串，便会得到  `"False"` 或 `"True"` ，而非 `'0'` 或 `'1'`。

  整数表示规则的主要目的是解释涉及负整数的位移和掩码操作。

- [numbers.Real](https://docs.python.org/3.6/library/numbers.html#numbers.Real) ([`float`](https://docs.python.org/3.6/library/functions.html#float))
  用于表示机器级的双精度(*double*)浮点数，当数值超出范围后，会被表示为 `inf` 。对于浮点数的取值范围和溢出处理，都由底层机器体系结构及实现方式（C 或 Java）决定，无法人为干涉。Python 不支持单精度浮点数；一般来说，使用单精度浮点数的原因是为了节省处理器和内存使用量。但是，与在 Python 中使用对象的开销相比，这些节省是微不足道的。因此，没有理由使用两种浮点数来将语言复杂化。

  [`sys.float_info`](https://docs.python.org/3.7/library/sys.html#sys.float_info) 中提供了与机器（运行程序的机器）的浮点数的精度和内部表示相关的信息。

- [numbers.Complex](https://docs.python.org/3.6/library/numbers.html#numbers.Complex) ([`complex`](https://docs.python.org/3.6/library/functions.html#complex))
  复数被表示为一对机器级的双精度浮点数，由实部(*real*)和虚部(*imaginary*)构成。对于浮点数的说明也适用于复数。可以通过只读属性 `z.real` 和 `z.imag` 来获取复数 `z` 的实部和虚部。

在标准库中还包含其他数值类型：[`fractions`](https://docs.python.org/3.7/library/fractions.html#module-fractions) 表示有理数(*rationals*)；[`decimal`](https://docs.python.org/3.7/library/decimal.html#module-decimal) 表示十进制浮点数（用户可自定义精度）。

## 2. 数值类型支持的操作

所有数值类型（除复数外）均支持下表中的操作，表格中所列操作的优先级从上至下依次增高。另外，所有数值操作的优先级均高于比较操作。

| Operation         | Result                                                       | Notes  | Full documentation                                           |
| ----------------- | ------------------------------------------------------------ | ------ | ------------------------------------------------------------ |
| `x + y`           | sum of *x* and *y*                                           |        |                                                              |
| `x - y`           | difference of *x* and *y*                                    |        |                                                              |
| `x * y`           | product of *x* and *y*                                       |        |                                                              |
| `x / y`           | quotient of *x* and *y*                                      |        |                                                              |
| `x // y`          | floored quotient of *x* and *y*                              | (1)    |                                                              |
| `x % y`           | remainder of `x / y`                                         | (2)    |                                                              |
| `-x`              | *x* negated                                                  |        |                                                              |
| `+x`              | *x* unchanged                                                |        |                                                              |
| `abs(x)`          | absolute value or magnitude of *x*                           |        | [`abs()`](https://docs.python.org/3.7/library/functions.html#abs) |
| `int(x)`          | *x* converted to integer                                     | (3)(6) | [`int()`](https://docs.python.org/3.7/library/functions.html#int) |
| `float(x)`        | *x* converted to floating point                              | (4)(6) | [`float()`](https://docs.python.org/3.7/library/functions.html#float) |
| `complex(re, im)` | a complex number with real part*re*, imaginary part *im*. *im* defaults to zero. | (6)    | [`complex()`](https://docs.python.org/3.7/library/functions.html#complex) |
| `c.conjugate()`   | conjugate of the complex number*c*                           |        |                                                              |
| `divmod(x, y)`    | the pair `(x // y, x % y)`                                   | (2)    | [`divmod()`](https://docs.python.org/3.7/library/functions.html#divmod) |
| `pow(x, y)`       | *x* to the power *y*                                         | (5)    | [`pow()`](https://docs.python.org/3.7/library/functions.html#pow) |
| `x ** y`          | *x* to the power *y*                                         | (5)    |                                                              |

Notes:

1. 也被称为整数除法(*integer* *division*)。地板除的结果一定是某个整数，但并不一定是 int 类型。地板除的结果始终向负无穷侧进行舍入：

   ```python
   1//2, (-1)//2, 1//(-2), (-1)//(-2)
   #> (0, -1, -1, 0)
   ```

2. 不能对复数求余数，而是在适当的情况下使用 [`abs()`](https://docs.python.org/3.7/library/functions.html#abs) 将其转换为浮点数

3. 从浮点到整数的转换可以像 C 中那样舍入(*round*)或截断(*truncate*)；详见函数 [`math.floor()`](https://docs.python.org/3.7/library/math.html#math.floor) 和 [`math.ceil()`](https://docs.python.org/3.7/library/math.html#math.ceil)

4. `float()` 还可接受带可选前缀(“+” 或 “-” )的字符串 “nan” 和 “inf” ，以表示非数值(NaN)、正无穷、负无穷。

   ```python
   float('nan'),float('inf'),float('-inf')
   #> (nan, inf, -inf)
   ```

5. Python 将 `pow(0,0)` 和 `0**0` 定义为 `1`，这种定义方式在编程语言中很常见。

6. 数值字面值可接受数字 `0` ~ `9` 或等效的 Unicode 字符（具备 `Nd` 属性的码点）。

   关于 `Nd` 属性的介绍，可参考『字符串方法.md』-> 附录

   具有 `Nd` 属性的代码点的完整列表，请参见 <http://www.unicode.org/Public/10.0.0/ucd/extracted/DerivedNumericType.txt> 

所有 [`numbers.Real`](https://docs.python.org/3.7/library/numbers.html#numbers.Real) 类型 ([`int`](https://docs.python.org/3.7/library/functions.html#int), [`float`](https://docs.python.org/3.7/library/functions.html#float), Fraction) 还支持以下操作：

| Operation                                                    | Result                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [`math.trunc(x)`](https://docs.python.org/3.7/library/math.html#math.trunc) | *x* truncated to [`Integral`](https://docs.python.org/3.7/library/numbers.html#numbers.Integral) |
| [`round(x[,n])`](https://docs.python.org/3.7/library/functions.html#round) | *x* rounded to *n* digits, rounding half to even. If *n* is omitted, it defaults to 0. |
| [`math.floor(x)`](https://docs.python.org/3.7/library/math.html#math.floor) | the greatest [`Integral`](https://docs.python.org/3.7/library/numbers.html#numbers.Integral) <= *x* |
| [`math.ceil(x)`](https://docs.python.org/3.7/library/math.html#math.ceil) | the least [`Integral`](https://docs.python.org/3.7/library/numbers.html#numbers.Integral) >= *x* |

在 [`math`](https://docs.python.org/3.7/library/math.html#module-math) 和 [`cmath`](https://docs.python.org/3.7/library/cmath.html#module-cmath) 模块中还提供了一些与数值类型相关的操作。

## 3. 基于整数类型的位运算

Bitwise Operations on Integer Types

位运算仅对整数有意义。Python 会以二进制补码的变体表示负数，从而在位运算过程中表现出符号位无限延伸到左侧的错觉。

二元位运算的优先级均低于数值运算，并高于比较操作；一元位运算 `~` 与一元数值运算( `+`, `-` )具备相同的优先级。

下表列出了位运算操作，表格中所列操作的优先级从上至下依次增高。

| Operation | Result                                | Notes  |
| --------- | ------------------------------------- | ------ |
| `x | y`   | bitwise *or* of *x* and *y*           | (4)    |
| `x ^ y`   | bitwise *exclusive or* of *x* and *y* | (4)    |
| `x & y`   | bitwise *and* of *x* and *y*          | (4)    |
| `x << n`  | *x* shifted left by *n* bits          | (1)(2) |
| `x >> n`  | *x* shifted right by *n* bits         | (1)(3) |
| `~x`      | the bits of *x* inverted              |        |

Notes：

1. 负位移计数(*n*)是非法的，会抛出 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError) 异常
2. 左移 *n* 位，相当于乘以 `pow(2, n)`，并且不会进行溢出检测
3. 右移 *n* 位，相当于除以 `pow(2, n)`，并且不会进行溢出检测
4. 在执行计算时，会在补码中使用至少一个额外的符号扩展位，也就是说工作位宽至少等于 `1 + max(x.bit_length(),y.bit_length())` 。这会使得在位运算过程中表现出符号位无限延伸到左侧的错觉。

对于 `|` , `^` , `&` , `~` ，符号扩展位也要参与运算：

```python
'''假设整数长度为8bit，并带一个扩展符号位
0 00000001 +1
0 00000010 +2
1 11111111 -1
1 11111110 -2
'''
1|2,1|-2,-1|-2 #>(3, -1, -1)
1^2,1^-2,-1^-2 #>(3, -1, 1)
1&2,1&-2,-1&-2 #>(0, 0, -2)
~2,~-2 #>(-3, 1)
```

## 4. int类型的附加方法

int 类型属于[抽象基类](https://docs.python.org/3.7/glossary.html#term-abstract-base-class) [`numbers.Integral`](https://docs.python.org/3.7/library/numbers.html#numbers.Integral) 的实现，并且还提供了以下附加附加方法：

### 🔨 bit_length

🔨 int.bit_length()

Return the number of bits necessary to represent an integer in binary, excluding the sign and leading zeros:

```python
>>> n = -37
>>> bin(n)
'-0b100101'
>>> n.bit_length()
6
```

More precisely, if `x` is nonzero, then `x.bit_length()` is the unique positive integer `k` such that `2**(k-1) <= abs(x) < 2**k`. Equivalently, when `abs(x)` is small enough to have a correctly rounded logarithm, then `k = 1 + int(log(abs(x), 2))`. If `x` is zero, then `x.bit_length()` returns `0`.

Equivalent to:

```
def bit_length(self):
    s = bin(self)       # binary representation:  bin(-37) --> '-0b100101'
    s = s.lstrip('-0b') # remove leading zeros and minus sign
    return len(s)       # len('100101') --> 6
```

New in version 3.1.

### 🔨 to_bytes

🔨 int.to_bytes(*length*, *byteorder*, *\**, *signed=False*)

Return an array of bytes representing an integer.

```
>>> (1024).to_bytes(2, byteorder='big')
b'\x04\x00'
>>> (1024).to_bytes(10, byteorder='big')
b'\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00'
>>> (-1024).to_bytes(10, byteorder='big', signed=True)
b'\xff\xff\xff\xff\xff\xff\xff\xff\xfc\x00'
>>> x = 1000
>>> x.to_bytes((x.bit_length() + 7) // 8, byteorder='little')
b'\xe8\x03'
```

The integer is represented using *length* bytes. An [`OverflowError`](https://docs.python.org/3.7/library/exceptions.html#OverflowError) is raised if the integer is not representable with the given number of bytes.

The *byteorder* argument determines the byte order used to represent the integer. If *byteorder* is `"big"`, the most significant byte is at the beginning of the byte array. If *byteorder* is `"little"`, the most significant byte is at the end of the byte array. To request the native byte order of the host system, use [`sys.byteorder`](https://docs.python.org/3.7/library/sys.html#sys.byteorder) as the byte order value.

The *signed* argument determines whether two’s complement is used to represent the integer. If *signed* is `False` and a negative integer is given, an [`OverflowError`](https://docs.python.org/3.7/library/exceptions.html#OverflowError) is raised. The default value for *signed* is `False`.

New in version 3.2.

### 🔨 from_bytes

🔨 *classmethod* int.from_bytes(*bytes*, *byteorder*, *\**, *signed=False*)

Return the integer represented by the given array of bytes.

```
>>> int.from_bytes(b'\x00\x10', byteorder='big')
16
>>> int.from_bytes(b'\x00\x10', byteorder='little')
4096
>>> int.from_bytes(b'\xfc\x00', byteorder='big', signed=True)
-1024
>>> int.from_bytes(b'\xfc\x00', byteorder='big', signed=False)
64512
>>> int.from_bytes([255, 0, 0], byteorder='big')
16711680
```

The argument *bytes* must either be a [bytes-like object](https://docs.python.org/3.7/glossary.html#term-bytes-like-object) or an iterable producing bytes.

The *byteorder* argument determines the byte order used to represent the integer. If *byteorder* is `"big"`, the most significant byte is at the beginning of the byte array. If *byteorder* is `"little"`, the most significant byte is at the end of the byte array. To request the native byte order of the host system, use [`sys.byteorder`](https://docs.python.org/3.7/library/sys.html#sys.byteorder) as the byte order value.

The *signed* argument indicates whether two’s complement is used to represent the integer.

New in version 3.2.

## 4. float类型的附加方法

float 类型属于[抽象基类](https://docs.python.org/3.7/glossary.html#term-abstract-base-class) [`numbers.Real`](https://docs.python.org/3.7/library/numbers.html#numbers.Real) 的实现，并且还提供了以下附加附加方法：

- 🔨 float.as_integer_ratio()

  Return a pair of integers whose ratio is exactly equal to the original float and with a positive denominator. Raises [`OverflowError`](https://docs.python.org/3.7/library/exceptions.html#OverflowError) on infinities and a [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError) on NaNs.

  ```python
  0.5.as_integer_ratio() #> (1, 2)
  ```

- 🔨 float.is_integer()

  Return `True` if the float instance is finite with integral value, and `False` otherwise:

  ```
  >>> (-2.0).is_integer()
  True
  >>> (3.2).is_integer()
  False
  ```

Two methods support conversion to and from hexadecimal strings. Since Python’s floats are stored internally as binary numbers, converting a float to or from a *decimal* string usually involves a small rounding error. In contrast, hexadecimal strings allow exact representation and specification of floating-point numbers. This can be useful when debugging, and in numerical work.

- 🔨 float.hex()

  Return a representation of a floating-point number as a hexadecimal string. For finite floating-point numbers, this representation will always include a leading `0x` and a trailing `p` and exponent.

- 🔨 *classmethod* float.fromhex(*s*)

  Class method to return the float represented by a hexadecimal string *s*. The string *s* may have leading and trailing whitespace.

Note that [`float.hex()`](https://docs.python.org/3.7/library/stdtypes.html#float.hex) is an instance method, while [`float.fromhex()`](https://docs.python.org/3.7/library/stdtypes.html#float.fromhex) is a class method.

A hexadecimal string takes the form:

```
[sign] ['0x'] integer ['.' fraction] ['p' exponent]
```

where the optional `sign` may by either `+` or `-`, `integer` and `fraction` are strings of hexadecimal digits, and `exponent` is a decimal integer with an optional leading sign. Case is not significant, and there must be at least one hexadecimal digit in either the integer or the fraction. This syntax is similar to the syntax specified in section 6.4.4.2 of the C99 standard, and also to the syntax used in Java 1.5 onwards. In particular, the output of [`float.hex()`](https://docs.python.org/3.7/library/stdtypes.html#float.hex) is usable as a hexadecimal floating-point literal in C or Java code, and hexadecimal strings produced by C’s `%a` format character or Java’s `Double.toHexString` are accepted by[`float.fromhex()`](https://docs.python.org/3.7/library/stdtypes.html#float.fromhex).

Note that the exponent is written in decimal rather than hexadecimal, and that it gives the power of 2 by which to multiply the coefficient. For example, the hexadecimal string `0x3.a7p10` represents the floating-point number `(3 + 10./16 + 7./16**2) * 2.0**10`, or`3740.0`:

```
>>> float.fromhex('0x3.a7p10')
3740.0
```

Applying the reverse conversion to `3740.0` gives a different hexadecimal string representing the same number:

```
>>> float.hex(3740.0)
'0x1.d380000000000p+11'
```

## 5. Hashing of numeric types

For numbers `x` and `y`, possibly of different types, it’s a requirement that `hash(x) == hash(y)`whenever `x == y` (see the [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) method documentation for more details). For ease of implementation and efficiency across a variety of numeric types (including [`int`](https://docs.python.org/3.7/library/functions.html#int), [`float`](https://docs.python.org/3.7/library/functions.html#float), [`decimal.Decimal`](https://docs.python.org/3.7/library/decimal.html#decimal.Decimal) and [`fractions.Fraction`](https://docs.python.org/3.7/library/fractions.html#fractions.Fraction)) Python’s hash for numeric types is based on a single mathematical function that’s defined for any rational number, and hence applies to all instances of [`int`](https://docs.python.org/3.7/library/functions.html#int) and [`fractions.Fraction`](https://docs.python.org/3.7/library/fractions.html#fractions.Fraction), and all finite instances of [`float`](https://docs.python.org/3.7/library/functions.html#float) and [`decimal.Decimal`](https://docs.python.org/3.7/library/decimal.html#decimal.Decimal). Essentially, this function is given by reduction modulo `P` for a fixed prime `P`. The value of `P` is made available to Python as the `modulus` attribute of [`sys.hash_info`](https://docs.python.org/3.7/library/sys.html#sys.hash_info).

**CPython implementation detail:** Currently, the prime used is `P = 2**31 - 1` on machines with 32-bit C longs and `P = 2**61 - 1` on machines with 64-bit C longs.

Here are the rules in detail:

- If `x = m / n` is a nonnegative rational number and `n` is not divisible by `P`, define `hash(x)`as `m * invmod(n, P) % P`, where `invmod(n, P)` gives the inverse of `n` modulo `P`.
- If `x = m / n` is a nonnegative rational number and `n` is divisible by `P` (but `m` is not) then `n` has no inverse modulo `P` and the rule above doesn’t apply; in this case define`hash(x)` to be the constant value `sys.hash_info.inf`.
- If `x = m / n` is a negative rational number define `hash(x)` as `-hash(-x)`. If the resulting hash is `-1`, replace it with `-2`.
- The particular values `sys.hash_info.inf`, `-sys.hash_info.inf` and `sys.hash_info.nan`are used as hash values for positive infinity, negative infinity, or nans (respectively). (All hashable nans have the same hash value.)
- For a [`complex`](https://docs.python.org/3.7/library/functions.html#complex) number `z`, the hash values of the real and imaginary parts are combined by computing `hash(z.real) + sys.hash_info.imag * hash(z.imag)`, reduced modulo`2**sys.hash_info.width` so that it lies in `range(-2**(sys.hash_info.width - 1), 2**(sys.hash_info.width - 1))`. Again, if the result is `-1`, it’s replaced with `-2`.

To clarify the above rules, here’s some example Python code, equivalent to the built-in hash, for computing the hash of a rational number, [`float`](https://docs.python.org/3.7/library/functions.html#float), or [`complex`](https://docs.python.org/3.7/library/functions.html#complex):

```python
import sys, math

def hash_fraction(m, n):
    """Compute the hash of a rational number m / n.

    Assumes m and n are integers, with n positive.
    Equivalent to hash(fractions.Fraction(m, n)).

    """
    P = sys.hash_info.modulus
    # Remove common factors of P.  (Unnecessary if m and n already coprime.)
    while m % P == n % P == 0:
        m, n = m // P, n // P

    if n % P == 0:
        hash_value = sys.hash_info.inf
    else:
        # Fermat's Little Theorem: pow(n, P-1, P) is 1, so
        # pow(n, P-2, P) gives the inverse of n modulo P.
        hash_value = (abs(m) % P) * pow(n, P - 2, P) % P
    if m < 0:
        hash_value = -hash_value
    if hash_value == -1:
        hash_value = -2
    return hash_value

def hash_float(x):
    """Compute the hash of a float x."""

    if math.isnan(x):
        return sys.hash_info.nan
    elif math.isinf(x):
        return sys.hash_info.inf if x > 0 else -sys.hash_info.inf
    else:
        return hash_fraction(*x.as_integer_ratio())

def hash_complex(z):
    """Compute the hash of a complex number z."""

    hash_value = hash_float(z.real) + sys.hash_info.imag * hash_float(z.imag)
    # do a signed reduction modulo 2**sys.hash_info.width
    M = 2**(sys.hash_info.width - 1)
    hash_value = (hash_value & (M - 1)) - (hash_value & M)
    if hash_value == -1:
        hash_value = -2
    return hash_value
```

