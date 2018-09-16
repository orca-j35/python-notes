# Old-Style vs. New-Style Classes

[TOC]

## 1. 概述

在 Python 中，类(class)和实例(instance)可被划分为两种风格：old-style (classic) 和 new-style。[^3]

在 Python 2 中为了保证兼容性，同时存在旧式类和新式类。

- 如果继承列表为空，便会创建一个旧式类；
- 如果继承旧式类，便会创建一个旧式类。
- 如果继承"顶级类型" object，便会创建一个新式类；
- 如果继承新式类(类型)，便会创建一个新式类。

在 Python 3 中移除了旧式类，仅保留新式类。如果继承列表为空，便会创建一个继承自 object 的新式类。

tips: 在 Python 2 和3 中[内置类型](https://docs.python.org/3.7/library/stdtypes.html)均是新式类。

```python
>>> type(int)
<type 'type'>
>>> type(list)
<type 'type'>
```

## 2. Old-Style

在 Python 2.1 及其之前，只有旧式(*old-style*)类可用，并且 "类(*class*)" 和 "类型(*type*)" 是两个完全不相干的概念。

### 2.1 旧式类

> classic class (in [Glossary of Python 2](https://docs.python.org/2/glossary.html#term-new-style-class))
>
> Any class which does **not inherit** from [`object`](https://docs.python.org/2/library/functions.html#object). See [new-style class](https://docs.python.org/2/glossary.html#term-new-style-class). Classic classes have been removed in Python 3.

在旧式类 OldCls 中，没有 `__class__` 属性。`type(OldCls)` 的返回值表示 OldCls 的类型(*type*)，且始终是 `<type 'classobj'>`。由此可见，旧式类统一由一个独立的内置类型实现，即 `types.ClassType` (也称为 `<type 'classobj'>`)。

如果旧式类没有显式继承任何旧式类，则其父类列表 `__bases__` 为空。

```python
>>> # in Python 2.7
>>> class OldCls: pass

>>>  # 旧式类没有__class__属性
>>> type(OldCls)
<type 'classobj'>
>>> OldCls.__bases__
()
>>> import types
>>> types.ClassType
<type 'classobj'>
```

#### a. ClassType in Python 2

[types.ClassType](https://docs.python.org/2/library/types.html#types.ClassType) 是 Python 2 中特有的内置类型，在 types 模块中的定义如下：

```python
'''在Python2的types模块中，ClassType的定义如下'''
class _C:  # _C是旧式类
    def _m(self): pass
ClassType = type(_C)
```

`types.ClassType` 是继承自 object 的**新式类(类型)**，其类型是 type：

```python
>>> # in Python 2.7
>>> import types
>>> types.ClassType
<type 'classobj'>
>>> types.ClassType.__bases__
(<type 'object'>,)
>>> type(types.ClassType)
<type 'type'>
>>> types.ClassType is type
False
```

`types.ClassType` 是旧式类的元类，负责构造旧式类。所以，用户定义的旧式类的类型均是 `<type 'classobj'>`。另外，该类型也可构造新式类。

```python
>>> # in Python 2.7
>>> # types.ClassType构造旧式类
>>> OldCls = types.ClassType('Other_OldCls', tuple(), dict())
>>> type(OldCls)
<type 'classobj'>
>>> OldCls.__bases__
()
>>> # types.ClassType也可构造新式类，此时和type等效
>>> NewCls = types.ClassType('X', tuple((object,)), dict())
>>> type(NewCls)
<type 'type'>
>>> NewCls.__bases__
(<type 'object'>,)
>>>
>>> # type只能构造新式类，若第二参数为空，则默认继承object
>>> Other_NewCls = type('X', tuple(), dict())
>>> Other_NewCls.__class__
<type 'type'>
>>> Other_NewCls.__bases__
(<type 'object'>,)
```

`types.ClassType` 不可以被继承，不能基于 `types.ClassType` 派生自定义元类。

```python
>>> class Metaclass(types.ClassType):pass

Traceback (most recent call last):
  File "<pyshell#31>", line 1, in <module>
    class Metaclass(types.ClassType):pass
AttributeError: module 'types' has no attribute 'ClassType'
```

### 2.2 旧式实例

对于某个旧式类的实例 x 而言，`x.__class__` 表示 x 的类(*class*) ；而 `type(x)` 的返回值表示 x 的类型(*type*)，且始终是 `<type 'instance'>`。由此可见，所有旧式实例与他们的类之间是相互独立的，旧式实例统一由一个独立的内置类型实现，即 `types.InstanceType`(也称为 `"<type 'instance'>"`)

```python
>>> # in Python 2.7
>>> class OldCls: pass

>>> OldCls().__class__
<class __main__.OldCls at 0x0000000003E73408>
>>> type(OldCls())
<type 'instance'>

>>> from types import *
>>> InstanceType
"<type 'instance'>"

>>> # 旧式实例均通过InstanceType构造
>>> old_inst = InstanceType(OldCls)
>>> old_inst.__class__
<class __main__.OldCls at 0x0000000003B23408>
>>> type(old_inst)
<type 'instance'>
```

#### a. InstanceType in Python 2

[types.InstanceType](https://docs.python.org/2/library/types.html#types.InstanceType) 是 Python 2 中特有的内置类型，在 types 模块中的定义如下：

```python
'''在types模块中，InstanceType的定义如下'''
class _C: # _C是旧式类
    def _m(self): pass
_x = _C()
InstanceType = type(_x)
```

`types.InstanceType` 是继承自 object 的**新式类(类型)**，其类型是 type，**不能被继承**：

```python
>>> # in Python 2.7
>>> import types
>>> types.InstanceType
<type 'instance'>
>>> types.InstanceType.__bases__
(<type 'object'>,)
>>> type(types.InstanceType)
<type 'type'>
```

通过 `types.InstanceType` 可为**旧式类**构造实例，但不会主动调用实例的 `__init__` 函数。所以，用户定义旧式类的实例的类型均是 `<type 'instance'>`：

```python
>>> in Python 2.7
>>> class OldCls:
    def __init__(self, a_str):
        self.a_str = a_str

>>> insts = OldCls("hello")
>>> type(insts)
<type 'instance'>
>>> insts.__class__
<class __main__.OldCls at 0x00000000040B4CA8>

>>> # types.InstanceType仅构造旧式类的实例，不会主动调用实例的__init__方法
>>> Other_insts = types.InstanceType(OldCls)
>>> type(Other_insts)
<type 'instance'>
>>> Other_insts.__class__
<class __main__.OldCls at 0x00000000040B4CA8>
>>> Other_insts.__init__("whale")
>>> Other_insts.a_str
'whale'
```

## 3. New-Style

新式(*New-style*)在 Python 2.2 中被引入，将 "类(*class*)" 和 "类型(*type*)" 的概念进行了统一，也就是说在新式类中 "类(*class*)" 和 "类型(*type*)" 是同义词，两者并没有任何区别。所以，我们可将一个新式类(*class*)视作一个自定义类型(*type*)。因此，对于某个新式类的实例 x 而言，`type(x)` 的返回值与`x.__class__` 完全相同。

虽然 "类(*class*)" 和 "类型(*type*)" 是同义词，但我们通常会将术语 "类型(*type*)" 用于内置类型，而将术语 "类(*class*)" 用于自定义类。

```python
>>> type("hello")
<class 'str'>
>>> # 通常我们会说字符串是str类型
>>> 
>>> class NewCls(object):pass

>>> type(NewCls())
<class '__main__.NewCls'>
>>> NewCls().__class__
<class '__main__.NewCls'>
>>> # 通常我们会说NewCls()是NewCls类的实例，
>>> # 但本质上而言，新式类就是一个自定义类型，
>>> # 因此，我们同样可以说NewCls是其实例的类型，
```

### 3.1 新式类

> new-style class (in [Glossary of Python 2](https://docs.python.org/2/glossary.html#term-new-style-class))
>
> Any class which inherits from [`object`](https://docs.python.org/2/library/functions.html#object). This includes all built-in types like `list` and [`dict`](https://docs.python.org/2/library/stdtypes.html#dict). Only new-style classes can use Python's newer, versatile features like `__slots__`, descriptors, properties, and [`__getattribute__()`](https://docs.python.org/2/reference/datamodel.html#object.__getattribute__), class methods, and static methods.

对于新式类 NewCls 而言，其类型(或类)始终是 `<type 'type'>`。由此可见，新式类统一由一个独立的内置类型实现，即 type (也称为 `<type 'type'>`)。

```python
>>> class NewCls(object):pass

>>> NewCls.__class__
<type 'type'>
>>> type(NewCls)
<type 'type'>
```

#### a. type in Python

type 本身是继承自 object 的**新式类(类型)**，其类型也是 type。Python 2 和 3 均包含 type 类型(类)。tips: 在 Python 2 中 [types.TypeType](https://docs.python.org/2/library/types.html#types.TypeType) 是 type 的别名。

```python
>>> type(type)
<type 'type'>
>>> type.__bases__
(<type 'object'>,)
```

用户定义的新式类的类型均为 type，内置类型的类型也是 type。

```python
>>> # 用户定义的新式类的类型均为 type
>>> class NewCls(object):pass

>>> type(NewCls)
<type 'type'>
>>> # 内置类型的类型也是 type
>>> type(int)
<type 'type'>
>>> type(list)
<type 'type'>
```

type 是新式类的元类，负责构造新式类：

```python
>>> # type只能构造新式类，若第二参数为空，则默认继承object
>>> NewCls = type('X', tuple(), dict())
>>> NewCls.__class__
<type 'type'>
>>> NewCls.__bases__
(<type 'object'>,)
```

type 可以被继承，我们可以基于 type 派生自定义元类。

### 3.2 新式实例

对于某个新式类的实例 x 而言，其类(或类型)始终是该新式类。不同于旧式类，新式类的实例不再由特定类型创建，而是由新式类自己创建。

```python
>>> class NewCls(object):pass

>>> type(NewCls())
<class '__main__.NewCls'>
>>> NewCls().__class__
<class '__main__.NewCls'>
```

## 4. 重要差异

引入新式类的主要动机是为了提供具有完整元模型(meta-model)的统一对象模型。新式类还具备许多实用功能：可将大多数内置类型子类化、引入了"描述符(*descriptors*)"等。

新式类和旧式类除了 `type()` 的返回值不同以外，两者在许多重要的细节上也拥有完全不同的行为。"新对象模型"与"旧对象模型"相比，一些行为拥有根本性的差异，比如调用特殊方法的方式。另外，"新对象模型"还对之前的部分行为进行"修正(fixes)"，比如在多重继承中的方法解析顺序。

新式类较旧式类的重要差异如下：[^1] [^2]

- 内置函数 `super` 仅支持新式类
- 新式类支持描述符([descriptors](http://docs.python.org/2/howto/descriptor.html))，可阅读 [【译】Python描述符指南](https://harveyqing.gitbooks.io/python-read-and-write/content/python_advance/python_descriptor.html)
- 新式类支持装饰器(decorators) - introduced in Python 2.4
- 新式类支持静态方法和类方法
- 新式类增加了 `__new__` 方法
- 新式类增加了 [`__getattribute__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getattribute__) 方法
- 新式类增加了 [`__slots__`](http://docs.python.org/2/reference/datamodel.html#slots) 方法
- properties (computed attributes)

- MRO 的算法更新，可阅读 [Method Resolution Order - Python 见闻志](https://harveyqing.gitbooks.io/python-read-and-write/content/python_advance/method_resolution_order.html) 

  **Classic classes** do a depth first search from left to right. Stop on first match. They do not have the `__mro__` attribute.

  ```python
  class C: i = 0
  class C1(C): pass
  class C2(C): i = 2
  class C12(C1, C2): pass
  class C21(C2, C1): pass
  
  assert C12().i == 0
  assert C21().i == 2
  
  try:
      C12.__mro__
  except AttributeError:
      pass
  else:
      assert False
  ```

  **New-style classes**

  ```python
  class C(object): i = 0
  class C1(C): pass
  class C2(C): i = 2
  class C12(C1, C2): pass
  class C21(C2, C1): pass
  
  assert C12().i == 2
  assert C21().i == 2
  
  assert C12.__mro__ == (C12, C1, C2, C, object)
  assert C21.__mro__ == (C21, C2, C1, C, object)
  ```

- 在抛出异常时，可使用任意旧式类，但只能使用继承自 `Exception` 的新式类。

  ```python
  # in Python 2.7
  # OK, old:
  class Old: pass
  try:
      raise Old()
  except Old:
      pass
  else:
      assert False
  
  # TypeError, new not derived from `Exception`.
  class New(object): pass
  try:
      raise New()
  except TypeError:
      pass
  else:
      assert False
  
  # OK, derived from `Exception`.
  class New(Exception): pass
  try:
      raise New()
  except New:
      pass
  else:
      assert False
  
  # `'str'` is a new style object, so you can't raise it:
  try:
      raise 'str'
  except TypeError:
      pass
  else:
      assert False
  ```



## 5. 扩展阅读

- https://wiki.python.org/moin/NewClassVsClassicClass

- https://www.python.org/doc/newstyle/


## 6. 注脚

[^1]: [What is the difference between old style and new style classes in Python?](https://stackoverflow.com/questions/54867/what-is-the-difference-between-old-style-and-new-style-classes-in-python)
[^2]: [The Inside Story on New-Style Classes](http://python-history.blogspot.com/2010/06/inside-story-on-new-style-classes.html) 
[^3]: [3.3. New-style and classic classes](https://docs.python.org/2/reference/datamodel.html#new-style-and-classic-classes)



