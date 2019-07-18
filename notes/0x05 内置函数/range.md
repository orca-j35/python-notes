# range

```
class range(object)
 |  range(stop) -> range object
 |  range(start, stop[, step]) -> range object
 |  
 |  Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step. 
 |	range(i, j) produces i, i+1, i+2, ..., j-1.
 |  start defaults to 0, and stop is omitted!  
 |	range(4) produces 0, 1, 2, 3.
 |  These are exactly the valid indices for a list of 4 elements.
 |  When step is given, it specifies the increment (or decrement).
```

🔨 *class* range(*stop*)

🔨 *class* range(*start*, *stop*[, *step*])

在调用 range 类的构造函数时，必须使用整数作为实参。细节上而言，实参可以是 `int` 对象，或是实现任何了 `__index__` 方法的对象。

各参数的含义如下：

- *start* - 用于指定 range 序列的起点，在 range 的实例中包含该值。如果没有为 *start* 提供实参值，则默认其值为 `0` 

- *stop* - 用于指定 range 序列的终点，必须为 *stop* 提供实参值，但是在 range 的实例中不包含该值

- *step* - 用于设定步长，其值有以下几种情况 ( `r` 表示 range 类的实例)

  - 如果没有为 *step* 提供实参值，则默认其值为 `1`

    ```python
    >>> list(range(10))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> list(range(1, 11))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ```

  - 如果为 *step* 提供的实参值为 `0` ，则会抛出 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError) 异常

  - 如果向 *step* 传递一个正整数，那么实例 `r` 中所包含的元素需通过此公式来确定：`r[i] =start + step*i` where `i >= 0` and `r[i] < stop`

    ```python
    >>> list(range(0, 30, 5))
    [0, 5, 10, 15, 20, 25]
    >>> list(range(0, 10, 3))
    [0, 3, 6, 9]
    ```

  - 如果向 *step* 传递一个负整数，那么实例 `r` 中所包含的元素需通过此公式来确定：`r[i] =start + step*i` where `i >= 0` and `r[i] > stop`

    ```python
    >>> list(range(0, -10, -1))
    [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
    ```

  对上述两个公式而言，如果 `r[0]` 不满足相应的约束条件，则实例 `r` 中的序列为空。

  ```
  >>> list(range(0))
  []
  >>> list(range(1, 0))
  []
  ```

虽然 Python 允许 range 对象的长度大于 [`sys.maxsize`](https://docs.python.org/3.7/library/sys.html#sys.maxsize)，但部分功能可能会因此抛出 [`OverflowError`](https://docs.python.org/3.7/library/exceptions.html#OverflowError) 异常，比如 `len()` ：

```python
>>> r=range(100000000000000000000000)
>>> len(r)
Traceback (most recent call last):
  File "<pyshell#79>", line 1, in <module>
    len(r)
OverflowError: Python int too large to convert to C ssize_t
```

range 类型相较于列表或元组的优势在于，无论 range 对象的长度如何变化，其占用的内存量总是相同的，而且占用的内存也很少。因为在 range 对象中仅存储了 *start* , *stop* , *step* 三个值，只有当我们需要某个项或 subrange 时，range 对象才会计算出相应的值，range 对象本身并不会直接存储所有的元素。

扩展阅读：

- 笔记『序列类型(list,tuple,range).md』
- [Ranges](https://docs.python.org/3.7/library/stdtypes.html#ranges) 
- [Sequence Types — list, tuple, range](https://docs.python.org/3.7/library/stdtypes.html#typesseq)

