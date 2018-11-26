# hex

🔨 hex(*x*)

该函数会将整数 *x* 表示为一个十六进制字符串(以 "0x" 为前缀，小写字母)。
该十六进制字符串是一个有效的 Python 表达式(可直接用于 `eval ()` 函数)。

示例：

```python
>>> hex(255)
'0xff'
>>> hex(-42)
'-0x2a'
>>> eval(hex(-42))
-42
# 如果x不是整数则会抛出异常
# 浮点数实现了__int__，没有实现__index__
>>> hex(10.1)
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    hex(10.1)
TypeError: 'float' object cannot be interpreted as an integer
```

如果 *x* 不是 [`int`](https://docs.python.org/3/library/functions.html#int) 对象，则 *x* 必须定义 [`__index__()`](https://docs.python.org/3/reference/datamodel.html#object.__index__) 方法，且必须返回一个整数；否则均会抛出异常。

```python
>>> class Cls:
    def __index__(self):
        return 10

>>> hex(Cls())
'0xa'
# 如果__index__未返回整数，便会抛出异常
>>> class ClsSub(Cls):
    def __index__(self):
        return 10.1

>>> hex(ClsSub())
Traceback (most recent call last):
  File "<pyshell#27>", line 1, in <module>
    hex(ClsSub())
TypeError: __index__ returned non-int (type float)
```

如果不需要 "0x" 前缀，或是想使用大写字母，可以使用以下三种方式(阅读 [`format()`](https://docs.python.org/3/library/functions.html#format) 可解更多格式化信息)：

```python
>>> '%#x' % 255, '%x' % 255, '%X' % 255
('0xff', 'ff', 'FF')
>>> format(255, '#x'), format(255, 'x'), format(255, 'X')
('0xff', 'ff', 'FF')
>>> f'{255:#x}', f'{255:x}', f'{255:X}'
('0xff', 'ff', 'FF')
```

如果需要将十六进制字符串转换为对应的整数，可使用以下两种方法：

```python
>>> int('a',base=16)
10
>>> int('0xa',base=16)
10
>>> eval('0xa')
10
```

注意：如果需要获取浮点数的十六进制表示形式，请使用 [`float.hex()`](https://docs.python.org/3.7/library/stdtypes.html#float.hex) 方法：

```python
>>> float.hex(10.10)
'0x1.4333333333333p+3'
```

要获取float的十六进制字符串表示形式，请使用float.hex（）方法。

有关 [`__index__()`](https://docs.python.org/3/reference/datamodel.html#object.__index__) 和 `__int__` 的区别，可阅读：

- [PEP 357: The ‘`__index__`’ method](https://docs.python.org/3/whatsnew/2.5.html#pep-357-the-index-method)
- [PEP 357 -- Allowing Any Object to be Used for Slicing](https://www.python.org/dev/peps/pep-0357/)