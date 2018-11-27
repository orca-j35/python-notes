# open

🔨 open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

该函数用于打开 *file* 并返回相应的文件对象([file object](https://docs.python.org/3.7/glossary.html#term-file-object))，如果打开失败则抛出 [`OSError`](https://docs.python.org/3.7/library/exceptions.html#OSError)。

`open()` 函数其实是[`io.open()`](https://docs.python.org/3.7/library/io.html#io.open) 方法的别名。

## 参数说明

### *file*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*file* 用于设置需要打开的文件，有以下两种形式：

- 可以是一个表示**文件系统路径**(绝对路径或相对路径均可)的对象，即 [path-like](https://docs.python.org/3.7/glossary.html#term-path-like-object) 对象。该对象可以是文本字符串或 byte 字符串，也可是实现了 [`os.PathLike`](https://docs.python.org/3.7/library/os.html#os.PathLike) 协议的对象。

  ```python
  """./somefile.txt中的内容
  first line
  second line
  """
  fin = open(b'somefile.txt')
  print(fin.read())
  print(fin.fileno())  # fileno()会返回文件描述符
  fin.close()
  """Out:
  first line
  second line
  3
  """
  ```

- 还可以是一个**整型文件描述符**(*integer file descriptor*)，该描述符代表一个被打包(*wrapped*)的文件。如果给出了文件描述符，那么当我们关闭 `open()` 返回的 I/O 对象时，该文件描述符也将被关闭，除非将 *closefd* 设置为 `False`。

  ```python
  """./somefile.txt中的内容
  first line
  second line
  """
  import os
  # 使用底层IO打开一个文件，并返回其文件描述符(integer)
  fd = os.open('somefile.txt', os.O_RDONLY)
  print("文件描述符的值是 {0}，类型是 {1}".format(fd, type(fd)))
  f = open(fd, 'r')
  print(f.read())
  f.close()
  f = open(fd, 'r')
  # 文件描述符被关闭后不能再次被打开
  f = open(fd, 'r')
  """Out:
  文件描述符的值是 3，类型是 <class 'int'>
  first line
  second line
  Traceback (most recent call last):
    File "c:/Users/iwhal/Desktop/内置函数/BI_open.py", line 13, in <module>
      f = open(fd, 'r')
  OSError: [WinError 6] 句柄无效。
  """
  ```

  如果需要再次打开文件描述，则需将 *closefd* 设置为 `False`：

  ```python
  """./somefile.txt中的内容
  first line
  second line
  """
  import os
  fd = os.open('somefile.txt', os.O_RDONLY)
  f = open(fd, 'r', closefd=False)
  f.close()
  f = open(fd, 'r')
  print(f.read())
  """Out:
  first line
  second line
  """
  ```

  **扩展阅读**: 5.18 将文件描述符包装成文件对象 - Python Cookbook

### *mode*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*mode* 用于设定文件的打开模式，默认值是 `'rt'`，有如下可用模式：

| Character | Meaning                                                      |
| --------- | ------------------------------------------------------------ |
| `'r'`     | open for reading (default)                                   |
| `'w'`     | open for writing , truncating the file first <br />如果文件已存在，则会清空其现有内容；如果文件不存在，则会创建该文件 |
| `'x'`     | open for exclusive creation, failing if the file already exists<br />如果文件不存在，则会创建该文件，并默认以 `'wt'` 打开；如果文件已存在，则会抛出 `FileExistsError` |
| `'a'`     | open for writing, appending to the end of the file if it exists<br />在某些 Unix 系统中，这意味着所有写入都会被附加到文件的末尾，并且无视 seek 位置。 |
| `'b'`     | binary mode (以字节形式读写数据，用于不包含文本的所有文件)<br />在读写 raw bytes 时，需使用 binary 模式，并且不需要指定编码方式 |
| `'t'`     | text mode (default)<br />在文本模式下，如果未指定 *encoding*，则依赖平台的编码方式，即调用`locale.getpreferredencoding(False)` 来获取当前本地编码方式。 |
| `'+'`     | open a disk file for updating (reading and writing)          |
| `'U'`     | [universal newlines](https://docs.python.org/3.7/glossary.html#term-universal-newlines) mode (deprecated), Use newline to control universal newlines mode.<br />`'U'` 模式已被弃用，在未来的 Python 版本中将会引发异常。该模式在 Python 3 中无效。 |

对于二进制读写访问，`'w+b'` 会截断文件至 0 字节，而 `'r+b'` 不会截断文件，这两种模式都以 0 偏移量为起点。

如 `io` 模块中[概述](https://docs.python.org/3.7/library/io.html#overview)部分所言，Python 会区分 binary I/O 和 text I/O： (即使底层操作系统并不会区分这两者，Python 仍然会进行区别)

- 以 binary 模式( `'b'` )打开文件后：在读取文件时，会将文件中的内容以 `bytes` 对象返回，不会进行任何解码操作；在写入文件时，会将 `bytes` 对象直接写入文件，不会进行任何编码操作。在使用 binary 模式时，需保持 `encoding=None`。
- 以 text 模式( `'t'` )打开文件后：在读取文件时，会先对读取到的字节进行解码，再以 `str` 对象返回解码后的内容；在写入文件时，会先对被写入的 `str` 对象进行编码，再将通过编码得到的字节写入文件。在 text 模式下，如果未指定 *encoding*，则依赖平台的编码方案，即调用`locale.getpreferredencoding(False)` 来获取当前本地编码方案。

```python
with open('a_file.txt', 'r+b') as fin:
    # 在binary模式下直接向文件写入字节
    fin.write(b'orca_j35 ' + bytes('鲸', 'utf8'))
    fin.seek(0)
    # 读取之前写入的字节
    print(fin.read())

with open('a_file.txt', 'r+', encoding='utf8') as fin:
    # 在text模式下，会先对读取到的字节进行解码，再以字符串对象返回解码后的内容
    print(fin.read())
"""Out:
b'orca_j35 \xe9\xb2\xb8'
orca_j35 鲸
"""
```

注意：Python 不依赖于底层操作系统定义的文本文件的概念；所有处理都由 Python 本身完成，因此与平台无关。

### *buffering*

open(*file*, *mode='r'*, *buffering=-1*, *encoding=None*, *errors=None*, *newline=None*, *closefd=True*, *opener=None*)

*buffering* 用于设置缓冲策略(*buffering policy*)，可以是以下整数值：

- 0 to switch buffering off (only allowed in binary mode)
- 1 to select line buffering (only usable in text mode)
- an integer > 1 to indicate the size in bytes of a fixed-size chunk buffer

如果没有给出 *buffering* 参数，默认缓冲策略的工作方式如下：

- Binary files are buffered in fixed-size chunks; the size of the buffer is chosen using a heuristic trying to determine the underlying device’s “block size” and falling back on [`io.DEFAULT_BUFFER_SIZE`](https://docs.python.org/3.7/library/io.html#io.DEFAULT_BUFFER_SIZE). On many systems, the buffer will typically be 4096 or 8192 bytes long.
- “Interactive” text files (files for which [`isatty()`](https://docs.python.org/3.7/library/io.html#io.IOBase.isatty) returns `True`) use line buffering. Other text files use the policy described above for binary files.



When no buffering argument is
given, the default buffering policy works as follows:
​    

​    


在 Windows 下，默认的编码方式是 cp936：

```python
>>> import locale
>>> locale.getpreferredencoding(False)
'cp936'
```





## 术语

### file object

An object exposing a file-oriented API (with methods such as `read()` or `write()`) to an underlying resource. Depending on the way it was created, a file object can mediate access to a real on-disk file or to another type of storage or communication device (for example standard input/output, in-memory buffers, sockets, pipes, etc.). File objects are also called *file-like objects* or *streams*.

There are actually three categories of file objects: raw [binary files](https://docs.python.org/3.7/glossary.html#term-binary-file), buffered [binary files](https://docs.python.org/3.7/glossary.html#term-binary-file)and [text files](https://docs.python.org/3.7/glossary.html#term-text-file). Their interfaces are defined in the [`io`](https://docs.python.org/3.7/library/io.html#module-io) module. The canonical way to create a file object is by using the [`open()`](https://docs.python.org/3.7/library/functions.html#open) function.

### file-like object

A synonym for [file object](https://docs.python.org/3.7/glossary.html#term-file-object).

### path-like object

An object representing a file system path. A path-like object is either a [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) or [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes)object representing a path, or an object implementing the [`os.PathLike`](https://docs.python.org/3.7/library/os.html#os.PathLike) protocol. An object that supports the [`os.PathLike`](https://docs.python.org/3.7/library/os.html#os.PathLike) protocol can be converted to a [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) or [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) file system path by calling the [`os.fspath()`](https://docs.python.org/3.7/library/os.html#os.fspath) function; [`os.fsdecode()`](https://docs.python.org/3.7/library/os.html#os.fsdecode) and [`os.fsencode()`](https://docs.python.org/3.7/library/os.html#os.fsencode) can be used to guarantee a [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) or [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) result instead, respectively. Introduced by [**PEP 519**](https://www.python.org/dev/peps/pep-0519).

text file

A [file object](https://docs.python.org/3.7/glossary.html#term-file-object) able to read and write [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) objects. Often, a text file actually accesses a byte-oriented datastream and handles the [text encoding](https://docs.python.org/3.7/glossary.html#term-text-encoding) automatically. Examples of text files are files opened in text mode (`'r'` or `'w'`), [`sys.stdin`](https://docs.python.org/3.7/library/sys.html#sys.stdin), [`sys.stdout`](https://docs.python.org/3.7/library/sys.html#sys.stdout), and instances of[`io.StringIO`](https://docs.python.org/3.7/library/io.html#io.StringIO).

See also [binary file](https://docs.python.org/3.7/glossary.html#term-binary-file) for a file object able to read and write [bytes-like objects](https://docs.python.org/3.7/glossary.html#term-bytes-like-object).

