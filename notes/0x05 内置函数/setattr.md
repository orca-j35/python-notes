# setattr

🔨 setattr(*object*, *name*, *value*)

`setattr()` 对应于 `getattr()`，前者用于设置对象的属性，后者用于获取对象的属性。

参数说明：

- *object* - 表示某个对象
- *name* - 表示属性名称的字符串，可以是已有属性名或新属性名
- *value* - 任意值

如果对象允许的话，`setattr()` 函数会将 *value* 赋给名为 *name* 的属性，即 `setattr(x, 'y', v)` 等效于 `x.y = v`。

```python
class Foo:
    def __init__(self, x):
         self.x = x
f = Foo('orca_j35')
# 重设已存在的属性
setattr(f, 'x','hello')
f.x #> 'hello'
# 新建一个属性
setattr(f,'y','whale')
f.y #> 'whale'

# 可以设置方法属性
setattr(f,'func',lambda x:x)
f.func('whale') #> 'whale'
```

扩展阅读：『getattr.md』、『delattr.md』