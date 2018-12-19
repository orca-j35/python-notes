# max

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

🔨 max(*iterable*, \*[, *key*, *default*])

🔨 max(*arg1*, *arg2*, **args*[, *key*])

如果只提供一个**位置实参**，则必须是一个可迭代([*iterable*](https://docs.python.org/3.7/glossary.html#term-iterable))对象，`max()` 将返回 *iterable* 中最大的一项。如果向 `max()` 传递一个非可迭代对象，则会抛出 `TypeError` 异常

```python
max([2,4,6,8]) #> 8
# 字符按照Unicode码点值进行比较
max('orca_j35') #> 'r'
# 大小与各项的长度无关
max(['ab','ac','d']) #> 'd'

max(1024) #> TypeError: 'int' object is not iterable
```

如果提供两个以上的**位置实参**，`max()` 将返回这些位置实参中最大的一项。

```python
max(1,3,5) #> 5
max('ab','ac','d') #> 'd'
```

`max()` 中可选关键字实参的功能如下：

- *key* 用于指定一个单参数排序函数，使用方法与 [`list.sort()`](https://docs.python.org/3.7/library/stdtypes.html#list.sort) 类似。详见笔记：

  - 『sorted.md』
  - 『序列类型(list, tuple, range).md』-> list.sort()

  ```python
  max(1,2,'3',key = int) #> '3'
  ```

- *default* 用于指定一个对象，当 *iterable* 为空时，便会返回该对象。如果 *iterable* 为空，但并未提供 *default* 参数，则会抛出 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError) 异常。

  ```python
  max((),default="empty") #> 'empty'
  max(list()) #> ValueError: max() arg is an empty sequence
  ```

如果存在多个最大项，`max()` 将返回第一个出现的最大项。该结果与其它稳定性排序工具一致，例如  `sorted(iterable,key=keyfunc, reverse=True)[0]` 和 `heapq.nlargest(1, iterable, key=keyfunc)`。

```python
cards = [(7,"黑桃"), (8,"红桃"), (2,"红桃"), (8,"黑桃")]
sorted(cards,key=lambda t:t[0],reverse=True)[0]
#> (8, '红桃')
max(cards,key=lambda t:t[0])
#> (8, '红桃')
```

关于稳定性排序，详见笔记『sorted.md』-> 稳定性

New in version 3.4: The *default* keyword-only argument.

