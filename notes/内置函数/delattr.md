# delattr

🔨 delattr(*object*, *name*)

`delattr()` 和 `setattr()` 的功能正好相反，前者用于删除指定属性，后者用于添加(或重设)指定属性。

参数说明：

- *object* - 表示某个对象
- *name* - 表示属性名称的字符串，且必须是 *object* 中的已有属性

如果对象允许的话，`delattr()` 函数将从 `vars(object)` 中删除名为 *name* 的属性，即 `delattr(x, 'y')` 等效于 `del x.y`。

```python
class Foo:
    def __init__(self, x):
        self.x = x
    def func(self):
        pass
f = Foo('orca_j35')
# 只能删除已有属性
delattr(f,'x')
f.x #> AttributeError: x
# 试图删除不存在的属性时，将抛出异常
delattr(f, 'y') #> AttributeError: y

# 试图删除某个方法时，将抛出异常
delattr(f,'func') #> AttributeError: func
```

注意：`delattr()` 只能删除 *object* 中绑定的属性，不能删除其类字典中的属性。

```python
class Foo:
    def __init__(self, x):
        self.x = x
    # 注意，func方法位于类字典中
    def func(self):
        pass
    
f = Foo('orca_j35')
# y是绑定到f中的方法
f.y = lambda j:j
vars(f) #> {'x': 'orca_j35', 'y': <function __main__.<lambda>>}
delattr(f,'y') # 可删除y
# 不能删除类字典中方法，否则会抛出异常
delattr(f,'func') #> AttributeError: func
```

