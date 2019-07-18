# zip

```python
class zip(object)
 |  zip(iter1 [,iter2 [...]]) --> zip object
 |  
 |  Return a zip object whose .__next__() method returns a tuple where
 |  the i-th element comes from the i-th iterable argument.  The .__next__()
 |  method continues until the shortest iterable in the argument sequence
 |  is exhausted and then it raises StopIteration.
```

🔨 zip(\**iterables*)

该函数会创建一个支持迭代器协议的 zip 对象，*iterables* 可以是 1 至多个**可迭代对象**。zip 迭代器生成的项均是**元组**：在迭代器生成的第 i 个元组中聚合了每个可迭代对象中的第 i 个元素。zip 对象的长度取决于可迭代对象中最短的那个，只要某个可迭代对象被耗尽，zip 对象便会停止迭代。zip 函数大致相当于如下代码：

```python
def zip(*iterables):
    # zip('ABCD', 'xy') --> Ax By
    sentinel = object()
    iterators = [iter(it) for it in iterables]
    while iterators:
        result = []
        for it in iterators:
            elem = next(it, sentinel)
            if elem is sentinel:
                return
            result.append(elem)
        yield tuple(result)
```

示例 - zip 对象的长度取决于可迭代对象中最短的那个

```python
>>> zipper = zip('abc', [0, 1, 2])
>>> zipper
<zip object at 0x000001C390BB29C8>
>>> list(zipper)
[('a', 0), ('b', 1), ('c', 2)]
```

当 *iterables* 中仅包含一个可迭代对象时，zip 迭代器由单元素元组构成：

```python
>>> list(zip('orca'))
[('o',), ('r',), ('c',), ('a',)]
```

当参数列表为空时，则会返回一个空迭代器：

```python
>>> list(zip())
[]
```

`zip(*[iter(s)]*n)` 相当于把 `zip(*[iter(s)])` 输出的每个元组均乘以 `n`，等效于 `zip(iter(s), ... ,iter(s))`：

```python
>>> x = [1,2,3]
>>> list(zip(*[x]*3))
[(1, 1, 1), (2, 2, 2), (3, 3, 3)]
>>> list(zip(x,x,x))
[(1, 1, 1), (2, 2, 2), (3, 3, 3)]
```

## 解压zip对象

当 [`zip()`](https://docs.python.org/3.7/library/functions.html#zip) 与 `*` 运算符一起使用时，可解压(*unzip*) zip 对象：

```python
>>> x = [1, 2, 3]
>>> y = [4, 5, 6]
>>> zipped = zip(x, y)
>>> list(zipped)
[(1, 4), (2, 5), (3, 6)]
>>> x2, y2 = zip(*zip(x, y))
>>> x == list(x2) and y == list(y2)
True
```

## Py2 vs. Py3

在 Python 2 中，zip 函数会生成一个列表对象：

```
in Python 2:
zip(seq1 [, seq2 [...]]) -> [(seq1[0], seq2[0] ...), (...)]
```

示例 - 在 Python 2 中的执行效果：

```python
>>> zip([1,2],[3,4])
[(1, 3), (2, 4)]
```

在 Python 3 中，zip 函数会生成一个支持迭代器协议 zip 对象(为了减少使用的空间)：

```
in Python 3:
zip(iter1 [,iter2 [...]]) --> zip object
```

示例 - 可使用 `list()` 函数将 zip 对象转换为一个列表

```python
>>> list(zip([1,2],[3,4]))
[(1, 3), (2, 4)]
```

## itertools.zip_longest()

zip 对象的长度取决于可迭代对象中**最短**的那个，只要某个可迭代对象被耗尽，zip 对象便会停止迭代。如果需要 zip 对象的尺寸与最长的可迭代对象一致，可使用 [`itertools.zip_longest()`](https://docs.python.org/3.7/library/itertools.html#itertools.zip_longest)。

zip_longest 迭代器生成的项也都是元组：在迭代器生成的第 i 个元组中聚合了每个可迭代对象中的第 i 个元素。zip_longest 对象的长度取决于可迭代对象中最长的那个，只有当最长的可迭代对象被耗尽时，zip_longest 对象才会停止迭代。在迭代过程中，如果各个迭代器不等长，则会使用 *fillvalue* 来填充缺失的元素。zip_longest 方法大致相当于如下代码：

```python
def zip_longest(*args, fillvalue=None):
    # zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
    iterators = [iter(it) for it in args]
    num_active = len(iterators)
    if not num_active:
        return
    while True:
        values = []
        for i, it in enumerate(iterators):
            try:
                value = next(it)
            except StopIteration:
                num_active -= 1
                if not num_active:
                    return
                iterators[i] = repeat(fillvalue)
                value = fillvalue
            values.append(value)
        yield tuple(values)
```

如果传递给 zip_longest 的实参中存在可被无限迭代的对象，此时 zip_longest 方法因包含一些限制调用次数的东西(例如 [`islice()`](https://docs.python.org/3.7/library/itertools.html#itertools.islice) or [`takewhile()`](https://docs.python.org/3.7/library/itertools.html#itertools.takewhile))。如果未指定，*fillvalue* 保持默认值 `None`。
