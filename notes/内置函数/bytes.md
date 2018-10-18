# bytes

🔨 *class* bytes([*source*[, *encoding*[, *errors*]]])

该内置函数本质上是 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 类的构造函数，用于创建一个 bytes 实例。bytes 实例是一个由字节(8-bits 无符号)构成的不可变序列。可将 bytes 视作 [`bytearray`](https://docs.python.org/3.7/library/stdtypes.html#bytearray) 的不可变版本，但在 bytes 中不包含可对自身做出修改的方法 [详见： [Bytes and Bytearray Operations](https://docs.python.org/3.7/library/stdtypes.html#bytes-methods) ]。

参数 *source* 、*encoding* 、*errors*  在 `bytes()` 和 `bytearray()` 中以相同方式使用：

- 没有任何参数时，将创建一个空实例

  ```python
  # bytes() -> empty bytes object
  >>> bytes()
  b''
  ```

- *source* 是一个**整数**时，将创建一个长度为 *source* 且每个字节均为空的 bytes 对象

  ```python
  # bytes(int) -> bytes object of size given by the parameter initialized with null bytes
  >>> bytes(5)
  b'\x00\x00\x00\x00\x00'
  ```

- *source* 是一个由自然数构成的**可迭代对象**，且每个元素的值 x 均满足 0 ≤ x ≤ 255

  ```python
  # bytes(iterable_of_ints) -> bytes
  >>> bytes(range(5)) # 最大范围是range(256)
  b'\x00\x01\x02\x03\x04'
  >>> bytes([1,2,3,4,5])
  b'\x01\x02\x03\x04\x05'
  ```

- *source* 是一个 bytes 对象，将通过缓冲器协议(buffer protocol)复制其中的二进制数据

  ```python
  # bytes(bytes) -> mutable copy of bytes
  >>> bytes(b'Hi!')
  b'Hi!'
  ```

- *source* 是一个实现了缓冲区(buffer) API 的对象时，则会使用 *source* 的只读缓冲区来初始化 bytes 对象。

  ```python
  # bytes(buffer) -> mutable copy of buffer
  ```

- *source* 是一个字符串时，必须给定 *encoding* 参数。此时，构造函数 `bytes()`  会通过 [`str.encode()`](https://docs.python.org/3.7/library/stdtypes.html#str.encode) 方法将 *source* 编码(encoding)为字节序列。

  - *encoding* 参数用于设置编码方案，会被传递给 `str.encode()`。在 [Standard Encodings](https://docs.python.org/3.7/library/codecs.html#standard-encodings) 中可查看编码方案列表。
  - *errors* 参数用于设置[错误处理方案](https://docs.python.org/3.7/library/codecs.html#error-handlers)，也会被传递给 `str.encode()`。如果 *errors* 为空，`str.encode()` 会使用默认方案 `'strict'`——该方案在出现编码错误时会抛出 [`UnicodeError`](https://docs.python.org/3.7/library/exceptions.html#UnicodeError)。*errors* 可以是 `'ignore'`, `'replace'`, `'xmlcharrefreplace'`, `'backslashreplace'` 或任何已通过 [`codecs.register_error()`](https://docs.python.org/3.7/library/codecs.html#codecs.register_error) 注册的名称。

  Tips: 在 Python 文档中，"编码(encoding)"是指将 Unicode 字符串转换为字节序列的规则，也就是说"编码"包含了从"抽象字符序列"到"字节序列"的全部过程。

  ```python
  # bytes(string, encoding[, errors]) -> bytes
  >>> bytes('abcd','utf-8')
  b'abcd'
  >>> bytes('鲸','utf-8')
  b'\xe9\xb2\xb8'
  
  >>> bytes('鲸','ascii')
  Traceback (most recent call last):
    File "<pyshell#11>", line 1, in <module>
      bytes('鲸','ascii')
  UnicodeEncodeError: 'ascii' codec can't encode character '\u9cb8' in position 0: ordinal not in range(128)
  >>> bytes('鲸','ascii','ignore')
  b''
  ```

扩展阅读：[Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3.7/library/stdtypes.html#binaryseq), [Bytes Objects](https://docs.python.org/3.7/library/stdtypes.html#typebytes), and [Bytes and Bytearray Operations](https://docs.python.org/3.7/library/stdtypes.html#bytes-methods).

## 深入理解 bytes 对象

bytes 对象与 C 语言中的字节数组类似，**每个索引位置都对应一个整数 x (且 0≤x≤255)**。不同之处在于 bytes 对象会以转义序列或 ASCII 字符显示相应数值(如，将十进制整数 65 显示为字母 A)，但是 bytes 对象的每个索引位置仍然是一个数值，而非一个字符。bytes 对象是一个实实在在的**字节序列**，每个索引位置对应一个字节(byte)而不是一个字符(char)。在读取 bytes 对象的任意索引位置时，只会得到某个数值，不会得到 ASCII 字符。

为了便于理解，先创建一个 C 语言字节数组：

```c
byte bytes_array[] = {0x02, 0x03, 0x0A, 0x41}
```

创建一个与 C 语言字节数组拥有相同内容的 bytes 对象：

```python
>>> a_obj = b'\x02\x03\x0a\x41'
>>> a_obj
b'\x02\x03\nA' # 以转义序列或 ASCII 编码显示相应数值
>>> [ x for x in a_obj]
[2, 3, 10, 65] # 每个索引位置始终对应一个数值，而非一个字符
```

注意：不能将 bytes 完全等同于 C 的字符数组，因为 bytes 远比字符数组强大。

### 如何显示数值

如果某个索引位置的数值对应 ASCII 编码中的可见字符，那么该索引位便会显示该字符：

```python
>>> b'\x41\x42'
b'AB'
```

如果某个索引位置的数值对应 ASCII 编码中的不可见字符，但该字符拥有"独立转义序列"，那么该索引位置会显示该"独立转义序列"：

```python
>>> b'\x0A\x0D'
b'\n\r'
```

如果某个索引位置的数值对应 ASCII 编码中的不可见字符，并且该字符没有"独立转义序列"；或该数值已超出了 ASCII 编码的范围。那么该索引位置会显示十六进制(`'\xhh'`)转义序列。在 bytes 对象中，十六进制(`'\xhh'`)转义序列用于表示具有指定数值的字节。

```python
>>> b'\x01\xFE'
b'\x01\xfe'
```

将 bytes 对象中各个字节的数值，尽力按照 ASCII 编码显示为相应字符的好处是：如果 bytes 对象是一个 ASCII 编码的字节序列，那么便可直接读懂其中的内容，无需解码：

```python
>>> hi = bytes('hello!\n','ascii')
>>> hi
b'hello!\n' # 虽然是字节序列，但是不用解码也读懂
>>> hi.decode('ascii')
'hello!\n'
```

再次提醒：bytes 对象是一个实实在在的**字节序列**，每个索引位置对应一个数值而不是一个字符。在读取 bytes 对象的任意索引位置时，只会得到某个数值，不会得到 ASCII 字符。

### bytes 字面值

在 Python 中不仅可以通过 `bytes` 函数创建 bytes 对象，还可以通过 bytes 字面值来创建 bytes 对象[详见 [String and Bytes literals](https://docs.python.org/3.7/reference/lexical_analysis.html#strings)] ，如下：

```python
# 单引号
>>> b'still allows embedded "double" quotes' # 可直接使用ASCII字符表示相应数值
b'still allows embedded "double" quotes'
>>> b'\x01AB\n\r' # 可使用转义序列表示相应数值
b'\x01AB\n\r'
>>> b'\x01\x41\x42\x0A\x0D'
b'\x01AB\n\r'
# 双引号
>>> b"still allows embedded 'single' quotes"
b"still allows embedded 'single' quotes"
# 多重引号
>>> b'''3 single quotes'''
b'3 single quotes'
>>> b"""3 double quotes"""
b'3 double quotes'
```

bytes 字面值也支持使用 `r` 前缀来禁止处理转义序列。

```python
>>> rb'\x01AB\n\r'
b'\\x01AB\\n\\r'
>>> for i in br'\x01AB\n\r':print(hex(i))

0x5c # 对应ASCII字符 \ 的16进制值
0x78 # 对应 x
0x30 # 对应 0
0x31 # 对应 1
0x41 # 对应 A
0x42 # 对应 B
0x5c # 对应 \\
0x6e # 对应 n
0x5c # 对应 \\
0x72 # 对应 n
```

