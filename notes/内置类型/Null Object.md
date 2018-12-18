# The Null Object
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本笔记涵盖了以下内容，并且进行了扩展：
>
> -  [The Null Object](https://docs.python.org/3.7/library/stdtypes.html#the-null-object)
> - [3.2. The standard type hierarchy](https://docs.python.org/3.7/reference/datamodel.html#the-standard-type-hierarchy) -> None
>
> 相关笔记:『3.2. 标准类型层次.md』

在 Python 中，null 对象被写作 `None`。

`None`  是 `NoneType` 类型的唯一值，表示一个 null 对象(没有值的对象)。在多数情况下，用于表示缺少应有的值。比如，当函数没有显式的返回值时，便会返回 `None` 。`None` 没有任何属性，不支持任何特殊操作，在布尔表达式中求值时为 `False` 。

`None` 经常用作可选参数的默认值，以便让函数检测调用者是否为该参数实际传递了值。

`type(None)()` 将生成同一个单列(*singleton*)：

```python
type(None) #> NoneType
type(None)() is None #> True
```

注意：不能将 `None` 理解为 `0`，`None` 表示空值，而 `0` 表示一个整数。但 `None` 和 `0` 的布尔值均是 `False`：

```python
bool(None),bool(0)
#> (False, False)
```

