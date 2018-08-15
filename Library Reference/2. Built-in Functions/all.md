### all

all(*iterable*) 

该函数将返回一个布尔值。
如果 *iterable* 中所有元素的布尔值均为真，则返回 `True` ；否则返回 `False`。
Tips：如果 *iterable* 为空，也会返回 `True`。

如下代码与该内置函数等效：

```python
def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True
```

示例

```python
>>> all([])
True

>>> all([True, False])
False
>>> all([True, True])
True

>>> all('True')
True
>>> all('False')
True
>>> all("")
True

>>> all([0, 1])
False
>>> all([1, 1])
True

>>> all((1, 1))
True
>>> all((1, 0))
False

>>> all({0: 'zero', 1: 'one'})
False
>>> all({1: 'one', 2: 'two'})
True

>>> all({0, 1})
False
>>> all({1, 1})
True
```



