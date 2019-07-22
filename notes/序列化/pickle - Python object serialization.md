# pickle - Python object serialization
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`pickle`](https://docs.python.org/3/library/pickle.html#module-pickle) — Python object serialization
> - https://pymotw.com/3/pickle/index.html
> - https://codingpy.com/books/thinkpython2/14-files.html

`pickle` 模块实现了序列化(*serializing*)和返序列化(*de-serializing*) Python 对象的二进制协议。Pickling 是指将 Python 对象的层次结构转换为字节流的过程，unpickling 是 pickling 的反向操作，用于将字节流(来自 [binary file](https://docs.python.org/3/glossary.html#term-binary-file) 或 [bytes-like object](https://docs.python.org/3/glossary.html#term-bytes-like-object))转换为 Python 对象。Pickling (和 unpickling) 在其它编程语言中也被称为 serialization、marshalling、flattening。为了避免术语之间的混淆，本文将使用术语 pickling 和 unpickling。



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



#### dumps()🔨

pickle.dumps(*obj*, *protocol=None*, ***, *fix_imports=True*)

将 *obj* 对象的 pickle 结果以 `bytes` 对象返回，各个参数的含义与 `dump()` 相同。

```python
import pickle
print(pickle.dumps(a))
```

输出:

```
b'\x80\x03}q\x00(X\x04\x00\x00\x00Typeq\x01X\x01\x00\x00\x00Aq\x02X\x06\x00\x00\x00field1q\x03X\x06\x00\x00\x00value1q\x04X\x06\x00\x00\x00field2q\x05X\x06\x00\x00\x00value2q\x06X\x06\x00\x00\x00field3q\x07X\x06\x00\x00\x00value3q\x08u.'
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

参数说明:

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
pickled = pickle.dumps(a)
pickled += pickle.dumps(b)
print(pickle.loads(pickled))
#> {'Type': 'A', 'field1': 'value1', 'field2': 'value2', 'field3': 'value3'}
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

参数说明:

- The optional *protocol* argument, an integer, tells the pickler to use the given protocol; supported protocols are 0 to [`HIGHEST_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.HIGHEST_PROTOCOL). If not specified, the default is [`DEFAULT_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.DEFAULT_PROTOCOL). If a negative number is specified, [`HIGHEST_PROTOCOL`](https://docs.python.org/3/library/pickle.html#pickle.HIGHEST_PROTOCOL) is selected.
- The *file* argument must have a write() method that accepts a single bytes argument. It can thus be an on-disk file opened for binary writing, an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) instance, or any other custom object that meets this interface.
- If *fix_imports* is true and *protocol* is less than 3, pickle will try to map the new Python 3 names to the old module names used in Python 2, so that the pickle data stream is readable with Python 2.

属性:(详见 https://docs.python.org/3/library/pickle.html#pickle.Pickler)

- dump(*obj*) - 将 *obj* 序列化后写入 *file*

- persistent_id(*obj*) - 在调用 `dump()` 方法时，会自动调用此方法。

  > Do nothing by default. This exists so a subclass can override it.
  >
  > If [`persistent_id()`](https://docs.python.org/3/library/pickle.html#pickle.Pickler.persistent_id) returns `None`, *obj* is pickled as usual. Any other value causes [`Pickler`](https://docs.python.org/3/library/pickle.html#pickle.Pickler) to emit the returned value as a persistent ID for *obj*. The meaning of this persistent ID should be defined by [`Unpickler.persistent_load()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.persistent_load). Note that the value returned by [`persistent_id()`](https://docs.python.org/3/library/pickle.html#pickle.Pickler.persistent_id) cannot itself have a persistent ID.
  >
  > See [Persistence of External Objects](https://docs.python.org/3/library/pickle.html#pickle-persistent) for details and examples of uses.

- dispatch_table

- fast - 已废弃



#### Unpickler🛠

🛠*class* pickle.Unpickler(*file*, ***, *fix_imports=True*, *encoding="ASCII"*, *errors="strict"*)

`Unpickler` 实例的功能是从二进制 *file* 中读取 pickle 数据流。

会自动检测 pickle 协议的版本，因此不再需要 *protocol* 参数。

参数说明:

- The argument *file* must have two methods, a read() method that takes an integer argument, and a readline() method that requires no arguments. Both methods should return bytes. Thus *file* can be an on-disk file object opened for binary reading, an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) object, or any other custom object that meets this interface.
- Optional keyword arguments are *fix_imports*, *encoding* and *errors*, which are used to control compatibility support for pickle stream generated by Python 2. If *fix_imports* is true, pickle will try to map the old Python 2 names to the new names used in Python 3. The *encoding* and *errors* tell pickle how to decode 8-bit string instances pickled by Python 2; these default to ‘ASCII’ and ‘strict’, respectively. The *encoding* can be ‘bytes’ to read these 8-bit string instances as bytes objects.

属性:(详见 https://docs.python.org/3/library/pickle.html#pickle.Unpickler)

- load() - 将 *file* 中的二进制内容逆序列化为 Python 对象，会自动检测 Python 对象经 pickle 后的二进制数据的长度，多余的二进制数据将被忽略:

- persistent_load(*pid*)

  > Raise an [`UnpicklingError`](https://docs.python.org/3/library/pickle.html#pickle.UnpicklingError) by default.
  >
  > If defined, [`persistent_load()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.persistent_load) should return the object specified by the persistent ID *pid*. If an invalid persistent ID is encountered, an [`UnpicklingError`](https://docs.python.org/3/library/pickle.html#pickle.UnpicklingError) should be raised.
  >
  > See [Persistence of External Objects](https://docs.python.org/3/library/pickle.html#pickle-persistent) for details and examples of uses.

- find_class(*module*, *name*)

  > Import *module* if necessary and return the object called *name* from it, where the *module* and *name* arguments are [`str`](https://docs.python.org/3/library/stdtypes.html#str) objects. Note, unlike its name suggests, [`find_class()`](https://docs.python.org/3/library/pickle.html#pickle.Unpickler.find_class) is also used for finding functions.
  >
  > Subclasses may override this to gain control over what type of objects and how they can be loaded, potentially reducing security risks. Refer to [Restricting Globals](https://docs.python.org/3/library/pickle.html#pickle-restrict) for details.

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

本节将介绍如何定义、如何自定义、如何控制类实例的 pickled/unpickled 过程。

默认情况下，pickled/unpickled 类实例的过程如下:

> In most cases, no additional code is needed to make instances picklable. By default, pickle will retrieve the class and the attributes of an instance via introspection. When a class instance is unpickled, its [`__init__()`](https://docs.python.org/3/reference/datamodel.html#object.__init__) method is usually *not* invoked. The default behaviour first creates an uninitialized instance and then restores the saved attributes. The following code shows an implementation of this behaviour:
>
> ```python
> def save(obj):
>     return (obj.__class__, obj.__dict__)
> 
> def load(cls, attributes):
>     obj = cls.__new__(cls)
>     obj.__dict__.update(attributes)
>     return obj
> ```

可以在类中提供一个或多个特殊方法来改变 pickled/unpickled 的默认行为:

- `object.__getnewargs_ex__()`
- `object.__getnewargs__()`
- `object.__getstate__()`
- `object.__setstate__(state)`
- `object.__reduce__()`
- `object.__reduce_ex__(protocol)`

详见: https://docs.python.org/3/library/pickle.html#pickling-class-instances

### 外部对象的持久化

pickle 模块支持引用 pickle 数据流之外的对象，我们可利用 persisten ID 来引用外部对象，





