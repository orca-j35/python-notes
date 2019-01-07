# functools - Higher-order functions and operations on callable objects
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 详见：
>
> - [`functools`](https://docs.python.org/3.7/library/functools.html#module-functools) — Higher-order functions and operations on callable objects
> - [functools — 函数操作工具箱](https://pythoncaff.com/docs/pymotw/functools-function-operation-toolbox/92)

`functools` 模块用于高阶函数，该模块提供了许多改写或拓展函数或其他可调用对象的工具，而无需完全重写它们。

在 `functions` 中定义了如下函数：

## 🔨cmp_to_key

> 相关笔记:﹝sorted.md﹞

🔨 functools.cmp_to_key(*func*)

用于将旧式的比较函数转换为键函数([*key* *function*](https://docs.python.org/3.7/glossary.html#term-key-function))。可与接受键函数的工具一起使用(e.g.,  [`sorted()`](https://docs.python.org/3.7/library/functions.html#sorted), [`min()`](https://docs.python.org/3.7/library/functions.html#min), [`max()`](https://docs.python.org/3.7/library/functions.html#max), [`heapq.nlargest()`](https://docs.python.org/3.7/library/heapq.html#heapq.nlargest), [`heapq.nsmallest()`](https://docs.python.org/3.7/library/heapq.html#heapq.nsmallest), [`itertools.groupby()`](https://docs.python.org/3.7/library/itertools.html#itertools.groupby))。

A comparison function is any callable that accept two arguments, compares them, and returns a negative number for less-than, zero for equality, or a positive number for greater-than. A key function is a callable that accepts one argument and returns another value to be used as the sort key.

Example:

```
sorted(iterable, key=cmp_to_key(locale.strcoll))  # locale-aware sort order
```

For sorting examples and a brief sorting tutorial, see [Sorting HOW TO](https://docs.python.org/3.7/howto/sorting.html#sortinghowto).

New in version 3.2.

## 🔨lru_cache

> 相关笔记:﹝装饰器.md﹞-> 标准库中的装饰器

🔨 @functools.lru_cache(*maxsize=128*, *typed=False*)

该装饰器实现了备忘(*memoization*)功能，会让某函数具有最近最小缓存机制([*Least* *Recently* *Used* (LRU) *cache*](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)))。所有传递过来的参数都会被哈希化，用于后续结果的映射。之后再次调用相同的参数时会从缓存中直接调取出结果而不再经过函数运算。同时此装饰器还给原函数加了一个用于检测缓存状态的方法(`cache_info()`)和一个清空缓存的方法(`cache_clear()`)。

The `maxsize` parameter specifies how many recent calls are cached. The default value is 128, but you can specify `maxsize=None` to cache all function calls. However, be aware that this can cause memory problems if you are caching many large objects.

You can use the `.cache_info()` method to see how the cache performs, and you can tune it if needed. 

```python
import functools

@functools.lru_cache(maxsize=4)
def fibonacci(num):
    print(f"Calculating fibonacci({num})")
    if num < 2:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)
```

 In our example, we used an artificially small `maxsize` to see the effect of elements being removed from the cache:

```python
>>> fibonacci(10)
Calculating fibonacci(10)
Calculating fibonacci(9)
Calculating fibonacci(8)
Calculating fibonacci(7)
Calculating fibonacci(6)
Calculating fibonacci(5)
Calculating fibonacci(4)
Calculating fibonacci(3)
Calculating fibonacci(2)
Calculating fibonacci(1)
Calculating fibonacci(0)
55

>>> fibonacci(8)
21

>>> fibonacci(5)
Calculating fibonacci(5)
Calculating fibonacci(4)
Calculating fibonacci(3)
Calculating fibonacci(2)
Calculating fibonacci(1)
Calculating fibonacci(0)
5

>>> fibonacci(8)
Calculating fibonacci(8)
Calculating fibonacci(7)
Calculating fibonacci(6)
21

>>> fibonacci(5)
5

>>> fibonacci.cache_info()
CacheInfo(hits=17, misses=20, maxsize=4, currsize=4)
```



## 🔨total_ordering

🔨 @functools.total_ordering

为定义了部分富比较方法的类自动提供其余的富比较方法，前提条件如下：

The class must define one of [`__lt__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__lt__), [`__le__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__le__), [`__gt__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__gt__), or [`__ge__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__ge__). In addition, the class should supply an [`__eq__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__eq__) method. ​

```python
@total_ordering
class Student:
    def _is_valid_operand(self, other):
        return (hasattr(other, "lastname") and
                hasattr(other, "firstname"))
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))
```

注意：虽然这个装饰器可以很容易地创建表现良好的完全有序的类型，但它确实以较慢的执行成本和更复杂的派生比较方法的堆栈跟踪为代价。

New in version 3.2.

Changed in version 3.4: Returning NotImplemented from the underlying comparison function for unrecognised types is now supported.

## 🔨partial

> 扩展阅读:
>
> - ﹝流畅的 Python﹞-> 5.10.2　使用 `functools.partial` 冻结参数

🔨 functools.partial(*func*, \**args*, \*\**keywords*)

此高阶函数用于部分应用一个函数，将返回一个 `partial` 对象。部分应用是指，基于一个函数创建一个新的可调用对象，把原函数的某些参数固定。使用这个函数可以把接受一个或多个参数的函数改编成需要回调的 API，这样参数更少。

示例 - 使用 `partial` 把一个两参数函数改编成需要单参数的可调用对象。

```python
>>> from operator import mul
>>> from functools import partial
>>> triple = partial(mul, 3)
>>> triple(7)
21
>>> list(map(triple, range(1, 10)))
[3, 6, 9, 12, 15, 18, 21, 24, 27]
```

`partial` 的第一个参数是一个可调用对象，后面跟着任意个要绑定的定位参数和关键字参数。 `partial` 大致相当于如下代码：

```python
def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args, *fargs, **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
```

### [`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) Objects

[`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) objects are callable objects created by [`partial()`](https://docs.python.org/3.7/library/functools.html#functools.partial). They have three read-only attributes:

- partial.func

  A callable object or function. Calls to the [`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) object will be forwarded to [`func`](https://docs.python.org/3.7/library/functools.html#functools.partial.func) with new arguments and keywords.

- partial.args

  The leftmost positional arguments that will be prepended to the positional arguments provided to a [`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) object call.

- partial.keywords

  The keyword arguments that will be supplied when the [`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) object is called.

[`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) objects are like `function` objects in that they are callable, weak referencable, and can have attributes. There are some important differences. For instance, the [`__name__`](https://docs.python.org/3.7/library/stdtypes.html#definition.__name__) and `__doc__` attributes are not created automatically. Also, [`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) objects defined in classes behave like static methods and do not transform into bound methods during instance attribute look-up.

## 🔨partialmethod

🔨 *class* functools.partialmethod(*func*, \**args*, \*\**keywords*)

`functools.partialmethod` 函数的作用与 `partial` 一样，不过被用于处理方法。

Return a new [`partialmethod`](https://docs.python.org/3.7/library/functools.html#functools.partialmethod) descriptor which behaves like [`partial`](https://docs.python.org/3.7/library/functools.html#functools.partial) except that it is designed to be used as a method definition rather than being directly callable.

示例:

```python
>>> class Cell(object):
...     def __init__(self):
...         self._alive = False
...     @property
...     def alive(self):
...         return self._alive
...     def set_state(self, state):
...         self._alive = bool(state)
...     set_alive = partialmethod(set_state, True)
...     set_dead = partialmethod(set_state, False)
...
>>> c = Cell()
>>> c.alive
False
>>> c.set_alive()
>>> c.alive
True
```

New in version 3.4.

## 🔨reduce

> 扩展阅读:
>
> - ﹝流畅的 Python﹞-> 5.2 高阶函数
> - ﹝流畅的 Python﹞-> 5.10 支持函数式编程的包

🔨 functools.reduce(*function*, *iterable*[, *initializer*])

该函数的功能如下：

```python
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
```

大致等效于以下代码：

```python
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value
```

tips: *function* 参数必须能够接受两个实参，且必须有恰当的返回值。

示例 - 实现 `int` 函数的功能：

```python
from functools import reduce
def str2int(s):
    def char2num(s):
        return {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9
        }[s]
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))
str2int('232') #> 232
```

## 🔨singledispatch

> 相关笔记:﹝装饰器.md﹞-> 标准库中的装饰器

🔨 @functools.singledispatch

在动态类型语言(如 Python)中，经常有在执行时需要辨别不同类型的参数的需求，比如要处理的是一个列表里的数据还是一个单个的数据。直接检测参数的类型当然简单，但不同的功能也可以写到不同的函数中，所以 `functools` 提供了 `singledispatch()` 装饰器来让我们注册 *泛型函数* 以自动基于类型进行切换。

## 🔨update_wrapper

🔨 functools.update_wrapper(*wrapper*, *wrapped*, *assigned=WRAPPER_ASSIGNMENTS*, *updated=WRAPPER_UPDATES*)

更新 *wrapper* 函数，使其看起来像 *wrapped* 函数。

## 🔨wraps

> 相关笔记:﹝装饰器.md﹞-> 标准库中的装饰器

🔨 @functools.wraps(*wrapped*, *assigned=WRAPPER_ASSIGNMENTS*, *updated=WRAPPER_UPDATES*)

等效于 `partial(update_wrapper,wrapped=wrapped, assigned=assigned, updated=updated)`. 