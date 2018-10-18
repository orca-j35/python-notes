# type

[TOC]

内置函数 `type()` 其实是元类 `type` 的构造函数，有如下两种使用方式：

## class type(*object*)

🔨 type(*object*) -> the object's type

对于新式类，type(*object*) 的返回值通常与 [`object.__class__`](https://docs.python.org/3.7/library/stdtypes.html#instance.__class__) 相同。

```python
>>> # in Python 3
>>> type(3)
<class 'int'>

>>> type(['foo', 'bar', 'baz'])
<class 'list'>

>>> t = (1, 2, 3, 4, 5)
>>> type(t)
<class 'tuple'>

>>> class Foo: pass

>>> type(Foo())
<class '__main__.Foo'>
```

当我们需要测试某个对象的类型时，最好使用内置函数 `isinstance`，因为该函数会将子类也纳入测试范围。

```python
>>> type("hello") is str
True
>>> type("hello") is object
False
>>> isinstance("hello",object)
True
```

See also [Type Objects](https://docs.python.org/3.7/library/stdtypes.html#bltin-type-objects).

## class type(*name*, *bases*, *dict*)

🔨 type(*name*, *bases*, *dict*) -> a new type(or class) object：

- *name* : a string specifies a name of  new type(or class) object. This becomes the `__name__` attribute of the type(or class).
- *bases* : a tuple itemizes the base classes. This becomes the `__bases__` attribute of the type(or class).
- *dict* : a dictionary is the namespace containing definitions for class body . This becomes the `__dict__` attribute of the type(or class).

type(*name*, *bases*, *dict*) 是[**类定义语句**](https://docs.python.org/3.7/reference/compound_stmts.html#class-definitions)的动态形式。在保证参数一直的前提下，通过这两种方式构造出的类对象完全等效。，示例如下：

```python
>>> class X:
...     a = 1
...
>>> X = type('X', (object,), dict(a=1))
```

此示例中，创建类对象 `X` 的两种方式完全等效。

**Changed in version 3.6**: Subclasses of [`type`](https://docs.python.org/3.7/library/functions.html#type) which don't override `type.__new__` may no longer use the one-argument form to get the type of an object.

```python
>>> class type_(type): pass

>>> type_("hello")
Traceback (most recent call last):
  File "<pyshell#14>", line 1, in <module>
    type_("hello")
TypeError: type.__new__() takes exactly 3 arguments (1 given)
```

### Example 1

In this first example, the *bases*  and *dict* arguments passed to `type()` are both empty. No inheritance from any parent class is specified, and nothing is initially placed in the namespace dictionary. 

```python
>>> Foo = type('Foo', (), {})

>>> x = Foo()
>>> x
<__main__.Foo object at 0x04CFAD50>
```

`Foo` 类也可通过类定义语句构造，如下：(两种构造方式等效)

```python
>>> class Foo:
...     pass
...
>>> x = Foo()
>>> x
<__main__.Foo object at 0x0370AD50>
```

### Example 2

*bases*  is a tuple with a single element `Foo`, specifying the parent class that `Bar` inherits from. An attribute, `attr`, is initially placed into the namespace dictionary:

```python
>>> Bar = type('Bar', (Foo,), dict(attr=100))

>>> x = Bar()
>>> x.attr
100
>>> x.__class__
<class '__main__.Bar'>
>>> x.__class__.__bases__
(<class '__main__.Foo'>,)
```

`Bar` 类也可通过类定义语句构造，如下：(两种构造方式等效)

```python
>>> class Bar(Foo):
...     attr = 100
...

>>> x = Bar()
>>> x.attr
100
>>> x.__class__
<class '__main__.Bar'>
>>> x.__class__.__bases__
(<class '__main__.Foo'>,)
```

### Example 3

This time, *bases* is again empty. Two objects are placed into the namespace dictionary via the *dict*  argument. The first is an attribute named `attr` and the second a function named `attr_val`, which becomes a method of the defined class:

```python
>>> Foo = type(
...     'Foo',
...     (),
...     {
...         'attr': 100,
...         'attr_val': lambda x : x.attr
...     }
... )

>>> x = Foo()
>>> x.attr
100
>>> x.attr_val()
100
```

`Foo` 类也可通过类定义语句构造，如下：(两种构造方式等效)

```python
>>> class Foo:
...     attr = 100
...     def attr_val(self):
...         return self.attr
...

>>> x = Foo()
>>> x.attr
100
>>> x.attr_val()
100
```

### Example 4

Only very simple functions can be defined with [`lambda` in Python](https://dbader.org/blog/python-lambda-functions). In the following example, a slightly more complex function is defined externally then assigned to `attr_val` in the namespace dictionary via the name `f`:

```python
>>> def f(obj):
...     print('attr =', obj.attr)
...
>>> Foo = type(
...     'Foo',
...     (),
...     {
...         'attr': 100,
...         'attr_val': f
...     }
... )

>>> x = Foo()
>>> x.attr
100
>>> x.attr_val()
attr = 100
```

`Foo` 类也可通过类定义语句构造，如下：(两种构造方式等效)

```python
>>> def f(obj):
...     print('attr =', obj.attr)
...
>>> class Foo:
...     attr = 100
...     attr_val = f
...

>>> x = Foo()
>>> x.attr
100
>>> x.attr_val()
attr = 100
```

