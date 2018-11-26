# pow

```python
pow(x, y, z=None, /)
    Equivalent to x**y (with two arguments) or x**y % z (with three arguments)
    
    Some types, such as ints, are able to use a more efficient algorithm when
    invoked using the three argument form.
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

