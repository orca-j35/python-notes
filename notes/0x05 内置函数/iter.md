# iter

iter(*object*[, *sentinel*])

该函数会返回一个 [iterator](https://docs.python.org/3.7/glossary.html#term-iterator) 对象，但 *object* 会因为 *sentinel* 的传入与否，而获得截然不同的解释。

## iter(object)

🔨iter(*object*) -> iterator

在没有传入 *sentinel*  的情况下，*object* 必须是一个支持迭代协议( [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 方法)的集合(collection)对象；或者是一个支持序列协议的对象 (the [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) method with integer arguments starting at `0`)。如果这两种协议同时存在，会优先使用迭代协议( `__iter__` )。如果这两种协议均不被 object 支持，`iter()` 便会抛出 [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError)。

Tips：这里提到的集合对象只是一种抽象概念，并非特指 [Collection](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Collection) 类型，仅实现 [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 方法即可支持 `iter` 函数；同样的，仅实现 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法也能支持 `iter` 函数。

```python
class ObjcIter:
    def __iter__(self):
        cont = 0
        while cont < 3:
            cont += 1
            yield cont


a_iter1 = iter(ObjcIter())
print(list(a_iter1))
# Out: [1, 2, 3]


class ObjcGetitem:
    def __getitem__(self, item):
        cont = 0

        while cont <= item:
            cont += 1
            if cont >= 5:
                raise StopIteration()
        return cont


a_iter2 = iter(ObjcGetitem())
print(list(a_iter2))
# Out: [1, 2, 3, 4]
```

列表、元组、字典等都可直接用作 `iter` 的参数：

```python
>>> i = iter([1, 2, 3])
>>> i.next()
1
>>> i.next()
2
>>> i.next()
3
>>> i.next()
Traceback (most recent call last):
  File "<interactive input>", line 1, in <module>
StopIteration
```

注意：将某个迭代器对象传递给 [`iter()`](https://docs.python.org/3.7/library/functions.html#iter) 后，只会返回指向该迭代器的引用，并不会创建具备新id的迭代器对象。

```python
>>> aa = [1,2,3,]
>>> bb = iter(aa)
>>> bb
<list_iterator object at 0x000001B393436E48>
>>> cc = iter(bb)
>>> cc # bb和cc引用同一个对象
<list_iterator object at 0x000001B393436E48>
```

## iter(object, sentinel)

🔨iter(*object*, *sentinel*) -> iterator

如果传入了第二参数 *sentinel*，此时 *object* 必须是一个可调用(callable)对象。对于在这种情况下创建的迭代器，每当调用其 [`__next__()`](https://docs.python.org/3.7/library/stdtypes.html#iterator.__next__) 方法时，便会以无参数形式调用 *object*。如果 *object* 的返回值等于 *sentinel*，便会抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration) ；如果返回值不等于 *sentinel*，则直接返回该值。比如下面这个示例：

```python
class AutoIncrement(object):
    """每次调用该类的实例，计数器便会自动加1"""

    def __init__(self):
        self._count = 0

    def __call__(self):
        self._count += 1
        return self._count


a_iter = AutoIncrement()
for i in iter(a_iter, 3):
    # 当a_iter()返回5时，便会抛出StopIteration
    # 停止迭代
    print(i, end=',')
# Out: 1,2,
```

也可直接使用函数对象，例如：

```python
_count = 0


def func():
    global _count
    _count += 1
    return _count


for i in iter(func, 3):
    print(i, end=",")
# Out: 1,2,
```

[`iter()`](https://docs.python.org/3.7/library/functions.html#iter) 带第二参数的一个使用场景是：可以一次性读取文件中的多个行，并在某个特定行停止读取。下面这个示例会持续读取一个文件，直到 [`readline()`](https://docs.python.org/3.7/library/io.html#io.TextIOBase.readline) 方法返回空字符串为止。

```python
with open('mydata.txt') as fp:
    for line in iter(fp.readline, ''):
        process_line(line)
```

[参考 Iterator Types 可了解更多有关迭代器的信息。](https://docs.python.org/3.7/library/stdtypes.html#typeiter)