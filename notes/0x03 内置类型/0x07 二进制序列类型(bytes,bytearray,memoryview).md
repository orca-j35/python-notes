# 二进制序列类型(bytes, bytearray, memoryview)

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库。
>
> 本笔记涵盖了 [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3.7/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview) 中的内容，并进行了扩展。

[bytes](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray) 是用于操纵二进制数据的核心内置类型。[bytes](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray) 由 [memoryview](https://docs.python.org/3.7/library/stdtypes.html#memoryview) 提供支持，memoryview 使用缓冲区协议([buffer protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects))访问来访问其它二进制对象的内存，且无需拷贝。

[array](https://docs.python.org/3.7/library/array.html#module-array) 模块支持存储基本数据类型，如 32-bit 整数和 IEEE754 双精度浮点值。



## Memory Views

> 扩展阅读:
>
> - 「流畅的 Python」-> 2.9.2 内存视图
> - [`array`](https://docs.python.org/3.7/library/array.html#module-array) — Efficient arrays of numeric values
>   - [array — 序列化的固定类型结构](https://pythoncaff.com/docs/pymotw/the-fixed-type-structure-of-array-serialization/83)
> - [`struct`](https://docs.python.org/3.7/library/struct.html#module-struct) — Interpret bytes as packed binary data
>   - [struct — 二进制数据结构](https://pythoncaff.com/docs/pymotw/struct-binary-data-structure/87)
> - [求解释一下python中bytearray和memoryview 的使用 以及适用的场景](https://segmentfault.com/q/1010000007137721)
> - [【Python】内存视图（操作数据共享内存）](https://blog.csdn.net/gx864102252/article/details/80875094)
> - https://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/
> - https://legacy.python.org/dev/peps/pep-3118/

内存视图([*memoryview*](https://docs.python.org/3.7/library/stdtypes.html#memoryview))对象允许 Python 代码访问支持缓冲区协议([*buffer* protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects))的对象的内部数据。

🔨*class* memoryview(*obj*)

该函数会创建一个引用自 *obj* 的内存视图对象。*obj* 必须支持缓冲区协议([*buffer* *protocol*](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects))。支持缓冲区协议的内置对象有 [bytes](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray)。[bytes](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray) 由 [memoryview](https://docs.python.org/3.7/library/stdtypes.html#memoryview) 提供支持，内存视图使用缓冲区协议([buffer protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects))访问来访问其它二进制对象的内存，且无需拷贝。

示例 - 使用内存视图对象修改一个短整型有符号整数数组的数据。

```python
from array import array

numbers = array('h', [-2, -1, 0, 1, 2]) # 'h'表示signed short
memv = memoryview(numbers) 
len(memv) #> 5
# 转换成列表形式
memv.tolist() #> [-2, -1, 0, 1, 2]
# 转换成无符号字符类型
memv_oct = memv.cast('B')       
memv_oct.tolist() #> [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
# 修改第3个元素的高位字段
memv_oct[5] = 4                 
numbers #> array('h', [-2, -1, 1024, 1, 2])
```

内存视图对象有元素(*element*)概念，元素是指由原始对象 *obj* 处理的原子存储单元(*atomic* *memory* *unit*)。对于许多简单类型(如 bytes 和 bytearray)而言，一个元素就是一个字节，但是其它类型(如  [array.array](https://docs.python.org/3.7/library/array.html#array.array) )的元素可能会用于更大的尺寸。

`len(view)` 等于 [`tolist`](https://docs.python.org/3.7/library/stdtypes.html#memoryview.tolist) 的长度。如果 `view.ndim = 0`，那么长度等于 1；如果 `view.ndim = 1`，那么长度等于视图中元素的个数；对于更高的维度，长的等于视图的嵌套列表表示的长度。[`itemsize`](https://docs.python.org/3.7/library/stdtypes.html#memoryview.itemsize) 属性用于给出单个元素的字节数。

内存视图支持切片和索引以便显示数据。一维切片将产生子视图：

```python
v = memoryview(b'abcefg')
v #> <memory at 0x0000029799EF5108>
v[1] #> 98
v[-1] #> 103
v[1:4] #> <memory at 0x0000029799EF5288>
bytes(v[1:4]) #> b'bce'
```

如果 [`format`](https://docs.python.org/3.7/library/stdtypes.html#memoryview.format) 是来自 [`struct`](https://docs.python.org/3.7/library/struct.html#module-struct) 模块的原生格式说明符之一，那么还支持使用整数或整数元组进行索引，并返回具有正确类型的单个元素。一维内存视图可使用一个整数或一个整数元组进行索引。多维内存视图可以使用 *ndim* 整数的元组进行索引，其中ndim 是维数。可以使用空元组索引零维存内存视图。

Here is an example with a non-byte format:

```python
>>> import array
>>> a = array.array('l', [-11111111, 22222222, -33333333, 44444444])
>>> m = memoryview(a)
>>> m[0]
-11111111
>>> m[-1]
44444444
>>> m[::2].tolist()
[-11111111, -33333333]
```

如果底层对象可写，那么内存视图支持一维切片复制，但不允许调整大小：

```python
>>> data = bytearray(b'abcefg')
>>> v = memoryview(data)
>>> v.readonly
False
>>> v[0] = ord(b'z')
>>> data
bytearray(b'zbcefg')
>>> v[1:4] = b'123'
>>> data
bytearray(b'z123fg')
>>> v[2:3] = b'spam'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: memoryview assignment: lvalue and rvalue have different structures
>>> v[2:6] = b'spam'
>>> data
bytearray(b'z1spam')
```

具备 ‘B’, ‘b’,  ‘c’ 格式的可哈希 hashable (read-only)类型的一维内存视图同样 hashable。哈希定义为 `hash(m) == hash(m.tobytes())`：

```python
>>> v = memoryview(b'abcefg')
>>> hash(v) == hash(b'abcefg')
True
>>> hash(v[2:4]) == hash(b'ce')
True
>>> hash(v[::-2]) == hash(b'abcefg'[::-2])
True
```

Changed in version 3.3: One-dimensional memoryviews can now be sliced. One-dimensional memoryviews with formats ‘B’, ‘b’ or ‘c’ are now hashable.

Changed in version 3.4: memoryview is now registered automatically with[`collections.abc.Sequence`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Sequence)

Changed in version 3.5: memoryviews can now be indexed with tuple of integers.

### a. 方法属性

> 详见 [Memory Views](https://docs.python.org/3.7/library/stdtypes.html#memory-views) 中介绍方法的部分。

- `__eq__`(*exporter*)
- `tobytes`() 
- `hex`()
- `tolist`()
- `release`()
- `cast`(*format*[, *shape*]) - 将内存视图转换为新格式或形状。

### b. 字段属性

> 详见 [Memory Views](https://docs.python.org/3.7/library/stdtypes.html#memory-views) 中介绍字段的部分。

- `obj` - 内存视图的底层对象

- `nbytes` - `nbytes == product(shape) * itemsize == len(m.tobytes())`，数组使用的空间(以字节为单位)

- `readonly` - 一个布尔值，表示内存是否只读

- `format` - 一个字符串，表示视图中每个元素的格式( [`struct`](https://docs.python.org/3.7/library/struct.html#module-struct) 模块的样式)。

- `itemsize` - 内存视图中的每个元素的尺寸(以字节为单位)：

- `ndim` - 一个整数，表示内存代表的多维数组的维数，

- `shape` - 内存视图的形状，一个由整数组成的数组，从左至右依次表示多维数组每一层的维数 `ndim`：

  ```python
  import numpy as np
  a = np.array([1,2,3], dtype=int)  
  # 创建1*3维数组 array([1,2,3])
  a.shape  #> (3,)
  b=np.array([[1,2,3],[4,5,6]],dtype=int)  
  # 创建2*3维数组  array([[1,2,3],[4,5,6]])
  b.shape  #> (2, 3)
  c=np.array([[1,2,3],[4,5,6],[4,5,6],[4,5,6]],dtype=int)
  c.shape #> (4, 3)
  ```

  Changed in version 3.3: An empty tuple instead of `None` when ndim = 0.

  参考：[python中的矩阵、多维数组----numpy](https://www.cnblogs.com/xzcfightingup/p/7598293.html)

- `strides` - 一个由整数组成的数组，从左至右依次表示多维数组每一层的尺寸(以字节为单位)

  ```python
  import numpy as np
  a = np.array([1,2,3], dtype=int)  
  a.itemsize #> 4
  a.strides #> (4,)
  b=np.array([[1,2,3],[4,5,6]],dtype=int)  
  b.strides #> (12, 4)
  c=np.array([[1,2,3],[4,5,6],[4,5,6],[4,5,6]],dtype=int)
  c.shape #> (12, 4)
  ```

  Changed in version 3.3: An empty tuple instead of `None` when ndim = 0.

  参考：[python中的矩阵、多维数组----numpy](https://www.cnblogs.com/xzcfightingup/p/7598293.html)

- `suboffsets` - Used internally for PIL-style arrays. The value is informational only.

- `c_contiguous` - 布尔值，表示内存是否是 C 连续([contiguous](https://docs.python.org/3.7/glossary.html#term-contiguous))。

- `f_contiguous` - 布尔值，表示内存是否是 Fortran  连续([contiguous](https://docs.python.org/3.7/glossary.html#term-contiguous))。

- `contiguous` - 布尔值，表示内存是否连续([contiguous](https://docs.python.org/3.7/glossary.html#term-contiguous))。



