# classmethod
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 扩展阅读：
>
> - [Python's Instance, Class, and Static Methods Demystified – Real Python](https://realpython.com/instance-class-and-static-methods-demystified/)
> - ﹝0x06 装饰器.md﹞
> - ﹝流畅的 Python﹞-> 9.4 classmethod与staticmethod
> - [如何正确理解@classmethod与@staticmethod](https://foofish.net/different_bettween_classmethod_and_staticmethod.html)
> - [如何在Python中正确使用static、class、abstract方法](https://foofish.net/guide-python-static-class-abstract-methods.html)

🔨 @classmethod

```python
class classmethod(object)
 |  classmethod(function) -> method
```

Transform a method into a class method.

A class method receives the **class** as implicit first argument, just like an instance method receives the instance. To declare a class method, use this idiom:

```python
class C:
    @classmethod
    def f(cls, arg1, arg2, ...): 
        # 在调用f方法时，会自动传入cls
        # cls表示当前类C
        ...
```

The `@classmethod` form is a function [decorator](https://docs.python.org/3.7/glossary.html#term-decorator) – see the description of function definitions in [Function definitions](https://docs.python.org/3.7/reference/compound_stmts.html#function) for details.

It can be called either on the class (such as `C.f()`) or on an instance (such as `C().f()`). The instance is ignored except for its class. If a class method is called for a derived class, the derived class object is passed as the implied first argument.

```python
class Cls(object):
    @classmethod
    def cm(cls, *args):
        # 可通过cls引用类中的属性
        print(cls)
# 类和实例均可调用
Cls.cm() #> <class '__main__.Cls'>
Cls().cm() #> <class '__main__.Cls'>

# 子类中也可正常工作
class SubCls(Cls):
    pass

SubCls.cm() #> <class '__main__.SubCls'>
SubCls().cm() #> <class '__main__.SubCls'>
```

Class methods are different than C++ or Java static methods. If you want those, see [`staticmethod()`](https://docs.python.org/3.7/library/functions.html#staticmethod) in this section.

For more information on class methods, consult the documentation on the standard type hierarchy in [The standard type hierarchy](https://docs.python.org/3.7/reference/datamodel.html#types).

## 使用场景

The `@classmethod` and `@staticmethod` decorators are used to define methods inside a class namespace that are not connected to a particular instance of that class. 

`@classmethod` Class methods are often used as factory methods that can create specific instances of the class. 详见﹝流畅的 Python﹞-> 9.4 classmethod与staticmethod 

`@staticmethod` It’s not really dependent on the class, except that it is part of its namespace. Static methods can be called on either an instance or the class.

## \_\_func\_\_

> 参考: [9.3 解除一个装饰器 —  python3-cookbook](https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p03_unwrapping_decorator.html#id1)

`@classmethod` 会将原始函数存储在 `__func__` 属性中：

```python
class Cls(object):
    @classmethod
    def cm(cls, *args):
        print('class method')

print(Cls.cm) #> <bound method Cls.cm of <class '__main__.Cls'>>
print(Cls.cm.__func__) #> <function Cls.cm at 0x000001D6B8C4C6A8>
```

## 实现

尝试自己实现了一个类方法装饰器，大致如下：

```python
import functools
class ImitateClassMethod(object):
    def __new__(cls, func):
        _cls_name = func.__qualname__.partition('.')[0]
        @functools.wraps(func)
        def wrapper(*args):
            _cls = eval(_cls_name)
            if len(args) >= 1 and isinstance(args[0], _cls):
                args = [args[0].__class__] + list(args[1:])
                return func(*args)
            else:
                args = [_cls] + list(args[:])
                return func(*args)
        return wrapper

class Cls(object):
    @ImitateClassMethod
    def func1(cls):
        print(cls)

    @ImitateClassMethod
    def func2(cls, a, b):
        print(cls, a, b)

print(type(Cls.func1), Cls.func1.__name__)
Cls.func1()
Cls().func1()

Cls.func2(1, 2)
Cls().func2(1, 2)
'''Out:
<class 'function'> func1
<class '__main__.Cls'>
<class '__main__.Cls'>
<class '__main__.Cls'> 1 2
<class '__main__.Cls'> 1 2
'''
```

不使用以下模板的原因是：为了保证类方法始终属于 `<class 'method'>` 。如果使用以下模板，类方法则是 `Name` 类的实例。

```python
import functools
class Name:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        # Initialize state attributes
    def __call__(self, *args, **kwargs):
        # Update state attributes
        return self.func(*args, **kwargs)
```




