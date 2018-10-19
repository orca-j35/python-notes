# id

🔨 id(*object*)

该函数会返回 *object* 的"身份(identity)"。
id 具有唯一性，在 Python 中以整数表示，并且在 *object* 的生命周期内恒定不变。

```python
>>> list_1 = [1,2]
>>> list_2 = [1,2]
>>> id(list_1),id(list_2)
(1815130623432, 1815130623112)
>>> list_1 is list_2
False
>>> list_1 == list_2
True
```

如果某两个对象的生命周期没有重叠，则这两个对象可能会拥有相同的 id。

```python
>>> class Cls:pass

>>> obj=Cls()
>>> id(obj)
1815129810984
>>> del obj
>>> obj_=Cls()
>>> id(obj_)
1815129810984
```

**CPython 实现细节**：在 CPython 中，标识符是 *object* 在内存中的地址。