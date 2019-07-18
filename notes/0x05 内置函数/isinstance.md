# isinstance

🔨 isinstance(*object*, *classinfo*)

*classinfo* 可以是某个类型(或类)，也可以是由类型(或类)构成的元组，具体如下：

- 当 *classinfo* 是某个类型(或类)时，如果 *object* 是 *classinfo* 的实例，或者 *object* 是 *classinfo* 的子类(direct, indirect 或 [virtual](https://docs.python.org/3.7/glossary.html#term-abstract-base-class))的实例，则 `isinstance()` 返回 `True`。如果 *object* 不是给定类型(或类)的实例，则 `isinstance()` 始终返回 `False`。

  ```python
  >>> isinstance(b'a', bytes)
  True
  # 直接子类
  >>> class A: pass
  
  >>> class B(A): pass
  
  >>> isinstance(B(), A)
  True
  # 虚拟子类:abc
  >>> from collections import abc
  >>> isinstance((i for i in range(10)), abc.Generator)
  True
  >>> isinstance(range(10),abc.Iterator)
  False
  # 虚拟子类:numbers
  >>> import numbers
  >>> isinstance(1.1,numbers.Number)
  True
  # 虚拟子类:io
  >>> with open('orca.txt','w') as f:
  	isinstance(f,io.TextIOWrapper)
  
  	
  True
  ```

  扩展阅读：

  - [abstract base class](https://docs.python.org/3.7/glossary.html#term-abstract-base-class)
  - 笔记『容器\_可迭代\_迭代器\_生成器.md』
  - [`abc`](https://docs.python.org/3.7/library/abc.html#module-abc) — Abstract Base Classes

- 当 *classinfo* 是由类型(或类)构成的元组(或递归包含类似元组)时，如果 *object* 是其中某个类型的实例，则 `isinstance()` 将返回 `True` (即，`isinstance(x, (A, B, ...))` 等效于 `isinstance(x, A) or isinstance(x , B) or ...` )：

  ```python
  >>> isinstance((1, 2, 3), (list, tuple))
  True
  # 可递归包含由类型(或类)构成的元组
  >>> isinstance((1, 2, 3), (list,(int,tuple)))
  True
  # 注意，只要值为True便会停止测试，并返回True，
  # 就算元组中的后续元素包含错误值，也不会抛出异常
  >>> isinstance('字符串',(int,bytes,str,'hello'))
  True
  ```

如果 *classinfo* 不是某个类型(或类)，也不是由类型(或类)构成的元组，则会抛出 [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError)

```python
>>> isinstance(1,1)
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    isinstance(1,1)
TypeError: isinstance() arg 2 must be a type or tuple of types
```

