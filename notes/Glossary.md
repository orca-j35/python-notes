# Glossary

[TOC]

## D

### decorator

装饰器

A function returning another function, usually applied as a function transformation using the `@wrapper` syntax. Common examples for decorators are [`classmethod()`](https://docs.python.org/3.7/library/functions.html#classmethod) and [`staticmethod()`](https://docs.python.org/3.7/library/functions.html#staticmethod).

The decorator syntax is merely syntactic sugar, the following two function definitions are semantically equivalent:

```
def f(...):
    ...
f = staticmethod(f)

@staticmethod
def f(...):
    ...
```

The same concept exists for classes, but is less commonly used there. See the documentation for [function definitions](https://docs.python.org/3.7/reference/compound_stmts.html#function) and [class definitions](https://docs.python.org/3.7/reference/compound_stmts.html#class) for more about decorators.

## G

### generator 

生成器

生成器是一个函数，它会返回一个 [generator iterator](https://docs.python.org/3.7/glossary.html#term-generator-iterator)。生成器与普通函数的区别在于它包含 [`yield`](https://docs.python.org/3.7/reference/simple_stmts.html#yield) 表达式。该表达式会生成一系列可用于 for 循环的值，另外这些值也可通过 [`next()`](https://docs.python.org/3.7/library/functions.html#next) 函数逐一检索。

生成器通常指代生成器函数，但是在一些情况下也用于指代  generator iterator 。如果预期含义并不明确，则建议使用完整术语来避免混淆。

### generator iterator 

通过生成器(generator)函数创建的对象。

 [`yield`](https://docs.python.org/3.7/reference/simple_stmts.html#yield) 用于暂停 generator iterator 的执行，并会记住当前位置的执行状态(包括局部变量和待处理的 try 语句)。当 generator iterator 恢复执行时，便会从之前中断的位置开始执行(普通函数每次调用时，都会从头开始重新执行)

generator iterator 调用的 `__iter__` 方法会返回 generator iterator 自身；对 generator iterator 调用内置函数 `iter()` 同样会返回 generator iterator 自身。并且对同一个 generator iterator 依次执行这两种方法，均返回带有同一 id 的对象。

```python
class Generator:
    def __iter__(self):#生成器
        cont = 0
        while cont < 3:
            cont += 1
            yield


a_generator = Generator()

# 通过同一个generator可创建不同的generator iterator。
# 例如g_iter1和g_iter2是两个具备不同标识符id的generator iterator
g_iter1 = iter(a_generator)
g_iter2 = a_generator.__iter__()
print("{0}的id是:{1}, 类型是:{2}".format("g_iter1", id(g_iter1), type(g_iter1)))
print("{0}的id是:{1}, 类型是:{2}".format("g_iter2", id(g_iter2), type(g_iter2)))

# 对同一个generator iterator依次执行这两种方法，均返回带有同一id的对象
print(id(g_iter1.__iter__()))
print(id(iter(g_iter1)))
```

输出

```
g_iter1的id是:2742184172272, 类型是:<class 'generator'>
g_iter2的id是:2742184172624, 类型是:<class 'generator'>
2742184172272
2742184172272
```



### generator expression

生成器表达式

该表达式会返回一个迭代器。该表达式与常规表达式一样，会使用 [`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环来定义一个循环变量 i 及其范围，同样可使用 `if` 表达式。该组合表达式可为封闭(enclosing)函数生成值：

```python
sum(i*i for i in range(10))  # sum of squares 0, 1, 4, ... 81; result 285
```

## I

### iterable

可迭代对象能够逐一返回其中的每个成员。所有的序列(sequence)类型都属于 iterable (如 [`list`](https://docs.python.org/3.7/library/stdtypes.html#list) | [`str`](https://docs.python.org/3.7/library/stdtypes.html#str) | [`tuple`](https://docs.python.org/3.7/library/stdtypes.html#tuple) )；一些非序列类型也属于 iterable (如 [`dict`](https://docs.python.org/3.7/library/stdtypes.html#dict) | [file objects](https://docs.python.org/3.7/glossary.html#term-file-object) | 任何定义了 [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 或 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 的类对象)。[`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 实现 [Sequence](https://docs.python.org/3.7/glossary.html#term-sequence) 语义。

Iterables 可用于 [`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环，以及任何需要顺序对象的地方 ([`zip()`](https://docs.python.org/3.7/library/functions.html#zip), [`map()`](https://docs.python.org/3.7/library/functions.html#map) 等)。内置函数 [`iter()`](https://docs.python.org/3.7/library/functions.html#iter) 接受一个 iterable 对象作为参数时，将返回该对象的迭代器。该迭代器适用于一次性传递传递一组值。在使用 iterable 时，通常不需要调用[`iter()`](https://docs.python.org/3.7/library/functions.html#iter) 或自己处理迭代器对象。`for` 语句会为我们自动完成如下操作：创建一个临时的无名变量，以便在循环期间保存保存迭代器。另请参见  [iterator](https://docs.python.org/3.7/glossary.html#term-iterator), [sequence](https://docs.python.org/3.7/glossary.html#term-sequence) 和 [generator](https://docs.python.org/3.7/glossary.html#term-generator)。

### iterator

迭代器是表示数据流的对象。重复调用迭代器的 [`__next__()`](https://docs.python.org/3.7/library/stdtypes.html#iterator.__next__) 方法(或通过内置函数[`next()`](https://docs.python.org/3.7/library/functions.html#next) 重复调用迭代器)，将返回流中连续的项。当没有再无数据可供使用时，便会抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration) 异常，这时表明该迭代器对象已经耗尽，若此后仍试图调用该迭代器的 `__next__()` 方法，将会再次抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration) 异常。迭代器需要一个 [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 方法来返回迭代器对象自身，因此每个迭代器也都属于 iterable；并且在其它接受 iterable 的地方，也多半可以接受迭代器。

不同的 iterable 对象在迭代过程中，也会有所区别。比如，对容器对象(如 [`list`](https://docs.python.org/3.7/library/stdtypes.html#list))而言，每次将其传递给 [`iter()`](https://docs.python.org/3.7/library/functions.html#iter) ，或用于 `for` 循环时，都将产生一个全新的迭代器。如果尝试将某个迭代器反复传递给 [`iter()`](https://docs.python.org/3.7/library/functions.html#iter) ，也只会返回指向该迭代器的引用；如果尝试将某个迭代器对象反复用于 `for` 循环，在第一次 `for` 循环时便会耗尽该迭代器，之后只会反复使用这个已被耗尽的迭代器，看起来就像是在使用一个空容器。

```python
>>> aa = [1,2,3,]
>>> bb = iter(aa)
>>> bb
<list_iterator object at 0x000001B393436E48>
>>> cc = iter(bb)
>>> cc
<list_iterator object at 0x000001B393436E48>
# 可以看到bb和cc引用了相同的对象
>>> for i in bb:
	print(i)

	
1
2
3
>>> for i in cc:
	print(i)

	
```

更多信息可以参考 [Iterator Types](https://docs.python.org/3.7/library/stdtypes.html#typeiter).

## Q

### sequence

序列是一个 [iterable](https://docs.python.org/3.7/glossary.html#term-iterable) 对象。通过定义 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 方法，使得序列能够通过整数索引来高效的访问其中的元素。通过定义 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 方法，以便查看序列的长度。如 [`list`](https://docs.python.org/3.7/library/stdtypes.html#list) | [`str`](https://docs.python.org/3.7/library/stdtypes.html#str)| [`tuple`](https://docs.python.org/3.7/library/stdtypes.html#tuple)|  [`bytes`](https://docs.python.org/3.7/library/stdtypes.html#bytes) 都属于内置序列类型。注意，[`dict`](https://docs.python.org/3.7/library/stdtypes.html#dict) 同样支持  [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 和 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__)，但是考虑到 `dict` 是映射而非序列，因此将 [不可变](https://docs.python.org/3.7/glossary.html#term-immutable)的 key 作为查找对象，而没有使用整数。

在 [`collections.abc.Sequence`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Sequence) 抽象基类中定义了更为丰富的接口，不仅包含了[`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 和 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) ，还添加了 `count()`, `index()`, [`__contains__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__contains__) 和 [`__reversed__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__reversed__)。 Types that implement this expanded interface can be registered explicitly using `register()`。

