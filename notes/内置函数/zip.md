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

该函数会创建一个支持迭代器协议的 zip 对象，*iterables* 可以是 1 至多个可迭代对象。zip 迭代器中的每一项均是一个元组，每个元组中聚合了各个可迭代对象中相同索引位置的元素。也就是说，zip 迭代器返回的第 i 个元组中，聚合每个可迭代对象中的第 i 个元素。zip 函数大致相当于如下代码：

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

在 zip 对象的迭代过程中，当最短的可迭代对象被耗尽时便会停止迭代。也就是说 zip 迭代器的尺寸与最短的可迭代对象相同。

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

当 *iterables* 为空时，则会返回一个空迭代器：

```python
>>> list(zip())
[]
```

zip 函数保证按照由左至右的顺从各个可迭代对象中逐一抽取相应位置的元素。

`zip(*[iter(s)]*n)` 等效于 `zip(iter(s),...iter(s))` 

The left-to-right evaluation order of the iterables is guaranteed. This makes possible an idiom for clustering a data series into n-length groups using `zip(*[iter(s)]*n)`. This repeats the *same* iterator `n` times so that each output tuple has the result of `n` calls to the iterator. This has the effect of dividing the input into n-length chunks.



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

## itertools.zip_longest()

在 zip 对象的迭代过程中，当最短的可迭代对象被耗尽时便会停止迭代。也就是说 zip 迭代器的尺寸与最短的可迭代对象相同。如果需要 zip 对象的尺寸与最长的可迭代对象一致，可使用 [`itertools.zip_longest()`](https://docs.python.org/3.7/library/itertools.html#itertools.zip_longest)。

Make an iterator that aggregates elements from each of the iterables. If the iterables are of uneven length, missing values are filled-in with *fillvalue*. Iteration continues until the longest iterable is exhausted. Roughly equivalent to:

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

If one of the iterables is potentially infinite, then the [`zip_longest()`](https://docs.python.org/3.7/library/itertools.html#itertools.zip_longest) function should be wrapped with something that limits the number of calls (for example [`islice()`](https://docs.python.org/3.7/library/itertools.html#itertools.islice) or [`takewhile()`](https://docs.python.org/3.7/library/itertools.html#itertools.takewhile)). If not specified, *fillvalue* defaults to `None`.





输出的结果是一个 **zip 对象**，包含了如何对其中元素进行迭代的信息。 `zip`函数最常用于 `for` 循环：

```
>>> for pair in zip(s, t):
...     print(pair)
...
('a', 0)
('b', 1)
('c', 2)
```

`zip`对象是**迭代器**的一种，即任何能够按照某个序列迭代的对象。 迭代器在某些方面与列表非常相似，但不同之处在于，你无法通过索引来选择迭代器中的某个元素。

如果你想使用列表操作符和方法，你可以通过 `zip` 对象创建一个列表：

```
>>> list(zip(s, t))
[('a', 0), ('b', 1), ('c', 2)]
```

结果就是一个包含若干元组的列表；在这个例子中，每个元组又包含了字符串中的一个字符和列表 中对应的一个元素。

如果用于创建的序列长度不一，返回对象的长度以最短序列的长度为准。

```
>>> list(zip('Anne', 'Elk'))
[('A', 'E'), ('n', 'l'), ('n', 'k')]
```

您可以在 `for` 循环中使用元组赋值，遍历包含元组的列表：

```
t = [('a', 0), ('b', 1), ('c', 2)]
for letter, number in t:
    print(number, letter)
```

每次循环时，Python 会选择列表中的下一个元组， 并将其内容赋给 `letter`和 `number` 。循环的输出是：

```
0 a
1 b
2 c
```

如果将 `zip` 、`for` 循环和元组赋值结合起来使用，你会得到一个可以同时遍历两个（甚至多个）序列的惯用法。 例如，`has_match` 接受两个序列 `t1` 和 `t2` ， 如果存在索引 `i` 让 `t1[i] == t2[i]` ，则返回 `True` ：

```
def has_match(t1, t2):
    for x, y in zip(t1, t2):
        if x == y:
            return True
    return False
```