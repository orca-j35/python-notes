# bin

bin(*x*)

该函数会将整数 *x* 表示为一个二进制字符串(以 "0b" 为前缀)。
该二进制字符串是一个有效的 Python 表达式(比如，可直接用于 `eval ()` 函数)。

示例：

```python
>>> bin(3)
'0b11'
>>> bin(-10)
'-0b1010'
```

如果不需要 "0b" 前缀，可以使用以下两种方式(阅读 [`format()`](https://docs.python.org/3/library/functions.html#format) 可解更多格式化信息)：

```python
>>> format(14, '#b'), format(14, 'b')
('0b1110', '1110')
>>> f'{14:#b}', f'{14:b}'
('0b1110', '1110')
```

如果 *x* 不是 [`int`](https://docs.python.org/3/library/functions.html#int) 对象，则 *x* 必须包含 [`__index__()`](https://docs.python.org/3/reference/datamodel.html#object.__index__) 方法，且该方法必须返回一个整数；否则会抛出异常。

```python
>>> class Cls:
    def __index__(self):
        return 6

>>> bin(Cls())
'0b110'
```

有关 [`__index__()`](https://docs.python.org/3/reference/datamodel.html#object.__index__) 和 `__int__` 的区别，可阅读：

- [PEP 357: The ‘`__index__`’ method](https://docs.python.org/3/whatsnew/2.5.html#pep-357-the-index-method)
- [PEP 357 -- Allowing Any Object to be Used for Slicing](https://www.python.org/dev/peps/pep-0357/)

