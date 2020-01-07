# 序列类型(list, tuple, range)

Python 中包含基本[序列类型](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range) ( [list](https://docs.python.org/3/library/stdtypes.html#list)、[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)、[range](https://docs.python.org/3/library/stdtypes.html#range) ) 和专门用于处理 [text strings](https://docs.python.org/3/library/stdtypes.html#textseq) 和  [binary data](https://docs.python.org/3/library/stdtypes.html#binaryseq) 的附加序列类型。

如果需要了解各种序列都支持哪些操作，请查看笔记『序列类型支持的操作.md』

## 1. 列表 list

> 本节涵盖了 [Lists](https://docs.python.org/3.7/library/stdtypes.html#lists) 中的所有知识点，并进行了扩展。

列表属于可变序列类型，在同一个列表中可以存储不同类型的元素。

### 1.1 构建列表

可通过以下几种方式来构建列表：

- 使用一对方括号可构建一个空列表：`[]`
- 使用一对方括号，并在其中填充以逗号分隔的项：`[a]`, `[a, b, c]` , `[*(1,2,3)]`
- 使用列表解析(*comprehension*)：`[x for x in iterable]`
- 使用类型构造器(*constructor*)：`list()` 或 `list(iterable)`

🔨 *class* list([*iterable*])

通过构造函数创建列表对象时，新建列表对象中各个项的值和顺序均与 *iterable* 中各个项的值和顺序相同。*iterable* 可以是序列，也可是支持迭代的容器，还可以是迭代器对象。如果没有向构造函数传递实参，则会创建一个空列表。

```python
>>> list('abc')
['a', 'b', 'c']
>>> list( (1, 2, 3) )
[1, 2, 3]
>>> list()
[]
```

如果 *iterable* 本身就是一个列表，则会返回该列表的浅拷贝，与 `iterable[:]` 等效：

```python
list_1 = [[1,2],'orca']
list_2 = list(list_1)
```

执行结果：

![构建列表](序列类型(list,tuple,range).assets/构建列表.png)

另外许多操作也会生成特定的列表，比如内置函数 `sorted` 。

### 1.2 列表支持的操作

列表中实现了所有[通用序列操作](https://docs.python.org/3/library/stdtypes.html#typesseq-common)和所有[可变序列操作](https://docs.python.org/3/library/stdtypes.html#typesseq-mutable)，并且还实现了下列附加方法：

#### list.sort()

🔨 list.sort(\*, *key=None*, *reverse=False*)

`sort` 方法会对列表对象进行原地排序(in-place)，并且仅会使用 `<` 来比较列表中不同的元素。该方法不会禁用异常，因此如果某个比较操作失败，整个排序操作都会失败。排序失败时，列表中可能会保留部分已被修改的状态。例如：

```python
list_ = [5, 2, 4, 6, 'A']
try:
    list_.sort()
except Exception:
    pass
finally:
    print(list_) # Out: [2, 4, 5, 6, 'A']
```

在向 `sort()` 传递实参时，只能使用关键字参数，各参数含义如下：

- *key* : 用于引入一个**单参数**的**可调用对象**(如 `key=str.lower`)，该对象用于提取列表中各个元素的比较键(*comparison key*)，并以"比较键"的顺序作为排序依据。如果保持默认值 `None`，则会直接比较列表中的各个元素。
- *reverse* : 一个布尔值，用于控制排列顺序。默认值 `False` 表示以升序排列列表中的元素；`True` 则表示以降序排列 *iterable* 中的元素。

[`functools.cmp_to_key()`](https://docs.python.org/3/library/functools.html#functools.cmp_to_key) 函数用于将 Py2.x 中的旧式比较函数(*comparison function*)转换为[键函数](https://docs.python.org/3.7/glossary.html#term-key-function)(*key function*)，在 Py3.2 中被引入。有关 `cmp_to_key` 的更多信息，需阅读笔记『sorted.md』

`sort` 方法会在原地(*in-place*)对列表进行排序以节省空间。为了提醒用户该操作的副作用，该操作并不会返回排序后的序列，而是返回 `None`。与 `sort` 不同， `sorted()` 函数并不会修改原序列对象，而是会返回一个已排序的新序列对象。

 [`sort()`](https://docs.python.org/3/library/stdtypes.html#list.sort) 方法采用稳定排序算法，阅读笔记『sorted.md』，可了解有关稳定性的更多信息。

**CPython implementation detail:** While a list is being sorted, the effect of attempting to mutate, or even inspect, the list is undefined. The C implementation of Python makes the list appear empty for the duration, and raises [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) if it can detect that the list has been mutated during a sort.

### 1.3 提示

#### a. 枚举列表

可使用内置函数 `enumerate` 对列表中的元素进行枚举：

```python
>>> for i in enumerate([1, 2, 3]): print(i)

(0, 1)
(1, 2)
(2, 3)
```

有关 `enumerate` 的更多信息，需阅读笔记『enumerate.md』

#### b. 浅拷贝和深拷贝

浅拷贝时，原序列中引用的可变对象**不会产生**新副本，仅会对可变对象的引用进行多次拷贝。若在新副本中修改可变对象，原副本中的可变对象也会发生改变。copy 模块中的 `copy()` 属于浅拷贝(*shallow copy*)

深拷贝时，原序列中引用的可变对象都**会产生**新副本，并会在新序列中引用这些副本。若在新副本中修改可变对象，原副本中的可变对象不受影响。copy 模块中的 `deepcopy()` 属于深拷贝(*deep copy*)

对于不可变对象，由于本身并不能被修改，因此在浅拷贝和深拷贝中都直接拷贝其引用。

示例 - 观察浅拷贝和深拷贝的区别：

```python
import copy
list_ = [[1,2],(3,4),'orca']
# 三种浅拷贝
list_2 = list(list_)
list_3 = list_[:]
list_4 = copy.copy(list_)
# 深拷贝
list_5 = copy.deepcopy(list_)
```

执行结果：

![浅拷贝和深拷贝](序列类型(list,tuple,range).assets/浅拷贝和深拷贝.png)

扩展阅读：

- [Python---copy()、deepcopy()与赋值的区别](https://blog.csdn.net/u011630575/article/details/78604226)
- [Python中 copy, deepcopy 的区别及原因](https://iaman.actor/blog/2016/04/17/copy-in-python)





#### c. 列表与栈

栈(*stack*)遵循『last-in, first-out』原则，并且在列表尾部可快速执行 `append` 和 `pop` 操作的速度，因此我们可将列表用作栈， `append()` 用于入栈，`pop()` 用于出栈。例如：

```python
>>> stack = [3, 4, 5]
>>> stack.append(6)
>>> stack.append(7)
>>> stack
[3, 4, 5, 6, 7]
>>> stack.pop()
7
>>> stack
[3, 4, 5, 6]
```

#### d. 列表与队列

队列(*queue*)遵循『first-in, first-out』原则，由于在列表头部执行插入和弹出操作会很慢——在列表头部进行操作时，其后的所有元素都会被移动。因此将列表用作队列时效率很低。

队列可使用 [`deque`](https://docs.python.org/3/library/collections.html#collections.deque) 对象（双端队列）实现，该类可从两端快速添加或删除。

```python
>>> from collections import deque
>>> queue = deque(["Eric", "John", "Michael"])
>>> queue.append("Terry")           # Terry arrives
>>> queue.append("Graham")          # Graham arrives
>>> queue.popleft()                 # The first to arrive now leaves
'Eric'
>>> queue.popleft()                 # The second to arrive now leaves
'John'
>>> queue                           # Remaining queue in order of arrival
deque(['Michael', 'Terry', 'Graham'])
```

#### e. 循环空列表

对空列表执行 for 循环时，将不会执行循环主体：

```python
for x in []:
    print('This never happens.')
```

#### f. 列表解析

参考笔记『解析式.md』

## 2. 元组 tuple

> 本节涵盖了 [Tuples](https://docs.python.org/3.7/library/stdtypes.html#tuples) 中的所有知识点，并进行了扩展。

元组属于不可变序列类型，实现了所有**通用序列操作**，可用于存储异构数据集合和同构数据集合。由于元组是不可变类型，因此可将其用作 [`dict`](https://docs.python.org/3/library/stdtypes.html#dict) 的键(*key*)，或是被存储在 [`set`](https://docs.python.org/3/library/stdtypes.html#set) 和 [`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset) 中。

尽管元组表面上类似于列表，但常被用于不同的目的。列表通常会包含同构元素序列，并以迭代的方式访问。元组通常包含异构元素序列，通过解包或索引进行访问。

相较于可变序列，元组会让代码更加安全，并且不会占据额外的内存空间(Hint：在创建列表时，系统为列表多分配一些空间，以优化"添加"操作的性能)。

### 2.1 构建元组

可通过以下几种方式来构建元组：

- 使用一对圆号可构建一个空元组：`()`
- 构建单元素元组时，需在元素后面附加一个逗号：`a,` 或 `(a,)`
- 构建多元素元组时，需使用逗号分隔每个项：`a, b, c` , `(a, b, c)`
- 使用类型构造器(*constructor*)：`tuple()` , `tuple(iterable)`

Note：通过中间两种方式构建元组时，实际上是由于逗号的存在才产生了元组，即便省略括号也可照常构建元组。圆括号作为可选部分，其作用是为了避免语法歧义。例如，`f(a, b, c)` 表示以三个实参来调用函数，而 `f((a, b, c))` 则表示以单个实参( 3 元元组)来调用函数。

🔨 *class* tuple([*iterable*])

通过构造函数创建元组对象时，新建元组对象中各个项的值和顺序均与 *iterable* 中各个项的值和顺序相同。*iterable* 可以是序列，也可是支持迭代的容器，还可以是迭代器对象。如果没有向构造函数传递实参，则会创建一个空元组。

```python
>>> tuple('abc')
('a', 'b', 'c')
>>> tuple( [1, 2, 3] )
(1, 2, 3)
>>> tuple()
()
```

如果 *iterable* 本身就是一个元组，则会直接返回该元组对象，与 `iterable[:]` 等效：

```python
tuple_ = ((1,2),'orca')
tupls_1 = tuple(tuple_)
tupls_2 = tuple_[:]
```

执行结果：

![元组_01](序列类型(list,tuple,range).assets/元组_01.png)

### 2.2 提示

#### a. namedtuple

在使用异构数据集合时，如果需要通过名称来访问其中的元素，可使用 [`collections.namedtuple()`](https://docs.python.org/3.7/library/collections.html#collections.namedtuple) 对象。

```python
>>> from collections import namedtuple
>>> Student = namedtuple('Student',['name','age'])
>>> joy = Student('Joy',16)
>>> joy.name
'Joy'
>>> joy.age
16
>>> joy
Student(name='Joy', age=16)
```

#### b. 引用可变对象

元组本身虽是不可变类型，但是元组的项可以引用可变对象，并且被引用的可变对象是可以被修改的。

如果尝试哈希"引用了可变对象"的元组，则会抛出  [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError) ，并且这样的元组不能用作 [`dict`](https://docs.python.org/3/library/stdtypes.html#dict) 的键(*key*)，或是被存储在 [`set`](https://docs.python.org/3/library/stdtypes.html#set) 和 [`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset) 中。

```python
>>> a_list = (1,[1,2])
>>> a_list[1].append(3)
>>> a_list
(1, [1, 2, 3])
>>> hash(a_list)
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    hash(a_list)
TypeError: unhashable type: 'list'
>>> {a_list = (1,[1,2])}
SyntaxError: invalid syntax
```

由此可见，不可变序列是指序列中每个项的引用不能被改变，而被引用的对象可以是可变对象。

#### c. 拷贝元组

当我们试图拷贝一个元组时，可能会出现以下两种情况：

- 被拷贝的元组中只包含不可变对象，此时会直接引用原来的元组对象，不会产生任何副本，浅拷贝和深拷贝均如此：

  ```python
  import copy
  tuple_ = ((1,2),'orca')
  tupls_1 = tuple(tuple_)
  tupls_2 = tuple_[:]
  tuple_3 = copy.copy(tuple_)
  tuple_4 = copy.deepcopy(tuple_)
  ```

  执行结果：

  ![拷贝元组_01](序列类型(list,tuple,range).assets/拷贝元组_01.png)

- 被拷贝的元组中包含可变对象，此时浅拷贝会直接引用原来的元组对象，不会产生任何副本；深拷贝会创建一个副本：

  ```python
  import copy
  tuple_ = ((1,2),'orca',[1,2])
  tupls_1 = tuple(tuple_)
  tupls_2 = tuple_[:]
  tuple_3 = copy.copy(tuple_)
  tuple_4 = copy.deepcopy(tuple_)
  ```

  执行结果：

  ![拷贝元组_02](序列类型(list,tuple,range).assets/拷贝元组_02.png)

## 3. range

> 本节涵盖了 [Ranges](https://docs.python.org/3.7/library/stdtypes.html#ranges) 中的所有知识点，并进行了扩展。

range 对象表示由一组整数构成的不可变序列，我们通常会在 [`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环中用 range 对象来指定循环次数。

### 3.1 构建 range 对象

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

  对上述两个公式而言，如果 `r[0]` 不满足相应的约束条件，则实例 `r` 为空。

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

Changed in version 3.2: Implement the Sequence ABC. Support slicing and negative indices. Test [`int`](https://docs.python.org/3.7/library/functions.html#int) objects for membership in constant time instead of iterating through all items.

Changed in version 3.3: Define ‘==’ and ‘!=’ to compare range objects based on the sequence of values they define (instead of comparing based on object identity).

New in version 3.3: The [`start`](https://docs.python.org/3.7/library/stdtypes.html#range.start), [`stop`](https://docs.python.org/3.7/library/stdtypes.html#range.stop) and [`step`](https://docs.python.org/3.7/library/stdtypes.html#range.step) attributes.

扩展阅读：[linspace recipe](http://code.activestate.com/recipes/579000/) 展示了如何实现一个浮点版本的 range 类型

### 3.2 range 支持的操作

range 对象中实现了除 `+` (连接) 和 `*` (重复)操作以外的所有通用序列操作。因为 range 对象表示的序列必须严格遵循既定模式(*pattern*)，而 `+` 和 `*` 操作通常会违反既定模式。

```python
>>> r = range(0, 20, 2)
>>> r
range(0, 20, 2)
>>> 11 in r
False
>>> 10 in r
True
>>> r.index(10)
5
>>> r[5]
10
>>> r[:5]
range(0, 10, 2)
>>> r[-1]
18
```

range 对象同样支持序列拆封

```python
>>> a, b = range(2)
```

### 3.2 提示

#### a. range 支持负索引

range 对象同样支持负索引，负索引表示相对于 `r` 中最后一个元素的偏移量(从 `-1` 开始)。

```python
>>> r = range(10)
>>> r[-1]
9
```

#### b. 拷贝 range 对象

如果对 range 对象进行浅拷贝，则会直接引用原 range 对象；如果对 range 对象进行深拷贝，则会创建一个新的 range 对象：

```
import copy
r = range(10)
r1 = copy.copy(r)
r2 = copy.deepcopy(r)
```

执行结果：

![拷贝 range 对象](0x05 序列类型(list,tuple,range).assets/拷贝 range 对象.png)

#### c. 比较 range 对象

可使用比较运算符 `==` 和 `!=` 来测试 range 对象中所包含的序列是否相等。注意，这里是在考察序列是否相等，即便拥有不同 *start* , *stop* , *step* 值，只要序列中的元素相等即可：

```python
>>> range(0) == range(2, 1, 3)
True
>>> range(0, 3, 2) == range(0, 4, 2)
True
```

