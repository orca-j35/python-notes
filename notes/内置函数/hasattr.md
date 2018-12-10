# hasattr

🔨 hasattr(*object*, *name*)

该函数用于检测 *object* 中是否含有名为 *name* 属性。如果包含，则返回 `True` ；否则返回 `False`。

`hasattr()` 实际上是通过调用 `getattr(object, name)` 函数，并检测是否抛出 [`AttributeError`](https://docs.python.org/3.7/library/exceptions.html#AttributeError) 异常来实现的。

```python
class Foo:
    def __init__(self, x):
         self.x = x
f = Foo('orca_j35')
hasattr(f,'x') #> True
hasattr(Foo,'x') #> False
```

关于 `getattr()` 函数，详见笔记 『getattr.md』。