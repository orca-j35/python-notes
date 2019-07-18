# slice

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记:『Subscriptions & Slicings.md』
>
> 如果需要生成迭代器版本的切片，则可使用 [`itertools.islice()`](https://docs.python.org/3.7/library/itertools.html#itertools.islice) 方法。

🔨 *class* slice(*stop*)

🔨 *class* slice(*start*, *stop*[, *step*])

该函数用于创建切片([*slice*](https://docs.python.org/3.7/glossary.html#term-slice))对象，切片对象表示由 `range(start, stop,step)` 指定的索引的集合。 

参数说明：

- *start* - 起点位置
- *stop* - 终点位置
- *step* - 步长

*start*, *stop*, *step* 可以是任意类型的值，其中 *start* 和 *step* 的默认值是 `None`。

```python
slice(6,b'a','b') #> slice(6, b'a', 'b')
slice(6) #> slice(None, 6, None)
```

在使用扩展索引语法时，会自动生成切片对象。例如 `a[start:stop:step] ` 将被翻译为 `a[slice(start,stop,step)]` ，并使用 `None` 填充切片中缺少的项，然后将结果传递给 `__getitem__` 方法。因此，在使用扩展索引语法时，也可直接使用切片对象。

```python
class Cls:
    def __getitem__(self,key):
        return key
# 使用扩展索引语法时，会自动生成切片对象，还会使用None填充空缺项
Cls()[0:1] #> slice(0, 1, None)

a = [1,2,3,4,5,6,7,8,9]
a[0:7:2] #> [1, 3, 5, 7]
# 与直接使用切片对象等效
a[slice(0,7,2)] #> [1, 3, 5, 7]
```

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
            # 展示如何利用切片对象完成切片操作
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

## Slice objects

> 本节涵盖了 [The standard type hierarchy](https://docs.python.org/3.7/reference/datamodel.html#types) -> Slice objects 中的内容。

切片对象用于表示 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法获得的切片，也可通过内置函数  [`slice()`](https://docs.python.org/3.7/library/functions.html#slice) 创建切片对象。

切片对象拥有三个特殊只读属性：

- `start` is the lower bound; 
- `stop` is the upper bound; 
- `step` is the step value; 

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



