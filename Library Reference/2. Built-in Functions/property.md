# property

[TOC]

## 函数形式

🔨class property(*fget=None*, *fset=None*, *fdel=None*, *doc=None*)

> 为了避免混淆 attribute 和 property，本文将 attribute 译作"属性"，property 使用单词形式。

该内置函数其实是 property 类的构造函数，用于创建 property 对象，各参数的含义如下：

- *fget* : **获取器(getter)方法**，用于获取指定属性的值；默认值 None，表示该属性不可读
- *fset* : **设置器(setter)方法**，用于设置指定属性的值；默认值 None，表示该属性不可写
- *fdel* : **删除器(deleter)方法**，用于删除指定属性；默认值 None，表示该属性不可删除
- *doc* : 一个字符串，被用作 property 对象的文档字符串；如果值为 None，则会拷贝获取器的文档字符串。

tips: 获取器(getter)、设置器(setter)和删除器(deleter)被统称为**访问器(accessor)函数**。

property 对象用于托管某个属性，可根据实际需求控制该属性的**访问权限**：

- 可读字段，需正确设置 *fget* 参数；不可读字段，需 *fget=None*
- 可写字段，需正确设置 *fset* 参数；不可写字段，需 *fset=None*
- 可删除字段，需正确设置 *fdel*  参数；不可删除字段，需 *fdel=None*

property 类的典型用法是定义托管属性(managed attribute)，如下：

```python
class C:
    def __init__(self):
        self._x = None

    def getx(self): # getter method
        print("into getter")
        return self._x

    def setx(self, value): # setter method
        print("into setter")
        self._x = value

    def delx(self): # deleter method
        print("into deleter")
        del self._x
    # 通过property函数定义托管属性x，注意x是实例属性
    x = property(getx, setx, delx, "I'm the 'x' property.")


c = C()
c.x  # Out: into getter
c.x = "hello"  # Out: into setter
del c.x  # Out: into deleter

# 通过类C可调用property对象，通过c只能访问被托管的属性
print(C.x)
# Out: <property object at 0x0000028E19885908>
print(C.x.__doc__) # 查看property对象的文档字符串
# Out: I'm the 'x' property.
```

在上述代码中，`getx` 是获取器；`setx` 是设置器；`delx` 是删除器。`c.x` 将调用获取器；`c.x = value` 将调用设置器；`del c.x` 将调用删除器。

在 property 对象中有三个属性： `fget`、`fset` 和 `fdel`。这三个属性与传递给构造函数的实参相对应，例如：

```python
# 使用上一个实例中创建的类C
c = C()
C.x.fget(c) # Out: into getter
C.x.fset(c, "whale") # Out: into setter
C.x.fdel(c) # Out: into deleter
```

Note: 在类中创建的 property 对象都属于实例属性，如果需要将 property 对象用作类属性，则需要在元类中创建 property 对象。

```python
class Meta(type): # 自定义元类
    def __init__(self, name, bases, attrs):
        self._field_of_class = None
        
    @property
    def field_of_class(self):
        print("获取类字段")
        return self._field_of_class

    @field_of_class.setter
    def field_of_class(self, value):
        print("设置类字段")
        self._field_of_class = value

class ClsObj(metaclass=Meta):
    pass

ClsObj.field_of_class
ClsObj.field_of_class = "hello"
```

**Changed in version 3.5:** The docstrings of property objects are now writeable.

## 装饰器形式

🔨@property

property 类还可被用作装饰器。在下面的代码中，将通过装饰器 `@property` 创建一个名为 `x` 的 property 对象，并将原 `x` 方法转换为该 property 对象的获取器。

```python
# -*- coding: utf-8 -*-
class C:
    def __init__(self):
        self._x = None
	# 创建一个名为x的property对象，等价于x=property(fget=x)
    @property
    def x(self):
        """I'm the 'x' property."""
        print("into getter")
        return self._x

    # 在名为x的property对象中，添加设置器(setter)
    @x.setter
    # 等价于 x=x.setter(x)
    def x(self, value):
        print("into setter")
        self._x = value

    # 在名为x的property对象中，添加删除器(deleter)
    @x.deleter
    # 等价于 x=x.deleter(x)
    def x(self):
        print("into deleter")
        del self._x

    # 重置x的获取器(getter)方法，包括文档字符串
    @x.getter
    def x(self):
        """hello"""
        print("new getter")
        return self._x

print(C.x.__doc__)  # Out: hello   
c = C()
c.x  # Out: new getter
c.x = 'whale'  # Out: into setter
del c.x  # Out: into deleter
```

property 对象有三个用于设置"访问器函数"的实例方法：`getter`、`setter`、`deleter`。这三个方法均会返回其 property 实例的新副本，并且会对副本中的"访问器函数"进行设置，具体如下：

- `getter` 用于设置实例副本的获取器(getter)方法
- `setter` 用于设置实例副本的设置器(setter)方法
- `deleter` 用于设置实例副本的删除器(deleter)方法

**tips: 这三个方法均可用作装饰器！！！**

下面这个示例展示了 `setter` 方法的工作原理，另外两个方法也与此类似。

```python
class C:
    def __init__(self):
        self._x = None
    """x/y/x拥有相同的获取器方法"""
    @property
    def x(self):
        """I'm the 'x' property."""
        print("into getter of x")
        return self._x

    """y和z均拥有独立的设置器方法，但x没有"""
    def y(self, value):
        print("into setter of y")
        self._x = value
    # y是x的新副本，拥有不同id，y包含独立的设置器
    y = x.setter(y)  
	# z也是x的新副本，拥有不同id，z包含独立的设置器
    @x.setter  
    def z(self, value):
        print("into setter of z")
        self._x = value


c = C()
print(id(C.x))  # Out: 2153400982008
print(id(C.y))  # Out: 2153401210264
print(id(C.z))  # Out: 2153401924568

c.x  # Out: into getter of x
c.y  # Out: into getter of x
c.z  # Out: into getter of x
c.y = "y"  # Out: into setter of y
c.z = "z"  # Out: into setter of z
c.x = "x"  # AttributeError: can't set attribute
```

## 应用场景

创建只读 property 对象，禁止外部直接修改被托管的属性

```python
class Parrot:
    def __init__(self):
        self._voltage = 100000

    @property # 等效于 voltage=property(fget=voltage)
    def voltage(self):
        """Get the current voltage."""
        return self._voltage
    
print(Parrot().voltage)
# Out: 100000
```

控制外部向被托管属性写入的内容

```python

```



