# dir

## dir()

🔨 dir()

如果实参为空，则会返回一个由当前本地作用域中的变量名组成的**已排序列表**，列表中的项与 `locals().keys()` 或 `vars().keys()` 中的项相同。

```python
print(dir())
print(sorted(vars().keys()))
print(sorted(locals().keys()))
def func():
    field = "orca_j35"
    print(dir())
    print(sorted(vars().keys()))
    print(sorted(locals().keys()))
func()
"""Out:
['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
['field']
['field']
['field']
"""
```

## dir(*object*)

🔨 dir(*object*)

如果将某个对象用作实参，则会尝试返回一个由 *object* 的有效属性组成的列表，并且该列表会按照字母表的顺序排序。根据 *object* 是否拥有 `__dir__()` 方法，可分为两种清理：

- 如果 *object* 拥有 `__dir__()` 的方法，`dir(object)` 便会调用 `object.__dir__()` 方法并返回其结果。`__dir__()` 方法须返回由 *object* 的属性组成的列表。对于实现了 [`__getattr__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getattr__) 或 [`__getattribute__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getattribute__) 的对象，我们可以通过自定义 `dir()` 的方式来报告对象的属性。

  ```python
  class Cls_(object):
      def __init__(self):
          self.attrs = dict()
  
      def __dir__(self):
          lists = super().__dir__() + list(self.attrs.keys())
          return lists
  
      def __getattr__(self, attr):
          if not self.attrs.get(attr):
              self.attrs[attr] = 'j35'
          return self.attrs[attr]
  
  
  x = Cls_()
  print(dir(x))
  x.orca
  print(dir(x))
  """Out:
  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__','__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'attrs']
  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__','__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'attrs', 'orca']
  """
  ```

- 如果 *object* 没有 `__dir__()` 的方法，dir(*object*) 则会尽力从 *object*.\_\_dict\_\_ (如果已定义) 和 type(*object*) 中收集信息。此时，dir(*object*) 返回的列表并不一定能完整描述 *object* 拥有的属性。当 *object* 包含 [`__getattr__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getattr__) 方式时，dir(*object*) 返回的结果也可能不能完整描述 *object* 拥有的属性。

  具体而言，`dir()` 的默认机制会对不同类型的对象会表现出不同的行为，因为 `dir()` 会尝试生成相关度最高的非完整信息。

  - 如果 *object* 是模块对象，则输出列表中将包含该模块中的属性名，即 `module.__dict__.keys()`；
  - 如果 *object* 是类(或类型)对象，则输出列表中将包含该类(或类型)对象中的属性名，并递归地包含其基类中的属性名。也就是说，会通过遍历该类(或类型)及其所有基类的 `__dict__` 来创建属性列表；
  - 如果 *object* 是实例对象，则输出列表中将包含 *object* 中的属性名，以及构造 *object* 的类中的属性名，并递归地包含其基类中的属性名。也就是说，会通过遍历该实例及其类(或类型)和所有基类的 `__dict__` 来创建属性列表。

示例：

```python
>>> import struct
>>> dir()   # show the names in the module namespace  # doctest: +SKIP
['__builtins__', '__name__', 'struct']
>>> dir(struct)   # show the names in the struct module # doctest: +SKIP
['Struct', '__all__', '__builtins__', '__cached__', '__doc__', '__file__',
 '__initializing__', '__loader__', '__name__', '__package__',
 '_clearcache', 'calcsize', 'error', 'pack', 'pack_into',
 'unpack', 'unpack_from']
>>> class Shape:
...     def __dir__(self):
...         return ['area', 'perimeter', 'location']
>>> s = Shape()
>>> dir(s)
['area', 'location', 'perimeter']
```

注意：由于提供 `dir()` 主要目的是为了方便在交互式提示符中使用，所以 `dir()` 会试图提供一组我们较为关注的名称，而非尝试提供严格或一致定义的名称集，并且 `dir()` 的行为细节可能在会在不同版本之间存在差异。例如，当类作为实参时，`dir()` 的输出列表中不会包含元类中的属性：

```python
class Meta(type):
    def method_of_meta(self):
        print("method_of_meta")

class Base(object, metaclass=Meta):
	def method_of_base(self):
        print("method_of_base")

print(dir(Base)) # 注意，输出结果中不包含元类中属性
"""Out:
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'method_of_base']
"""
```

### 实现细节

`dir(obj)` 会在内部调用 `type(obj).__dir__(obj)`，从而使用类字典中的 `__dir__()` 方法来获取属性列表。也就是说在获取属性列表时，会跳过实例字典：

```python
class Shape:
    def __dir__(self):
        return ['area', 'perimeter', 'location']
s = Shape()
def __dir__(self):
    return ['orca', 'j35']
from types import MethodType
print(dir(s))
s.__dir__ = MethodType(__dir__, s)
print(dir(s))
```

### \_\_dir\_\_

> Called when [`dir()`](https://docs.python.org/3.7/library/functions.html#dir) is called on the object. A sequence must be returned. [`dir()`](https://docs.python.org/3.7/library/functions.html#dir) converts the returned sequence to a list and sorts it.

`__dir__` 方法对子类同样有效

```python
class ClassA:
    num_A = 1
    def foo_A(self):
        pass
    def __str__(self):
        return 'this is ClassA'
    def __dir__(self):
        return ['height', 'color', '222']

class ClassB(ClassA):
    num_B = 2
    def __init__(self, name='ClassB'):
        self.name = name
    def foo_B(self):
        pass


objB = ClassB()
objB.grade = 123
```

### 缺少 \_\_dict\_\_ 的情况

> object.\_\_dict\_\_
> A dictionary or other mapping object used to store an object’s (writable) attributes.

不是所有对象都有 `__dict__` 字段，`vars()` 仅对拥有 `__dict__` 字段的对象有效，但即便没有 `__dict__` 属性，`dir()` 也可以生成属性列表，只不过此时类和实例的属性列表相同。

例如，当我们在类中添加了 `__slots__` 属性后，该类的实例便不再拥有 `__dict__` 属性，但 `dir()` 仍可以正常工作。

```python
>>> class Foo(object):
	__slots__ = ('bar', )

>>> Foo.__dict__
mappingproxy({'__module__': '__main__', '__slots__': ('bar',), 'bar': <member 'bar' of 'Foo' objects>, '__doc__': None})
>>> vars(Foo()) # 实例不再拥有__dict__属性
Traceback (most recent call last):
  File "<pyshell#10>", line 1, in <module>
    vars(Foo())
TypeError: vars() argument must have __dict__ attribute
>>> dir(Foo())
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', 'bar']
>>> dir(Foo)
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', 'bar']
```

许多内置类型的实例并没有 `__dict__` 属性，但 `dir()` 仍可以正常工作。

```python
>>> vars([1,2])
Traceback (most recent call last):
  File "<pyshell#16>", line 1, in <module>
    vars([1,2])
TypeError: vars() argument must have __dict__ attribute
>>> dir([1,2])
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```

## 参考

- [dir() 与 __dict__，__slots__ 的区别](https://www.cnblogs.com/ifantastic/p/3768415.html)
- [python 查看对象属性相关方法(__dict__, dir(), vars(), locals())](https://www.cnblogs.com/elie/p/6685413.html)
- [what's the biggest difference between dir and __dict__ in python](https://stackoverflow.com/questions/14361256/whats-the-biggest-difference-between-dir-and-dict-in-python)
- [Difference between dir(…) and vars(…).keys() in Python?](https://stackoverflow.com/questions/980249/difference-between-dir-and-vars-keys-in-python)



