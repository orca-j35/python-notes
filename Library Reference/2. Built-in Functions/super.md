# super

[TOC]

## 调用父类中的方法

子类中的方法会覆盖父类中的同名方法，如果需要调用父类中的方法，可以采用以下两种方式：

1. 通过父类名称来调用父类中方法：

   ```
   <parent class name>.<method name>(self, <other arguments>)
   ```

2. 构造一个 super 对象，并通过该对象调用父类中的方法。这种方法的优点在于无需显式引用父类，从而使代码更容易维护；并且在"钻石形"多继承的类层次结构中可避免重复调用父类中的方法。

在单继承的类层次结构中，上述两种方法并没有太显著的区别。`super` 的优点在于无需显式引用父类，从而使代码更容易维护。比如，在子类中调用父类的 `__init__()` 方法，以确保正确初始化：

```python
class Base:
    def __init__(self, arg):
        print('Base.__init__')

class A(Base):
    def __init__(self, arg):
        Base.__init__(self, arg) # 等效于 super().__init__(arg)
        print('A.__init__')
```

在"钻石形"多继承的类层次结构中，如果直接引用父类名称，则可能会重复调用父类中的方法。比如，考虑如下的情况： 

```python
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')

class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')

class C(A,B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
```

如果你运行这段代码就会发现 `Base.__init__()` 被调用两次，如下所示： 

```python
>>> c = C()
Base.__init__
A.__init__
Base.__init__
B.__init__
C.__init__
>>>
```

两次调用 `Base.__init__()` 通常没有什么坏处，但有时却会出现意外。如果我们在代码中使用 `super()`，则可避免重复调用的问题：

```python
class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A,B):
    def __init__(self):
        super().__init__()  # Only one call to super() here
        print('C.__init__')
```

运行这个新版本后，你会发现每个 `__init__()` 方法只会被调用一次了： 

```python
>>> c = C()
Base.__init__
B.__init__
A.__init__
C.__init__
>>>
```

为了弄清 `super()` 的原理，这里需要补充一个知识点：方法解析顺序(MRO) 

## what's MRO

方法解析顺序(Method Resolution Order - **MRO**)，是一种在多重继承中用于确定方法搜索顺序的算法，又称 C3 超类线性化(superclass linearization)。Python 会计算出每一个类的 MRO 列表。一个类的 MRO 列表是一个包含了其继承链上所有基类的线性顺序列，并且列表中的每一项均保持唯一。 

我们不必深究这个算法的数学原理，它实际上就是合并所有父类的MRO列表并遵循如下三条准则：

- 子类会先于父类被检查
- 多个父类会根据它们在列表中的顺序被检查
- 如果对下一个类存在两个合法的选择，选择第一个父类

其实我们只需要知道 MRO 列表中类的顺序代表着类层次结构间的关系即可。

Python 中的相关属性如下：

- `class.__mro__` - 该属性用于存储 MRO 元组，以便在方法解析期间提供基类排序。该属性是动态的，每当继承层次更新时，该属性都可能发生改变。
- `class.mro()` - 通过元类(metaclass)可以覆盖此方法，以自定义类实例的方法解析顺序。该方法会在程序初始化时调用，其结果存储在 [`__mro__`](https://docs.python.org/3.7/library/stdtypes.html#class.__mro__) 中。

Tips：在旧式类中，没有这两个属性

考虑如下类层次结构的 MRO 列表：

```python
class Base:
    def __init__(self):
        print('Base.__init__')
    def find(self):
        pass

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A,B):
    def __init__(self):
        super().__init__()  # Only one call to super() here
        print('C.__init__')
```

C 类的 MRO 列表如下：

```python
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,
<class '__main__.Base'>, <class 'object'>)
>>>
```

当需要在继承链中寻找某个属性时，Python会在 MRO 列表中从左到右开始查找各个基类，直到找到第一个匹配这个属性的类为止。比如，当我们调用 `C().find()` 后，会在 Base 类中找到该方法。

### 异常

如果 Python 无法为 MRO 创建一个线性化的列表，便会抛出异常。
例如，由于父类排序不当，便可能会抛出这样的异常。

```python
class Base(object): pass
class A(Base): pass
class B(Base, A): pass
```

因为 MRO 是在程序初始化时完成的，所以只要试图加载程序，编译器便会抛出异常：

```python
Traceback (most recent call last):
  File "c:/Users/iwhal/Desktop/PyTest/mro学习.py", line 11, in <module>
    class B(Base, A):
TypeError: Cannot create a consistent method resolution
order (MRO) for bases Base, A
```

另外，并列的基类间也需要遵循相同的顺序，否则也回抛出异常。例如下面的 A 类和 B 类，如果它们的基类排序不一致，则会抛出异常。

```python
class Base_1: pass
class Base_2: pass
class A(Base_2, Base_1): pass
class B(Base_1, Base_2): pass
class C(A, B): pass
```

### 扩展阅读

- [Method Resolution Order](https://python-history.blogspot.com/2010/06/method-resolution-order.html)
- [The Python 2.3 Method Resolution Order](https://www.python.org/download/releases/2.3/mro/)
  - [Python的MRO算法(The Python 2.3 Method Resolution Order-翻译)](https://sq.163yun.com/blog/article/181102632228446208)
  - [python2.3方法解析顺序（译）](http://www.nanerbang.com/article/40/)
- [wiki/C3_linearization](https://en.wikipedia.org/wiki/C3_linearization)

## what's super

super([*type1*[, *object-or-type2*]])

`super` 仅支持继承自 `object` 的新式类。

该内置函数本质上是 super 类的构造函数，用于创建一个 super 实例。通过 super 实例可调用 "游标类(*type1*)" 的父类或兄弟类[^1]中的方法。super 类的构造函数大致如下：(这里只为了是方便理解，真正的实现过程并非如此)

```python
class super:
    def __init__(self, type1, objc_or_type2=None):
        """
        :param type1:游标类，用于标记MRO列表搜索的起点
        :param objc_or_type2:被绑定实例或类
        """
        if objc_or_type2 is not None:
            """构造一个已绑定的super实例"""
            if isinstance(objc_or_type2, type1):
                # 游标类
                self._cursor = type1
                # 被绑定的实例对象 objc_or_type2
                self._instance = objc_or_type2
                # 被绑定的类对象 objc_or_type2.__class__
                self._cls = objc_or_type2.__class__
                # 获取MRO列表 
                self._mro = self._cls.__mro__
            elif issubclass(objc_or_type2, type1):
                # 游标类
                self._cursor = type1
                # 被绑定的类对象，由于缺少实例，所以不支持实例方法调用
                self._cls = objc_or_type2
                # 获取MRO列表
                self._mro = objc_or_type2.__mro__
            else:
                raise TypeError("super(type, obj): \
                    obj must be an instance or subtype of type")
        else:
            """构造一个未绑定的super实例"""
            pass
```

这里需要特别注意"游标类"、"被绑定的实例对象"(`self._instance`)、"被绑定的类对象"(`self._cls`)和 MRO 列表(`self._mro`)，下面会详细阐述 super 对象这三个参数是如何协作的。

### 1. super(type1, obj)

当 `objc_or_type2` 是一个实例对象时：

```python
# 双参数形式可用于任何地方，不限于类方法。
super(type1, obj) -> 
bound super object; requires isinstance(obj, type1) == True
# 无参数形式仅用在类方法中，因为编译器会根据其所在的类来填写剩余的两个参数。
super() -> same as super(self.__class__, self)
```

下面给出一个简单的类层次结构，并且在类外部展示通过 super 实例调用各种方法的过程。

```python
class A:
    class_field = "A类的类字段"

    def __init__(self):
        print("A -> __init__")
        self._field = "_instance_A"

    def instance_method(self):
        print(self._field)

    @classmethod
    def class_method(cls):
        print("类名:", cls.__name__)

    @staticmethod
    def static_method():
        print("A_staticmethod")

class X:pass

class B(X,A):
    class_field = "B类的类字段"

    def __init__(self):
        print("B -> __init__")
        self._field = "_instance_B"
```

构造 super 实例 `super_objc` ：

```python
>>> b_objc = B() # 构造 B 类实例，初始化实例字段
B -> __init__
>>> super_objc = super(B,b_objc) 
# super_objc实例的"被绑定的实例对象"：super_objc._instance=b_objc
# super_objc实例的"被绑定的类对象"：super_objc._cls=B
```

通过 `super_objc` 调用**实例方法**时，`super_objc` 会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有该实例方法，便会将该类的此实例方法绑定到`b_objc` 中；如果没有类拥有此方法，则抛出 `AttributeError`。

比如，在调用 `super_objc.instance_method()` 后，类 A 是 MRO 列表中游标类之后第一个拥有该方法的类(虽然类 X 在类 A 之前，但它没有该实例方法)，便会将`A.instance_method` 绑定到 `b_objc` 中(假设绑定后会在 `b_objc` 中创建一个名为 `A_inst_methd` 的实例方法)。然后再会调用 `b_objc.A_inst_methd()` ， 此时 `A_inst_methd()` 将 `b_objc` 实例作为第一参数使用，也就是说 `A_inst_methd()`  会套用 `b_objc` 的实例属性。完成调用后会删除该绑定方法。

```python
>>> super_objc.instance_method()
_instance_B # 实例方法使用b_objc作为第一参数，因此会输出b_objc的实例字段
>>> super_objc.instance_method
<bound method A.instance_method of <__main__.B object at 0x0000029269780AC8>>
```

通过 `super_objc` 调用**类方法**时，`super_objc` 会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有此类方法，便会将该类的此类方法绑定到`b_objc` 中；如果没有类拥有此方法，则抛出 `AttributeError`。

比如，在调用 `super_objc.class_method()` 后，类 A 是 MRO 列表中游标类之后第一个拥有该方法的类(虽然类 X 在类 A 之前，但没有该类方法)，便会将`A.class_method` 绑定到 B 类中(假设绑定后会在 B 类中创建一个名为 `A_clas_methd ` 的类方法)。然后再会调用 `B.A_clas_methd()` ， 此时 `A_clas_methd()` 中被省略的第一参数 `cls` 指向 B 类，也就是说 `A_clas_methd()` 将 B 类作为第一参数使用。完成调用后会删除该绑定方法。

```python
>>> super_objc.class_method()
类名: B # 实例方法使用B类作为第一参数，因此会输出B类的类字段
>>> super_objc.class_method
<bound method A.class_method of <class '__main__.B'>>
```

通过 `super_objc` 调用**静态方法**时，`super_objc` 会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有此静态方法，便会直接调用该类的此静态方法，不会进行绑定；如果没有类拥有此方法，则抛出 `AttributeError`。

```python
>>> super_objc.static_method()
A_staticmethod
>>> super_objc.static_method
<function A.static_method at 0x00000292697CFEA0>
```

通过 `super_objc` 调用**类字段**时，`super_objc` 会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有此类字段，便会直接返回该类的该类字段，不会进行绑定；如果没有类拥有此方法，则抛出 `AttributeError`。

```python
>>> super_objc.class_field
'A类的类字段'
```

### 2. super(type1, type2)

当 `objc_or_type2` 是一个类时：

```python
# 双参数形式可用于任何地方，不限于类方法。
super(type1, type2) -> 
bound super object(this is useful for classmethod and staticmethod); requires issubclass(type2, type1) == True
```

下面给出一个简单的类层次结构，并且在类外部展示通过 super 实例调用各种方法的过程。由于只有"被绑定的类对象"(`self._cls`)，所以 super 对象无法调用实例方法，因此这里省略掉类实例方法。

```python
"""类层次结构"""
class A():
    class_field = "A类的类字段"
    @classmethod
    def class_method(cls):
        print("类名:", cls.__name__)

    @staticmethod
    def static_method():
        print("A_staticmethod")

class X:pass

class B(X,A):
    class_field = "B类的类字段"

```

构造 super 实例 `super_objc` ：

```python
>>> super_objc = super(B,B)
# super_objc实例的"绑定实例对象"：没有
# super_objc实例的"绑定类对象"：super_objc._cls=B
```

通过 `super_objc` 调用**类方法**时，`super_objc` 会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有此类方法，便会将该类的此类方法绑定到 B 类中；如果没有类拥有此方法，则抛出 `AttributeError`。

比如，在调用 `super_objc.class_method()` 后，类 A 是 MRO 列表中游标类之后第一个拥有该方法的类(虽然类 X 在类 A 之前，但没有该类方法)。便会将`A.class_method` 绑定到 B 类中(假设绑定后会在 B 类中创建一个名为 `A_clas_methd ` 的类方法)。然后再会调用 `B.A_clas_methd()` ， 此时 `A_clas_methd()` 将类 B 作为第一参数使用，也就是说 `A_inst_methd()`  会套用 B 的类属性。完成调用后会删除该绑定方法。

```python
>>> super_objc.class_method()
类名: B # 实例方法使用B类作为第一参数，因此会输出B类的类字段
>>> super_objc.class_method
<bound method A.class_method of <class '__main__.B'>>
```

通过 `super_objc` 调用**静态方法**时，`super_objc` 会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有此静态方法，便会直接调用该类的此静态方法，不会进行绑定；如果没有类拥有此方法，则抛出 `AttributeError`。

```python
>>> super_objc.static_method()
A_staticmethod
>>> super_objc.static_method
<function A.static_method at 0x00000292697CFEA0>
```

通过 `super_objc` 调用**类字段**时，`super_objc` 会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有此类字段，便会直接返回该类的该类字段，不会进行绑定；如果没有类拥有此方法，则抛出 `AttributeError`。

```python
>>> super_objc.class_field
'A类的类字段'
```

### 3. super(type1)

当 `objc_or_type2` 为空时：

```python
super(type1) -> unbound super object
```

第二参数的默认值为是 `None`。

### 4. 只用第一个

super 对象会在 MRO 列表中依次查找游标类之后的各个类，谁第一个拥有目标方法，便会将该类的此方法绑定到 `self._instance` 或 `self._cls` 中(注：静态方法直接调用，不会绑定)，然后通过 `self._instance` 或 `self._cls` 调用被绑定的方法，剩余的类都会被忽略；如果游标类之后的所有类都不包含目标方法，则抛出 `AttributeError`。

```python
class A():
    def func(self):
        print ("enter A")

class B():
    def func(self):
        print ("enter B")

class C(A, B):
    def func(self):
        print ("enter C")
        super().func()
```

只有 A 类中的 `func` 方法会被绑定到 C 类实例中，并且会通过 C 类实例调用该绑定方法。尽管 B 类也拥有 `func` 方法，但不会被用到。

```python
>>> C().func()
enter C
enter A
```

如果需要同时调用 B 类中的方法，则需要将继承关系修改为：

```python
class A():
    def func(self):
        print ("enter A")
        super().func()

class B():
    def func(self):
        print ("enter B")

class C(A, B):
    def func(self):
        print ("enter C")
        super().func()
```

验证：

```python
>>> C().func()
enter C
enter A
enter B
```

### 4. 改变游标类

下面的代码展示了一个典型的"钻石型"多继承的类层次结构。

```python
class Base(object):
    def func(self):
        print ("enter Base")

class A(Base):
    def func(self):
        print ("enter A")

class B(Base):
    def func(self):
        print ("enter B")

class C(A, B):
    def func(self):
        print ("enter C")
```

继承关系链如下：

```
	  Base
      /  \
     /    \
    A      B
     \    /
      \  /
       C
```

C 类的 MRO 列表如下：

```python
[<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>, <class '__main__.Base'>, <class 'object'>]
```

通过改变游标类(*type1*) ，便会改变 MRO 列表的搜索起点，游标类之前的类会被忽略。下面这个示例中，我们将游标类改为 B 类，则会使用 Base 中的 `func` 方法。

```python
>>> super(B,C()).func()
enter Base
```

### 6. 其他提醒

注意，如果 MRO 中游标类之后的类中包含 `__getitem__` 方法，那么 super 对象支持显式调用 `super().__getitem__(name)`，但并不支持隐式调用(如 `super()[name]`)。因为，`super().__getattribute__()` 会拦截 `__getitem__` ，并在其内部处理 `__getitem__`。但 super 对象并没有独立实现 `__getitem__` 方法，所以并不支持 `super()[name]` 。

```python
class A():
    def func(self):
        print ("enter A")
        super().func()
    def __getitem__(self,name):
        print(name)


class C(A):
    def func(self):
        print ("enter C")
        super().func()
```

测试：

```python
>>> A()[2]
2
>>> super(C,C()).__getitem__(2)
2
>>> super(C,C())[2]
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    super(C,C())[2]
TypeError: 'super' object is not subscriptable
>>> 
```

通过 `help` 函数，我们可以查看 `super` 的文档信息，以了解其包含的方法。

```
>>> help(super)
Help on class super in module builtins:

class super(object)
 |  --snip--
 |  Methods defined here:
 |  
 |  __get__(self, instance, owner, /)
 |      Return an attribute of instance, which is of type owner.
 |  
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |  
 |  __init__(self, /, *args, **kwargs)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __new__(*args, **kwargs) from builtins.type
 |      Create and return a new object.  See help(type) for accurate signature.
 |  
 |  __repr__(self, /)
 |      Return repr(self).
 |  --snip--
```

## 参考

- [8.7 调用父类方法 - python3_cookbook](http://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p07_calling_method_on_parent_class.html#id1)
- [你不知道的 super - Python 之旅](https://funhacks.net/explore-python/Class/super.html)
- [深入super，看Python如何解决钻石继承难题](https://www.cnblogs.com/testview/p/4651198.html)
- [Python内置函数(63)——super](https://www.cnblogs.com/sesshoumaru/p/6120517.html)
- [Python’s super() considered super!](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/) 
  - [深入思考python的super()](https://blog.csdn.net/tab_space/article/details/50506138) - 译
- [How does Python's super() work with multiple inheritance? - stackoverflow](https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance)

注脚：

[^1]: [What is a sibling class in Python?](https://stackoverflow.com/questions/27954695/what-is-a-sibling-class-in-python)

