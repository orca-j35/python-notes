# types — 为内置类型创建动态类型和名称

types — Dynamic type creation and names for built-in types

## MappingProxyType

🔨 class types.[MappingProxyType](https://docs.python.org/3.7/library/types.html#types.MappingProxyType)(*mapping*)

该构造函数会创建一个基于 *mapping* 的只读代理对象。此代理对象会提供 *mapping* 条目的动态视图，这意味着当 *mapping* 发生变化时，在代理对象中也会表现出同样的变化。

```python
>>> from types import MappingProxyType
>>> a_map = dict(a='orca',b='j35')
>>> proxy_map = MappingProxyType(a_map)
>>> proxy_map
mappingproxy({'a': 'orca', 'b': 'j35'})
>>> a_map['c'] = 'update'
>>> proxy_map # 代理对象会自动更新视图
mappingproxy({'a': 'orca', 'b': 'j35', 'c': 'update'})
```

MappingProxyType 是 Py 3.3 中添加的新功能，支持下列操作：

- `key in proxy`

  Return `True` if the underlying mapping has a key *key*, else `False`.

- `proxy[key]`

  Return the item of the underlying mapping with key *key*. Raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) if *key* is not in the underlying mapping.

- `iter(proxy)`

  Return an iterator over the keys of the underlying mapping. This is a shortcut for `iter(proxy.keys())`.

- `len(proxy)`

  Return the number of items in the underlying mapping.

- `copy`()

  Return a shallow copy of the underlying mapping.

- `get`(*key*[, *default*])

  Return the value for *key* if *key* is in the underlying mapping, else *default*. If *default* is not given, it defaults to `None`, so that this method never raises a [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError).

- `items`()

  Return a new view of the underlying mapping’s items (`(key, value)` pairs).

- `keys`()

  Return a new view of the underlying mapping’s keys.

- `values`()

  Return a new view of the underlying mapping’s values.

如果尝试修改代理对象，则会抛出异常：

```python
>>> from types import MappingProxyType
>>> a_map = dict(a='orca',b='j35')
>>> proxy_map = MappingProxyType(a_map)
>>> proxy_map['a'] = 'whale'
Traceback (most recent call last):
  File "<pyshell#21>", line 1, in <module>
    proxy_map['a'] = 'whale'
TypeError: 'mappingproxy' object does not support item assignment
```





