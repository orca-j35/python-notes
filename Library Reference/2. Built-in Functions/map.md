# map

```
class map(object)
 |  map(func, *iterables) -> map object
 |  
 |  Make an iterator that computes the function using arguments from
 |  each of the iterables.  Stops when the shortest iterable is exhausted.
```

map 函数大致相当于如下代码：

```python
def map_(function, *iterable):
    args_zip = zip(*iterable)
    for args in args_zip:
        yield function(*args)
"""测试：
>>> list(map_(lambda x, y: (x, y), [1, 2, 3, 4], [1, 2, 3]))
[(1, 1), (2, 2), (3, 3)]
"""
```

🔨map(*function*, *iterable*, ...)

map 函数会返回一个迭代器——该迭代器其实是一个支持迭代器协议的 map 对象。
此迭代器会将 *iterable* 中的各个元素依次传递给 *function*，并将 *function* 的返回值依次用作迭代器的生成项。

```python
>>> map_obj_str = map(str,[1,2,3,4])
>>> map_obj_str
<map object at 0x0000027540C370B8>
>>> list(map_obj_str)
['1', '2', '3', '4']
>>> list(map_obj_str) # map对象不可以被重复迭代
[]
```

map 函数可接受多个的 *iterable* 对象，这些 *iterable* 对象中的元素会被**并行**传递给 *function* ，因此 *function* 函数的**参数的数量**必须与 *iterable* 对象的数量相**匹配**，否则会抛出 `TypeError`。

```python
>>> # map函数可接受多个iterable对象
>>> map_obj = map(lambda x,y: (x ,y), [1, 2, 3, 4],[1, 2, 3, 4])
>>> list(map_obj)
[(1, 1), (2, 2), (3, 3), (4, 4)]
>>>
>>> # 如果参数不匹配，便会抛出 TypeError
>>> map_obj_err = map(lambda x: x, [1, 2, 3, 4],[1, 2, 3])
>>> list(map_obj_err)
Traceback (most recent call last):
  File "<pyshell#23>", line 1, in <module>
    list(map_obj_err)
TypeError: <lambda>() takes 1 positional argument but 2 were given
```

使用多个 *iterable* 对象时，其中最短的 *iterable* 对象决定了迭代器的迭代次数。也就是说，只要有一个 *iterable* 对象已被耗尽，迭代器便会停止。

```python
>>> # 最短的iterable对象决定了迭代器的迭代次数
>>> map_obj_ = map(lambda x,y: (x ,y), [1, 2, 3, 4],[1, 2, 3])
>>> list(map_obj_)
[(1, 1), (2, 2), (3, 3)]
```

**扩展阅读**：Google 的论文“[MapReduce: Simplified Data Processing on Large Clusters](https://ai.google/research/pubs/pub62)”，有助于理解 map/reduce 的概念。

## itertools.starmap

在 map 函数中，*function* 的实参被分散在不同的 *iterable* 对象中。如果已提前将这些实参打包至不同的元组中，则需要使用[`itertools.starmap()`](https://docs.python.org/3.7/library/itertools.html#itertools.starmap) 函数。

starmap 函数大致相当于如下代码：

```python
def starmap(function, iterable):
    # starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000
    for args in iterable:
        yield function(*args)
```

🔨itertools.starmap(*function*, *iterable*)

starmap 函数会返回一个迭代器，该迭代器同样会将 *iterable* 中的各个元素依次传递给 *function*，并将 *function* 的返回值依次用作迭代器的生成项。与 map 函数的不同之处在于， *iterable* 对象中的每个元素都是一个由 *function* 的实参组合而成的元组。

```python
>>> import itertools
>>> star_map_ = itertools.starmap(lambda x,y: (x,y), 
                                  [(1, 1), (2, 2), (3, 3), (4,4)])
							# 每次调用function所需的实参，被组合为一个元组
>>> list(star_map_)
[(1, 1), (2, 2), (3, 3), (4, 4)]
>>>
>>> star_map = itertools.starmap(lambda *args: (args), 
                                 [(1, 1), (2, 2), (3, 3), (4,)])
>>> list(star_map)
[(1, 1), (2, 2), (3, 3), (4,)]
```

如果某个元组与 *function* 所需参数不匹配，便会抛出 `TypeError`：

```python
>>> # 如果某个元组与参数不匹配，便会抛出 TypeError
>>> star_map_err = itertools.starmap(lambda x,y: (
    x,y), [(1, 1), (2, 2), (3, 3), (4,)])
>>> list(star_map_err)
Traceback (most recent call last):
  File "<pyshell#42>", line 1, in <module>
    list(star_map_)
TypeError: <lambda>() missing 1 required positional argument: 'y'
>>> 
```

