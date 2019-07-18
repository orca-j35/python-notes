# dict

```
class dict(object)
 |  dict() -> new empty dictionary
 |  dict(mapping) -> new dictionary initialized from a mapping object's
 |      (key, value) pairs
 |  dict(iterable) -> new dictionary initialized as if via:
 |      d = {}
 |      for k, v in iterable:
 |          d[k] = v
 |  dict(**kwargs) -> new dictionary initialized with the name=value pairs
 |      in the keyword argument list.  For example:  dict(one=1, two=2)
```

构造器 `dict()` 用于创建字典对象。如果想要了解其它容器类型，可以参考内置类型 ([list](https://docs.python.org/3.7/library/stdtypes.html#list)、[set](https://docs.python.org/3.7/library/stdtypes.html#set)、[tuple](https://docs.python.org/3.7/library/stdtypes.html#tuple)) 以及 [collections](https://docs.python.org/3.7/library/collections.html#module-collections) 模块。

🔨 *class* dict()

```
 dict() -> new empty dictionary
```

🔨 *class* dict(\*\**kwarg*)

```
dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list.  
For example:  dict(one=1, two=2)
```

示例 - 展示两种传递关键字实参的方法

```python
>>> d = dict(one=1, two=2) # 直接给出关键字实参
>>> d
{'one': 1, 'two': 2} 
>>> d_ = dict(**d) # 通过拆封传递关键字实参
>>> d_
{'one': 1, 'two': 2}
```

注意，关键字实参的名称必须是有效标识符。

🔨 *class* dict(*mapping*, \*\**kwarg*)

```
dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs
```

如果将一个映射对象作为实参，则会新建一个该映射对象的浅拷贝副本：

```python
dict_ = {'a':1,'b':(1,2),'c':[3,4]}
d1 = dict(dict_)
```

执行结果：

![构建字典](dict.assets/构建字典.png)

🔨 class dict(*iterable*, \*\**kwarg*)

```
dict(iterable) -> new dictionary initialized as if via:
       d = {}
       for k, v in iterable:
           d[k] = v
```

被用作实参的可迭代对象中的每一项必须是一个包含两个元素的可迭代对象。例如：

```python
>>> dict(zip(['one', 'two', 'three'], [1, 2, 3]))
{'one': 1, 'two': 2, 'three': 3}
>>> dict([('two', 2), ('one', 1), ('three', 3)])
{'two': 2, 'one': 1, 'three': 3}
```

扩展阅读：

- 笔记『 映射类型(dict).md』
- [`dict`](https://docs.python.org/3.7/library/stdtypes.html#dict)
- [Mapping Types — dict](https://docs.python.org/3.7/library/stdtypes.html#dict)