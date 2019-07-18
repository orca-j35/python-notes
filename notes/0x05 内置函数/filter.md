# filter

```
class filter(object)
 |  filter(function or None, iterable) --> filter object
 |  
 |  Return an iterator yielding those items of iterable for which function(item)
 |  is true. If function is None, return the items that are true.
```

filter 函数大致相当于如下代码：

```python
def filter(function, iterable):
    if function is None:
        function = bool
    for x in iterable:
        if function(x):
            yield x
```

filter 函数会返回一个迭代器——该迭代器其实是一个支持迭代器协议的 filter 对象。
*iterable* 参数可以是序列(sequence)，或是支持迭代的容器(container)，还可以是迭代器。

🔨 filter(*None*, *iterable*)

如果在调用 filter 函数时，***function* 的值是 None**，便会将 *iterable* 中布尔值为真的元素依次用作迭代器的生成项。下面这个生成器表达式与 `filter(None, iterable)` 等价：

```
(item for item in iterable if item)
```

一个简单的示例：

```python
>>> list(filter(None,['',False,'I',{}]))
['I']
```

🔨 filter(*function*, *iterable*)

如果在调用 filter 函数时，***function* 的值是一个可调用对象**，迭代器会将 *iterable* 中的各个元素依次传递给 *function*，并将返回值为真的元素依次用作迭代器的生成项。下面这个生成器表达式与 `filter(function, iterable)` 等价：

```
(item for item in iterable if function(item))
```

一些简单的示例：

```python
>>> # 保留iterable中的奇数
>>> list(filter(lambda x: x % 2,range(10)))
[1, 3, 5, 7, 9]
>>> # 删除序列中的空字符串
>>> list(filter(lambda x: x and x.strip(), 
                ['A', '', 'B', None, 'C', '  ']))
['A', 'B', 'C']
```

示例，利用[埃氏筛法](http://baike.baidu.com/view/3784258.htm)来获取全体素数的集合：

```python
# 奇数生成器
def _odd_iter(): 
    n = 1
    while True:
        n = n + 2
        yield n
# 定义筛选函数：
def _not_divisible(n):
    return lambda x: x % n > 0
    
# 定义用于返回素数的生成器：
def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列
```

## itertools.filterfalse

filterfalse 函数大致相当于如下代码：

```python
def filterfalse(predicate, iterable):
    # filterfalse(lambda x: x%2, range(10)) --> 0 2 4 6 8
    if predicate is None:
        predicate = bool
    for x in iterable:
        if not predicate(x):
            yield x
```

[filterfalse](https://docs.python.org/3.7/library/itertools.html#itertools.filterfalse) 函数会返回一个迭代器，它的功能与 filter 函数正好相反。

🔨 itertools.filterfalse(*None*, *iterable*) 

如果在调用 filterfalse 函数时，*predicate* 的值是 *None*，便会将 *iterable* 中布尔值为**假**的元素依次用作迭代器的生成项。

```python
>>> import itertools
>>> list(itertools.filterfalse(None,['',False,'I',{}]))
['', False, {}]
```

🔨 itertools.filterfalse(*predicate*, *iterable*) 

如果在调用 filterfalse 函数时，***predicate* 的值是一个可调用对象**，迭代器会将 *iterable* 中的各个元素依次传递给 *predicate*，并将返回值为**假**的元素依次用作迭代器的生成项。

```python
>>> import itertools
>>> list(itertools.filterfalse(lambda x: x%2, range(10)))
[0, 2, 4, 6, 8]
```

