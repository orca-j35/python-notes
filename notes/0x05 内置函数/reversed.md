# reversed

🔨 reversed(*seq*, /)

该函数会生成 *seq* 的反向迭代器(*reverse* [*iterator*](https://docs.python.org/3.7/glossary.html#term-iterator))，该迭代器会以相反的顺序迭代 *seq* 中的所有对象，并且反向迭代器不会随原序列变化：

```python
>>> a = [1,2,3,4]
>>> b = reversed(a)
>>> a.append(5)
>>> a
[1, 2, 3, 4, 5]
>>> list(b)
[4, 3, 2, 1]
```

*seq* 必须是下述两种对象之一，否则会抛出 TypeError：

- 包含 [`__reversed__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__reversed__) 方法的对象

  ```python
  class Cls(object):
      def __init__(self, seq):
          self._seq = seq
      def __reversed__(self):
          return (x for x in self._seq[::-1])
  x = Cls([1, 2, 3, 4])
  y = reversed(x)
  x._seq.append(5)
  print(list(y)) # Out: [4, 3, 2, 1]
  ```

- 支持序列协议的对象 ([`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 和 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__))，且 `__getitem__()` 需以整数 `0` 作为起点。必须同时包含 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 和 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__)。

  ```python
  class Cls(object):
      def __init__(self, seq):
          self._seq = seq
      def __len__(self):
          return len(self._seq)
      def __getitem__(self, index):
          return self._seq[index]
  x = Cls([1, 2, 3, 4])
  y = reversed(x)
  x._seq.append(5)
  print(list(y)) # Out:[4, 3, 2, 1]
  ```

## \_\_reversed\_\_

object.[`__reversed__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__reversed__)(*self*)

内置函数 [`reversed()`](https://docs.python.org/3.7/library/functions.html#reversed) 会调用该方法(如果存在)来实现反向迭代。`__reversed__` 应返回一个新的迭代器对象，该对象会以相反的顺序迭代容器中的所有对象。

如果没有提供 [`__reversed__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__reversed__) 方法，内置函数 [`reversed()`](https://docs.python.org/3.7/library/functions.html#reversed) 则会使用序列协议 ([`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 和 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__))。只有当支持序列协议的对象能提供比 [`reversed()`](https://docs.python.org/3.7/library/functions.html#reversed) 的原生实现的更高效的实现时，才应实现自己的 [`__reversed__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__reversed__) 方法。

## sequence

https://docs.python.org/3.7/glossary.html#term-sequence

[序列](https://docs.python.org/3.7/glossary.html#term-sequence)是一个 [iterable](https://docs.python.org/3.7/glossary.html#term-iterable) 对象。通过定义 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法，可使得序列能够通过整数索引来高效的访问其中的元素。通过定义 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 方法，以便查看序列的长度。如 [`list`](https://docs.python.org/3.7/library/stdtypes.html#list) | [`str`](https://docs.python.org/3.7/library/stdtypes.html#str)| [`tuple`](https://docs.python.org/3.7/library/stdtypes.html#tuple)|  [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 都属于内置序列类型。注意，[`dict`](https://docs.python.org/3.7/library/stdtypes.html#dict) 同样支持  [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 和 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__)，但是考虑到 `dict` 是映射而非序列，因此将 [不可变](https://docs.python.org/3.7/glossary.html#term-immutable)的 key 作为查找对象，而没有使用整数。

在 [`collections.abc.Sequence`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Sequence) 抽象基类中定义了更为丰富的接口，不仅包含了[`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 和 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) ，还添加了 `count()`, `index()`, [`__contains__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__contains__) 和 [`__reversed__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__reversed__)。 Types that implement this expanded interface can be registered explicitly using `register()`。

想解容器类型，可阅读：[`collections.abc`](https://docs.python.org/3.7/library/collections.abc.html#module-collections.abc) — Abstract Base Classes for Containers



