# 映射类型(dict)

> 本章涵盖了 [Mapping Types — dict](https://docs.python.org/3.7/library/stdtypes.html#dict) 中的所有知识点，并进行了扩展。

映射([*mapping*](https://docs.python.org/3/glossary.html#term-mapping))对象会将可哈希([*hashable*](https://docs.python.org/3/glossary.html#term-hashable))对象映射到另一个对象。映射属于可变对象。目前只有一种标准的映射类型，即字典(*dictionary*)。如果想要了解其它容器类型，可以参考内置类型 ([list](https://docs.python.org/3.7/library/stdtypes.html#list)、[set](https://docs.python.org/3.7/library/stdtypes.html#set)、[tuple](https://docs.python.org/3.7/library/stdtypes.html#tuple)) 以及 [collections](https://docs.python.org/3.7/library/collections.html#module-collections) 模块。

## 1. hashable

> 本节内容涵盖了 [hashable - 术语表](https://docs.python.org/3.7/glossary.html#term-hashable) 中的所有知识点，并进行了扩展

"可哈希对象(*hashable*)"需实现 [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) 方法，并且"可哈希对象"的哈希值在其生命周期内永远不会发生变化。"可哈希对象"还需实现 [`__eq__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__eq__) 方法，且满足：当  `x==y` 时，`hash(x) == hash(y)` (x, y 是具备不同id的"可哈希对象")。即便"可哈希对象"拥有不同的 id，只要它们的哈希值相同，便可等效使用，例如：

```python
>>> x = (1,2)
>>> y = (1,2)
>>> x is y
False
>>> z = {x:"orca"}
>>> z[y]
'orca'
```

"可哈希对象"可用作字典的键和集合的成员，因为这两种数据结构会在内部使用相关对象的哈希值。

在 Python 中，所有内置不可变对象都属于"可哈希对象"，内置可变容器不属于"可哈希对象"(如，列表和字典等)。默认情况下，自定义类的实例属于可哈希对象，但这些实例的哈希值基于其 id，也就是说不同 id 的实例的哈希值不同，例如：

```python
>>> class Cls:pass

>>> i = Cls()
>>> j = Cls()
>>> hash(i)
156321732037
>>> hash(j)
-9223371880532492263
>>> i == j # 相等性测试也基于id
False
```

可利用 [`collections.abc.Hashable`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Hashable) 来测试目标对象是否属于"可哈希对象"：

```python
>>> # isinstance(obj, collections.abc.Hashable)
>>> import collections
>>> isinstance(1,collections.abc.Hashable)
True
>>> isinstance(set((1,2)),collections.abc.Hashable)
False
>>> isinstance((1,2),collections.abc.Hashable)
True
```

扩展阅读：

- [bject.\_\_hash\_\_(self)](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__)
- [class collections.abc.Hashable](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Hashable)

## 2. 字典

只有"可哈希对象"才可用作字典的键(*key*)。

数值类型被用作键时，依旧遵循数值比较规则：如果两个数值相等(如 `1` 和 `1.0` )，字典会认为这两个数值均表示同一个键。因此在索引字典时，相等的数值可互换使用。不过由于计算机以近似值存储浮点数，因此最好不要将浮点数用作字典的键。

```python
>>> j = {1:"orca"}
>>> j[1.0] # 1和1.0可互换使用
'orca'
```

### 2.1 构建字典

可通过以下几种方式来构建字典：

- 使用一对花括号可构建一个空字典：`{}`

- 使用一对花括号，并在其中填充以逗号分隔的键值对：

  ```python
  >>> i = {'jack': 4098, 'sjoerd': 4127}
  >>> j = {4098: 'jack', 4127: 'sjoerd'}
  >>> k = {**i, **j} # 拆封i和j
  >>> k
  {'jack': 4098, 'sjoerd': 4127, 4098: 'jack', 4127: 'sjoerd'}
  ```

- 使用字典解析式：`{x: x * x for x in [1,2,3,4,5,6]}`

- 使用类型构造器：`dict(**kwarg)` , `dict(mapping, **kwarg)` , `dict(iterable, **kwarg)`

在构造字典对象时，如果某个键多次出现在不同的键值对中，那么此键在新字典中的值是最后出现的那个值。

#### a. 构造器 dict()

构造器 `dict()` 的使用方法如下：

🔨 class dict()

```
 dict() -> new empty dictionary
```

🔨 class dict(\*\**kwarg*)

```
dict(**kwargs) -> new dictionary initialized with the name=value pairs in the keyword argument list.  
For example:  dict(one=1, two=2)
```

示例 - 展示两种传递关键之实参的方法

```python
>>> d = dict(one=1, two=2)
>>> d
{'one': 1, 'two': 2} 
>>> d_ = dict(**d) # 通过字典拆封传递关键字实参
>>> d_
{'one': 1, 'two': 2}
```

注意，必须以 Python 中的有效标识符作为关键字实参的名称。

🔨 class dict(*mapping*, \*\**kwarg*)

```
dict(mapping) -> new dictionary initialized from a mapping object's (key, value) pairs
```

如果将一个映射对象作为实参，则会新建一个该映射对象的浅拷贝副本：

```python
dict_ = {'a':1,'b':(1,2),'c':[3,4]}
d1 = dict(dict_)
```

执行结果：

![构建字典](0x09 映射类型(dict).assets/构建字典.png)

🔨 class dict(*iterable*, \*\**kwarg*)

```
dict(iterable) -> new dictionary initialized as if via:
 |      d = {}
 |      for k, v in iterable:
 |          d[k] = v
```

被用作实参的可迭代对象中的每一项必须是一个包含两个元素的可迭代对象。例如：

```python
>>> dict(zip(['one', 'two', 'three'], [1, 2, 3]))
{'one': 1, 'two': 2, 'three': 3}
>>> dict([('two', 2), ('one', 1), ('three', 3)])
{'two': 2, 'one': 1, 'three': 3}
```

### 2.2 字典支持的操作

以下是字典所支持的操作，自定义映射类型也应支持这些操作。

- `len(d)`

  Return the number of items in the dictionary *d*.

- `d[key]`

  Return the item of *d* with key *key*. Raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) if *key* is not in the map.

  If a subclass of dict defines a method [`__missing__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__missing__) and *key* is not present, the `d[key]` operation calls that method with the key *key* as argument. The `d[key]`operation then returns or raises whatever is returned or raised by the `__missing__(key)` call. No other operations or methods invoke [`__missing__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__missing__). If[`__missing__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__missing__) is not defined, [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) is raised. [`__missing__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__missing__) must be a method; it cannot be an instance variable:

  ```python
  >>> class Counter(dict):
      def __missing__(self, key):
          return 0
  
  >>> c = Counter()
  >>> c['red']
  0
  >>> c['red'] += 1
  >>> c['red']
  1
  ```


- `d[key] = value`

  Set `d[key]` to *value*.

- `del d[key]`

  Remove `d[key]` from *d*. Raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) if *key* is not in the map.

- `key in d`

  Return `True` if *d* has a key *key*, else `False`.

- `key not in d`

  Equivalent to `not key in d`.

- `iter(d)`

  Return an iterator over the keys of the dictionary. This is a shortcut for `iter(d.keys())`.

- `clear`()

  Remove all items from the dictionary.

- `copy`()

  Return a shallow copy of the dictionary.

- *classmethod* `fromkeys`(*seq*[, *value*])

  Create a new dictionary with keys from *seq* and values set to *value*.[`fromkeys()`](https://docs.python.org/3.7/library/stdtypes.html#dict.fromkeys) is a class method that returns a new dictionary. *value* defaults to `None`.

- `get`(*key*[, *default*])

  Return the value for *key* if *key* is in the dictionary, else *default*. If *default* is not given, it defaults to `None`, so that this method never raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError).

- `items`()

  Return a new view of the dictionary’s items (`(key, value)` pairs). See the [documentation of view objects](https://docs.python.org/3.7/library/stdtypes.html#dict-views).

- `keys`()

  Return a new view of the dictionary’s keys. See the [documentation of view objects](https://docs.python.org/3.7/library/stdtypes.html#dict-views).

- `pop`(*key*[, *default*])

  If *key* is in the dictionary, remove it and return its value, else return *default*. If *default*is not given and *key* is not in the dictionary, a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) is raised.

- `popitem`()

  Remove and return a `(key, value)` pair from the dictionary. Pairs are returned in LIFO order.[`popitem()`](https://docs.python.org/3.7/library/stdtypes.html#dict.popitem) is useful to destructively iterate over a dictionary, as often used in set algorithms. If the dictionary is empty, calling [`popitem()`](https://docs.python.org/3.7/library/stdtypes.html#dict.popitem) raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError).Changed in version 3.7: LIFO order is now guaranteed. In prior versions, [`popitem()`](https://docs.python.org/3.7/library/stdtypes.html#dict.popitem)would return an arbitrary key/value pair.

- `setdefault`(*key*[, *default*])

  If *key* is in the dictionary, return its value. If not, insert *key* with a value of *default* and return *default*. *default* defaults to `None`.

- `update`([*other*])

  Update the dictionary with the key/value pairs from *other*, overwriting existing keys. Return `None`.[`update()`](https://docs.python.org/3.7/library/stdtypes.html#dict.update) accepts either another dictionary object or an iterable of key/value pairs (as tuples or other iterables of length two). If keyword arguments are specified, the dictionary is then updated with those key/value pairs: `d.update(red=1, blue=2)`.

- `values`()

  Return a new view of the dictionary’s values. See the [documentation of view objects](https://docs.python.org/3.7/library/stdtypes.html#dict-views).

Dictionaries compare equal if and only if they have the same `(key, value)` pairs. Order comparisons (‘<’, ‘<=’, ‘>=’, ‘>’) raise [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError).

Dictionaries preserve insertion order. Note that updating a key does not affect the order. Keys added after deletion are inserted at the end.

```python
>>> d = {"one": 1, "two": 2, "three": 3, "four": 4}
>>> d
{'one': 1, 'two': 2, 'three': 3, 'four': 4}
>>> list(d)
['one', 'two', 'three', 'four']
>>> list(d.values())
[1, 2, 3, 4]
>>> d["one"] = 42
>>> d
{'one': 42, 'two': 2, 'three': 3, 'four': 4}
>>> del d["two"]
>>> d["two"] = None
>>> d
{'one': 42, 'three': 3, 'four': 4, 'two': None}
```

Changed in version 3.7: Dictionary order is guaranteed to be insertion order. This behavior was implementation detail of CPython from 3.6.

See also

[`types.MappingProxyType`](https://docs.python.org/3.7/library/types.html#types.MappingProxyType) can be used to create a read-only view of a [`dict`](https://docs.python.org/3.7/library/stdtypes.html#dict).

### 字典拆封

> 本节内容参考自 [6.2.7. Dictionary displays](https://docs.python.org/3.7/reference/expressions.html#dictionary-displays)

双星号 `**` 用于字典拆封(*unpacking*)，其操作数必须是映射([*mapping*](https://docs.python.org/3.7/glossary.html#term-mapping))。

在构建字典时，可使用 `**` 拆封某个字典，以便获取该字典中的键值对：

```python
>>> i = {'jack': 4098, 'sjoerd': 4127}
>>> j = {4098: 'jack', 4127: 'sjoerd'}
>>> k = {**i, **j} # 拆封
>>> k
{'jack': 4098, 'sjoerd': 4127, 4098: 'jack', 4127: 'sjoerd'}
```

被拆封的字典中的全部条目都会被添加到新字典中。如果某个键被重复添加，则保留最后一次添加的值。

在调用函数时，可使用 `**` 对打包到字典中的参数进行拆封：

```python
>>> def func(a,b,c):
	print(a,b,c)

>>> func(**dict(a=1,b=2,c=3))
1 2 3
```

## 提示

### a. 拷贝字典

浅拷贝时，原映射中"值"引用的可变对象**不会产生**新副本，仅会对可变对象的引用进行多次拷贝。若在新副本中修改可变对象，原副本中的可变对象也会发生改变。copy 模块中的 `copy()` 属于浅拷贝(*shallow copy*)

深拷贝时，原映射中"值"引用的可变对象都**会产生**新副本，并会在新映射中引用这些副本。若在新副本中修改可变对象，原副本中的可变对象不受影响。copy 模块中的 `deepcopy()` 属于深拷贝(*deep copy*)

对于不可变对象，由于本身并不能被修改，因此在浅拷贝和深拷贝中都直接拷贝其引用。

示例 - 观察浅拷贝和深拷贝的区别：

```python
import copy
dict_ = {'a':1,'b':(1,2),'c':[3,4]}
d1 = dict(dict_)
d2 = copy.copy(dict_)
d3 = copy.deepcopy(dict_)
```

执行结果：

![拷贝字典](0x09 映射类型(dict).assets/拷贝字典.png)

## 扩展阅读

