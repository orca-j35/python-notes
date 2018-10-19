# 序列类型(list, tuple, range)

Python 中包含基本[序列类型](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range) ( [list](https://docs.python.org/3/library/stdtypes.html#list)、[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)、[range](https://docs.python.org/3/library/stdtypes.html#range) ) 和专门用于处理 [text strings](https://docs.python.org/3/library/stdtypes.html#textseq) 和  [binary data](https://docs.python.org/3/library/stdtypes.html#binaryseq) 的附加序列类型。



## 1. 通用序列操作

大多数的序列类型都支持下表中的操作(*operation*)，包括可变(*mutable*)序列和不可变(immutable)序列。如果需要在自定义序列类型中实现下列操作，可以继承抽象基类 [`collections.abc.Sequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence) ，这样可以使实现过程更加容易。

下表中越靠近底部的"序列操作"优先级越高，其中 *s* 和 *t* 是相同类型的序列，*n*、*i*、*j* 、*k* 是整数。*x* 是满足 *s* 给定的限制条件的任意对象，限制条件包含类型限制和值限制。例如，[`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray) 对象只接受满足限制条件的整数：`0 <= x <= 255` 。

 `in` 和 `not in` 与比较操作具有相同的优先级。`+` (连接) 和 `*` (重复)操作符和数学运算中的 `+` 和 `*` 具有相同的优先级。

| Operation              | Result                                                       | Notes      |
| ---------------------- | ------------------------------------------------------------ | ---------- |
| `x in s`               | `True` if an item of *s* is equal to *x*, else `False`       | (1.1)      |
| `x not in s`           | `False` if an item of *s* is equal to *x*, else `True`       | (1.1)      |
| `s + t`                | the concatenation of *s* and *t*                             | (1.6)(1.7) |
| `s * n` or `n * s`     | equivalent to adding *s* to itself *n* times                 | (1.2)(1.7) |
| `s[i]`                 | *i* th item of *s*, origin 0                                 | (1.3)      |
| `s[i:j]`               | slice of *s* from *i* to *j*                                 | (1.3)(1.4) |
| `s[i:j:k]`             | slice of *s* from *i* to *j* with step *k*                   | (1.3)(1.5) |
| `len(s)`               | length of *s*                                                |            |
| `min(s)`               | smallest item of *s*                                         |            |
| `max(s)`               | largest item of *s*                                          |            |
| `s.index(x[, i[, j]])` | index of the first occurrence of *x* in *s* (at or after index *i* and before index *j*) | (1.8)      |
| `s.count(x)`           | total number of occurrences of *x* in *s*                    |            |

相同类型的序列对象还支持比较操作，但只有当两个序列对象属于相同类型，且两个序列中的每个元素均相等，以及两个序列类型长度相同时，才认为两个序列相等(更多细节请参考 [Comparisons](https://docs.python.org/3/reference/expressions.html#comparisons) )。

```python
>>> [1,2,3,4]<[2,3]
True
>>> [1,2]==[1,2]
True
```

### 1.1 in / not in

`in` 和 `not in` 通常被用于测试序列中是否包含某个元素，但在某些特殊序列类型中(如 [`str`](https://docs.python.org/3/library/stdtypes.html#str) 、[`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes) 、[`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray))，也可用于测试是否包含某个子序列：

```python
>>> "gg" in "eggs"
True
```

### 1.2 s\*n / n\*s

小于 `0` 的 *n* 值被视为 `0` 。如果 *n* 小于等于 `0` 将生成一个与 *s* 具备相同类型的空序列，例如：

```python
>>> 'orca'*-1
''
>>> 'orca'*0
''
```

在序列 *s* 中引用的可变对象并不会产生多个新副本，仅会对可变对象的引用进行多次拷贝，例如：

```python
>>> lists = [[]] * 3 # 对内层的空列表的引用进行了三次拷贝
>>> lists
[[], [], []] # 内层的三个空列表均指向同一个对象
>>> lists[0] is lists[1] is lists[2]
True
>>> lists[0].append(3)
>>> lists
[[3], [3], [3]]
```

列表 `[[]]` 是内含一个空列表的列表，而列表 `[[]] * 3` 中的三个子列表其实是对同一个空列表引用了三次。因此，只要对任意一个子列表做出了修改，便会同时影响 `lists` 中的所有子列表。

示例 - lists_2 中的两个子列表和 `list_1[0]` 引用了相同的对象。

```python
list_1 = [[1,2],'orca']
lists_2 = list_1*2
lists_2[0].append(3)
```

运行结果如下：

![通用序列操作_01](序列类型(list,tuple,range).assets/通用序列操作_01.png)



如果需要的话，可以通过以下方式创建出不同的子列表：

```python
>>> lists = [[] for i in range(3)]
>>> lists[0].append(3)
>>> lists[1].append(5)
>>> lists[2].append(7)
>>> lists
[[3], [5], [7]]
```

还可参考 [How do I create a multidimensional list?](https://docs.python.org/3/faq/programming.html#faq-multidimensional-list)

### 1.3 索引

*i* 和 *j* 都是索引(*index*)，如果索引是正整数，则表示相对于序列 *s* 中第一个元素的偏移量(从 `0` 开始)；如果索引是负整数，则表示相对于序列 *s* 中最后一个元素的偏移量(从 `-1` 开始)。负索引 *i* 或 *j* 等于 `len(s) + i` 或 `len(s)+ j`，因此，负索引的绝对值不能大于序列的长度。另外， `-0` 仍然等于 `0`。

```python
 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
   0   1   2   3   4   5
  -6  -5  -4  -3  -2  -1
```

在 `s[i]` 中使用超过序列的长度的索引，会抛出 IndexError 异常。

### 1.4 s[i:j]

`s[i:j]` 表示切片，用于从序列 *s* 中获取子序列，范围是 `i≤x<j`。切片是由原序列中对应项的**浅拷贝**组成的新序列。在 `s[i:j]` 中，若 *i* 或 *j* 超出了序列长度，则会被替换为序列长度 `len(s)`；若 *i* 被省略或是 `None`，则将 *i* 视为 `0`；若 *j* 被省略或是 `None`，则将 *j* 视为 `len(s)`；如果 `i≥j`，则切片为空。

```python
>>> list_=[1, 4, 9, 16, 25]
>>> list_[:] # 返回一个新的浅拷贝(shallow)
[1, 4, 9, 16, 25]
>>> list(list_) # 也会返回一个浅拷贝
```

### 1.5 s[i:j:k]

`s[i:j:k]` 表示以特定步长(*step*) *k* 进行切片：

- 如果 *k* 是正数，每一步的索引是 `x=i+n*k`，且 `i≤x<j`。也就是说，在进行切片时每一步的索引依次是 `i`, `i+k`, `i+2*k`, `i+3*k` ... 直到 *j* 为止，但不包含 *j* 。*i* 的"终值"为 `0` ，*j* 的终值为 `len(s)` 

  ```python
  >>> a_list = [0,1,2,3,4,5]
  >>> a_list[0:4:2]
  [0, 2]
  >>> a_list[0:5:2]
  [0, 2, 4]
  ```

- 如果 *k* 是负数，每一步的索引是 `x=i+n*k`，且 `i≥x>j`。也就是说，在进行切片时每一步的索引依次是 `i`, `i+k`, `i+2*k`, `i+3*k` ... 直到 *j* 为止，但不包含 *j* 。*i* 的"终值"为 `len(s) - 1` ；如果省略 *j* ，则会使用 *j* 的"终值"。

  ```python
  >>> a_list = [0,1,2,3,4,5]
  >>> a_list[4:1:-2] # 注意: i>j
  [4, 2]
  >>> a_list[4::-2]
  [4, 2, 0]
  >>> a_list[len(a_list)-1::-1]
  [5, 4, 3, 2, 1, 0]
  ```

在 `s[i:j:k]` 中，如果 *i* 或 *j* 被省略或是 `None`，则会将 *i* 或 *j* 视为对应的"终值(end value)" - 注意，"终值"依赖于 *k* 的符号。*k* 不可以被设置为 `0`，如果 *k* 是 `None` ，则会被视为 `1` 。

### 1.6 s + t

使用 `+` 连接序列时，会产生一个新的对象，不会改变原序列。这意味着通过连接多个序列的方式来构建一个新序列时，会花费较高的时间成本。如果想要将时间复杂度变为线性，可采用以下替代方案：

- 如果需要连接 `str` 对象，可构建一个由 `str` 对象组成的列表并在最后使用 [`str.join()`](https://docs.python.org/3/library/stdtypes.html#str.join) 进行合并；或将 `str` 对象写入到一个 [`io.StringIO`](https://docs.python.org/3/library/io.html#io.StringIO) 实例中，并在写入完成了检索该实例的值。
- 如果需要连接 `bytes` 对象，可以使用 [`bytes.join()`](https://docs.python.org/3/library/stdtypes.html#bytes.join) 或 [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO)，另外还可以使用 [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray) 对象执行原地(*in-place*)合并。 [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray) 是可变对象，并拥有高效的过度分配(overallocation )机制。
- 如果需要连接 `tuple` 对象，可使用 `list` 替代
- 对于其他类型，请阅读相关文档

### 1.7 特定序列类型

某些序列类型(如 [`range`](https://docs.python.org/3/library/stdtypes.html#range)) 仅支持由遵循特定模式(*pattern*)的构成的序列，因此不支持连接操作和重复操作。

### 1.8 s.index()

如果在序列 *s* 中无法找到值为 *x* 的项，`s.index(x[, i[, j]])` 便会抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) 。附加参数 *i* 和 *j* 用于指定搜索范围，但并非所有 `index` 方法的实现都支持附加参数。`s.index(x,i,j)` 大致相当于 `s[i:j].index(x)`，但并不会像后者一样拷贝列表中的数据以创建切片；并且前者返回的索引是相对于序列 *s* 起点处的偏移量，而后者的返回的索引是相对于切片起点处的偏移量。


## 2. 不可变序列类型

通常仅由不可变序列来实现的唯一一个操作是支持内置函数 [`hash()`](https://docs.python.org/3/library/functions.html#hash)，可变序列类型不会实现该操作。

```python
>>> hash('orca')
-4938345707532569492
>>> hash([1,2])
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    hash([1,2])
TypeError: unhashable type: 'list'
```

由于不可变序列支持 `hash` 函数，因此不可变序列可用作 [`dict`](https://docs.python.org/3/library/stdtypes.html#dict) 的键(*key*)，或是被存储在 [`set`](https://docs.python.org/3/library/stdtypes.html#set) 和 [`frozenset`](https://docs.python.org/3/library/stdtypes.html#frozenset) 中。

如果尝试哈希(*hash*)的不可变序列中包含了不可哈希(*unhashable*)的值，则会抛出  [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError) ：

```python
>>> hash((1,[1,2]))
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    hash((1,[1,2]))
TypeError: unhashable type: 'list'
```



## 3. 可变序列类型

可变序列类型包含了下表中的各种操作，通过这些操作可对序列对象自身进行修改。如果需要在自定义序列类型中实现下列操作，可以继承抽象基类 [`collections.abc.MutableSequence`](https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableSequence) ，这样可以使实现过程更加容易。

在下表中，*s* 是可变类型序列的一个实例，*t* 是任意可迭代(*iterable*)对象，*x* 是满足 *s* 给定的限制条件的任意对象，限制条件包含类型限制和值限制。例如，[`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray) 对象只接受满足限制条件的整数：`0 <= x <= 255` 。

| Operation                 | Result                                                       | Notes |
| ------------------------- | ------------------------------------------------------------ | ----- |
| `s[i] = x`                | item *i* of *s* is replaced by *x*                           |       |
| `s[i:j] = t`              | slice of *s* from *i* to *j* is replaced by the contents of the iterable *t* | (3.1) |
| `del s[i:j]`              | same as `s[i:j] = []`                                        |       |
| `s[i:j:k] = t`            | the elements of `s[i:j:k]` are replaced by those of *t*      | (3.2) |
| `del s[i:j:k]`            | removes the elements of `s[i:j:k]`from the list              |       |
| `s.append(x)`             | appends *x* to the end of the sequence (same as`s[len(s):len(s)] = [x]` ); return `None` |       |
| `s.clear()`               | removes all items from `s` (same as `del s[:]`); return `None` | (3.6) |
| `s.copy()`                | creates a shallow copy of `s` (same as `s[:]`)               | (3.6) |
| `s.extend(t)` or `s += t` | extends *s* with the contents of *t* (for the most part the same as `s[len(s):len(s)] = t` / `s[len(s):] = t`); return `None` |       |
| `s *= n`                  | updates *s* with its contents repeated *n* times             | (3.7) |
| `s.insert(i, x)`          | inserts *x* into *s* at the index given by *i* (same as `s[i:i] = [x]`); return `None` |       |
| `s.pop([i])`              | retrieves the item at *i* and also removes it from *s*       | (3.3) |
| `s.remove(x)`             | remove the first item from *s* where `s[i] == x`; return `None` | (3.4) |
| `s.reverse()`             | reverses the items of *s* in place; return `None`            | (3.5) |

### 3.1 s[i:j] = t

`j-i` 并不一定等于 `len(t)`，应理解为先从 `s[i]` 开始依次填充 *t* 中的内容，如果 `len(t)>(j-i)` ，便会继续填充 `s[j]` 之后的内容；反之则压缩 *s* 的长度：

```python
>>> list_1 = [1,2,3,4,5]
>>> list_1[0:3]=['#','#','#','#','#','#']
>>> list_1
['#', '#', '#', '#', '#', '#', 4, 5]
>>> list_2 = [1,2,3,4,5]
>>> list_2[0:3]=['#','#']
>>> list_2
['#', '#', 4, 5]
```

### 3.2 s[i:j:k] = t

*t* 必须和被替换的切片具有相同的长度。

```python
>>> list_1 = [1,2,3,4,5]
>>> list_1[::2] = ['#','#']
Traceback (most recent call last):
  File "<pyshell#27>", line 1, in <module>
    list_1[::2] = ['#','#']
ValueError: attempt to assign sequence of size 2 to extended slice of size 3
>>> list_1[::2] = ['#','#','#','#']
Traceback (most recent call last):
  File "<pyshell#28>", line 1, in <module>
    list_1[::2] = ['#','#','#','#']
ValueError: attempt to assign sequence of size 4 to extended slice of size 3
>>>
>>> list_1[::2] = ['#','#','#']
>>> list_1
['#', 2, '#', 4, '#']
```

### 3.3 s.pop([i])

可选实参 *i* 的默认值是 `-1`，因此在默认情况下会移除并返回最后一项

```python
>>> list_1 = [0,1,2]
>>> list_1.pop()
2
```

### 3.4 s.remove(x)

如果在 *s* 中并没有值为 *x* 的项，则会抛出 [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) 异常。

```python
>>> list_ = [0,1,2]
>>> list_.remove(2)
>>> list_.remove(2)
Traceback (most recent call last):
  File "<pyshell#37>", line 1, in <module>
    list_.remove(2)
ValueError: list.remove(x): x not in list
```

该方法的返回值是 `None`。

### 3.5 s.reverse()

在反转序列时，`reverse()` 方法会在原地(*in-place*)修改序列以节省空间。为了提醒用户该操作的副作用，该操作并不会返回反转后的序列，而是返回 `None`。

```python
>>> list_=[0,1,2]
>>> id(list_)
2688950370056
>>> list_.reverse()
>>> list_
[2, 1, 0]
>>> id(list_) # 内存地址保持一致
2688950370056
```

### 3.6 s.clear()和s.copy()

在不支持切片操作的可变容器中(如  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict) 和 [`set`](https://docs.python.org/3/library/stdtypes.html#set))，也包含了 `clear()` 和 `copy()`，以保持接口的一致性。

New in version 3.3: `clear()` and `copy()` methods.

### 3.7 s *= n

*n* 是一个整数，或是一个实现了 [`__index__()`](https://docs.python.org/3/reference/datamodel.html#object.__index__) 方法的对象。如果 *n* 值为 `0` 或负整数，将清空序列。

```python
>>> list_=[0,1,2]
>>> list_ *= 0
>>> list_
[]
```

在序列 *s* 中引用的可变对象并不会产生多个新副本，仅会对可变对象的引用进行多次拷贝，效果和 `s * n` 相同。例如：

```python
list_ = [[1,2],'orca']
list_ *= 3
```

运行结果如下：

![可变序列类型](序列类型(list,tuple,range).assets/可变序列类型.png)

## 4. 列表 list

列表属于可变序列类型，在同一个列表中可以存储不同类型的元素。

### 4.1 构建列表

存在以下几种构建列表的方式：

- 使用一对方括号可构建一个空列表：`[]`
- 使用一对方括号，并在其中填充以逗号分隔的项：`[a]`, `[a, b, c]`
- 是使用列表解析(*comprehension*)：`[x for x in iterable]`
- 使用类型构造器(*constructor*)：`list()` or `list(iterable)`

🔨 *class* `list`([*iterable*])

通过构造函数创建列表对象时，新建列表对象中各个项的值和顺序均与 *iterable* 中各个项的值和顺序相同。*iterable* 可以是序列，也可是支持迭代的容器，还可以是迭代器对象。如果没有向构造函数传递实参，则会创建一个空列表。

```python
>>> list('abc')
['a', 'b', 'c']
>>> list( (1, 2, 3) )
[1, 2, 3]
>>> list()
[]
```

如果 *iterable* 本身就是一个列表，则会返回该列表的浅拷贝，类似于 `iterable[:]`：

```python
list_1 = [[1,2],'orca']
list_2 = list(list_1)
```

执行结果：

![列表_01](序列类型(list,tuple,range).assets/列表_01.png)

另外许多操作也会生成特定的列表，比如内置函数 `sorted`

### 4.2 列表解析



### 4.3 列表支持的操作

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

### 4.4 提示

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

深拷贝时，原序列中引用的可变对象都**会产生**新副本，并会在新序列中引用这些副本。若在新副本中修改可变对象，原副本中的可变对象不受影响。copy 模块中的 `deepcopy()` 属于深拷贝(**deep copy*)

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

队列可使用 [`deque`](https://docs.python.org/3/library/collections.html#collections.deque) 对象实现，该类可从两端快速添加或删除。

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



### tuple [¶](https://docs.python.org/3/library/stdtypes.html#tuples)

元组作为不可变序列不能使用 **可变序列类型的操作方法**[¶](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types) ，但可以使用 **通用序列操作** 。不能为元组中单独的项赋值，但是可以创建包含可变对象的元组。
正是因为元组的不可变性，相较于可变序列，使用元组会让代码更加安全。
另外，程序在创建小列表时(包含的项少于12个)，会浪费一些内存。因为系统会为列表稍微多分配一些内存，以优化添加新项时的操作性能。而元组是不可变的，所以它们的表示更为紧凑，不会占据额外的内存空间。

```
>>> t = 12345, 54321, 'hello!'
>>> t[0]
12345
>>> t
(12345, 54321, 'hello!')
>>> # Tuples may be nested:
... u = t, (1, 2, 3, 4, 5)
>>> u
((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))
>>> # Tuples are immutable:元组是不可变的
... t[0] = 88888
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> # but they can contain mutable objects:
... v = ([1, 2, 3], [3, 2, 1])
>>> v
([1, 2, 3], [3, 2, 1])
```

#### 序列拆封

尽管元祖表面上类似于列表，但常被用于不同的用途。
列表通常包含同构元素序列，以迭代的方式访问，更加方便。
元组通常包含异构元素序列，通过 unpacking 或索引的方法更好。
如果是 [namedtuples](https://docs.python.org/3/library/collections.html#collections.namedtuple) ，甚至可通过属性访问其中的元素。

```
In [62]: from collections import namedtuple

In [63]: Point = namedtuple('Point', ['x', 'y'])

In [64]: p = Point(11, y=22)

In [65]: p.x
Out[65]: 11

In [66]: p.y
Out[66]: 22

In [67]: p
Out[67]: Point(x=11, y=22)

In [68]: a, b = p #解包unpacking操作

In [69]: a,b
Out[69]: (11, 22)
```

注意：执行序列拆封 *sequence unpacking* 时，等号右侧可以是任何序列。
拆封时，要求左侧变量的数目和右侧序列中元素的个数相同。
多重赋值(multiple assignment) 实际上就是序列封装和拆封的应用。

```
>>> x, y, z = t

>>> list_ = [(1,2,3),(4,5,6)]
>>> for a,b,c in list_:
	print(a,b,c)

	
1 2 3
4 5 6
```

嵌套的元组也可一次性拆封

```python
>>> rgb = (1,2,3)
>>> rgb = ("red" ,"green", "blue")
>>> hexString = 0xFF
>>> rgbTuple = (rgb, hexString)
>>> ((r, g, b), hexStr) = rgbTuple
```



#### 定义空元组

`a = ()`

#### 定义单元素元组

```
In [75]: a  = (1)

In [76]: a #此时a是一个整数
Out[76]: 1

In [77]: b = (1,)#需要附加逗号

In [78]: b
Out[78]: (1,)
```

#### 包含可变对象的元组

元组虽是不可变序列，但是可以创建包含可变对象的元组。

```
>>> t = ('a', 'b', ['A', 'B'])
>>> t[2][0] = 'X'
>>> t[2][1] = 'Y'
>>> t
('a', 'b', ['X', 'Y'])

```

从表面上看，元组中的元素发生了改变。
但是变化的并非是 tuple，而是 list 中的元素。
所谓的不可变序列，是指 tuple 中每个元素的指向永远不变。
即，指向 `a ` 便不能改为 `c` ；指向 list_a ，同样也不能改为 list_b，但是 list_a 本身是可变的。所以说变化是 list 而非 tuple。

