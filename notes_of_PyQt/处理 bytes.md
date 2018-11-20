# 处理 bytes

[TOC]

在 Python 3.x 中，字符串默认使用 Unicode 的编码。如果需要向 Arduino 发送数据，则需要将 Python 中的 `str` 转换为 `bytes` 。通过为字符串加上前缀 `b` ，即可完成这种转换：

```
>>> ser.write(b'5') # 前缀b，对于Python3是必须的。
```

示例 bytes：

```
test_bytes = b'\xA0\x60\x00\x00\x0F\xCF'
```

## struct

7.1. `struct` — 处理二进制数据记录格式

利用 `pack` 将整型转换为 `bytes` ，`>` 表示按照 big-endian 排序，即从左到右排序

```
>>> import struct
>>> struct.pack('>I', 10240099)
b'\x00\x9c@c'
```

利用 `unpack` 把 `bytes` 转换为相应数据类型：

```
>>> struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
(4042322160, 32896)
```







------

4.8. Binary Sequence Types — [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes), [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray), [`memoryview`](https://docs.python.org/3/library/stdtypes.html#memoryview)[¶](https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)

- *classmethod *`fromhex`(*string*)

  This [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) class method returns a bytes object, decoding the given string object. The string must contain two hexadecimal digits per byte, with ASCII whitespace being ignored.>>>`>>> bytes.fromhex('2Ef0 F1f2  ')b'.\xf0\xf1\xf2'`

A reverse conversion function exists to transform a bytes object into its hexadecimal representation.

- `hex`()

  Return a string object containing two hexadecimal digits for each byte in the instance.>>>`>>> b'\xf0\xf1\xf2'.hex()'f0f1f2'`New in version 3.5.

------

https://docs.python.org/3/library/functions.html#hex

## 将数值转换为字符串

### 以16进制字符串显示数值

hex(x)[¶](https://docs.python.org/3/library/functions.html#hex) -> str

Convert an integer number to a lowercase hexadecimal string prefixed with “0x”. If x is not a Python [`int`](https://docs.python.org/3/library/functions.html#int) object, it has to define an `__index__()` method that returns an integer. Some examples:

```
>>> hex(255)
'0xff'
>>> hex(-42)
'-0x2a'

```

If you want to convert an integer number to an uppercase or lower hexadecimal string with prefix or not, you can use either of the following ways:

```
>>> '%#x' % 255, '%x' % 255, '%X' % 255
('0xff', 'ff', 'FF')
>>> format(255, '#x'), format(255, 'x'), format(255, 'X')
('0xff', 'ff', 'FF')
>>> f'{255:#x}', f'{255:x}', f'{255:X}'
('0xff', 'ff', 'FF')

```

See also [`format()`](https://docs.python.org/3/library/functions.html#format) for more information.

See also [`int()`](https://docs.python.org/3/library/functions.html#int) for converting a hexadecimal string to an integer using a base of 16.

Note

To obtain a hexadecimal string representation for a float, use the [`float.hex()`](https://docs.python.org/3/library/stdtypes.html#float.hex)method.

## 删除 `0x` 字符

str.lstrip([chars]); str.rstrip([chars]); str.strip([chars])

```
>>> '0x0'.lstrip('0x')
''
>>> '0x0F'.lstrip('0x')
'F'
```

## 在字符的左侧填充 `'0'` 

有时，在处理16进制的字符串时，往往会遇到 `'0x7'` 这种情况。为了将显示的格式同一为形如 `'FF'` 的样式，我们需要在 `7` 之前补 `0` 

此时需要在 `7` 之前补 `0` ，以便统一显示格式。 

> str.zfill(*width*) [¶](https://docs.python.org/3/library/stdtypes.html#string-methods) 
>
> Return a copy of the string left filled with ASCII `'0'` digits to make a string of length *width*. A leading sign prefix (`'+'`/`'-'`) is handled by inserting the padding *after* the sign character rather than before. The original string is returned if *width* is less than or equal to `len(s)`.
>

示例：

```python
>>> "42".zfill(5)
'00042'
>>> "-42".zfill(5)
'-0042'

>>> '0x7'.lstrip('0x').zfill(2)
'07'
>>> '0x0'.lstrip('0x').zfill(2)
'00'
```


