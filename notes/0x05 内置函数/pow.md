# pow

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记:『3.3. Special method names.md』-> 3.3.8. Emulating numeric types

```python
pow(x, y, z=None, /)
    Equivalent to x**y (with two arguments) or x**y % z (with three arguments)
    
    Some types, such as ints, are able to use a more efficient algorithm when invoked using the three argument form.
```

🔨 pow(*x*, *y*[, *z*])

`pow(x, y)` 等价于 `x**y`；`pow(x, y, z)` 等效于 `pow(x, y) % z`，但前者更高效。

```python
>>> pow(-1,2)
1
# 等效于如下表达式，注意括号
>>> (-1)**2
1
# 否则会按照运算符优先级，从右至左进行计算
>>> -1**2
-1
```

参数 *x*、*y*、*z* 都必须是数值类型。对于混合操作数类型，将使用二元算术运算规则。对于 [`int`](https://docs.python.org/3.7/library/functions.html#int) 类型的操作数， 计算结果与操作数具备相同的类型，除非 *y* 是负数(在这种情况下，所有参数都将被转换为 float，并且结果也是 float)。

```python
>>> 10**2
100
>>> 10**-2
0.01
>>> pow(2,0.1)
1.0717734625362931
```

只有在 *x* 和 *y* 都是整数，且 *y* 非负的情况下，才能使用参数 *z*：

```python
>>> pow(10,2,9)
1
```

如果 *y* 是负数，则不能使用参数 *z*

```python
>>> pow(10,-2,1)
Traceback (most recent call last):
  File "<pyshell#64>", line 1, in <module>
    pow(10,-2,1)
ValueError: pow() 2nd argument cannot be negative when 3rd argument specified
```

`0` 的负数幂将抛出 [`ZeroDivisionError`](https://docs.python.org/3.7/library/exceptions.html#ZeroDivisionError)：负数的小数(分数)幂将产生一个复数([`complex`](https://docs.python.org/3.7/library/functions.html#complex))，在早期版本中会抛出 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError)。

```python
>>> pow(0,-1)
Traceback (most recent call last):
  File "<pyshell#71>", line 1, in <module>
    pow(0,-1)
ZeroDivisionError: 0.0 cannot be raised to a negative power
>>> (-1)**(1/2)
(6.123233995736766e-17+1j)
>>> (-1)**(0.5)
(6.123233995736766e-17+1j)
```

## \_\_pow\_\_

> 相关笔记:『3.3. Special method names.md』-> 3.3.8. Emulating numeric types

🔨 object.`__pow__`(*self*, *other*[, *modulo*])

`__pow__` 用于实现 `pow()` (`**`)：

```python
class ExampleCls:
    def __pow__(self,other):
        return self,other
pow(ExampleCls(),2)
#> (<__main__.ExampleCls at 0x1ef59b72860>, 2)
ExampleCls()**2
#> (<__main__.ExampleCls at 0x1ef59bc9da0>, 2)
```

注意：如果需要 `pow()` 支持三参数形式，则应使 `__pow__()` 可接受第三个可选参数。

## \_\_rpow\_\_

> 相关笔记:『3.3. Special method names.md』-> 3.3.8. Emulating numeric types

🔨 object.`__rpow__`(*self*, *other*)

注意：以三参数形式调用 `pow()` 时，不会尝试调用 `__rpow__()`。

`__rpow__` 用于为 `pow()` (`**`) 实现反射(交换)操作，只有当左操作数"不支持"相应操作，并且操作数是"不同类型"时，才会调用反射方法。

```python
class A:
    def __pow__(self,other):
        return NotImplemented
class B:
    def __rpow__(self,other):
        return 'in B'
class C:pass

pow(A(),B()) #> in B
pow(C(),B()) #> in B
```

"不支持"的意思是类中不包含相应方法，或虽实现了相应方法但返回值是 `NotImplemented`。如果需要强制回退至右操作数的反射方法，则不应将左操作数的方法设置为 `None`。`None` 会显示阻止回退操作，并将 `None` 直接用作返回值。

```python
class A:
    def __pow__(self,other):
        return None
class B:
    def __pow__(self,other):
        return 'in B'
print(pow(A(),B())) #> None
```

对于相同类型的操作数，如果非反射方法失效(例如， [`__add__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__add__))，则认为操作数不支持相应的操作，并不会调用反射方法。

```python
class A:
    def __pow__(self,other):
        return NotImplemented
    def __rpow__(self,other):
        return 'in rpow'
pow(A(),A()) 
#> TypeError: unsupported operand type(s) for ** or pow(): 'A' and 'A'
```