# bytearray

*class* bytearray([*source*[, *encoding*[, *errors*]]])

该内置函数本质上是 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray) 类的构造函数，用于创建一个 bytearray 实例。bytearray 实例是一个由字节(8-bits 无符号)构成的可变序列，并拥有大多数可变序列的常见方法[详见：[Mutable Sequence Types](https://docs.python.org/3.7/library/stdtypes.html#typesseq-mutable)]，并且还包含 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 类型中的大多数方法[详见： [Bytes and Bytearray Operations](https://docs.python.org/3.7/library/stdtypes.html#bytes-methods) ]

在 Python 中，我们可以通过 bytes 字面值来创建 bytes 对象，但并没有用于创建 bytearray 字面值的语法，我们只能通过调用构造函数 `bytearray()` 来创建 bytearray 对象。

初始化 bytearray 实例的方式如下：

- 没有任何参数时，将创建一个空实例

  ```python
  # bytearray() -> empty bytes array
  >>> bytearray()
  bytearray(b'')
  ```

- *source* 是一个**整数**时，将创建一个长度为 *source* 且每个字节均为空的 bytearray 对象

  ```python
  # bytearray(int) -> bytearray
  >>> bytearray(5)
  bytearray(b'\x00\x00\x00\x00\x00')
  ```

- *source* 是一个由自然数构成的**可迭代对象**，且每个元素的值 x 均满足 0 ≤ x ≤ 255

  ```python
  # bytearray(iterable_of_ints) -> bytearray
  >>> bytearray(range(5)) # 最大范围是range(256)
  bytearray(b'\x00\x01\x02\x03\x04')
  >>> bytearray([1,2,3,4,5])
  bytearray(b'\x01\x02\x03\x04\x05')
  ```

- *source* 是一个 bytes 对象，将通过缓冲器协议(buffer protocol)复制其中的二进制数据

  ```python
  # bytearray(bytes) -> mutable copy of bytes
  >>> bytearray(b'Hi!')
  bytearray(b'Hi!')
  ```

- *source* 是一个实现了缓冲区(buffer) API 的对象时，则会使用 *source* 的只读缓冲区来初始化 bytearray 对象。

  ```python
  # bytearray(buffer) -> mutable copy of buffer
  ```

- *source* 是一个字符串时，必须给定 *encoding* 参数。此时，构造函数 `bytearray()`  会通过 [`str.encode()`](https://docs.python.org/3.7/library/stdtypes.html#str.encode) 方法将 *source* 编码(encoding)为字节序列。

  - *encoding* 参数用于设置编码方案，会被传递给 `str.encode()`。在 [Standard Encodings](https://docs.python.org/3.7/library/codecs.html#standard-encodings) 中可查看编码方案列表。
  - *errors* 参数用于设置[错误处理方案](https://docs.python.org/3.7/library/codecs.html#error-handlers)，也会被传递给 `str.encode()`。如果 *errors* 为空，`str.encode()` 会使用默认方案 `'strict'`——该方案在出现编码错误时会抛出 [`UnicodeError`](https://docs.python.org/3.7/library/exceptions.html#UnicodeError)。*errors* 可以是 `'ignore'`, `'replace'`, `'xmlcharrefreplace'`, `'backslashreplace'` 或任何已通过 [`codecs.register_error()`](https://docs.python.org/3.7/library/codecs.html#codecs.register_error) 注册的名称。

  Tips: 在 Python 文档中，"编码(encoding)"是指将 Unicode 字符串转换为字节序列的规则，也就是说"编码"包含了从"抽象字符序列"到"字节序列"的全部过程。

  ```python
  # bytearray(string, encoding[, errors]) -> bytearray
  >>> bytearray('abcd','utf-8')
  bytearray(b'abcd')
  >>> bytearray('鲸','utf-8')
  bytearray(b'\xe9\xb2\xb8')
  
  >>> bytearray('鲸','ascii')
  Traceback (most recent call last):
    File "<pyshell#11>", line 1, in <module>
      bytearray('鲸','ascii')
  UnicodeEncodeError: 'ascii' codec can't encode character '\u9cb8' in position 0: ordinal not in range(128)
  >>> bytearray('鲸','ascii','ignore')
  bytearray(b'')
  ```

扩展阅读: [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3.7/library/stdtypes.html#binaryseq) 及 [Bytearray Objects](https://docs.python.org/3.7/library/stdtypes.html#typebytearray).

## 深入理解 bytearray 对象

在 C 语言中创建字节数组的语法如下：

```c
byte bytes_array[] = {0x02, 0x03, 0x0A, 0x41}
```

Python 中的 bytearray 对象与 C 语言中的字节数组类似，**每个索引位置都对应一个整数 x (且 0≤x≤255)**。不同之处在于 bytearray 对象会以转义序列或 ASCII 字符显示相应数值(如，将十进制整数 65 显示为字母 A)，但是 bytearray 对象的每个索引位置仍然是一个数值，而非一个字符。bytearray 对象是一个实实在在的**字节序列**，每个索引位置对应一个字节(byte)而不是一个字符(char)。

注意：不能将 bytearray 完全等同于 C 的字符数组，因为 bytearray 远比字符数组强大。

下面创建一个与上面的 C 语言字节数组拥有相同内容的 bytearray 对象：

```python
>>> a_obj = bytearray((0x02, 0x03, 0x0A, 0x41))
>>> a_obj
bytearray(b'\x02\x03\nA') # 以转义序列或 ASCII 编码显示相应数值
>>> [ x for x in a_obj]
[2, 3, 10, 65] # 每个索引位置始终对应一个数值，而非一个字符
```

### 如何显示数值

如果某个索引位置的数值对应 ASCII 编码中的可见字符，那么该索引位便会显示该字符：

```python
>>> bytearray((0x41, 0x42))
bytearray(b'AB')
```

如果某个索引位置的数值对应 ASCII 编码中的不可见字符，但该字符拥有"独立转义序列"，那么该索引位置会显示该"独立转义序列"：

```python
>>> bytearray((0x0A, 0x0D))
bytearray(b'\n\r')
```

如果某个索引位置的数值对应 ASCII 编码中的不可见字符，并且该字符没有"独立转义序列"；或该数值已超出了 ASCII 编码的范围。那么该索引位置会显示十六进制(`'\xhh'`)转义序列。在 bytearray 对象中，十六进制(`'\xhh'`)转义序列用于表示具有指定数值的字节。

```python
>>> bytearray((0x01, 0xFE))
bytearray(b'\x01\xfe')
```

将 bytearray 对象中各个字节的数值，尽力按照 ASCII 编码显示为相应字符的好处是：如果 bytearray 对象是一个 ASCII 编码的字节序列，那么便可直接读懂其中的内容，无需解码：

```python
>>> hi = bytearray('hello!\n','ascii')
>>> hi
bytearray(b'hello!\n') # 虽然是字节序列，但是不用解码也读懂
>>> hi.decode('ascii')
'hello!\n'
```

再次提醒：bytes 对象是一个实实在在的**字节序列**，每个索引位置对应一个数值而不是一个字符。在读取 bytes 对象的任意索引位置时，只会得到某个数值，不会得到 ASCII 字符。