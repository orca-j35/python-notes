# io — Core tools for working with streams

> 本文仅提 io 模块的简要参考，如需了解详细信息请阅读：
>
> - [io — Core tools for working with streams](https://docs.python.org/3.7/library/io.html)
>
> 扩展阅读：
>
> - [io — Text, Binary, and Raw Stream I/O Tools](https://pymotw.com/3/io/index.html#wrapping-byte-streams-for-text-data)
> - [io — 文本、二进制和原生流的 I/O 工具](https://pythoncaff.com/docs/pymotw/io-io-tool-for-text-binary-and-native-streams/118#%E5%86%85%E5%AD%98%E6%B5%81)

`io` 模块的作用是提供处理各种 I/O 类型的工具。

`io` 模块为 Python 提供了处理各种 I/O 类型的主要工具。主要有三种 I/O 类型： *text I/O*, *binary I/O* 和 *raw I/O*。属于这些类别的具体对象被称为文件对象([file object](https://docs.python.org/3.7/glossary.html#term-file-object))。例如，`open()` 函数返回的对象便是文件对象，我们可以在 `io` 模块中查阅文件对象所支持的方法。

## Overview

### Text I/O

Text I/O expects and produces [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) objects. This means that whenever the backing store is natively made of bytes (such as in the case of a file), encoding and decoding of data is made transparently as well as optional translation of platform-specific newline characters.

The easiest way to create a text stream is with [`open()`](https://docs.python.org/3.7/library/functions.html#open), optionally specifying an encoding:

```
f = open("myfile.txt", "r", encoding="utf-8")
```

In-memory text streams are also available as [`StringIO`](https://docs.python.org/3.7/library/io.html#io.StringIO) objects:

```
f = io.StringIO("some initial text data")
```

The text stream API is described in detail in the documentation of [`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase).

### Binary I/O

Binary I/O (also called *buffered I/O*) expects [bytes-like objects](https://docs.python.org/3.7/glossary.html#term-bytes-like-object) and produces [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) objects. No encoding, decoding, or newline translation is performed. This category of streams can be used for all kinds of non-text data, and also when manual control over the handling of text data is desired.

The easiest way to create a binary stream is with [`open()`](https://docs.python.org/3.7/library/functions.html#open) with `'b'` in the mode string:

```
f = open("myfile.jpg", "rb")
```

In-memory binary streams are also available as [`BytesIO`](https://docs.python.org/3.7/library/io.html#io.BytesIO) objects:

```
f = io.BytesIO(b"some initial binary data: \x00\x01")
```

The binary stream API is described in detail in the docs of [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase).

Other library modules may provide additional ways to create text or binary streams. See [`socket.socket.makefile()`](https://docs.python.org/3.7/library/socket.html#socket.socket.makefile) for example.

### Raw I/O

Raw I/O (also called *unbuffered I/O*) is generally used as a **low-level building-block** for binary and text streams; it is rarely useful to directly manipulate a raw stream from user code. Nevertheless, you can create a raw stream by opening a file in binary mode with buffering disabled:

```
f = open("myfile.jpg", "rb", buffering=0)
```

The raw stream API is described in detail in the docs of [`RawIOBase`](https://docs.python.org/3.7/library/io.html#io.RawIOBase).

## High-level Module Interface

- io.DEFAULT_BUFFER_SIZE

  默认缓冲区尺寸

  An int containing the default buffer size used by the module’s buffered I/O classes.[`open()`](https://docs.python.org/3.7/library/functions.html#open) uses the file’s blksize (as obtained by [`os.stat()`](https://docs.python.org/3.7/library/os.html#os.stat)) if possible.

- io.open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

  内置函数 `open()` 的别名

- *exception* io.BlockingIOError

  内置 [`BlockingIOError`](https://docs.python.org/3.7/library/exceptions.html#BlockingIOError) 异常的兼容性别名。

- *exception* io.UnsupportedOperation

  该异常继承自 [`OSError`](https://docs.python.org/3.7/library/exceptions.html#OSError) 和 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError)，如果在流上调用不支持的操作，便会抛出该异常。

## 类层次结构

Class hierarchy

`io` 模块中，各个 I/O 类间的继承关系如下：

```
IOBase
|--RawIOBase
	|--FileIO
|--BufferedIOBase
	|--BytesIO
	|--BufferedReader
	|--BufferedWriter
	|--BufferedRandom
	|--BufferedRWPair
|--TextIOBase
	|--TextIOWrapper
	|--StringIO
```

下表总结了 `io` 模块所提供的抽象基类(ABC)：

| ABC                                                          | Inherits                                                     | Stub Methods                            | Mixin Methods and Properties                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | --------------------------------------- | ------------------------------------------------------------ |
| [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) |                                                              | `fileno`, `seek`, and `truncate`        | `close`, `closed`, `__enter__`, `__exit__`, `flush`, `isatty`, `__iter__`, `__next__`, `readable`, `readline`, `readlines`, `seekable`, `tell`, `writable`, and `writelines` |
| [`RawIOBase`](https://docs.python.org/3.7/library/io.html#io.RawIOBase) | [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) | `readinto` and`write`                   | Inherited [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) methods, `read`, and `readall` |
| [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase) | [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) | `detach`, `read`,`read1`, and `write`   | Inherited [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) methods, `readinto`, and `readinto1` |
| [`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase) | [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) | `detach`, `read`,`readline`, and`write` | Inherited [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) methods, `encoding`,`errors`, and `newlines` |

### I/O Base Classes

#### 📐 IOBase

class io.IOBase

`IOBase` 是所有 I/O 类的抽象基类，作用于字节流。没有公共构造函数。

- close()

- closed

- fileno() - 如果流存在，返回流的底层文件描述符(整数)。如果 IO 对象不使用文件描述符，则会抛出 [`OSError`](https://docs.python.org/3.7/library/exceptions.html#OSError)。

- flush()

- isatty() - Return `True` if the stream is interactive (i.e., connected to a terminal/tty device).

- readable()

- readline(*size=-1*)

- readlines(*hint=-1*) - 等效于 `list(f)` 

- seek(*offset*[, *whence*]) - 设置在流中位置

- seekable()

- tell() - 返回当前流位置，以字节为单位

- truncate(*size=None*) - 重置流的尺寸

- writable()

- writelines(*lines*) - 将一个由多行数据组成的列表写入到流中，不会添加行分隔符。

- `__del__`() - 用于销毁对象，`IOBase` 为该方法提供默认实现——调用实例的 `close()` 方法

#### 📐 RawIOBase

class io.RawIOBase

`RawIOBase` 是 raw binary I/O 基类，继承自 [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase)。没有公共构造函数。

除了 `IOBase` 的属性和方法之外，`RawIOBase` 还提供以下方法：

- read(*size=-1*)

- readall()

- readinto(*b*)

- write(*b*)

#### 📐 BufferedIOBase

class io.BufferedIOBase

支持缓冲区的 binary 流的基类，继承自 [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase)。没有公共构造函数。

A typical [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase) implementation should not inherit from a [`RawIOBase`](https://docs.python.org/3.7/library/io.html#io.RawIOBase)implementation, but wrap one, like [`BufferedWriter`](https://docs.python.org/3.7/library/io.html#io.BufferedWriter) and [`BufferedReader`](https://docs.python.org/3.7/library/io.html#io.BufferedReader) do.

除 `IOBase` 中的方法和属性外，`BufferedIOBase` 还提供或覆盖这些方法和属性：

- raw - 获取底层 raw 流

- detach() - 分离出 buffer 中的底层 raw 流，并返回该 raw 流。

- read(*size=-1*) 

- read1([*size*])

- readinto(*b*)

- readinto1(*b*)

- write(*b*)

### Raw File I/O

#### 📐 FileIO

🔨 *class* io.FileIO(*name*, *mode='r'*, *closefd=True*, *opener=None*)

[`FileIO`](https://docs.python.org/3.7/library/io.html#io.FileIO) 表示一个包含字节数据的 OS-level 文件，它实现了 [`RawIOBase`](https://docs.python.org/3.7/library/io.html#io.RawIOBase) 中接口(因此也实现了 `IOBase` 中的接口)

除了IOBase和RawIOBase的属性和方法之外，`FileIO` 还提供以下数据属性：

- mode - The mode as given in the constructor.

- name - The file name. This is the file descriptor of the file when no name is given in the constructor.

### Buffered Streams

Buffered I/O 流为 I/O 设备提供了比 raw I/O 更高级别的接口。

#### 📐 BytesIO

🔨 *class* io.BytesIO([*initial_bytes*])

> 相关文档：[In-memory Streams](https://pymotw.com/3/io/index.html#in-memory-streams) | [内存流](https://pythoncaff.com/docs/pymotw/io-io-tool-for-text-binary-and-native-streams/118#%E5%86%85%E5%AD%98%E6%B5%81)

该类继承自 [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase)，其构造器会在内存中创建一个 bytes I/O 流。在 [`BytesIO`](https://docs.python.org/3.7/library/io.html#io.BytesIO) 类的实例上调用 `close()` 方法时，将丢弃缓冲区中的数据。

*initial_bytes* 用于设置缓冲区的初始值，必须是一个  [bytes-like](https://docs.python.org/3.7/glossary.html#term-bytes-like-object) 对象，但即便置了初始值，在流中仍会以 0 偏移量为起点。

除了来自 [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase) 和 [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) 的方法之外，`BytesIO` 还提供或覆写如下方法：

- getbuffer() - 返回缓冲区中内容的可读写视图，而不是进行拷贝。如果改变视图中的内容，便会同步更新缓冲区的内容：

  ```python
  >>> b = io.BytesIO(b"abcdef")
  >>> view = b.getbuffer()
  >>> view[2:4] = b"56"
  >>> b.getvalue()
  b'ab56ef'
  ```

  Note: 只要视图存在，就无法调整 BytesIO 对象大小，也不能关闭 BytesIO 对象。

  New in version 3.2.

- getvalue()

  返回一个包含缓冲区中全部内容的 [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 对象。

- read1([*size*])

  在 [`BytesIO`](https://docs.python.org/3.7/library/io.html#io.BytesIO) 中，该方法相当于 [`read()`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase.read)。

  Changed in version 3.7: The *size* argument is now optional.

- readinto1(*b*)

  在 [`BytesIO`](https://docs.python.org/3.7/library/io.html#io.BytesIO) 中，该方法相当于 [`readinto()`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase.readinto)。

  New in version 3.5.

示例：

```python
>>> b_io = io.BytesIO(b'orca')
>>> b.read()
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    b.read()
ValueError: I/O operation on closed file.
>>> b_io.read()
b'orca'
>>> b_io.write('逆戟鲸'.encode('utf8'))
9
>>> b_io.getvalue()
b'orca\xe9\x80\x86\xe6\x88\x9f\xe9\xb2\xb8'
>>> b_io.close() # 使用完毕后，同样需要关闭
```

#### 📐 BufferedReader

*class* io.BufferedReader(*raw*, *buffer_size=DEFAULT_BUFFER_SIZE*)

该类提供了对 [`RawIOBase`](https://docs.python.org/3.7/library/io.html#io.RawIOBase) 对象的更高级别的访问，继承自 [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase)。
`io.BufferedReader()` 构造器将基于给定的 *raw* 流和 *buffer_size* 创建一个 [`BufferedReader`](https://docs.python.org/3.7/library/io.html#io.BufferedReader) 实例。如果省略 *buffer_size* 参数，则默认使用 [`DEFAULT_BUFFER_SIZE`](https://docs.python.org/3.7/library/io.html#io.DEFAULT_BUFFER_SIZE)。

除了来自 [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase) 和 [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) 的方法之外，[`BufferedReader`](https://docs.python.org/3.7/library/io.html#io.BufferedReader)还提供或覆写了如下方法：

- peek([*size*]) - 偷看指定长度的字节

- read([*size*]) - 读取指定长度的字节

- read1([*size*]) 

#### 📐 BufferedWriter

*class* io.BufferedWriter(*raw*, *buffer_size=DEFAULT_BUFFER_SIZE*)

除了来自 [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase) 和 [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) 的方法之外，`BufferedWriter`还提供或覆写了如下方法：

- flush()

- write(*b*)

#### 📐 BufferedRandom

*class* io.BufferedRandom(*raw*, *buffer_size=DEFAULT_BUFFER_SIZE*)

A buffered interface to random access streams. It **inherits** [`BufferedReader`](https://docs.python.org/3.7/library/io.html#io.BufferedReader) and [`BufferedWriter`](https://docs.python.org/3.7/library/io.html#io.BufferedWriter), and further supports `seek()` and `tell()` functionality.

#### 📐 BufferedRWPair

*class* io.BufferedRWPair(*reader*, *writer*, *buffer_size=DEFAULT_BUFFER_SIZE*)

A buffered I/O object combining two unidirectional [`RawIOBase`](https://docs.python.org/3.7/library/io.html#io.RawIOBase) objects – one readable, the other writeable – into a single bidirectional endpoint. It inherits [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase).

### Text I/O

#### 📐 TextIOBase

*class* io.TextIOBase

> 相关文档：[TextIOBase](https://docs.python.org/3.7/library/io.html#io.TextIOBase)

`TextIOBase` 是文本流的基类，继承自 [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase)，没有公共构造函数，其作用是为 I/O 流提供基于字符和行的接口。该类没有 `readinto()` 方法，因为 Python 的字符串是不可变类型。

除了来自 [`IOBase`](https://docs.python.org/3.7/library/io.html#io.IOBase) 的数据属性和方法之外，[`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase) 还提供或覆写了如下数据属性和方法：

- encoding - 查看编码方案的名称

- errors - 查看错误处理方案

- newlines

- buffer - [`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase) 对应的底层 binary 缓冲区

- detach() - 分离出 `TextIOBase` 中的底层 binary 缓冲区，并返回该缓冲区。分离底层缓冲区后，`TextIOBase` 将处于不可用状态。某些 `TextIOBase` 实现(如 `StringIO`)可能没有底层缓冲区的概念，调用此方法将抛出 `UnsupportedOperation`。

- read(*size=-1*) - 从流中读取最多 *size* 个字符并作为单个 str 对象返回。如果 *size* 为负或 `None`，则读取至 EOF 为止。在读取文件时，如果文件内容两倍于机器的内存，则会出现问题。在文末重复读取时，会返回空字符 `''`。

- readline(*size=-1*) - 阅读直到换行符或 EOF，并作为单个 str 对象返回。如果流已经位于 EOF，则返回空字符串。如果指定了大小，则将读取最多 *size* 个字符。在文末重复读取时，会返回空字符 `''`。

- seek(*offset*[, *whence*]) - 将流位置更改为给定的偏移量。行为取决于 *whence* 参数。*whence* 的默认值是 `SEEK_SET`。

- tell() - 将当前流位置返回为不透明数字。该数字通常不代表底层二进制存储中的多个字节。

- write(*s*) - 将字符串 *s* 写入流并返回写入的字符数。

#### 📐 TextIOWrapper

🔨 *class* io.TextIOWrapper(*buffer*, *encoding=None*, *errors=None*, *newline=None*, *line_buffering=False*, *write_through=False*)

> 相关文档：[io.TextIOWrapper](https://docs.python.org/3.7/library/io.html#io.BufferedRWPair) | [Wrapping Byte Streams for Text Data](https://pymotw.com/3/io/index.html#wrapping-byte-streams-for-text-data) | [包装文本数据的字节流](https://pythoncaff.com/docs/pymotw/io-io-tool-for-text-binary-and-native-streams/118#%E5%86%85%E5%AD%98%E6%B5%81)

A buffered text stream over a [`BufferedIOBase`](https://docs.python.org/3.7/library/io.html#io.BufferedIOBase) binary stream. It inherits [`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase).

`TextIOWrapper` 类的实例同时支持读写操作。 

```python
import io

# 写入一个缓冲区
output = io.BytesIO()
# 将output用作二进制流
wrapper = io.TextIOWrapper(
    output,
    encoding='utf-8',
    write_through=True,
)
wrapper.write('This goes into the buffer. ')
wrapper.write('ÁÇÊ')

# 获取写入的值
print(output.getvalue())

output.close()  # discard buffer memory

# 初始化一个读缓冲区
input = io.BytesIO(
    b'Inital value for read buffer with unicode characters ' +
    'ÁÇÊ'.encode('utf-8')
)
wrapper = io.TextIOWrapper(input, encoding='utf-8')

# 读取缓冲池
print(wrapper.read())
'''Out:
b'This goes into the buffer. \xc3\x81\xc3\x87\xc3\x8a'
Inital value for read buffer with unicode characters ÁÇÊ
'''
```

在 `TextIOWrapper` 中，除包含 [`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase) 及其父类中的方法之外，还提供下述成员：

- line_buffering - 是否启用了行缓冲

- write_through - 是否立即将写入的数据传递至底层二进制缓冲区。

- reconfigure(**\[, encoding\]\[, errors\]\[, newline\]\[, line_buffering\]\[, write_through\]*) 

  重新配置 text 流的各个参数( *encoding*, *errors*, *newline*, *line_buffering*, *write_through*)，未设置的参数保持当前值。如果设置了 *encoding* 但没有设置 *errors*，则  `errors='strict`。如果已从流中读取了某些数据，则无法更改编码或换行符。另一方面，可以在写入之后改变编码。此方法在设置新参数之前会隐式执行流刷新。

  New in version 3.7.

#### 📐 StringIO

🔨 *class* io.StringIO(*initial_value=''*, *newline='\n'*)

> 相关文档：[In-memory Streams](https://pymotw.com/3/io/index.html#in-memory-streams) | [内存流](https://pythoncaff.com/docs/pymotw/io-io-tool-for-text-binary-and-native-streams/118#%E5%86%85%E5%AD%98%E6%B5%81)

该构造器会在内存中创建一个 text I/O 流。在 [`StringIO`](https://docs.python.org/3.7/library/io.html#io.StringIO) 类的实例上调用 `close()` 方法时，将丢弃文本缓冲区中的数据。相较于其它字符串连接技术，通过 `StringIO` 构建大型字符串时性能更有益。

**参数说明**：

- *initial_value* 用于设置缓冲区的初始值，但即便置了初始值，在流中仍会以 0 偏移量为起点
- *newline* 用于设置是否启用换行符转换，其工作方式与 [`TextIOWrapper`](https://docs.python.org/3.7/library/io.html#io.TextIOWrapper) 的同名参数一致，具体行为可参考本笔记的「参数说明.*newline*」小节

在 `StringIO` 中，除包含 [`TextIOBase`](https://docs.python.org/3.7/library/io.html#io.TextIOBase) 及其父类中的方法之外，还提供下述方法：

- getvalue() - 返回一个包含缓冲区中全部内容的 str 对象。换行符的处理方式依赖于 *newline* 参数，具体行为可参考本笔记的「参数说明.*newline*」小节

示例：

```python
import io
output = io.StringIO()
output.write('First line.\n')
print('Second line.', file=output)

# Retrieve file contents -- this will be
# 'First line.\nSecond line.\n'
contents = output.getvalue()

# Close object and discard memory buffer --
# .getvalue() will now raise an exception.
output.close() # 使用完毕后，同样需要关闭
```

