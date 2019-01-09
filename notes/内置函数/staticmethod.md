# staticmethod
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记:﹝classmethod.md﹞

🔨 @staticmethod

```python
class staticmethod(object)
 |  staticmethod(function) -> method
```

Transform a method into a static method.

A static method does not receive an implicit first argument. To declare a static method, use this idiom:

```python
class C:
    @staticmethod
    def f(arg1, arg2, ...): 
        ...
```

The `@staticmethod` form is a function [decorator](https://docs.python.org/3.7/glossary.html#term-decorator) – see the description of function definitions in [Function definitions](https://docs.python.org/3.7/reference/compound_stmts.html#function) for details.

It can be called either on the **class** (such as `C.f()`) or on an **instance** (such as `C().f()`). The instance is ignored except for its class.

```python
class Cls(object):
    @staticmethod
    def sm(*args):
        print(*args)

# 类和实例均可调用
Cls.sm(1, 2)  #> 1 2
Cls().sm(1, 2)  #> 1 2

# 子类中也可正常工作
class SubCls(Cls):
    pass

SubCls.sm(1, 2)  #> 1 2
SubCls().sm(1, 2)  #> 1 2
```

Static methods in Python are similar to those found in Java or C++. Also see [`classmethod()`](https://docs.python.org/3.7/library/functions.html#classmethod) for a variant that is useful for creating alternate class constructors.

Like all decorators, it is also possible to call `staticmethod` as a regular function and do something with its result. This is needed in some cases where you need a reference to a function from a class body and you want to avoid the automatic transformation to instance method. For these cases, use this idiom:

```python
class C:
    builtin_open = staticmethod(open)
```

For more information on static methods, consult the documentation on the standard type hierarchy in [The standard type hierarchy](https://docs.python.org/3.7/reference/datamodel.html#types).

## 使用场景

The `@classmethod` and `@staticmethod` decorators are used to define methods inside a class namespace that are not connected to a particular instance of that class. 

`@classmethod` Class methods are often used as factory methods that can create specific instances of the class. 详见﹝流畅的 Python﹞-> 9.4 classmethod与staticmethod 

`@staticmethod` It’s not really dependent on the class, except that it is part of its namespace. Static methods can be called on either an instance or the class.

## 实现

尝试自己实现了一个静态方法装饰器，大致如下：

```python
import functools
class ImitateStaticMethod(object):
    def __new__(cls, func):
        _cls_name = func.__qualname__.partition('.')[0]
        @functools.wraps(func)
        def wrapper(*args):
            _cls = eval(_cls_name)
            if len(args) >= 1 and isinstance(args[0], _cls):
                return func(*list(args[1:]))
            else:
                return func(*list(args[:]))
        return wrapper

class Cls(object):
    @ImitateStaticMethod
    def func1(*args):
        print(args)


print(type(Cls.func1), Cls.func1.__name__)
Cls.func1()
Cls().func1()

Cls.func1(1, 2)
Cls().func1(1, 2)
'''Out:
<class 'function'> func1
()
()
(1, 2)
(1, 2)
'''
```

