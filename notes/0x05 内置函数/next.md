# next

next(*iterator*[, *default*])

通过调用迭代器对象 *iterator* 的 [`__next__()`](https://docs.python.org/3.7/library/stdtypes.html#iterator.__next__) 方法来检索迭代器中的下一项。

如果已传入第二参数 *default* ，当迭代器耗尽时便会返回 *default*；如果没有传入第二参数，当迭代器耗尽时，则会抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration)。

示例 1：

```python
>>> i = iter([1, 2])
>>> next(i)
1
>>> next(i)
2
>>> next(i)
Traceback (most recent call last):
  File "<interactive input>", line 1, in <module>
StopIteration
```

示例 2：

```python
>>> i = iter([1, 2])
>>> next(i, 'No more items in the list.')
1
>>> next(i, 'No more items in the list.')
2
>>> next(i, 'No more items in the list.')
'No more items in the list.'
```

