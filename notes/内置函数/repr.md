# repr

🔨 repr(*obj*, /)

该方法会返回 *obj* 的标准(*canonical*)字符串表示形式——可供解释器读取的表示形式。

对于大多数类型(包含大多数内置类型)来说，`repr(obj)`  返回的字符串应该像是一个有效的 Python 表达式，并且将该字符串传递给 `evla()` 后，可以创建一个具备相同值的对象(需给定恰当的环境)，即 `eval(repr(obj)) == obj`

如果 `repr(obj)` 无法返回一个有效的表达式，则应返回形如 `<...some useful description...>` 的字符串，其中会包含对象的类型的名称和附加信息(对象的名称和地址)。如果将 `<...some useful description...>` 字符串传递给 `evla()` 函数，则会抛出[`SyntaxError`](https://docs.python.org/3.7/library/exceptions.html#SyntaxError) 异常。

示例 - 观察 `str` 和 `repr` 的区别：

```python
>>> value = 'orca_j35\n'
>>> str(value)
'orca_j35\n'
>>> repr(value)
"'orca_j35\\n'"
>>> eval(repr(value))
'orca_j35\n'
>>> eval(str(value))
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    eval(str(value))
  File "<string>", line 1, in <module>
NameError: name 'orca_j35' is not defined
```

示例 - 无法返回有效表达式的情况：

```python
>>> class Student:
    def __init__(self,name):
        self.name = name

        
>>> a = Student('Bob')
>>> repr(a)
'<__main__.Student object at 0x000001243768AEF0>'
```

当我们通过 `repr(obj)` 获取对象的标准字符串表示形式时，实际上在 `repr()` 内部会调用 `type(obj).__repr__(obj)` 来获取对象的字符串表示形式。因此，可通过覆写类中的 `__repr__()` 方法来控制 `repr()` 的返回值。

示例 - 覆写类中的 `__repr__` 方法：

```python
>>> class Cls:
    def __repr__(self):
        return 'Cls类的实例:{}'.format(super().__repr__())

>>> repr(Cls())
'Cls类的实例:<__main__.Cls object at 0x0000012437522FD0>'
# 如没有覆写__str__，同样会调用__repr__
>>> str(Cls())
'Cls类的实例:<__main__.Cls object at 0x00000124375C89E8>'
```

示例 - 如果 `__repr__` 和 `__str__` 相同，可直接写作 `__repr__ = __str__`

```python
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name=%s)' % self.name
    __repr__ = __str__
```

## 实现细节

`repr(obj)` 会在内部调用 `type(obj).__repr__(obj)`，从而使用类字典中的 `__repr__()` 方法来获取 *obj* 的标准字符串表示形式。也就是说在获取属性列表时，会跳过实例字典：

```python
class Cls:
    def __repr__(self):
        return super().__repr__()


obj = Cls()
from types import MethodType
obj.__repr__ = MethodType(lambda self: '绑定到实例的__repr__方法', obj)
print(repr(obj))
'''Out:
<__main__.Cls object at 0x000001F0D7A35470>
'''
```

如果仅考虑类和实例，这好像并没有什么意义，因为不会有人在实例字典中重新绑定 `__repr__` 方法。但是，如果考虑到元类和类，这就很有意义了。类是元类的实例，当 *obj* 是一个类时，实际上需要调用元类中的 `__repr__` 方法，此时我们便需要跳过类字典中 `__repr__` 方法，使用元类中的同名方法。

## \_\_repr\_\_

🔨 object.\_\_repr\_\_(*self*)

该方法会返回对象的正式的(*official*)字符串表示形式(可供解释器读取的表示形式)，其返回值必须是一个字符串对象。`repr()` 函数会在内部调用该方法。

通常来说，`__repr__` 返回的字符串应该像是一个有效的 Python 表达式，并且可用该字符串重新创建一个具备相同值的对象(需给定恰当的环境)。

如果 `__repr__` 无法返回一个有效的表达式，则应返回形如 `<...some useful description...>` 的字符串，其中会包含对象的类型的名称和附加信息(对象的名称和地址)。

如果在某个类中覆写了 `__repr__` ，但并没有覆写 `__str__` 。那么当需要该类的实例的"非正式(*informal*)"的字符串表示形式时，也会调用 `__repr__()`。

通常会在调试时使用 `__repr__` ，因此在描述对象时最重要的是提供丰富的信息和明确的含义。

## repr() vs str()

`str(object)` 会返回易于人类阅读的字符串表示形式， `repr()` 则会生成一个可被解释器读取的字符串表示形式(如果没有等效语法，将会强制抛出 [`SyntaxError`](https://docs.python.org/3/library/exceptions.html#SyntaxError) 异常)。部分对象并不具备适于人类阅读的特定表示形式，此时 `str()` 与 `repr()` 的返回值相同。像是数字或结构(如列表和字典)这样的值，`str()` 和 `repr()` 会给出相同的表示形式。比较特殊的是字符串，`str()` 和 `repr()` 会给出不同的表示形式。一些示例：

```python
>>> s = 'Hello, world.'
>>> str(s),repr(s)
('Hello, world.', "'Hello, world.'")
>>> str(1/7),repr(1/7)
('0.14285714285714285', '0.14285714285714285')
>>> str(10 * 3.25),repr(10 * 3.25)
('32.5', '32.5')
# repr()会为字符串添加引号和反斜线
>>> str('hello, world\n'),repr('hello, world\n')
('hello, world\n', "'hello, world\\n'")
# 注意观察输出效果
>>> print(str('hello, world\n')+repr('hello, world\n'))
hello, world
'hello, world\n'
# 可以将任何对象用作repr()的参数
>>> x = 10 * 3.25
>>> repr((x, ('spam', 'eggs')))
"(32.5, ('spam', 'eggs'))"
>>> str((x, ('spam', 'eggs')))
"(32.5, ('spam', 'eggs'))"
```



