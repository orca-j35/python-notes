# 集合类型(set, frozenset)

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库。
>
> 本笔记涵盖了 [Set Types — set, frozenset](https://docs.python.org/3.7/library/stdtypes.html#set-types-set-frozenset)，并进行了扩展。

集合(*set*)对象是由不同的可哈希([*hashable*](https://docs.python.org/3.7/glossary.html#term-hashable))对象组成的无序集合。set 对象常用于成员测试；从序列中删除重复项；进行数学运算，如交集(*intersection*), 并集(*union*), 差集(*difference*), 对称差集(*symmetric* difference)。如果想要了解其它容器类型，可以参考内置类型 ([list](https://docs.python.org/3.7/library/stdtypes.html#list)、[set](https://docs.python.org/3.7/library/stdtypes.html#set)、[tuple](https://docs.python.org/3.7/library/stdtypes.html#tuple)) 以及 [collections](https://docs.python.org/3.7/library/collections.html#module-collections) 模块。

关于可哈希([*hashable*](https://docs.python.org/3.7/glossary.html#term-hashable))对象，详见笔记「映射类型(dict).md」-> 1. hashable

与其它集合(*collection*)一样，set 同样支持 `x in set`、`len(set)` 和 `for x in set` (还可参考 [collections.abc.Set](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Set))。set 作为无需集合，不会记录元素的位置或插入顺序。因此，set 不支持索引、切片或其它类序列(*sequence*-*like*)行为。

目前有两种内置 set 类型：[set](https://docs.python.org/3.7/library/stdtypes.html#set) 和 [frozenset](https://docs.python.org/3.7/library/stdtypes.html#frozenset) 。set 类型是可变类型——可使用 `add()` 和 `remove()` 等方法来更改其内容。由于 set 是可变类型，因此 set 对象没有哈希值，且不能用作字典的键，也不能用作其它 set 对象的元素。frozenset 类型是不可变类型，并且可哈希——frozenset 对象在创建后不能被改变；因此 frozenset 对象可用作字典的键值或是其它 set 对象的元素。

## 1. 构建集合

可通过以下几种方式来构建集合(set, frozenset)：

- 使用一对花括号，并在其中填充以逗号分割的项 - 可构建非空 set，但不能构建 frozenset，例如 `{'jack', 'sjoerd'}` , `{*[1,2,3]}`

- 使用集合解析(*comprehension*) - 可构建非空 set，但不能构建 frozenset，例如

  ```python
  {x for x in 'abracadabra' if x not in 'abc'}
  #> {'d', 'r'}
  ```

- 使用类型构造器(*constructor*) - 可构建 set 或 frozenset，例如 `set()` , `set(iterable)` ,  `frozenset()` , `frozenset(iterable)`

集合中的元素必须是可哈希([*hashable*](https://docs.python.org/3.7/glossary.html#term-hashable))对象，如果想构建一个内含集合(*set*)对象的 set，内层的集合必须是 frozenset 对象。

```python
{1,2,frozenset((3,4))} #> {1, 2, frozenset({3, 4})}
```

注意：`{}` 将构造一个空字典，并不会构建空集合。

### a. 构造器

🔨 *class* set([*iterable*])

🔨 *class* frozenset([*iterable*])

构造器 `set()` 和 `frozenset()` 拥有相同的工作方式，可分为以下两种情况：

- 如果未指定 *iterable*，将构建一个空 set (或 frozenset)对象：

  ```python
  set(),frozenset()
  #> (set(), frozenset())
  ```

- 如果给定了 *iterable* 参数，则会用 *iterable* 中的元素构建一个 set (或 frozenset)对象。*iterable* 中的元素必须都是可哈希对象，`set()` (或 `frozenset()`) 会自动剔除 *iterable* 中的重复项。

  ```python
  set([1,2,2,3]) #> {1, 2, 3}
  set('abracadabra') #> {'a', 'b', 'c', 'd', 'r'}
  frozenset([1,2,2,3]) #> frozenset({1, 2, 3})
  ```

## 2. 支持的操作

### a. for set & frozenset 

set 和 frozenset 实例支持以下操作：

- `len(s)` - 返回集合 *s* 中元素的个数，也称集合 *s* 的势(*cardinality*)

- `x in s` - Test *x* for membership in *s*. 

  *x* 可以是 set 对象，为了支持搜索与之等效的 frozenset 对象，将通过 *x* 创建一个临时的 frozenset 对象。

- `x not in s` - Test *x* for non-membership in *s*.

- `isdisjoint`(*other*) - 如果集合与 *other* 互斥(*disjoint*)，即集合与 *other* 的交集(intersection)为空，则返回 `True` 

  ```python
  a = {1,2,3}
  assert a.isdisjoint([4,5,6]) is True
  assert a.isdisjoint({4,5}) is True
  ```

- `issubset`(*other*) 或 `set <= other` - 测试集合是否是 *other* 的子集。

  Test whether every element in the set is in *other*.

- `set < other` - 测试集合是否是 *other* 的真子集。

  Test whether the set is a proper subset of *other*, that is, `set <= other and set !=other`.

- `issuperset`(*other*) 或 `set >= other` - 测试 *other* 是否是集合的子集。

  Test whether every element in *other* is in the set.

- `set > other`  - 测试 *other* 是否是集合的真子集。

  Test whether the set is a proper superset of *other*, that is, `set >= other and set !=other`.

- `union`(**others*) 或 `set | other | ...` - 并集

  Return a new set with elements from the set and all others.

- `intersection`(**others*) 或 `set & other & ...` - 交集

  Return a new set with elements common to the set and all others.

- `difference`(**others*) 或 `set - other - ...` - 差集

  Return a new set with elements in the set that are not in the others.

- `symmetric_difference`(*other*) 或 `set ^ other` - 对称差集

  Return a new set with elements in either the set or *other* but not both.

- `copy`()

  Return a new set with a shallow copy of *s*.

任何可迭代对象均可用作以下方法的参数，但这些方法对应的运算符版本只能使用集合作为操作数：

- `union()`, `intersection()`, `difference()`, `symmetric_difference()`
- `issubset()`, `issuperset()` 

使用以上方法可以避免像 `set('abc') & 'cbs'` 这样的错误，并且 `set('abc').intersection('cbs')` 也更加易读。

set 和 frozenset 均支持集合间的比较操作：当且仅当两个集合相互包含对方的每个元素(即两个集合互为子集)时，才认为两个集合相等。当且仅当 A 集合是 B 集合的真子集(即 A 是 B 的子集，但 A 不等于 B)时，才认为集合 A 小于集合 B。当且仅当 A 集合是 B 集合的真超集(即 A 是 B 的超集，但 A 不等于 B)时，才认为集合 A 大于集合 B。

set 实例和 frozenset 实例间的比较操作是基于内部成员进行的，例如：

```python
set('abc') == frozenset('abc') #> True
set('abc') in set([frozenset('abc')]) #> Ture
```

子集(*subset*)和相等比较不能被推广到全(*total*)排序函数。例如，任何两个非空且无交集的集合被认为互不相等，并且均不是对方的子集，因此以下表达式均为假：

```python
# a,b是互斥且无交集的集合，以下表达式均为假
a < b
a == b
a > b
```

由于集合仅定义了部分(*partial*)排序关系(子集关系)，所以在集合列表中并没有定义 [`list.sort()`](https://docs.python.org/3.7/library/stdtypes.html#list.sort) 方法的输出：

```python
sets = [{3,4},{1,2},{4,5}]
sets.sort() # 不会改变集合间的序列顺序
sets #> [{3, 4}, {1, 2}, {4, 5}]
```

若在二元集合操作中混用 set 和 frozenset 对象，则返回值是第一个操作数的类型。例如， `frozenset('ab') | set('bc')` 的返回值是 frozenset 对象。

### a. for set

以下操作仅适用于 set 对象(可变)，不能用于 frozenset 对象(不可变)：

- `update`(**others*) 或 `set |= other | ...` 

  Update the set, adding elements from all others.

- `intersection_update`(**others*) 或 `set &= other & ...`

  Update the set, keeping only elements found in it and all others.

- `difference_update`(**others*) 或 `set -= other | ...`

  Update the set, removing elements found in others.

- `symmetric_difference_update`(*other*) 或 `set ^= other`

  Update the set, keeping only elements found in either set, but not in both.

- `add`(*elem*)

  Add element *elem* to the set.

- `remove`(*elem*)

  Remove element *elem* from the set. Raises [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) if *elem* is not contained in the set.

- `discard`(*elem*)

  Remove element *elem* from the set if it is present.

- `pop`()

  Remove and return an arbitrary element from the set. Raises [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError) if the set is empty.

- `clear`()

  Remove all elements from the set.

任何可迭代对象均可用作以下方法的参数，但这些方法对应的运算符版本只能使用集合作为操作数：`update()`, `intersection_update()`, `difference_update()`, `symmetric_difference_update()`。

可将 set 对象用作 [`__contains__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__contains__), [`remove()`](https://docs.python.org/3.7/library/stdtypes.html#frozenset.remove) 或 [`discard()`](https://docs.python.org/3.7/library/stdtypes.html#frozenset.discard) 的 *elem* 参数。为了支持搜索与之等效的 frozenset 对象，将通过 *elem* 创建一个临时的 frozenset 对象。

















