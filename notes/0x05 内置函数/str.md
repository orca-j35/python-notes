# str

## str(*obj*)

🔨 *class* str(*obj=''*)

使用单参数形式时，该方法会返回 *obj* 的非正式(*informal*)字符串表示形式，即易于人类阅读的表示形式。单参数形式的使用方法如下：

```
str(object='') -> str
 | str() -> empty string ''
 | str(object) -> type(object).__str__()
 |
 | object 可以是任意对象，包括 bytes 和 buffer 的实例
```

示例 - 展示在内置类型的实例上调用 `str()` 的效果：

```python
>>> str("orca_j35") # 字符串实例，将返回其自身
'orca_j35'
>>> str(b'abs') # bytes实例
"b'abs'"
>>> str(list)				  
"<class 'list'>"
>>> str([1,2])					  
'[1, 2]'
```

当我们通过 `str(obj)` 获取对象的非正式的字符串表示形式时，实际上在 `str()` 内部会调用 `type(obj).__str__(obj)` 来获取对象的字符串表示形式。因此，可通过覆写类中的 `__str__()` 方法来控制 `str()` 的返回值。如果 `type(obj)` 没有覆写 `__str__()` 方法，则会返回 [`repr(object)`](https://docs.python.org/3.7/library/functions.html#repr)：

```python
class Cls():
    def __repr__(self):
        return 'in __repr__'
print(str(Cls())) # Out: in __repr__
```

**扩展阅读** -『repr.md』

### 实现细节

`str(obj)` 会在内部调用 `type(obj).__str__(obj)`，从而使用类字典中的 `__str__()` 方法来获取 *obj* 的非正式的字符串表示形式。也就是说在获取属性列表时，会跳过实例字典：

```python
class Cls():
    def __str__(self):
        return 'Cls 类的实例对象'
obj = Cls()
from types import MethodType
obj.__str__ = MethodType(lambda self: '绑定到实例的__str__方法', obj)
print(str(obj))
"""Out:
Cls 类的实例对象
"""
```

如果仅考虑类和实例，这好像并没有什么意义，因为不会有人在实例字典中重新绑定 `__str__` 方法。但是，如果考虑到元类和类，这就很有意义了。类是元类的实例，当 *obj* 是一个类时，实际上需要调用元类中的 `__str__` 方法，此时我们便需要跳过类字典中 `__str__` 方法，使用元类中的同名方法。

### _\_str\_\_

🔨 object.\_\_str\_\_(*self*)

该方法会返回对象的非正式(*informal*)的字符串表示形式(易于人类阅读的表示形式)，其返回值必须是一个字符串对象。 [`str(object)`](https://docs.python.org/3.7/library/stdtypes.html#str) 、 [`format()`](https://docs.python.org/3.7/library/functions.html#format)、[`print()`](https://docs.python.org/3.7/library/functions.html#print) 会在内部调用该方法。 

 `__str__()` 和 [`__repr__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__repr__) 的区别在于，不要期望 `__str__()` 返回的字符串是一个有效的 Python 表达式。`__str__()` 会采用更恰当(或简洁)的方式来描述目标对象。

`__str__` 方法的默认实现是通过内置类型 [`object`](https://docs.python.org/3.7/library/functions.html#object) 调用 [`object.__repr__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__repr__)。

## str(*obj*, *encoding*, *errors*)

🔨 *class* str(*obj=b''*, *encoding='utf-8'*, *errors='strict'*)

此时会按照给定编码方式对 *obj* 进行**解码**，并返回解码后的字符串，使用方法如下：

```
str(obj[, encoding[, errors]]) -> str
 | str(obj, encoding='...') -> obj.decode(encoding='...')
 | str(obj, errors='...') -> obj.decode(errors='...')
 | str(obj, encoding='...', errors='...') -> obj.decode(encoding='...', errors='...')
 | 
 | 注意：obj 必须是 bytes 和 buffer 的实例
```

各参数的含义如下：(这三个参数均是 *positional-or-keyword*)

- *object* 是被解码的 [bytes-like](https://docs.python.org/3.7/glossary.html#term-bytes-like-object) 对象：
  - 如果 *object* 是 `bytes`(或 `bytearray`)对象， `str(object, encoding, errors)`会调用 [`object.decode(encoding, errors)`](https://docs.python.org/3.7/library/stdtypes.html#bytes.decode) 并返回其结果
  - 否则，`str(object, encoding, errors)` 会先获取缓冲器对象下的字节对象，然后再调用 `object.decode()` 并返回其结果
- *encoding* 用于设置编码方案，会被传递给 `bytes_or_buffer.decode()`，其默认值是 `sys.getdefaultencoding()`，可在 [Standard Encodings](https://docs.python.org/3.7/library/codecs.html#standard-encodings) 中可查看编码方案列表。
- *errors* 用于设置[错误处理方案](https://docs.python.org/3.7/library/codecs.html#error-handlers)，也会被传递给 `bytes_or_buffer.decode()`，其默认值是 `'strict'`。*errors* 可以是 `'ignore'`, `'replace'`, `'xmlcharrefreplace'`, `'backslashreplace'` 或任何已通过 [`codecs.register_error()`](https://docs.python.org/3.7/library/codecs.html#codecs.register_error) 注册的名称。

```python
>>> a_bytes = bytes('鲸','utf-8') # 对Unicode码点按照UTF8编码
>>> a_bytes
b'\xe9\xb2\xb8'
>>> str(a_bytes,'utf-8') # 对bytes对象进行解码
'鲸'
>>> str(a_bytes,'ascii') # 提供错误的编码方案会抛出异常
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    str(a_bytes,'ascii')
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe9 in position 0: ordinal not in range(128)
>>> str(a_bytes,'ascii','ignore') # 修改错误处理方案
''
```

有关缓冲区对象的详细信息，可阅读 [Binary Sequence Types — bytes, bytearray, memoryview](https://docs.python.org/3.7/library/stdtypes.html#binaryseq) 和 [Buffer Protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects)。

Tips: 在 Python 文档中，"编码(*encoding*)"是指将 Unicode 字符串转换为字节序列的规则，也就是说"编码"包含了从"抽象字符序列"到"字节序列"的全部过程；反之，"解码"则包含了从"字节序列"到"抽象字符序列"的全部过程。
