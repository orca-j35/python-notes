# vars

```
vars(...)
    vars([object]) -> MappingProxyType
    
    Without arguments, equivalent to locals().
    With an argument, equivalent to object.__dict__.
```

## 🔨 vars(*object*)

该函数会返回 *object* 的 [`__dict__`](https://docs.python.org/3.7/library/stdtypes.html#object.__dict__) 字段属性。*object* 必须是包含 `__dict__` 属性的对象(比如：模块、类、实例等等)，否则会抛出 `TypeError` 异常。

`__dict__` 用于存储对象中所含(可写)属性的映射关系，可以是字典或其它映射对象。对象所含(可写)属性是指被绑定到对象的(可写)属性：

- 如果 *object* 是实例，则只包含绑定到该实例的属性，不包含类和基类中的属性；
- 如果 *object* 是类(或类型)，则只包含绑定到该类(或类型)的属性，不包含基类和元类中的属性。

```python
from pprint import pprint
class Meta(type):
    def method_of_meta(self): # 绑定到Mate的属性
        print("method_of_meta")
class Base(object, metaclass=Meta):
    def __init__(self):
        self.x = 1 # 绑定到实例的属性
    def method_of_base(self): # 绑定到Base的属性
        print("method_of_base")
class Child(Base):
    def __init__(self): # 绑定到Child的属性
        self.y = 2 # 绑定到实例的属性
        super().__init__()
    def method_of_child(self): # 绑定到Child的属性
        print("method_of_child")
pprint(vars(Child()))  # 只包含绑定到实例的属性
pprint(vars(Child))  # 只包含绑定到类的属性，不包含基类和元类中的属性
pprint(vars(Meta))  # 只包含绑定到元类的属性，不包括基类中的属性
"""Out:
{'x': 1, 'y': 2}
mappingproxy({'__doc__': None,
              '__init__': <function Child.__init__ at 0x000001A76695C268>,
              '__module__': '__main__',
              'method_of_child': <function Child.method_of_child at 0x000001A76695C2F0>})
mappingproxy({'__doc__': None,
              '__module__': '__main__',
              'method_of_meta': <function Meta.method_of_meta at 0x000001A76695C0D0>})
"""
```

一些对象(如，模块和实例)的 `__dict__` 属性没有写入限制，可被直接更新。这些 `__dict__` 属性和对象是联动的，两者中只要有一个发生变化，另一个便会自动改变。

```python
from pprint import pprint
import types
class Cls:
    pass
inst = Cls()
dict_inst = vars(inst)
pprint(type(dict_inst))
pprint(dict_inst)
inst.update = "orca_j35" # 添加实例属性
pprint(dict_inst)  # __dict__会自动更新
dict_inst['a'] = "a new field"  # 实例的__dict__属性是dict对象，可直接更新__dict__
pprint(inst.a)  # 更新__dict__后，实例可直接调用新增属性
"""Out:
<class 'dict'>
{}
{'update': 'orca_j35'}
'a new field'
"""
```

但是，部分对象的 `__dict__` 属性可能存在写入限制(比如，类对象会将 [`types.MappingProxyType`](https://docs.python.org/3.7/library/types.html#types.MappingProxyType) 类型用作 `__dict__` 属性，以防止类用户直接更新 `__dict__` 属性)。

```python
from pprint import pprint
import types
class Cls:
    pass
map_proxy = vars(Cls)
pprint(type(map_proxy))
pprint(map_proxy)
Cls.update = 'orca_j35' # 添加类属性
pprint(map_proxy) # __dict__会自动更新
# 类的__dict__属性是MappingProxyType对象，不可直接更新__dict__，否则会抛出异常
map_proxy['a'] = "a new field"
"""Out：
<class 'mappingproxy'>
mappingproxy({'__dict__': <attribute '__dict__' of 'Cls' objects>,
              '__doc__': None,
              '__module__': '__main__',
              '__weakref__': <attribute '__weakref__' of 'Cls' objects>})
mappingproxy({'__dict__': <attribute '__dict__' of 'Cls' objects>,
              '__doc__': None,
              '__module__': '__main__',
              '__weakref__': <attribute '__weakref__' of 'Cls' objects>,
              'update': 'orca_j35'})
Traceback (most recent call last):
  File "c:/Users/iwhal/Desktop/内置函数/BI_vars.py", line 15, in <module>
    map_proxy['a'] = "a new field"
TypeError: 'mappingproxy' object does not support item assignment
"""
```

## 🔨 vars()

当实参为空时，可能出现以下两种情况：

- 如果位于全局作用域中，则 `vars()`、`locals()` 和 `globals()` 三者等效。在全局字典中所做的修改会影响解释器所使用的全局变量，反之亦然：

  ```python
  >>> vars() is locals() is globals()
  True
  >>> globals()['update'] = "orca_j35"
  >>> update
  'orca_j35'
  >>> del update
  >>> globals().get('update','not to exist')
  'not to exist'
  ```

- 如果位于本地作用域中，则 `vars()` 和 `locals()` 等效：

  ```python
  >>> def func():
  	print(vars() is locals())
  
  	
  >>> func()
  True
  ```

  tiap：不要手动修改本地字典中的内容。因为就算对本地字典做出了修改，也并不会影响解释器所使用的本地变量和自由变量的值，在本地字典所做的修改均会被忽略。 

  ```python
  def vars_():
      a_field = 'orca'
      pprint(vars())
      vars()['a_field'] = "j35"
      pprint(vars())
      pprint(a_field)
      
  vars_()
  """Out:
  {'a_field': 'orca'}
  {'a_field': 'orca'}
  'orca'
  """
  ```

## \_\_dict\_\_

> object.\_\_dict\_\_
> A dictionary or other mapping object used to store an object’s (writable) attributes.

不是所有对象都有 `__dict__` 属性。

例如，当我们在类中添加了 `__slots__` 属性后，该类的实例便不再拥有 `__dict__` 属性：

```python
>>> class Foo(object):
	__slots__ = ('bar', )

>>> Foo.__dict__
mappingproxy({'__module__': '__main__', '__slots__': ('bar',), 'bar': <member 'bar' of 'Foo' objects>, '__doc__': None})
>>> Foo().__dict__
Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    Foo().__dict__
AttributeError: 'Foo' object has no attribute '__dict__'
```

另外，许多内置类型的实例并没有 `__dict__` 属性：

```python
>>> vars([1,2])
Traceback (most recent call last):
  File "<pyshell#16>", line 1, in <module>
    vars([1,2])
TypeError: vars() argument must have __dict__ attribute
```



## MappingProxyType

🔨 class types.[MappingProxyType](https://docs.python.org/3.7/library/types.html#types.MappingProxyType)(*mapping*)

该构造函数会创建一个基于 *mapping* 的只读代理对象。此代理对象会提供 *mapping* 条目的动态视图，这意味着当 *mapping* 发生变化时，在代理对象中也会表现出同样的变化。

```python
>>> from types import MappingProxyType
>>> a_map = dict(a='orca',b='j35')
>>> proxy_map = MappingProxyType(a_map)
>>> proxy_map
mappingproxy({'a': 'orca', 'b': 'j35'})
>>> a_map['c'] = 'update'
>>> proxy_map # 代理对象会自动更新视图
mappingproxy({'a': 'orca', 'b': 'j35', 'c': 'update'})
```

MappingProxyType 是 Py 3.3 中添加的新功能，支持下列操作：

- `key in proxy`

  Return `True` if the underlying mapping has a key *key*, else `False`.

- `proxy[key]`

  Return the item of the underlying mapping with key *key*. Raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) if *key* is not in the underlying mapping.

- `iter(proxy)`

  Return an iterator over the keys of the underlying mapping. This is a shortcut for `iter(proxy.keys())`.

- `len(proxy)`

  Return the number of items in the underlying mapping.

- `copy`()

  Return a shallow copy of the underlying mapping.

- `get`(*key*[, *default*])

  Return the value for *key* if *key* is in the underlying mapping, else *default*. If *default* is not given, it defaults to `None`, so that this method never raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError).

- `items`()

  Return a new view of the underlying mapping’s items (`(key, value)` pairs).

- `keys`()

  Return a new view of the underlying mapping’s keys.

- `values`()

  Return a new view of the underlying mapping’s values.

如果尝试修改代理对象，则会抛出异常：

```python
>>> from types import MappingProxyType
>>> a_map = dict(a='orca',b='j35')
>>> proxy_map = MappingProxyType(a_map)
>>> proxy_map['a'] = 'whale'
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    proxy_map['a'] = 'whale'
TypeError: 'mappingproxy' object does not support item assignment
```





