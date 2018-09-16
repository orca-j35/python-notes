# Old-Style vs. New-Style Classes

https://docs.python.org/2/reference/datamodel.html#new-style-and-classic-classes

在 Python 中，类(class)和实例(instance)可被划分为两种风格：old-style (classic) 和 new-style。

在 Python 2.1 及其之前，只有旧式(*old-style*)类可用，并且 "类(*class*)" 和 "类型(*type*)" 是两个完全不相干的概念。在旧式实例 x 中，`x.__class__` 表示 x 的类(*class*) ；而 `type(x)` 的返回值表示 x 的类型(*type*)，且始终是 `<type 'instance'>`。由此可见，所有旧式实例与他们的类之间是相互独立的，旧式实例统一由一个独立的内置类型实现，即  `types.InstanceType` (也称为 `"<type 'instance'>"`)

```python
>>> # in Python 2.7
>>> class OldCls: pass

>>> OldCls().__class__
<class __main__.OldCls at 0x0000000003E73408>
>>> type(OldCls())
<type 'instance'>

>>> from types import *
>>> str(InstanceType)
"<type 'instance'>"

>>> # 旧式实例均通过InstanceType实现
>>> old_inst = InstanceType(OldCls)
>>> old_inst.__class__
<class __main__.OldCls at 0x0000000003B23408>
>>> type(old_inst)
<type 'instance'>
```

新式(*New-style*)在 Python 2.2 中被引入，将 "类(*class*)" 和 "类型(*type*)" 的概念进行了统一，也就是说在新式类中 "类(*class*)" 和 "类型(*type*)" 是同义词，两者并没有任何区别。所以，我们可将一个新式类(*class*)视作一个自定义类型(*type*)。因此，对于某个新式类的实例 x 而言，`type(x)` 的返回值与`x.__class__` 完全相同。不过，我们通常会将术语 "类型(*type*)" 用于内置类型，而将术语 "类(*class*)" 用于自定义类。

```python
>>> type("hello")
<class 'str'>
>>> # 通常我们会说字符串是str类型(type)
>>> 
>>> class NewCls(object):pass

>>> type(NewCls())
<class '__main__.NewCls'>
>>> NewCls().__class__
<class '__main__.NewCls'>
>>> # 通常我们会说NewCls()是NewCls类(class)的实例，
>>> # 但本质上而言，新式类就是一个自定义类型(type)，
>>> # 因此，我们同样可以说NewCls()是NewCls类型，
```

注意，用户可修改 `x.__class__` 的值。

```python
>>> class NewCls(object):pass

>>> class NewCls_(object):pass

>>> x = NewCls()
>>> type(x)
<class '__main__.NewCls'>
>>> x.__class__ = NewCls_
>>> type(x)
<class '__main__.NewCls_'>
```

引入新式类的主要动机是为了提供具有完整元模型(meta-model)的统一对象模型。新式类还具备许多实用功能：可将大多数内置类型子类化、引入了"描述符(*descriptors*)"等。

在 Python 2 中为了保证兼容性，如果没有显式继承任何类，则默认创建旧式类；如果显式继承了任何新式类(即类型)则创建新式类；如果显示继承"顶级类型" object 也可创建新式类。

```python
>>> # in Python2.7
>>> # 默认创建旧式类
>>> class OldCls: pass

>>> type(OldCls)
<type 'classobj'>

>>> # 创建新式类
>>> class NewCls(object):pass

>>> type(NewCls)
<type 'type'>
```

新式类和旧式类除了 `type()` 的返回值不同以外，两者在许多重要的细节上也拥有完全不同的行为。"新对象模型"与"旧对象模型"相比，一些行为拥有根本性的差异，比如调用特殊方法的方式。另外，"新对象模型"还对之前的部分行为进行"修正(fixes)"，比如在多重继承中的方法解析顺序。

在 Python 3 中移除了旧式类，仅保留新式类，即使没有显式继承任何类，也默认创建新式类，并始终继承自 object。

```python
>>> # in Python3.7
>>> class Cls:pass

>>> type(Cls)
<class 'type'>
```

扩展阅读： https://www.python.org/doc/newstyle/