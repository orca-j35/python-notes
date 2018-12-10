# issubclass

🔨 issubclass(*class*, *classinfo*)

*classinfo* 可以是某个类型(或类)，也可以是由类型(或类)构成的元组，具体如下：

- 当 *classinfo* 是某个类型(或类)时，如果 *class* 是 *classinfo* 的子类(direct, indirect 或 [virtual](https://docs.python.org/3.7/glossary.html#term-abstract-base-class))，则 `issubclass()` 返回 `True`。注意，对该函数而言，类对象被视作其自身的子类。

  ```python
  >>> issubclass(int,int)
  True
  >>> issubclass(bool,int)
  True
  # 直接子类
  >>> class A: pass
  
  >>> class B(A): pass
  
  >>> issubclass(B,A)
  True
  # 虚拟子类:abc
  >>> from collections import abc
  >>> issubclass(list,abc.Iterable)
  True
  # 虚拟子类:numbers
  >>> import numbers
  >>> issubclass(int,numbers.Number)
  True
  ```

  扩展阅读：

  - [abstract base class](https://docs.python.org/3.7/glossary.html#term-abstract-base-class)
  - [`abc`](https://docs.python.org/3.7/library/abc.html#module-abc) — Abstract Base Classes

- 当 *classinfo* 是由类型(或类)构成的元组(或递归包含类似元组)时，如果 *class* 是其中某个类型(或类)的子类，则 `issubclass()` 将返回 `True` (即，`issubclass(X, (A, B, ...))` 等效于 `issubclass(X, A) or issubclass(X , B) or ...` )：

  ```python
  >>> issubclass(list, (list,int,tuple))
  True
  # 可递归包含由类型(或类)构成的元组
  >>> issubclass(int, (list,(int,tuple)))
  True
  # 注意，只要值为True便会停止测试，并返回True，
  # 就算元组中的后续元素包含错误值，也不会抛出异常
  >>> issubclass(int, (list,(int,'orca_j35')))
  True
  ```

如果 *classinfo* 不是某个类型(或类)，也不是由类型(或类)构成的元组，则会抛出 [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError)

```python
>>> issubclass(int,'string')
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    issubclass(int,'string')
TypeError: issubclass() arg 2 must be a class or tuple of classes
```

