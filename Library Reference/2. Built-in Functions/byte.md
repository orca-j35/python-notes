# bytearray

*class* bytearray([*source*[, *encoding*[, *errors*]]])

该内置函数本质上是 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray) 类的构造函数，用于创建一个 bytearray 实例。bytearray 实例是一个由字节(8-bits 无符号)构成的可变序列，并拥有大多数可变序列的常见方法[详见：[Mutable Sequence Types](https://docs.python.org/3.7/library/stdtypes.html#typesseq-mutable)]，并且还包含 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 类型中的大多数方法[详见： [Bytes and Bytearray Operations](https://docs.python.org/3.7/library/stdtypes.html#bytes-methods) ]

在 Python 中，我们可以通过 bytes 字面值来创建 bytes 对象，但并没有用于创建 bytearray 字面值的语法，我们只能通过调用构造函数 `bytearray()` 来创建 bytearray 对象。

可选形参 *source* 用于初始化 bytearray，有以下几种方式：

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

- *source* 是一个由自然数构成的**可迭代对象**，且每个元素均小于256

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

  - *encoding* 参数用于设置编码方案，会被传递给 `str.encode()`。在 [Standard Encodings](https://docs.python.org/3.7/library/codecs.html#standard-encodings) 中可查看编码方案的列表。

  - *errors* 参数用于设置[错误处理方案](https://docs.python.org/3.7/library/codecs.html#error-handlers)，也会被传递给 `str.encode()`。如果 *errors* 为空，`str.encode()` 会使用默认方案 `'strict'`——该方案在出现编码错误时会抛出 [`UnicodeError`](https://docs.python.org/3.7/library/exceptions.html#UnicodeError)。*errors* 可以是 `'ignore'`, `'replace'`, `'xmlcharrefreplace'`, `'backslashreplace'` 或任何已通过 [`codecs.register_error()`](https://docs.python.org/3.7/library/codecs.html#codecs.register_error) 注册的名称。

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

Tips: 在 Python 文档中，"编码(encoding)"是指将 Unicode 字符串转换为字节序列的规则，也就是说"编码"包含了从"抽象字符序列"到"字节序列"的全部过程。

扩展阅读: [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3.7/library/stdtypes.html#binaryseq) 及 [Bytearray Objects](https://docs.python.org/3.7/library/stdtypes.html#typebytearray).

## 深入理解 bytearray 对象

在 C 语言中创建字节数组的语法如下：

```c
byte bytes_instance[] = {0x02, 0x03, 0x0A, 0x41}
```

Python 中的 bytearray 对象与 C 语言中的字节数组类似，它们的每个索引位置都对应一个整数 x (且 0≤x≤255)。不同之处在于 bytearray 对象会以转义序列或 ASCII 字符显示相应的整数值(如，会将十进制整数 65 显示为字母 A)，但是 bytearray 对象的每个索引位置都仅表示一个数值，而非一个字母。因此，bytearray 对象是一个实实在在的字节序列，每个索引位置对应一个字节(byte)而不是一个字符(char)。

下面创建一个与 C 字节数组拥有相同内容的 bytearray 对象

```python
>>> a_obj = bytearray((0x02, 0x03, 0x0A, 0x41))
>>> a_obj
bytearray(b'\x02\x03\nA')
>>> [ x for x in a_obj]
[2, 3, 10, 65]
```

显示为 ASCII 字符的好处在于，如果 bytearray 对象是一个 ASCII 编码的字节序列，那么便可直接读懂其中的内容，无需解码

```python
>>> hi = bytearray('hello!','ascii')
>>> hi
bytearray(b'hello!') # 虽然是字节序列，但是不用解码也读懂
>>> hi.decode('ascii')
'hello!'
```



不同之处在于 bytearray 对象的长度可变，同时拥有很多

在使用过程中，我们可将 bytearray 对象类比于 C 语言中的字节数组，如：

==在 bytes 字面值中，十六进制(`'\xhh'`)和八进制(`'\ooo'`)转义序列用于表示具有给定值的字节，`hh` 和 `ooo` 分别是十六进制和八进制的给定值。==



### 显示方式

在字符串字面值中，十六进制(`'\xhh'`)和八进制(`'\ooo'`)转义序列用于表示指定码点的 Unicode 字符(`hh` 以十六进制表示指定码点；`ooo` 以八进制表示指定码点)。也就是说，在字符串字面值中使用这两种转义序列的效果，与直接使用 Unicode 字符完全相同。

对于可见 Unicode 字符，这两种转义序列最终都会以 Unicode 字符表示；对于不可见 Unicode 字符，转义序列的最终表示方式分以下两种情况：

1. 如果"不可见字符"拥有独立的转义序列，最终会表示为该独立的转义序列
2. 如果没有独立的转义序列，最终会表示为十六进制转义序列





bytes就是一个字节序列





[`str`](https://docs.python.org/3/library/stdtypes.html#str) 对象用于处理 Python 中的文本数据。从技术上来说，字符串是由 Unicode 码点组成的不可变序列。因此，Unicode 字符的本质就是 Unicode 码点。











