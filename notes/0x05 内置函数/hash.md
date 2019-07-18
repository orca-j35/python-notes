# hash

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

🔨 hash(*object*)

如果 *object* 属于可哈希对象，`hash()` 函数将返回其哈希值；如果 *object* 不属于可哈希对象，`hash()` 函数则会抛出异常。哈希值是一个整数。

```python
hash('orca_j35') #> 3721949548176702466
hash([1,2]) #> TypeError: unhashable type: 'list
```

在查找字典时，会使用哈希值来快速比较字典的键。具有相同哈希值的对象，被字典视作同一个键。

```python
x = (1,2)
y = (1,2)
# x和y是具备不同id的对象
x is y #> False
z = {x:"orca"}
# 只要哈希值相同，便可互换使用
z[y] #> 'orca'
```

相等(`==`)的数值拥有相同的哈希值，即使两个相等的数值属于不同的类型，它们的哈希值也相同，例如 `1` 和 `1.0`:

```python
1 == 1.0 #> True
hash(1),hash(1.0) #> (1, 1)
```

tips: 两个相等(`==`)的对象必定拥有相同的哈希值，但返回过并不一定成立。

注意：对于拥有自定义 [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) 方法的对象，`hash()` 函数会根据主机(*host machine*)的位宽来截断 [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) 的返回值。详见 [`__hash__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__) 方法的文档。

扩展阅读：

- [bject.\_\_hash\_\_(self)](https://docs.python.org/3.7/reference/datamodel.html#object.__hash__)
- [class collections.abc.Hashable](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Hashable)
- 『映射类型(dict).md』 -> 1. hashable

