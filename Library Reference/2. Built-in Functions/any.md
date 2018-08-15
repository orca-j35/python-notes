### any

any(iterable)

如下代码与该内置函数等效：

```python
def any(iterable):
    for element in iterable:
        if element:
            return True
    return False
```

如果可迭代(iterable)对象中存在布尔值为真的元素，则返回 `True`。
注意，如果可迭代对象为空，也是返回 `True`。