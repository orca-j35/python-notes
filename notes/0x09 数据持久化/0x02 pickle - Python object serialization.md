# pickle - Python object serialization
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) — Python object serialization
> - https://pymotw.com/3/pickle/index.html 🧀
> - https://codingpy.com/books/thinkpython2/14-files.html
>
> 扩展阅读:
>
> - Module [`copyreg`](https://docs.python.org/3/library/copyreg.html#module-copyreg) - Pickle interface constructor registration for extension types.
> - Module [`pickletools`](https://docs.python.org/3/library/pickletools.html#module-pickletools) - Tools for working with and analyzing pickled data.
> - Module [`shelve`](https://docs.python.org/3/library/shelve.html#module-shelve) - Indexed databases of objects; uses [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle).
> - Module [`copy`](https://docs.python.org/3/library/copy.html#module-copy) - Shallow and deep object copying.
> - Module [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal) - High-performance serialization of built-in types.



## 概述

`pickle` 模块实现了多种用于序列化(*serializing*) Python 对象的二进制协议，并支持逆序列化(*de-serializing*)操作:

- pickling 是指将 Python 对象的层次结构转换为字节流的过程，
- unpickling 是 pickling 的反向操作，用于将字节流(来自 [binary file](https://docs.python.org/3/glossary.html#term-binary-file) 或 [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object))转换为 Python 对象。


在其它编程语言中，pickling/unpickling 也被称为 serialization、marshalling、flattening。为了避免术语之间的混淆，本文将使用术语 pickling 和 unpickling。

> ⚠ The [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) module is not secure against erroneous or maliciously constructed data. Never unpickle data received from an untrusted or unauthenticated source.
>
> In fact, unpickling data can execute arbitrary code. Be careful using `pickle` for inter-process communication or data storage, and do not trust data that cannot be verified as secure. See the [`hmac`](https://pymotw.com/3/hmac/index.html#module-hmac) module for an example of a secure way to verify the source of a pickled data source.



## 类似模块

### vs. marshal

在 Python 中还有一个更原始的序列化模块: [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal)。一般来说 `pickle` 应该是序列化 Python 对象的首选方案。`marshal` 主要用于支持 Python 的 `.pyc` 文件。

> `pickle` 和 `marshal` 主要存在以下区别:
>
> - The [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) module keeps track of the objects it has already serialized, so that later references to the same object won’t be serialized again. [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal) doesn’t do this.
>
>   This has implications both for recursive objects and object sharing. Recursive objects are objects that contain references to themselves. These are not handled by marshal, and in fact, attempting to marshal recursive objects will crash your Python interpreter. Object sharing happens when there are multiple references to the same object in different places in the object hierarchy being serialized. [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) stores such objects only once, and ensures that all other references point to the master copy. Shared objects remain shared, which can be very important for mutable objects.
>
> - [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal) cannot be used to serialize user-defined classes and their instances. [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle)can save and restore class instances transparently, however the class definition must be importable and live in the same module as when the object was stored.
>
> - The [`marshal`](https://docs.python.org/3/library/marshal.html#module-marshal) serialization format is not guaranteed to be portable across Python versions. Because its primary job in life is to support `.pyc` files, the Python implementers reserve the right to change the serialization format in non-backwards compatible ways should the need arise. The [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) serialization format is guaranteed to be backwards compatible across Python releases provided a compatible pickle protocol is chosen and pickling and unpickling code deals with Python 2 to Python 3 type differences if your data is crossing that unique breaking change language boundary.

### vs. JSON

pickle 协议和 [JSON (JavaScript Object Notation)](http://json.org/) 主要存在以下区别:

- JSON 是一种文本序列化格式(*text* *serialization* *format*)，输出结果是 Unicode 文本(在大多数时候 Unicode 文本会被编码为 UTF-8)；pickle 是一种二进制序列化格式(*binary* *serialization* format)，输出结果是二进制数据。
- JSON 的输出结果人类可读，pickle 的输出结果人类不可读。
- JSON 是可互操作的，并且在 Python 生态系统之外广泛使用，而 pickle 只能在 Python 中使用。
- 默认情况下，JSON 仅支持部分 Python 内置类型，并不支持自定义类；pickle 支持任意 Python 类型 (many of them automatically, by clever usage of Python’s introspection facilities; complex cases can be tackled by implementing [specific object APIs](https://docs.python.org/3/library/pickle.html#pickle-inst)).

扩展阅读: [`json`](https://docs.python.org/3/library/json.html#module-json) 模块

## 数据流格式

`pickle` 使用 Python 特定的数据流格式(*data* *stream* *format*)，这样做的优点是没有外部标准强加的限制，例如 JSON 或 XDR (which can’t represent pointer sharing)，缺点是非 Python 程序无法对 pickling 结果进行逆序列化。

默认情况下 `pickle` 数据格式会使用相对紧凑的二进制表示。如果你需要最佳的尺寸特征，则可以对 pickle 数据进行[压缩](https://docs.python.org/3/library/archiving.html)。

可使用 [`pickletools`](https://docs.python.org/3/library/pickletools.html#module-pickletools) 模块中的工具来分析 pickle 生成的数据流。[`pickletools`](https://docs.python.org/3/library/pickletools.html#module-pickletools) 源码包含很多对 pickle 协议所用 opcodes 的注释。

### 协议版本

目前有 5 种不同的 pickle 协议，协议版本数字越大，所需 Python 版本越新:

- 协议版本 0 是最初的版本，该版本"人类可读"，并且向后兼容早期版本的 Python

- 协议版本 1 是旧的二进制格式，它也与早期版本的Python兼容。

- 协议版本 2 (在 Python 2.3 中被引入)，为[新式类](https://docs.python.org/3/glossary.html#term-new-style-class)提供了更高效的 pickle 协议。有关协议 2 的改进信息，请参考 [**PEP 307**](https://www.python.org/dev/peps/pep-0307)。

- 协议版本 3 (在 Python 3 中被引入，默认协议版本)，该版本显式支持 `bytes` 对象，并且与 Python 2.x 不兼容。协议 3 是默认协议，当需要兼容其它 Python 3 版本时，推荐使用该协议。

- 协议版本 4 (在 Python 3.4 中被引入)，改进如下:

  - support for very large objects
  - pickling more kinds of objects
  - some data format optimizations

  有关协议 4 的改进的信息，请参考 [**PEP 3154**](https://www.python.org/dev/peps/pep-3154)。

> ⚠ Serialization is a more primitive notion than persistence; although [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) reads and writes file objects, it does not handle the issue of naming persistent objects, nor the (even more complicated) issue of concurrent access to persistent objects. The [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle)module can transform a complex object into a byte stream and it can transform the byte stream into an object with the same internal structure. Perhaps the most obvious thing to do with these byte streams is to write them onto a file, but it is also conceivable to send them across a network or store them in a database. 

 [`shelve`](https://docs.python.org/3/library/shelve.html#module-shelve) 模块为在 DBM-style 数据库文件中 pickle 和 unpickle 对象提供了一个简单的接口。

## 性能

新版的 pcikle 协议(protocol 2 及之后的协议)具有针对若干常见功能和内置类型的高效二进制编码。此外，pickle 模块有一个用 C 编写的透明优化器。

示例 - 对于简单的代码可使用 `dump()` 和 `load()` 函数:

```python
import pickle

# An arbitrary collection of objects supported by pickle.
data = {
    'a': [1, 2.0, 3, 4+6j],
    'b': ("character string", b"byte string"),
    'c': {None, True, False}
}

with open('data.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
```

示例 - 从文件中读取二进制数据，并 unpickle:

```python
import pickle

with open('data.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)
```

## 循环引用

pickle 协议会自动处理对象之间的循环引用，即使是复杂的数据结构也不需要做任何特殊处理。在下面这张图中包含了多个循环引用，pickle 可以正确处理这种结构。

![digraph pickle_example {   "root";   "root" -> "a";   "root" -> "b";   "a" -> "b";   "b" -> "a";   "b" -> "c";   "a" -> "a"; }](0x02 pickle - Python object serialization.assets/graphviz-6918aca85154b5d4f11d0d7f943c1305a3b781d7.png)

示例代码:

```python
# pickle_cycle.py
import pickle


class Node:
    """A simple digraph
    """
    def __init__(self, name):
        self.name = name
        self.connections = []

    def add_edge(self, node):
        "Create an edge between this node and the other."
        self.connections.append(node)

    def __iter__(self):
        return iter(self.connections)


def preorder_traversal(root, seen=None, parent=None):
    """Generator function to yield the edges in a graph.
    """
    if seen is None:
        seen = set()
    yield (parent, root)
    if root in seen:
        return
    seen.add(root)
    for node in root:
        recurse = preorder_traversal(node, seen, root)
        for parent, subnode in recurse:
            yield (parent, subnode)


def show_edges(root):
    "Print all the edges in the graph."
    for parent, child in preorder_traversal(root):
        if not parent:
            continue
        print('{:>5} -> {:>2} ({})'.format(
            parent.name, child.name, id(child)))


# Set up the nodes.
root = Node('root')
a = Node('a')
b = Node('b')
c = Node('c')

# Add edges between them.
root.add_edge(a)
root.add_edge(b)
a.add_edge(b)
b.add_edge(a)
b.add_edge(c)
a.add_edge(a)

print('ORIGINAL GRAPH:')
show_edges(root)

# Pickle and unpickle the graph to create
# a new set of nodes.
dumped = pickle.dumps(root)
reloaded = pickle.loads(dumped)

print('\nRELOADED GRAPH:')
show_edges(reloaded)
```

The reloaded nodes are not the same object, but the relationship between the nodes is maintained and only one copy of the object with multiple references is reloaded. Both of these statements can be verified by examining the `id()` values for the nodes before and after being passed through pickle.

```python
$ python3 pickle_cycle.py

ORIGINAL GRAPH:
 root ->  a (4315798272)
    a ->  b (4315798384)
    b ->  a (4315798272)
    b ->  c (4315799112)
    a ->  a (4315798272)
 root ->  b (4315798384)

RELOADED GRAPH:
 root ->  a (4315904096)
    a ->  b (4315904152)
    b ->  a (4315904096)
    b ->  c (4315904208)
    a ->  a (4315904096)
 root ->  b (4315904152)
```



## 模块接口

`dumps()` 用于将 Python 对象序列化为数据流，`loads()` 用于将数据流中逆序列化为 Python 对象。如果需要在序列化和逆序列化的过程中进行更多控制，可使用 [`Pickler`](https://docs.python.org/3/library/pickle.html#pickle.Pickler) 或 [`Unpickler`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler) 对象。

### 常量

#### HIGHEST_PROTOCOL🔧

🔧pickle.HIGHEST_PROTOCOL

整数，可用的最高 pickle [协议版本](#协议版本)。

> This value can be passed as a *protocol* value to functions [`dump()`](https://docs.python.org/3/library/pickle.html#pickle.dump) and [`dumps()`](https://docs.python.org/3/library/pickle.html#pickle.dumps) as well as the [`Pickler`](https://docs.python.org/3/library/pickle.html#pickle.Pickler) constructor.

#### DEFAULT_PROTOCOL🔧

🔧pickle.DEFAULT_PROTOCOL

整数，默认 pickle [协议版本](#协议版本)。

> May be less than [`HIGHEST_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.HIGHEST_PROTOCOL). Currently the default protocol is 3, a new protocol designed for Python 3.

### 函数

#### dump()🔨

🔨pickle.dump(*obj*, *file*, *protocol=None*, *\**, *fix_imports=True*)

将 *obj* 对象的 pickle 结果写入到打开的文件对象 *file* 中，等效于 `Pickler(file, protocol).dump(obj)`。

参数说明:

- The optional *protocol* argument, an integer, tells the pickler to use the given protocol; supported protocols are 0 to [`HIGHEST_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.HIGHEST_PROTOCOL). If not specified, the default is [`DEFAULT_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.DEFAULT_PROTOCOL). If a negative number is specified, [`HIGHEST_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.HIGHEST_PROTOCOL) is selected.
- The *file* argument must have a write() method that accepts a single bytes argument. It can thus be an on-disk file opened for binary writing, an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) instance, or any other custom object that meets this interface.
- If *fix_imports* is true and *protocol* is less than 3, pickle will try to map the new Python 3 names to the old module names used in Python 2, so that the pickle data stream is readable with Python 2.

`dump()` 和 `load()` 需配合 file-like 流使用，`dump()` 用于将多个对象 pickle 至 file-like 流中，`load()` 用于从 file-like 流中 unpickle 出 Python 对象。从 file-like 流中 unpickle 对象时，无需事先知道 file-like 流中的二进制数据包含多少个 Python 对象:

```python
import io
import pickle
import pprint


class SimpleObject:
    def __init__(self, name):
        self.name = name
        self.name_backwards = name[::-1]
        return


data = []
data.append(SimpleObject('pickle'))
data.append(SimpleObject('preserve'))
data.append(SimpleObject('last'))

# Simulate a file.
out_s = io.BytesIO()

# Write to the stream
for o in data:
    print('WRITING : {} ({})'.format(o.name, o.name_backwards))
    pickle.dump(o, out_s)
    out_s.flush()

# Set up a read-able stream
in_s = io.BytesIO(out_s.getvalue())

# Read the data
while True:
    try:
        o = pickle.load(in_s)
    except EOFError:
        break
    else:
        print('READ    : {} ({})'.format(o.name, o.name_backwards))
```

输出:

```
WRITING : pickle (elkcip)
WRITING : preserve (evreserp)
WRITING : last (tsal)
READ    : pickle (elkcip)
READ    : preserve (evreserp)
READ    : last (tsal)
```

某些简单的数据库格式也可以使用 pickle 来存储对象，比如 [`shelve`](https://pymotw.com/3/shelve/index.html#module-shelve)

pickle 不仅可用于存储数据，还可用于进程间通讯。例如 `os.fork()` 和 `os.pip()` 可用于建立从一个管道(*pipe*)读取工作指令的工作进程，并将结果写入另一个管道:

> The core code for managing the worker pool and sending jobs in and receiving responses can be reused, since the job and response objects do not have to be based on a particular class. When using pipes or sockets, do not forget to flush after dumping each object, to push the data through the connection to the other end. See the [`multiprocessing`](https://pymotw.com/3/multiprocessing/index.html#module-multiprocessing)module for a reusable worker pool manager.
>
> -- https://pymotw.com/3/pickle/index.html#working-with-streams



#### dumps()🔨

pickle.dumps(*obj*, *protocol=None*, ***, *fix_imports=True*)

将 *obj* 按照 pickle 协议序列化为二进制序列，并返回内含此序列的 `bytes` 对象，各个参数的含义与 `dump()` 相同。

```python
import pickle
import pprint
# data是由内置类型组成的数据结构
data = [{'a': 'A', 'b': 2, 'c': 3.0}]
print('DATA:', end=' ')
pprint.pprint(data)

# dumps()会将data序列化为二进制序列,默认采用protocol3,兼容Python3的所有版本
# 我们可以将二进制序列写入文件、套接字、pipe...
data_bytes = pickle.dumps(data)
print('PICKLE: {}'.format(data_bytes))
```

输出:

```
DATA: [{'a': 'A', 'b': 2, 'c': 3.0}]
PICKLE: b'\x80\x03]q\x00}q\x01(X\x01\x00\x00\x00aq\x02X\x01\x00\x00\x00Aq\x03X\x01\x00\x00\x00bq\x04K\x02X\x01\x00\x00\x00cq\x05G@\x08\x00\x00\x00\x00\x00\x00ua.'
```



#### load()🔨

🔨pickle.load(*file*, ***, *fix_imports=True*, *encoding="ASCII"*, *errors="strict"*)

读取 *file* 中的二进制数据，并通过这些数据逆序列化出 Python 对象，等效于 `Unpickler(file).load()`。

参数说明:

- The argument *file* must have two methods, a read() method that takes an integer argument, and a readline() method that requires no arguments. Both methods should return bytes. Thus *file* can be an on-disk file opened for binary reading, an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO)object, or any other custom object that meets this interface.
- Optional keyword arguments are *fix_imports*, *encoding* and *errors*, which are used to control compatibility support for pickle stream generated by Python 2. 
  - If *fix_imports* is true, pickle will try to map the old Python 2 names to the new names used in Python 3. 
  - The *encoding* and *errors* tell pickle how to decode 8-bit string instances pickled by Python 2; these default to ‘ASCII’ and ‘strict’, respectively. The *encoding* can be ‘bytes’ to read these 8-bit string instances as bytes objects. Using `encoding='latin1'` is required for unpickling NumPy arrays and instances of [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime), [`date`](https://docs.python.org/3/library/datetime.html#datetime.date) and [`time`](https://docs.python.org/3/library/datetime.html#datetime.time) pickled by Python 2.

会自动检测 pickle 协议的版本，因此不再需要 *protocol* 参数；还会自动检测 Python 对象经 pickle 后的二进制数据的长度，多余的二进制数据将被忽略:

```python
a = {
    "Type": "A",
    "field1": "value1",
    "field2": "value2",
    "field3": "value3",
}
b = [1, 2, 3]

import pickle

with open('./file.txt', 'wb') as f:
    pickle.dump(a, f)
    pickle.dump(b, f)

with open('./file.txt', 'rb') as f:
    print(pickle.load(f))
    print(pickle.load(f))
```

输出:

```
{'Type': 'A', 'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}
[1, 2, 3]
```



#### loads()🔨

🔨pickle.loads(*bytes_object*, ***, *fix_imports=True*, *encoding="ASCII"*, *errors="strict"*)

将 *bytes_object* 中的二进制数据逆序列化为 Python 对象。

`pickle` 会自动检测 protocol 的版本，因此无需传递与 protocol 相关的参数；`pickle` 会自动检测 Python 对象经 pickle 后的二进制数据的长度，多余的二进制数据将被忽略:

参数说明:

- Optional keyword arguments are *fix_imports*, *encoding* and *errors*, which are used to control compatibility support for pickle stream generated by Python 2. 
  - If *fix_imports* is true, pickle will try to map the old Python 2 names to the new names used in Python 3. 
  - The *encoding* and *errors* tell pickle how to decode 8-bit string instances pickled by Python 2; these default to ‘ASCII’ and ‘strict’, respectively. The *encoding* can be ‘bytes’ to read these 8-bit string instances as bytes objects. Using `encoding='latin1'` is required for unpickling NumPy arrays and instances of [`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime), [`date`](https://docs.python.org/3/library/datetime.html#datetime.date) and [`time`](https://docs.python.org/3/library/datetime.html#datetime.time) pickled by Python 2.

`pickle` 会自动检测 protocol 的版本，因此无需传递与 protocol 相关的参数

`pickle` 会自动检测 Python 对象经 pickle 后的二进制数据的长度，多余的二进制数据将被忽略:

```python
a = {
    "Type": "A",
    "field1": "value1",
    "field2": "value2",
    "field3": "value3",
}
b = [1, 2, 3]

import pickle
pickled = pickle.dumps(a)
pickled += pickle.dumps(b)
print(pickle.loads(pickled))
#> {'Type': 'A', 'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}
```

`loads()` 会重构一个具备相同字段值的新对象，与原对象具备不同的 id:

```python
import pickle
import pprint

data1 = [{'a': 'A', 'b': 2, 'c': 3.0}]
print('BEFORE: ', end=' ')
pprint.pprint(data1)

data1_string = pickle.dumps(data1)

# 对二进制序列执行unpickle操作后,会构建一个具备相同字段值的新对象
data2 = pickle.loads(data1_string)
print('AFTER : ', end=' ')
pprint.pprint(data2)

print('SAME? :', (data1 is data2))
print('EQUAL?:', (data1 == data2))
```

输出:

```
BEFORE:  [{'a': 'A', 'b': 2, 'c': 3.0}]
AFTER :  [{'a': 'A', 'b': 2, 'c': 3.0}]
SAME? : False
EQUAL?: True
```





### 异常

#### PickleError☣

☣*exception* pickle.PickleError

Common base class for the other pickling exceptions. It inherits [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception).



#### PicklingError☣

☣*exception* pickle.PicklingError

Error raised when an unpicklable object is encountered by [`Pickler`](https://docs.python.org/3/library/pickle.html#pickle.Pickler). It inherits [`PickleError`](https://docs.python.org/3/library/pickle.html#pickle.PickleError).Refer to [What can be pickled and unpickled?](https://docs.python.org/3/library/pickle.html#pickle-picklable) to learn what kinds of objects can be pickled.



#### UnpicklingError☣

☣*exception* pickle.UnpicklingError

Error raised when there is a problem unpickling an object, such as a data corruption or a security violation. It inherits [`PickleError`](https://docs.python.org/3/library/pickle.html#pickle.PickleError).Note that other exceptions may also be raised during unpickling, including (but not necessarily limited to) AttributeError, EOFError, ImportError, and IndexError.

### 类

> The [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) module exports two classes, [`Pickler`](https://docs.python.org/3/library/pickle.html#pickle.Pickler) and [`Unpickler`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler):

#### Pickler🛠

🛠*class* pickle.Pickler(*file*, *protocol=None*, ***, *fix_imports=True*)

`Pickle` 实例的功能是向 *file* 写入 pickle 数据流。

**参数说明:**

- The optional *protocol* argument, an integer, tells the pickler to use the given protocol; supported protocols are 0 to [`HIGHEST_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.HIGHEST_PROTOCOL). If not specified, the default is [`DEFAULT_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.DEFAULT_PROTOCOL). If a negative number is specified, [`HIGHEST_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.HIGHEST_PROTOCOL) is selected.
- The *file* argument must have a write() method that accepts a single bytes argument. It can thus be an on-disk file opened for binary writing, an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) instance, or any other custom object that meets this interface.
- If *fix_imports* is true and *protocol* is less than 3, pickle will try to map the new Python 3 names to the old module names used in Python 2, so that the pickle data stream is readable with Python 2.

**属性:**

- dump(*obj*) - 将 *obj* 序列化后写入 *file*

- persistent_id(*obj*) - 在调用 `dump()` 方法时，会自动调用此方法，以便引用持久化的外部对象。

  > Do nothing by default. This exists so a subclass can override it.
  >
  > If [`persistent_id()`](https://docs.python.org/3/library/pickle.html#pickle.Pickler.persistent_id) returns `None`, *obj* is pickled as usual. Any other value causes [`Pickler`](https://docs.python.org/3/library/pickle.html#pickle.Pickler) to emit the returned value as a persistent ID for *obj*. The meaning of this persistent ID should be defined by [`Unpickler.persistent_load()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.persistent_load). Note that the value returned by [`persistent_id()`](https://docs.python.org/3/library/pickle.html#pickle.Pickler.persistent_id) cannot itself have a persistent ID.
  >
  > See [Persistence of External Objects](https://docs.python.org/3/library/pickle.html#pickle-persistent) for details and examples of uses.

  详见: [引用持久化的外部对象](#引用持久化的外部对象)

- dispatch_table - 引入私有调度表，以便处理特定类型的对象，参考 [Dispatch Tables](#Dispatch Tables)

- fast - 已废弃

详见 https://docs.python.org/3/library/pickle.html#pickle.Pickler)



#### Unpickler🛠

🛠*class* pickle.Unpickler(*file*, ***, *fix_imports=True*, *encoding="ASCII"*, *errors="strict"*)

`Unpickler` 实例的功能是从二进制 *file* 中读取 pickle 数据流。

会自动检测 pickle 协议的版本，因此不再需要 *protocol* 参数。

**参数说明:**

- The argument *file* must have two methods, a read() method that takes an integer argument, and a readline() method that requires no arguments. Both methods should return bytes. Thus *file* can be an on-disk file object opened for binary reading, an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) object, or any other custom object that meets this interface.
- Optional keyword arguments are *fix_imports*, *encoding* and *errors*, which are used to control compatibility support for pickle stream generated by Python 2. If *fix_imports* is true, pickle will try to map the old Python 2 names to the new names used in Python 3. The *encoding* and *errors* tell pickle how to decode 8-bit string instances pickled by Python 2; these default to ‘ASCII’ and ‘strict’, respectively. The *encoding* can be ‘bytes’ to read these 8-bit string instances as bytes objects.

**属性:**

- load() - 将 *file* 中的二进制内容逆序列化为 Python 对象，会自动检测 Python 对象经 pickle 后的二进制数据的长度，多余的二进制数据将被忽略:

- persistent_load(*pid*)

  > Raise an [`UnpicklingError`](https://docs.python.org/3/library/pickle.html#pickle.UnpicklingError) by default.
  >
  > If defined, [`persistent_load()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.persistent_load) should return the object specified by the persistent ID *pid*. If an invalid persistent ID is encountered, an [`UnpicklingError`](https://docs.python.org/3/library/pickle.html#pickle.UnpicklingError) should be raised.
  >
  > See [Persistence of External Objects](https://docs.python.org/3/library/pickle.html#pickle-persistent) for details and examples of uses.

  详见: [引用持久化的外部对象](#引用持久化的外部对象)

- find_class(*module*, *name*)

  > Import *module* if necessary and return the object called *name* from it, where the *module* and *name* arguments are [`str`](https://docs.python.org/3/library/stdtypes.html#str) objects. Note, unlike its name suggests, [`find_class()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.find_class) is also used for finding functions.
  >
  > Subclasses may override this to gain control over what type of objects and how they can be loaded, potentially reducing security risks. Refer to [Restricting Globals](https://docs.python.org/3/library/pickle.html#pickle-restrict) for details.

详见 https://docs.python.org/3/library/pickle.html#pickle.Unpickler

## 可pickle的类型

以下类型可以通过 `pickle` 序列化:

- `None`, `True`, and `False`
- integers, floating point numbers, complex numbers
- strings, bytes, bytearrays
- tuples, lists, sets, and dictionaries containing only picklable objects
- functions defined at the top level of a module (using [`def`](https://docs.python.org/3/reference/compound_stmts.html#def), not [`lambda`](https://docs.python.org/3/reference/expressions.html#lambda))
- built-in functions defined at the top level of a module
- classes that are defined at the top level of a module
- instances of such classes whose [`__dict__`](https://docs.python.org/3/library/stdtypes.html#object.__dict__) or the result of calling [`__getstate__()`](https://docs.python.org/3/library/pickle.html#object.__getstate__) is picklable (see section [Pickling Class Instances](https://docs.python.org/3/library/pickle.html#pickle-inst) for details).

关于 pickle 过程中存在限制和异常，详见: https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled



## pickling类实例

> 参考: https://docs.python.org/3/library/pickle.html#pickling-class-instances

本节将介绍如何定义、如何自定义、如何控制类实例的 pickled/unpickled 过程。

默认情况下，pickled/unpickled 类实例的过程如下:

> In most cases, no additional code is needed to make instances picklable. By default, pickle will retrieve the class and the attributes of an instance via introspection. When a class instance is unpickled, its [`__init__()`](https://docs.python.org/3/reference/datamodel.html#object.__init__) method is usually *not* invoked. The default behaviour first creates an uninitialized instance and then restores the saved attributes. The following code shows an implementation of this behaviour:
>
> ```python
> def save(obj):
>        return (obj.__class__, obj.__dict__)
> 
> def load(cls, attributes):
>        obj = cls.__new__(cls)
>        obj.__dict__.update(attributes)
>        return obj
> ```

### 特殊方法

> 参考: https://docs.python.org/3/library/pickle.html#pickling-class-instances

可以在类中提供一个或多个特殊方法来改变 pickled/unpickled 的默认行为。

#### `object.__getnewargs_ex__()`

在 protocol 2 及其之后的版本中，如果类中实现了 `__getnewargs_ex__()` 方法，则会在 unpickle 时自动调用该方法，并把其返回值传递给类的 [`__new__()`](https://docs.python.org/3/reference/datamodel.html#object.__new__)。

`__getnewargs_ex__()` 方法的返回值必须是一对 `(args, kwargs)`，其中 `args` 是由位置参数组成的元组，`kwagrs` 是由命名参数组成的字典。在 unpickle 时，会将 `(args, kwargs)` 传递给 `__new__()`

如果自定义类的 `__new__()` 方法需要 keyword-only 参数，则应实现此方法；否则，为了保证兼容性，建议实现 `__getnewargs_ex__()` 方法。

*Changed in version 3.6:* [`__getnewargs_ex__()`](https://docs.python.org/3/library/pickle.html#object.__getnewargs_ex__) is now used in protocols 2 and 3.

```python
import pickle


class Cls(object):
    def __new__(cls, n):
        print('in to __new__')
        inst = super().__new__(cls)
        inst.n2 = n
        return inst

    def __init__(self, n):
        print('in to __init__')
        self.n1 = n
        del self.n2

    def __getnewargs_ex__(self):
        return ((2, ), {})


inst = Cls('1')
print('======')
p = pickle.dumps(inst)
print(pickle.loads(p).n2)
```

输出:

```
in to __new__
in to __init__
======
in to __new__
2
======
```



#### `object.__getnewargs__()`

该方法的功能与 `__getnewargs_ex__()` 相似，但仅支持位置参数，其返回值必须是一个包含参数的元组，该元组会被传递给 `__new__()` 方法

如果没有定义 `__getnewargs_ex__()`，则会调用 `__getnewargs__()`

*Changed in version 3.6:* Before Python 3.6, [`__getnewargs__()`](https://docs.python.org/3/library/pickle.html#object.__getnewargs__) was called instead of[`__getnewargs_ex__()`](https://docs.python.org/3/library/pickle.html#object.__getnewargs_ex__) in protocols 2 and 3.



#### `object.__getstate__()`

如果类中定义了 `__getstate__()` 方法，在 pickle 类实例时会自动调用该方法，并将其返回的对象作为实例的内容进行 pickle，此时不会继续 pickle 实例字典 `__dict__` 中的内容。

如果没有定义 `__getstate__()` 方法，则会按照默认方式对实例的 `__dict__` 进行 pickle。

```python
import pickle
class Cls(object):
    def __init__(self):
        self.a = 'a1'

    def __getstate__(self):
        print('in to __getstate__')
        return {'a': 'a2'}

inst = Cls()
p = pickle.dumps(inst)
print('=========')
print(pickle.loads(p))
print(pickle.loads(p).a)
```

输出:

```
in to __getstate__
=========
<__main__.Cls object at 0x000001A50EA28C88>
a2
```

扩展阅读: [无法pickle的对象](#无法pickle的对象)



#### `object.__setstate__(state)`

如果类定义中包含 `__setstate__()` 方法，则会在 unpickle 时自动调用该方法，并通过该方法对实例进行初始化。此时，*state* 可以是非字典类型的对象。

```python
import pickle
class Cls(object):
    def __init__(self):
        self.a = 'a1'

    def __setstate__(self, state):
        print(f'in to __getstate__:{state}')
        self.__dict__.update({'a': 'a3'})

inst = Cls()
p = pickle.dumps(inst)
print('=========')
print(pickle.loads(p))
print(pickle.loads(p).a)
```

输出:

```
=========
in to __getstate__:{'a': 'a1'}
<__main__.Cls object at 0x0000023C74588BE0>
in to __getstate__:{'a': 'a1'}
a3
```

如果没有定义 `__setstate__()` 方法，pickled state 必须是字典，并且会将字典中的条目分配给新实例的字典 `__dict__` 。

⚠如果 `__getstate__()` 的返回值为假，则不会在 unpickling 时调用 `__setstate__()` 方法。

扩展阅读: [无法pickle的对象](#无法pickle的对象)



#### `object.__reduce__()`

详见: <https://docs.python.org/3/library/pickle.html#object.__reduce__>



#### `object.__reduce_ex__(protocol)`

详见: <https://docs.python.org/3/library/pickle.html#object.__reduce_ex__>



### 重建对象

> 参考: https://pymotw.com/3/pickle/index.html#problems-reconstructing-objects

pickle 某个实例对象时，只会 pickle 该实例中的数据，并不会 pickle 类定义。unpickle 时，会在命名空间中查找对应的类，并使用这个类来重建实例对象。

因此，使用 `pickle` 模块操作类实例时，在包含 unpickle 操作的进程的命名空间中，必须包含被重建的实例对象所属的类，才能成功重建实例对象。

下面我们先将类实例写入文件:

```python
# pickle_dump_to_file_1.py
import pickle
import sys

class SimpleObject:
    def __init__(self, name):
        self.name = name
        l = list(name)
        l.reverse()
        self.name_backwards = ''.join(l)

if __name__ == '__main__':
    data = []
    data.append(SimpleObject('pickle'))
    data.append(SimpleObject('preserve'))
    data.append(SimpleObject('last'))

    filename = sys.argv[1]

    with open(filename, 'wb') as out_s:
        for o in data:
            print('WRITING: {} ({})'.format(
                o.name, o.name_backwards))
            pickle.dump(o, out_s)
```

运行时，脚本会根据命令行中的参数创建相应的文件:

```python
$ python3 pickle_dump_to_file_1.py test.dat

WRITING: pickle (elkcip)
WRITING: preserve (evreserp)
WRITING: last (tsal)
```

如果直接 unpickle 文件中的二进制内容，会抛出异常:

```python
# pickle_load_from_file_1.py
import pickle
import pprint
import sys

filename = sys.argv[1]

with open(filename, 'rb') as in_s:
    while True:
        try:
            o = pickle.load(in_s)
        except EOFError:
            break
        else:
            print('READ: {} ({})'.format(
                o.name, o.name_backwards))
```

出现异常的原因是在当前命名空间中 `SimpleObject` 不可用:

```python
$ python3 pickle_load_from_file_1.py test.dat

Traceback (most recent call last):
  File "pickle_load_from_file_1.py", line 15, in <module>
    o = pickle.load(in_s)
AttributeError: Can't get attribute 'SimpleObject' on <module '_
_main__' from 'pickle_load_from_file_1.py'>
```

在 pickle_load_from_file_1.py 中导入 `SimpleObject` 类后，便可成功 unpickle:

```python
from pickle_dump_to_file_1 import SimpleObject
```

运行脚本:

```python
$ python3 pickle_load_from_file_2.py test.dat

READ: pickle (elkcip)
READ: preserve (evreserp)
READ: last (tsal)
```



### 无法pickle的对象

> 参考: https://pymotw.com/3/pickle/index.html#unpicklable-objects

并不是所有对象都可以被 pickle。依赖于操作系统或其他进程的运行时状态的套接字、文件句柄、数据库连接以及其它类似对象都无法以有意义的方式保存。如果实例对象中包含无法 pickle 的属性，则需要通过 `__getstate__()` 来剔除无法 pickle 的属性，并返回由可 pickle 属性组成的集合；在 unpickle 二进制序列时，还要使用 `__setstate__()` 来恢复哪些无法 pickle 的属性:

- The `__getstate__()` method must return an object containing the internal state of the object. One convenient way to represent that state is with a dictionary, but the value can be any picklable object.
- The state is stored, and passed to `__setstate__()` when the object is loaded from the pickle.

示例 - 由于文件对象不能被 pickle，因此需要利用 `__setsate__()` 和 `__getstate__()` 来处理文件对象:

> Here’s an example that shows how to modify pickling behavior for a class. The `TextReader`class opens a text file, and returns the line number and line contents each time its `readline()` method is called. If a `TextReader` instance is pickled, all attributes *except* the file object member are saved. When the instance is unpickled, the file is reopened, and reading resumes from the last location. The [`__setstate__()`](https://docs.python.org/3/library/pickle.html#object.__setstate__) and [`__getstate__()`](https://docs.python.org/3/library/pickle.html#object.__getstate__) methods are used to implement this behavior.

```python
class TextReader:
    """Print and number lines in a text file."""

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename)
        self.lineno = 0

    def readline(self):
        self.lineno += 1
        line = self.file.readline()
        if not line:
            return None
        if line.endswith('\n'):
            line = line[:-1]
        return "%i: %s" % (self.lineno, line)

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['file']
        return state

    def __setstate__(self, state):
        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)
        # Restore the previously opened file's state. To do so, we need to
        # reopen it and read from it until the line count is restored.
        file = open(self.filename)
        for _ in range(self.lineno):
            file.readline()
        # Finally, save the file.
        self.file = file
```

> A sample usage might be something like this:

```python
>>> reader = TextReader("hello.txt")
>>> reader.readline()
'1: Hello world!'
>>> reader.readline()
'2: I am line number two.'
>>> new_reader = pickle.loads(pickle.dumps(reader))
>>> new_reader.readline()
'3: Goodbye!'
```

示例 - This example uses a separate `State` object to hold the internal state of `MyClass`. When an instance of `MyClass` is loaded from a pickle, `__setstate__()` is passed a `State`instance which it uses to initialize the object.

```python
# pickle_state.py
import pickle


class State:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'State({!r})'.format(self.__dict__)


class MyClass:

    def __init__(self, name):
        print('MyClass.__init__({})'.format(name))
        self._set_name(name)

    def _set_name(self, name):
        self.name = name
        self.computed = name[::-1]

    def __repr__(self):
        return 'MyClass({!r}) (computed={!r})'.format(
            self.name, self.computed)

    def __getstate__(self):
        state = State(self.name)
        print('__getstate__ -> {!r}'.format(state))
        return state

    def __setstate__(self, state):
        print('__setstate__({!r})'.format(state))
        self._set_name(state.name)


inst = MyClass('name here')
print('Before:', inst)

dumped = pickle.dumps(inst)

reloaded = pickle.loads(dumped)
print('After:', reloaded)
```

输出:

```
$ python3 pickle_state.py

MyClass.__init__(name here)
Before: MyClass('name here') (computed='ereh eman')
__getstate__ -> State({'name': 'name here'})
__setstate__(State({'name': 'name here'}))
After: MyClass('name here') (computed='ereh eman')
```



### 引用持久化的外部对象

Persistence of External Objects

> 参考: https://docs.python.org/3/library/pickle.html#persistence-of-external-objects

在使用 pickle 模块时，我们可利用 persisten ID 来引用位于 pickle 数据流外部的对象。persisten ID 可以是由字母和数字组成的字符串(仅限 protocol 0)，也可以是任何 Python 对象(需使用较新的 protocol)。

解析 persistent ID 的工作并不是由 pickle 模块定义的，我们需要将解析工作分别委托给 pickler 的[`persistent_id()`](https://docs.python.org/3/library/pickle.html#pickle.Pickler.persistent_id) 方法和 unpickler 的 [`persistent_load()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.persistent_load) 来完成。

在 pickle 具备 persistent ID 的 Python 对象时，pickler 必须具备自定的 `persistent_id()` 方法，并以 Python 对象为参数，返回值是 `None` 或该对象的 persistent ID。当返回值是 `None` 时，pickler 会以默认方式 pickle 输入对象；当返回值是输入对象的 persistent ID 时，pickler 会将输入对象和标记 ID 一同 pickle，以便 unpickler 可能够识别到 persistent ID。在调用 `pickler.dump()` 时，会自动调用 `persistent_id()`。

在 unpickle 外部对象时，unpickler 必须具有自定的 `persistent_load()` 方法，该方法以 persistent ID 为输入参数，并返回引用的对象，并且 `unpickler.load()` 的会将该对象作为返回值。如果二进制数据包含 persistent ID，则会在调用 `unpickler.load()` 时，会自动调用 `persistent_load()`；如果二进制数据不包含 persistent ID，则不会调用 `persistent_load()`。

下面这是示例展示了如何使用 persistent ID 来引用 pickle 数据流外部的对象:

```python
import pickle
import sqlite3
from collections import namedtuple

# Simple class representing a record in our database.
MemoRecord = namedtuple("MemoRecord", "key, task")


class DBPickler(pickle.Pickler):
    def persistent_id(self, obj):
        # 在调用self.dump()时，会自动调用该方法
        # Instead of pickling MemoRecord as a regular class instance,
        # we emit a persistent ID.
        if isinstance(obj, MemoRecord):
            # Here, our persistent ID is simply a tuple, containing a tag and a
            # key, which refers to a specific record in the database.
            return ("MemoRecord", obj.key)
        else:
            # If obj does not have a persistent ID, return None. 
            # This means obj needs to be pickled as usual.
            return None


class DBUnpickler(pickle.Unpickler):
    def __init__(self, file, connection):
        super().__init__(file)
        self.connection = connection

    def persistent_load(self, pid):
        # 在调用self.load()时，会自动调用该方法
        # This method is invoked whenever a persistent ID is encountered.
        # Here, pid is the tuple returned by DBPickler.
        cursor = self.connection.cursor()
        type_tag, key_id = pid
        if type_tag == "MemoRecord":
            # Fetch the referenced record from the database and return it.
            # 引用持久化的外部数据
            cursor.execute("SELECT * FROM memos WHERE key=?", (str(key_id), ))
            key, task = cursor.fetchone()
            return MemoRecord(key, task)
        else:
            # Always raises an error if you cannot return the correct object.
            # Otherwise, the unpickler will think None is the object referenced
            # by the persistent ID.
            raise pickle.UnpicklingError("unsupported persistent object")


def main():
    import io
    import pprint

    # Initialize and populate our database.
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE memos(key INTEGER PRIMARY KEY, task TEXT)")
    tasks = (
        'give food to fish',
        'prepare group meeting',
        'fight with a zebra',
    )
    for task in tasks:
        cursor.execute("INSERT INTO memos VALUES(NULL, ?)", (task, ))

    # Fetch the records to be pickled.
    cursor.execute("SELECT * FROM memos")
    memos = [MemoRecord(key, task) for key, task in cursor]
    # Save the records using our custom DBPickler.
    file = io.BytesIO()
    DBPickler(file).dump(memos)

    print("Pickled records:")
    pprint.pprint(memos)

    # Update a record, just for good measure.
    cursor.execute("UPDATE memos SET task='learn italian' WHERE key=1")

    # Load the records from the pickle data stream.
    file.seek(0)
    memos = DBUnpickler(file, conn).load()

    print("Unpickled records:")
    pprint.pprint(memos)


if __name__ == '__main__':
    main()
```

输出:

```
Pickled records:
[MemoRecord(key=1, task='give food to fish'),
 MemoRecord(key=2, task='prepare group meeting'),
 MemoRecord(key=3, task='fight with a zebra')]
Unpickled records:
[MemoRecord(key=1, task='learn italian'),
 MemoRecord(key=2, task='prepare group meeting'),
 MemoRecord(key=3, task='fight with a zebra')]
```

### Dispatch Tables

> 参考: https://docs.python.org/3/library/pickle.html#id5

如果想要自定义某些类的 pickling 过程，同时不像其它对象的 pickling 过程，便可以使用私有调度表(*private* *dispatch* *table*)。

示例 - 在源代码中用于处理 `bool` 类型的 pickling 函数如下:

```python
def save_bool(self, obj):
    if self.proto >= 2:
        self.write(NEWTRUE if obj else NEWFALSE)
        else:
            self.write(TRUE if obj else FALSE)
dispatch[bool] = save_bool
# save_bool函数会被添加到pickler内建的调度表dispatch中,
# 每当需要pickling bool类型时,便会调用此方法
```

> The global dispatch table managed by the [`copyreg`](https://docs.python.org/3/library/copyreg.html#module-copyreg) module is available as `copyreg.dispatch_table`. Therefore, one may choose to use a modified copy of `copyreg.dispatch_table` as a private dispatch table.

示例 - 添加私有调度表:

```python
f = io.BytesIO()
p = pickle.Pickler(f)
p.dispatch_table = copyreg.dispatch_table.copy()
p.dispatch_table[SomeClass] = reduce_SomeClass
# SomeClass表示某个类,reduce_SomeClass表示pickling该类的实例的方法
```

> creates an instance of [`pickle.Pickler`](https://docs.python.org/3/library/pickle.html#pickle.Pickler) with a private dispatch table which handles the `SomeClass` class specially. Alternatively, the code

```python
class MyPickler(pickle.Pickler):
    dispatch_table = copyreg.dispatch_table.copy()
    dispatch_table[SomeClass] = reduce_SomeClass
f = io.BytesIO()
p = MyPickler(f)
```

> does the same, but all instances of `MyPickler` will by default share the same dispatch table. The equivalent code using the [`copyreg`](https://docs.python.org/3/library/copyreg.html#module-copyreg) module is

```python
copyreg.pickle(SomeClass, reduce_SomeClass)
f = io.BytesIO()
p = pickle.Pickler(f)
```



## Restricting Globals

> 参考: https://docs.python.org/3/library/pickle.html#restricting-globals

在 unpickling 时，限制其对全局符号表的改动。

By default, unpickling will import any class or function that it finds in the pickle data. For many applications, this behaviour is unacceptable as it permits the unpickler to import and invoke arbitrary code. Just consider what this hand-crafted pickle data stream does when loaded:

```python
>>> import pickle
>>> pickle.loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
hello world
0
```

In this example, the unpickler imports the [`os.system()`](https://docs.python.org/3/library/os.html#os.system) function and then apply the string argument “echo hello world”. Although this example is inoffensive, it is not difficult to imagine one that could damage your system.

For this reason, you may want to control what gets unpickled by customizing[`Unpickler.find_class()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.find_class). Unlike its name suggests, [`Unpickler.find_class()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.find_class) is called whenever a global (i.e., a class or a function) is requested. Thus it is possible to either completely forbid globals or restrict them to a safe subset.

Here is an example of an unpickler allowing only few safe classes from the [`builtins`](https://docs.python.org/3/library/builtins.html#module-builtins) module to be loaded:

```python
import builtins
import io
import pickle

safe_builtins = {
    'range',
    'complex',
    'set',
    'frozenset',
    'slice',
}

class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        # Only allow safe classes from builtins.
        if module == "builtins" and name in safe_builtins:
            return getattr(builtins, name)
        # Forbid everything else.
        raise pickle.UnpicklingError("global '%s.%s' is forbidden" %
                                     (module, name))

def restricted_loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()
```

A sample usage of our unpickler working has intended:

```python
>>> restricted_loads(pickle.dumps([1, 2, range(15)]))
[1, 2, range(0, 15)]
>>> restricted_loads(b"cos\nsystem\n(S'echo hello world'\ntR.")
Traceback (most recent call last):
  ...
pickle.UnpicklingError: global 'os.system' is forbidden
>>> restricted_loads(b'cbuiltins\neval\n'
...                  b'(S\'getattr(__import__("os"), "system")'
...                  b'("echo hello world")\'\ntR.')
Traceback (most recent call last):
  ...
pickle.UnpicklingError: global 'builtins.eval' is forbidden
```

As our examples shows, you have to be careful with what you allow to be unpickled. Therefore if security is a concern, you may want to consider alternatives such as the marshalling API in [`xmlrpc.client`](https://docs.python.org/3/library/xmlrpc.client.html#module-xmlrpc.client) or third-party solutions.