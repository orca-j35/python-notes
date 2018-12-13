# Subscriptions & Slicings

GitHub@[orca-j35](https://github.com/orca-j35) /📦[python_notes](https://github.com/orca-j35/python_notes) 

## aSubscriptions

### a. 语法

> 本节涵盖了 [6.3.2. Subscriptions](https://docs.python.org/3.7/reference/expressions.html#subscriptions) 中的内容。

Subscription 用于选择序列 (string, tuple or list) 或映射 (dictionary) 中的项，其语法如下：

```
subscription ::=  primary "[" expression_list "]"
```

primary 的值必须是支持 subscription 的对象。通过实现 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法，可使用户定义的对象支持 subscription。

在内置对象中，有两类对象支持 subscription，如下：

- primary 可以是映射，此时 expression_list 的值必须是映射中的 key，subscription 将通过 key 获取映射中对应的 value。除非 expression_list 中仅有一项，否则 expression_list 将是一个元组。

  ```python
  class Cls:
      def __getitem__(self, key):
          return key
  Cls()[1] #> 1
  Cls()[1, 2, 3] #> (1, 2, 3)
  ```

- primary 可以是序列，此时 expression_list 的值必须是某个整数(索引)或切片(详见后文「Slicings」小节)。

  ```python
  class Cls:
      def __getitem__(self, key):
          return key
  Cls()[1] #> 1
  Cls()[0:1] #> slice(0, 1, None)
  ```

在 Subscription 的语法中，并未对序列的负索引给出特殊规定。所有内置序列提供的 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法均支持负索引，`__getitem__` 通过将负索引与序列长度相加来得到正索引 (例如， `x[-1]` 表示 `x` 序列中的最后一项)。正索引必须是小于序列长度的非负整数(起始值是 0)。

负索引和切片均通过 `__getitem__` 实现，如果在子类中覆写了 `__getitem__` 方法，则需要显式添加对负索引和切片的支持。

字符串的项是字符(*character*)，但在 Python 中字符并非独立的数据类型，字符就是长度为 1 的字符串。

### b. 实现

------

以下三个特殊方法用于实现 subscription：

- `__getitem__(self, key)` 用于获取对象中项
- `__setitem__(self, key)` 用于设置对象中项
- `__delitem__(self, key)` 用于删除对象中的项

支持 subscription 的对象至少需要实现 `__getitem__` 方法，例如：

- [`Sequence`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Sequence) 和 [`Mapping`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Mapping) 只需实现 `__getitem__`
- [`MutableSequence`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.MutableSequence) 和 [`MutableMapping`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.MutableMapping) 需同时实现三个方法

示例 - 为自定义类实现 subscription(基于整数索引)

```python
# 该示例没有实现负索引
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
f=Fib()
f[100] #> 573147844013817084101
```

示例 - 为自定义类实现 subscription(基于键)

```python
class Count():
    def __getitem__(self, n):
        if n is 'a':
            return 1
        else:
            return 'x'
num = Count()
num['a'] #> 1
```

## Slicings

### a. 语法

> 本节涵盖了 [6.3.3. Slicings](https://docs.python.org/3.7/reference/expressions.html#slicings) 中的内容。

Slicing 用于选择序列 (e.g., a string, tuple, list) 中的多个项，可用于赋值语句和 [`del`](https://docs.python.org/3.7/reference/simple_stmts.html#del) 语句，其语法如下：

```python
slicing      ::=  primary "[" slice_list "]"
slice_list   ::=  slice_item ("," slice_item)* [","]
slice_item   ::=  expression | proper_slice
proper_slice ::=  [lower_bound] ":" [upper_bound] [ ":" [stride] ]
lower_bound  ::=  expression
upper_bound  ::=  expression
stride       ::=  expression
```

此处的形式语法存在歧义：看起来既像 expression_list 又像 slice_list，因此任何 subscription 都可解释为 slicing。为了消除歧义，并且不使语法变得更加复杂。因此，在遇到上述形式语法时，将其解释为 subscription 的优先级高于 slicing (slice_list 包含不恰当切片的情况)

slicing 的语义是，使用通过 slice_list 创建的 key 来对 primary 进行索引 (使用与标准 subscription 相同的 [`__getitem__(self,key)`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法)，具体如下：

- 如果 slice_list 中包含至少一个逗号，key 将是一个包含 slice 对象的元组 (Python 会自动将 proper_slice 转换为 slice 对象)：

  ```python
  class Cls:
      def __getitem__(self,key):
          return key
  Cls()[0,0:1,:,0]
  #> (0, slice(0, 1, None), slice(None, None, None), 0)
  # 0:1会被自动转换为slice对象
  ```

- 否则，key 是一个独立的 slice 对象 (Python 会自动将 proper_slice 转换为 slice 对象)：

  ```python
  class Cls:
      def __getitem__(self,key):
          return key
  Cls()[0:1] #> slice(0, 1, None)
  # 0:1会被自动转换为slice对象
  ```

slice 对象拥的三个属性 ( `start`、`stop` 和 `step` )，分别对应 proper_slice 中的三个值 (lower_bound、upper_bound 和 stride)。lower_bound、upper_bound 和 stride 可以是任意类型的值，并使用 `None` 填充 proper_slice 空缺的值。

```python
class Cls:
    def __getitem__(self,key):
        return key
Cls()[0,b'orca':'_':[1,]]
#> (0, slice(b'orca', '_', [1]))
```

关 slice 对象的细节，详见后文「Slice objects」小节，或阅读 [The standard type hierarchy](https://docs.python.org/3.7/reference/datamodel.html#types) 。

### b. 实现

只能通过以下三个特殊方法来实现 Slicing：

- `__getitem__(self, key)` 用于获取对象中项
- `__setitem__(self, key)` 用于设置对象中项
- `__delitem__(self, key)` 用于删除对象中的项

可以看到，Slicing 和 subscription 使用了相同的特殊方法。

在切片时，例如 `a[1:2] = b` 将被翻译为 `a[slice(1, 2, None)] = b` ，并使用 `None` 填充切片中缺少的项。在切片时，还可直接使用 slice 对象 (例如 `a[slice(5)]`)。

示例 - 为自定义类实现 subscription 和 slicing：

```python
# 该示例没有实现负索引，也没有对切片的step进行处理
class Fib(object):
    def __getitem__(self, n):
        # 需要手动判断实参类型，从而区分subscription和slicing
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start # 获取切片的下界
            stop = n.stop # 获取切片的上界
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
Fib()[:5] #> [1, 1, 2, 3, 5]
# 可直接使用 slice 对象
Fib()[slice(10)] #> [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

### c. Slice objects

> 本节涵盖了 [The standard type hierarchy](https://docs.python.org/3.7/reference/datamodel.html#types) -> Slice objects 中的内容。

切片对象用于表示 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法获得的切片，也可通过内置函数  [`slice()`](https://docs.python.org/3.7/library/functions.html#slice) 创建切片对象。

切片对象拥有三个特殊只读属性：

- `start` is the lower bound; 
- `stop` is the upper bound; 
- `step`is the step value; 

以上三个属性可以是任意类型的值，并且没有其他功能，但是 Numerical Python 和其它第三方扩展会使用这三个属性。如果在创建切片对象时，省略了上述某个属性，则会将其设置为 `None`。

```python
class Cls:
    def __getitem__(self,key):
        return key
Cls()[0,b'orca':'_']
#> (0, slice(b'orca', '_', None))
```

在使用扩展索引语法时，会自动生成切片对象。例如 `a[start:stop:step] ` 将被翻译为 `a[slice(start,stop,step)]` ，并使用 `None` 填充切片中缺少的项。在使用扩展索引语法时，也可直接使用切片对象。

```python
class Cls:
    def __getitem__(self,key):
        return key
# 使用扩展索引语法时，会自动生成切片对象，还会使用None填充空缺项
Cls()[0:1] #> slice(0, 1, None)

a = [1,2,3,4,5,6,7,8,9]
a[0:7:2] #> [1, 3, 5, 7]
# 直接使用切片对象
a[slice(0,7,2)] #> [1, 3, 5, 7]
```

切片对象支持一种方法：

- slice.indices(*self*, *length*)

  This method takes a single integer argument *length* and computes information about the slice that the slice object would describe if applied to a sequence of *length* items. It returns a tuple of three integers; respectively these are the *start* and *stop* indices and the *step* or stride length of the slice. Missing or out-of-bounds indices are handled in a manner consistent with regular slices.

  ```python
  # S.indices(len) -> (start, stop, stride)
  # 该方法用于计算，将长度为length的序列按照slice对象执行切片时，
  # 子序列在原序列中的(start, stop, step)
  slice(3).indices(4) #> (0, 3, 1)
  slice(3).indices(2) #> (0, 2, 1)
  ```

因为 `slice.__hash__` 等于 `None`，所以当试图获取 slice 类的实例的哈希值时会抛出异常。

## 相关特殊方法

### \_\_getitem\_\_

> 本节涵盖了 [object.\_\_getitem\_\_(self, key)](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 中的内容。
> 相关笔记: 『3.3. Special method names.md』

🔨 object.`__getitem__`(*self*, *key*)

该方法用于实现对 `self[key]` 进行求值，可用于序列和映射：

- 对于序列类型，*key* 可以是整数或切片(*slice*)对象。如果希望自定义类模仿序列类型，那么 `__getitem__()` 方法需要对负索引进行解释。
  如果 *key* 并非合适的类型，则可能会抛出 [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError)；如果索引值超过了可索引的范围(需要考虑负索引的范围)，则应抛出 [`IndexError`](https://docs.python.org/3.7/library/exceptions.html#IndexError)。
- 对于映射类型，如果容器中不包含 *key*，则应抛出 [`KeyError`](https://docs.python.org/3.7/library/exceptions.html#KeyError)。

注意：[`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环会期望在进行非法索引时抛出 [`IndexError`](https://docs.python.org/3.7/library/exceptions.html#IndexError)，从而能够正确检测序列的结尾。

### \_\_setitem\_\_

> 本节涵盖了 [object.\_\_setitem\_\_(*self*, *key*, *value*)](https://docs.python.org/3.7/reference/datamodel.html#object.__setitem__) 中的内容。
> 相关笔记: 『3.3. Special method names.md』

🔨 object.`__setitem__`(*self*, *key*, *value*)

该方法用于实现对 `self[key]` 进行赋值，可参考 `__getitem__` 的用法。

对于映射类型，可通过 `__setitem__` 对现有的 *key* 重新赋值，或添加新的 *key-value*  对。

对于序列类型，可通过 `__setitem__` 对索引 *key* 重新赋值。

对于错误的 *key* 值应抛出与 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 相同的异常。

### \_\_delitem\_\_

> 本节涵盖了 [object.\_\_delitem\_\_(*self*, *key*)](https://docs.python.org/3.7/reference/datamodel.html#object.__delitem__) 中的内容。
> 相关笔记: 『3.3. Special method names.md』

🔨 object.`__delitem__`(*self*, *key*)

该方法用于实现删除 `self[key]`，可参考 `__getitem__` 的用法。

对于映射类型，可通过 `__delitem__` 删除 *key*。

对于序列类型，可通过 `__delitem__` 删除索引 *key* 处的元素。

对于错误的 *key* 值应抛出与 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 相同的异常。

### \_\_missing\_\_

> 本节涵盖了 [object.\_\_missing\_\_(*self*, *key*)](https://docs.python.org/3.7/reference/datamodel.html#object.__missing__) 中的内容。
> 相关笔记: 『3.3. Special method names.md』

对于 dict 的子类，当 *key* 不是字典中键时，便会通过 [`dict`](https://docs.python.org/3.7/library/stdtypes.html#dict).[`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 调用 `__missing__` 方法。

```python
class SubDict(dict):
    def __missing__(self, key):
        return 'orca_j35'

x = SubDict()
x['2'] #> 'orca_j35'
```

