# any

🔨 any(*iterable*)

该函数将返回一个布尔值。
如果 *iterable* 中存在布尔值为真的元素，则返回 `True`；否则返回 `False`。
Tips：如果 *iterable* 为空，则会返回 `False` 。

如下代码与该内置函数等效：

```python
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
```

示例：

```python
>>> any([True, True])
True
>>> any([True, False])
True
>>> any([False, False])
False
>>> any('False')
True
>>> any([])
False
```

