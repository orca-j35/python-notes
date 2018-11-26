# oct

🔨 oct(*x*)

该函数会将整数 *x* 表示为一个八进制字符串(以 "0o" 为前缀)。
该八进制字符串是一个有效的 Python 表达式(可直接用于 `eval ()` 函数)。

示例：

```python
>>> oct(8)
'0o10'
>>> oct(-56)
'-0o70'
>>> eval(oct(-56))
-56
# 如果x不是整数则会抛出异常
# 浮点数实现了__int__，没有实现__index__
>>> oct(1.1)
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    oct(1.1)
TypeError: 'float' object cannot be interpreted as an integer
```

如果 *x* 不是 [`int`](https://docs.python.org/3/library/functions.html#int) 对象，则 *x* 必须定义 [`__index__()`](https://docs.python.org/3/reference/datamodel.html#object.__index__) 方法，且必须返回一个整数；否则均会抛出异常。

```python
>>> class Cls:
    def __index__(self):
        return 8

>>> oct(Cls())
'0o10'
>>> class ClsSub(Cls):
    def __index__(self):
        return 1.1
# 如果__index__未返回整数，便会抛出异常
>>> oct(ClsSub())
Traceback (most recent call last):
  File "<pyshell#16>", line 1, in <module>
    oct(ClsSub())
TypeError: __index__ returned non-int (type float)
```

如果不需要 "0o" 前缀，可以使用以下三种方式(阅读 [`format()`](https://docs.python.org/3/library/functions.html#format) 可解更多格式化信息)：

```python
>>> '%#o' % 10, '%o' % 10
('0o12', '12')
>>> format(10, '#o'), format(10, 'o')
('0o12', '12')
>>> f'{10:#o}', f'{10:o}'
('0o12', '12')
```

有关 [`__index__()`](https://docs.python.org/3/reference/datamodel.html#object.__index__) 和 `__int__` 的区别，可阅读：

- [PEP 357: The ‘`__index__`’ method](https://docs.python.org/3/whatsnew/2.5.html#pep-357-the-index-method)
- [PEP 357 -- Allowing Any Object to be Used for Slicing](https://www.python.org/dev/peps/pep-0357/)