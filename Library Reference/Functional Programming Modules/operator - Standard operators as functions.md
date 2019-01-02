# operator - Standard operators as functions
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 扩展阅读：
>
> - [`operator`](https://docs.python.org/3.7/library/operator.html#module-operator) — Standard operators as functions
> - [operator — 内置操作符接口](https://pythoncaff.com/docs/pymotw/operator-built-in-operator-interface/94)

`operater` 模块导出了一组与 Python 的内部运算符相对应的函数。例如 `operator.add(x, y)` 等价于表达式 `x+y`。

在本模块中，大多数函数名直接使用对应的特殊方法名(但不带下划线)。为了向后兼容，本模块中的许多方法还保留了具备双下划线方法名的变体。为了使代码易读，请优先使用没有双下划线的版本。

本模块中的方法可分为以下四类：

- 对象比较(*object* compa*r*isons)
- 逻辑运算(*logical* *operations*)
- 数学运算(*mathematical* *operations*)和位运算(*bitwise* *operations*)
- 序列操作(*sequence* *operations*)

## 运算符和函数的映射关系

Mapping Operators to Functions

This table shows how abstract operations correspond to operator symbols in the Python syntax and the functions in the [`operator`](https://docs.python.org/3.7/library/operator.html#module-operator) module.

| Operation             | Syntax              | Function                            |
| --------------------- | ------------------- | ----------------------------------- |
| Addition              | `a + b`             | `add(a, b)`                         |
| Concatenation         | `seq1 + seq2`       | `concat(seq1, seq2)`                |
| Containment Test      | `obj in seq`        | `contains(seq, obj)`                |
| Division              | `a / b`             | `truediv(a, b)`                     |
| Division              | `a // b`            | `floordiv(a, b)`                    |
| Bitwise And           | `a & b`             | `and_(a, b)`                        |
| Bitwise Exclusive Or  | `a ^ b`             | `xor(a, b)`                         |
| Bitwise Inversion     | `~ a`               | `invert(a)`                         |
| Bitwise Or            | `a | b`             | `or_(a, b)`                         |
| Exponentiation        | `a ** b`            | `pow(a, b)`                         |
| Identity              | `a is b`            | `is_(a, b)`                         |
| Identity              | `a is not b`        | `is_not(a, b)`                      |
| Indexed Assignment    | `obj[k] = v`        | `setitem(obj, k, v)`                |
| Indexed Deletion      | `del obj[k]`        | `delitem(obj, k)`                   |
| Indexing              | `obj[k]`            | `getitem(obj, k)`                   |
| Left Shift            | `a << b`            | `lshift(a, b)`                      |
| Modulo                | `a % b`             | `mod(a, b)`                         |
| Multiplication        | `a * b`             | `mul(a, b)`                         |
| Matrix Multiplication | `a @ b`             | `matmul(a, b)`                      |
| Negation (Arithmetic) | `- a`               | `neg(a)`                            |
| Negation (Logical)    | `not a`             | `not_(a)`                           |
| Positive              | `+ a`               | `pos(a)`                            |
| Right Shift           | `a >> b`            | `rshift(a, b)`                      |
| Slice Assignment      | `seq[i:j] = values` | `setitem(seq, slice(i, j), values)` |
| Slice Deletion        | `del seq[i:j]`      | `delitem(seq, slice(i, j))`         |
| Slicing               | `seq[i:j]`          | `getitem(seq, slice(i, j))`         |
| String Formatting     | `s % obj`           | `mod(s, obj)`                       |
| Subtraction           | `a - b`             | `sub(a, b)`                         |
| Truth Test            | `obj`               | `truth(obj)`                        |
| Ordering              | `a < b`             | `lt(a, b)`                          |
| Ordering              | `a <= b`            | `le(a, b)`                          |
| Equality              | `a == b`            | `eq(a, b)`                          |
| Difference            | `a != b`            | `ne(a, b)`                          |
| Ordering              | `a >= b`            | `ge(a, b)`                          |
| Ordering              | `a > b`             | `gt(a, b)`                          |

### 对象比较

支持所有的富比较运算符，并以对应的丰富比较运算符来命名：

```python
operator.lt(a, b)
operator.le(a, b)
operator.eq(a, b)
operator.ne(a, b)
operator.ge(a, b)
operator.gt(a, b)
operator.__lt__(a, b)
operator.__le__(a, b)
operator.__eq__(a, b)
operator.__ne__(a, b)
operator.__ge__(a, b)
operator.__gt__(a, b)
```

具体来说，当在 *a* 和 *b* 之间执行"富比较"时：

- `lt(a, b)` is equivalent to `a <b`
- `le(a, b)` is equivalent to `a <= b`
- `eq(a, b)` is equivalent to `a == b`
- `ne(a, b)` is equivalent to `a != b`
- `gt(a, b)` is equivalent to `a > b` 
- `ge(a, b)` is equivalent to `a >=b`. 

注意：以上方法可以返回任意值，这些值可能会(也可能不会)被解释为布尔值。有关丰富比较的详细信息，请参阅 [Comparisons](https://docs.python.org/3.7/reference/expressions.html#comparisons) 。

### 逻辑运算

逻辑操作通常也适用于所有对象，并支持真值测试，身份(*identity*)测试和布尔操作：

```python
operator.not_(obj)
operator.__not__(obj)
# Return the outcome of not obj. (Note that there is no __not__() method for object instances; only the interpreter core defines this operation. The result is affected by the __bool__() and __len__() methods.)

operator.truth(obj)
# Return True if obj is true, and False otherwise. This is equivalent to using the bool constructor.

operator.is_(a, b)
# Return a is b. Tests object identity.

operator.is_not(a, b)
# Return a is not b. Tests object identity.
```

### 数学运算和位运算

#### 数学运算

```python
operator.abs(obj)
operator.__abs__(obj)
# Return the absolute value of obj.

operator.add(a, b)
operator.__add__(a, b)
# Return a + b, for a and b numbers.

operator.floordiv(a, b)
operator.__floordiv__(a, b)
# Return a // b.

operator.index(a)
operator.__index__(a)
# Return a converted to an integer. Equivalent to a.__index__().

operator.mod(a, b)
operator.__mod__(a, b)
# Return a % b.

operator.mul(a, b)
operator.__mul__(a, b)
# Return a * b, for a and b numbers.

operator.matmul(a, b)
operator.__matmul__(a, b)
# Return a @ b.
# New in version 3.5.

operator.neg(obj)
operator.__neg__(obj)
# Return obj negated (-obj).

operator.pos(obj)
operator.__pos__(obj)
# Return obj positive (+obj).

operator.pow(a, b)
operator.__pow__(a, b)
# Return a ** b, for a and b numbers.

operator.sub(a, b)
operator.__sub__(a, b)
# Return a - b.

operator.truediv(a, b)
operator.__truediv__(a, b)
# Return a / b where 2/3 is .66 rather than 0. This is also known as “true” division.
```

#### 位运算

```python
operator.and_(a, b)
operator.__and__(a, b)
# Return the bitwise and of a and b.

operator.inv(obj)
operator.invert(obj)
operator.__inv__(obj)
operator.__invert__(obj)
# Return the bitwise inverse of the number obj. This is equivalent to ~obj.

operator.lshift(a, b)
operator.__lshift__(a, b)
# Return a shifted left by b.

operator.or_(a, b)
operator.__or__(a, b)
# Return the bitwise or of a and b.

operator.rshift(a, b)
operator.__rshift__(a, b)
# Return a shifted right by b.

operator.xor(a, b)
operator.__xor__(a, b)
# Return the bitwise exclusive or of a and b.
```

### 序列操作

以下操作工作于序列(部分也可用于映射)之上：

```python
operator.concat(a, b)
operator.__concat__(a, b)
# Return a + b for a and b sequences.

operator.contains(a, b)
operator.__contains__(a, b)
# Return the outcome of the test b in a. Note the reversed operands.

operator.countOf(a, b)
# Return the number of occurrences of b in a.

operator.delitem(a, b)
operator.__delitem__(a, b)
# Remove the value of a at index b.

operator.getitem(a, b)
operator.__getitem__(a, b)
# Return the value of a at index b.

operator.indexOf(a, b)
# Return the index of the first of occurrence of b in a.

operator.setitem(a, b, c)
operator.__setitem__(a, b, c)
# Set the value of a at index b to c.

operator.length_hint(obj, default=0)
# Return an estimated length for the object o. First try to return its actual length, then an estimate using object.__length_hint__(), and finally return the default value.
# New in version 3.4.
```

## 属性和项获取器

> 扩展阅读:﹝流畅的 Python﹞-> 5.10 支持函数式编程的包

[`operator`](https://docs.python.org/3.7/library/operator.html#module-operator) 模块还定义了用于通用属性和项查找的工具。这些工具可用于 [`map()`](https://docs.python.org/3.7/library/functions.html#map), [`sorted()`](https://docs.python.org/3.7/library/functions.html#sorted), [`itertools.groupby()`](https://docs.python.org/3.7/library/itertools.html#itertools.groupby) 等函数的键函数，以便快速提取相应的字段。

获取器(*getter*)的开销比 `lambda` (或普通函数)小。

### attrgetter

🔨 operator.attrgetter(*attr*)

🔨 operator.attrgetter(**attrs*)

Return a callable object that fetches *attr* from its operand. If more than one attribute is requested, returns a tuple of attributes. The attribute names can also contain dots. For example:

- After `f = attrgetter('name')`, the call `f(b)` returns `b.name`.
- After `f = attrgetter('name', 'date')`, the call `f(b)` returns `(b.name, b.date)`.
- After `f = attrgetter('name.first', 'name.last')`, the call `f(b)` returns `(b.name.first, b.name.last)`.

Equivalent to:

```python
def attrgetter(*items):
    if any(not isinstance(item, str) for item in items):
        raise TypeError('attribute name must be a string')
    if len(items) == 1:
        attr = items[0]
        def g(obj):
            return resolve_attr(obj, attr)
    else:
        def g(obj):
            return tuple(resolve_attr(obj, attr) for attr in items)
    return g

def resolve_attr(obj, attr):
    for name in attr.split("."):
        obj = getattr(obj, name)
    return obj
```

### itemgetter

🔨 operator.itemgetter(*item*)

🔨 operator.itemgetter(**items*)

Return a callable object that fetches *item* from its operand using the operand’s [`__getitem__()`](https://docs.python.org/3.7/library/operator.html#operator.__getitem__) method. If multiple items are specified, returns a tuple of lookup values. For example:

- After `f = itemgetter(2)`, the call `f(r)` returns `r[2]`.
- After `g = itemgetter(2, 5, 3)`, the call `g(r)` returns `(r[2], r[5], r[3])`.

Equivalent to:

```python
def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g
```

The items can be any type accepted by the operand’s [`__getitem__()`](https://docs.python.org/3.7/library/operator.html#operator.__getitem__) method. Dictionaries accept any hashable value. Lists, tuples, and strings accept an index or a slice:

```python
>>> itemgetter(1)('ABCDEFG')
'B'
>>> itemgetter(1,3,5)('ABCDEFG')
('B', 'D', 'F')
>>> itemgetter(slice(2,None))('ABCDEFG')
'CDEFG'
```

```python
>>> soldier = dict(rank='captain', name='dotterbart')
>>> itemgetter('rank')(soldier)
'captain
```

Example of using [`itemgetter()`](https://docs.python.org/3.7/library/operator.html#operator.itemgetter) to retrieve specific fields from a tuple record:

```python
>>> inventory = [('apple', 3), ('banana', 2), ('pear', 5), ('orange', 1)]
>>> getcount = itemgetter(1)
>>> list(map(getcount, inventory))
[3, 2, 5, 1]
>>> sorted(inventory, key=getcount)
[('orange', 1), ('banana', 2), ('apple', 3), ('pear', 5)]
```

### methodcaller

🔨 operator.methodcaller(*name*[, *args...*])

Return a callable object that calls the method *name* on its operand. If additional arguments and/or keyword arguments are given, they will be given to the method as well. For example:

- After `f = methodcaller('name')`, the call `f(b)` returns `b.name()`.
- After `f = methodcaller('name', 'foo', bar=1)`, the call `f(b)` returns `b.name('foo', bar=1)`.

Equivalent to:

```python
def methodcaller(name, *args, **kwargs):
    def caller(obj):
        return getattr(obj, name)(*args, **kwargs)
    return caller
```

## Inplace Operators

大多数运算符都有 “in-place” 版本(增量赋值)。下面列出的函数提供了比常用语法更原始的访问方法。例如：

- the [statement](https://docs.python.org/3.7/glossary.html#term-statement) `x += y` is equivalent to `x = operator.iadd(x, y)`. 
- Another way to put it is to say that `z = operator.iadd(x, y)` is equivalent to the compound statement `z = x; z += y`.

如果增量赋值运算符的第一个参数是可变的，那么这些运算符函数会就地修改它；否则，作用与不带 `i` 的函数(e.g. `iadd()`)一样，直接返回运算结果。

In those examples, note that when an in-place method is called, the computation and assignment are performed in two separate steps. The in-place functions listed below only do the first step, calling the in-place method. The second step, assignment, is not handled.

For **immutable** targets such as strings, numbers, and tuples, the updated value is computed, but not assigned back to the input variable:

```
>>> a = 'hello'
>>> iadd(a, ' world')
'hello world'
>>> a
'hello'
```

For **mutable** targets such as lists and dictionaries, the inplace method will perform the update, so no subsequent assignment is necessary:

```
>>> s = ['h', 'e', 'l', 'l', 'o']
>>> iadd(s, [' ', 'w', 'o', 'r', 'l', 'd'])
['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']
>>> s
['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']
```

```python
operator.iadd(a, b)
operator.__iadd__(a, b)
# a = iadd(a, b) is equivalent to a += b.

operator.iand(a, b)
operator.__iand__(a, b)
# a = iand(a, b) is equivalent to a &= b.

operator.iconcat(a, b)
operator.__iconcat__(a, b)
# a = iconcat(a, b) is equivalent to a += b for a and b sequences.

operator.ifloordiv(a, b)
operator.__ifloordiv__(a, b)
# a = ifloordiv(a, b) is equivalent to a //= b.

operator.ilshift(a, b)
operator.__ilshift__(a, b)
# a = ilshift(a, b) is equivalent to a <<= b.

operator.imod(a, b)
operator.__imod__(a, b)
# a = imod(a, b) is equivalent to a %= b.

operator.imul(a, b)
operator.__imul__(a, b)
# a = imul(a, b) is equivalent to a *= b.

operator.imatmul(a, b)
operator.__imatmul__(a, b)
# a = imatmul(a, b) is equivalent to a @= b.
# New in version 3.5.

operator.ior(a, b)
operator.__ior__(a, b)
# a = ior(a, b) is equivalent to a |= b.

operator.ipow(a, b)
operator.__ipow__(a, b)
# a = ipow(a, b) is equivalent to a **= b.

operator.irshift(a, b)
operator.__irshift__(a, b)
# a = irshift(a, b) is equivalent to a >>= b.

operator.isub(a, b)
operator.__isub__(a, b)
# a = isub(a, b) is equivalent to a -= b.

operator.itruediv(a, b)
operator.__itruediv__(a, b)
# a = itruediv(a, b) is equivalent to a /= b.

operator.ixor(a, b)
operator.__ixor__(a, b)
# a = ixor(a, b) is equivalent to a ^= b.
```

