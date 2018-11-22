# object

🔨 *class* object

 `object()` 构造函数将返回一个新的无特征(*featureless*)对象，此函数不接受任何参数。

`object` 是所有**新式类**的最终基类，它提供了所有 Python 类实例的共有方法，如下：

```python
>>> dir(object)
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
```

Note: `object` 的实例不包含 `__dict__` 字段，因此不能为 `object` 的实例绑定任何属性。

```python
>>> vars(object())
Traceback (most recent call last):
  File "<pyshell#14>", line 1, in <module>
    vars(object())
TypeError: vars() argument must have __dict__ attribute
>>> x = object()
>>> x.i = 10 # 不能设置属性
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    x.i = 10
AttributeError: 'object' object has no attribute 'i'
```

