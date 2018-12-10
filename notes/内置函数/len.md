# len

🔨 len(*s*)

该函数会返回对象的长度(即对象中包含的项数)。

参数 *s* 可以是某个序列(如 string、bytes、tuple、list、range)或某个集合(如 dictionary、set、frozen set)。

实际上内置函数 `len()` 会调用 `type(s).__len__(s)` 来获得对象 *s* 的长度。如果 `type(s)` 没有实现 `__len__` ，或是 `__len__` 的返回值并非正整数，`len()` 均会抛出异常。

```python
class Cls(object):
    def __init__(self, lst):
        self._lst = lst

    def __len__(self):
        return len(self._lst)
len(Cls([1,2])) #> 2
len(Cls([])) #> 0

class A(object):
    def __len__(self):
        return 111
a = A()
a.__len__=lambda x:222
len(a) #> 111
```

## \_\_len\_\_

🔨 object.`__len__`(*self*)

该函数用于返回对象的长度(长度值是 `>=0` 的整数)，内置函数 [`len()`](https://docs.python.org/3.7/library/functions.html#len) 会调用此函数来获取长度值。另外，对于未定义 [`__bool__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__bool__) 方法的对象，在 Boolean 上下文中会将 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 返回 0 的情形视为 `False`。

```python
class Cls(object):
    def __init__(self, lst):
        self._lst = lst

    def __len__(self):
        return len(self._lst)
print(bool(Cls([]))) # Out: False
print(bool(Cls([1, 2, 3]))) # Out: True
```

**CPython 实现细节：**在 CPython 中，长度(length)的最大值不能超过 [`sys.maxsize`](https://docs.python.org/3.7/library/sys.html#sys.maxsize)。如果长度大于 `sys.maxsize`，某些功能(如 `len()`)便可能会引发 [`OverflowError`](https://docs.python.org/3.7/library/exceptions.html#OverflowError)。为了避免进行真值测试时抛出 `OverflowError`，对象必须定义 [`__bool__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__bool__) 方法。