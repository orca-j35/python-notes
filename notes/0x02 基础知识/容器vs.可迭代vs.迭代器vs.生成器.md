# 容器vs.可迭代vs.迭代器vs.生成器

[TOC]

## 1. 容器

container

在某些对象中会包含对其它对象的引用，这样的对象被称作**容器**(*containers*)。我们可以把容器视作用于组织各种元素的数据结构。

下面是一些常见的容器对象：

- list, deque, …
- set, frozensets, …
- dict, defaultdict, OrderedDict, Counter, …
- tuple, namedtuple, …
- str

另外，容器是存储在内存中的数据结构，并且通常会将全部的值都保存在内存中(也有一些特例，并不是所有的元素都放在内存，比如迭代器和生成器对象)。

在大多数情况下，当谈到某个容器的值时，我们谈论的仅是值，而不是所包含的对象的 ID(identities)；但是，在讨论容器的可变性时，则是在谈论容器中直接包含的对象的 ID。因此，如果不可变容器(比如，元组)中包含了对可变对象的引用，那么当被引用的可变对象发生改变时，相应的容器值也将发生改变。[^1]

从技术角度来讲：参考 [`collections.abc`](https://docs.python.org/3.7/library/collections.abc.html#module-collections.abc) 中抽象基类的定义，可见容器是实现了 `__contains__` 方法的对象[^2]。容器一定支持成员测试，但支持成员测试的不一定是容器——实现了 `__iter__` 或 `__getitem__` 的对象也支持成员测试。

```python
import collections.abc as abc


class Fib(object):
    def __reset(self):
        self.a = 0
        self.b = 1

    def __init__(self):
        self.__reset()

    def __contains__(self, item):
        print("调用 __contains__")
        self.__reset()
        while True:
            self.a, self.b = self.b, self.a + self.b
            if item == self.a:
                return True
            elif item < self.a:
                return False


a_fib = Fib()
assert isinstance(a_fib, abc.Container)
```

注意：尽管绝大多数容器都提供了某种方式来获取其中包含的每一个元素，但这并不是容器本身提供的能力，而是 iterable 赋予了容器这种能力。容器并不一定都是 iterable，比如：[Bloom filter](https://zh.wikipedia.org/wiki/%E5%B8%83%E9%9A%86%E8%BF%87%E6%BB%A4%E5%99%A8) ，虽然 Bloom filter 可以检测某个元素是否存在于容器中，但是并不能从容器中获取其中的每一个值，因为 Bloom filter 并没有把元素存储在容器中，而是通过一个散列函数映射成一个值保存在数组中。

综上可见，当我在讨论容器时，可能存在两种含义：

- 第一种是特指实现了 `__contains__` 方法的对象，**本节后续部分会将此类对象称作 ContainerObjc。**
- 另一种是将容器视作用于组织各种元素的数据结构，这是一种更加抽象的概念，泛指存放数据的容器，并不特指实现了 `__contains__` 方法的对象。文档中大多数时候会采用这种概念，因此在阅读文档时需要注意区分。

## 2. 可迭代对象

iterable

容器和 iterable 间没有必然的关联性。对象可以是非 iterable 的容器，也可以是非容器的 iterable (如，文件对象和套接字对象)。另外，容器通常是有限的，而 iterable 可以表示一个无限的数据源。

iterable 在官方文档的语境中存在如下两种含义：

- 第一种是特指实现了 `__iter__ ` 方法的对象[^2]，**本节后续部分会将此类对象称作 IterableObjc。**

  Tips：[`Iterator`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Iterator) 和 [`Generator`](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Generator) 均属于 IterableObjc。

  ```python
  from collections import abc
  
  
  class IterableObjc:
      def __iter__(self):
          cont = 0
          while cont < 3:
              cont += 1
              yield cont
  
  
  a_iterable = IterableObjc()
  assert isinstance(a_iterable, abc.Iterable)  # 无异常
  ```

- 第二种将 iterable 视作一种抽象概念。只要内置函数 `iter()` [^5]可接受的对象，均被视作 iterable (这里特指 `iter()` 的单参数形式，不含第二参数)。因此，只要定义了 [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 或 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 中的任意一个，便可被认定为 iterable。但是，只定义了 [`__getitem__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__getitem__) 的对象，并不是 IterableObjc。可见，第二种含义所含对象的范围大于第一种含义，可认为 IterableObjc 是 iterable 的子集。如果同时定义了 `__iter__` 和 `__getitem__`，内置函数会优先使用 `__iter__`。

  **本节后续部分提及的 iterable 均采用第二种含义。**

  ```python
  class GetitemObjc:
      def __getitem__(self, item):
          cont = 0
          while cont <= item:
              cont += 1
              if cont >= 5:
                  raise StopIteration()
          return cont
  
  
  a_getitem = GetitemObjc()
  assert isinstance(a_getitem, abc.Iterable)  # 异常
  ```

### 2.1 iterable 与 for 循环

**迭代**(Iteration)是指通过 `for` 循环遍历 iterable 对象的过程。将 iterable 用于 [`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环时，我们不需要自己调用[`iter()`](https://docs.python.org/3.7/library/functions.html#iter) ，也不需要自己处理迭代器对象。`for` 语句会在循环期间，自动创建一个用于保存迭代器的临时无名变量。通过反汇编(disassemble)，可以让我们更加直观的了解 `for` 循环的执行过程，代码如下：

```python
dis.dis("for _ in iterable: pass")
```

输出：

```
1           0 SETUP_LOOP              12 (to 14)
              2 LOAD_NAME                0 (iterable)
              4 GET_ITER
        >>    6 FOR_ITER                 4 (to 12)
              8 STORE_NAME               1 (_)
             10 JUMP_ABSOLUTE            6
        >>   12 POP_BLOCK
        >>   14 LOAD_CONST               0 (None)
             16 RETURN_VALUE
```

通过观察输出，可见解释器会显式调用 `GET_ITER`，这相当于调用了 `iter(iterable) ` 。也就是说`for` 语句会自动调用 `iter(iterable)`，从而将 `iterable` 对象转换为一个迭代器[^6]。以便能够通过 `FOR_ITER` 指令 (相当于 `next()` 方法) 获取下一个元素。注意：无法直接从字节码指令中观察到全部过程，因为解释器对此进行了优化。可做如下理解：

```python
for x in [1, 2, 3, 4, 5]:
    pass
# 该for语句，与以下内容等价

# 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
# 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break
```

Tips:`for i in ...` 语句中创建的变量 `i` 会被储存到当前作用域的符号表中，该变量在循环完成后依然存在。因此，该变量会覆盖当前作用域中的同名变量。

```python
for i in range(3):
    print(i)
print(i)
```

### 2.2 iterable 与内置函数

iterable 还可用于任何需要顺序对象的地方，比如内置函数：

- `any(iterable)`
- `class list([iterable])`
- `map(function, iterable, ...)`
- ....

对内置函数来说，其 iterable 参数仍采用第二种含义，绝非严格意义上的 `IterableObjc`。

比如文档中对内置函数 `any(iterable)` 的解释如下：

> 如果可迭代(iterable)对象中某个元素的布尔值为 `True`，则返回 `True` 。如果可迭代对象为空，则返回 `False` 。相当于如下代码：
>
> ```python
> def any(iterable):
>     for element in iterable:
>         if element:
>             return True
>     return False
> ```

由此可以推测，如果内置函数带有 iterable 参数，则会先将 iterable 转换为迭代器，然后再进行处理。在内置函数内部可以通过 `for` 循环间接转换，也可直接使用 `iter()` 进行转换(注意，内置函数是 C 实现，这里段文字仅是为了给出一种思路)

### 2.3 IterableObjc 与 \_\_iter\_\_ 

首先明确两个概念：

- IterableObjc ：所有实现了 `__iter__` 的对象均可称作 IterableObjc。
- 迭代器：同时实现了 `__iter__` 和 `__next__` 的对象，迭代器也属于 IterableObjc。

从本质上来说， `__iter__` 方法就是为了返回迭代器而存在的，当需要容器提供迭代器时，便会调用此方法。但由于 IterableObjc 本身也可能是迭代器，所以便产生了以下两种情形：

```python
# 第一种情况：IterableObjc本身不是迭代器
class IterableObjc:
    """
    在这种情况下，每次调用__iter__方法时，
    都会返回一个具备新id的迭代器对象，不会返回实例本身。
    """
    def __iter__(self):
        """调用该生成器函数，便会返回一个迭代器"""
        cont = 0
        while cont < 3:
            cont += 1
            yield cont
            
# 第二种情况：IterableObjc本身就是迭代器
class IteratorObjc:
    """
    在这种情况下，每次调用__iter__方法时，
    会返回实例对象自身，不会创建具备新id的迭代器对象。
    """
    def __iter__(self):
        self._count = 0
        # 调用时返回实例自身
        return self

    def __next__(self):
        while self._count < 3:
            self._count += 1
            return self._count
```

## 3. 迭代器

iterator

迭代器是表示数据流的对象，属于惰性计算序列，只有在调用 `next()` 函数时，才会计算并返回下一个数据。

迭代器对象自身需要支持以下两个方法，这两个共同构成了迭代器协议：[^7]

- `iterator.__iter__()`

  返回迭代器对象本身。由于实现了 `__iter__` 对象都是属于 IterableObjc ，因此迭代器也属于 IterableObjc；并且在其它接受 IterableObjc 的地方，也多半可以接受迭代器。

- `iterator.__next__()`

  返迭代器中的下一个项。重复调用迭代器的 [`__next__()`](https://docs.python.org/3.7/library/stdtypes.html#iterator.__next__) 方法(或通过内置函数[`next()`](https://docs.python.org/3.7/library/functions.html#next) 重复调用迭代器)，将返回流中连续的项。当没有再无数据可供使用时，便会抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration) 异常，这时表明该迭代器对象已经耗尽，若此后仍试图调用该迭代器的 `__next__()` 方法，将会再次抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration) 异常。[^4]

  一旦迭代器的 [`__next__()`](https://docs.python.org/3.7/library/stdtypes.html#iterator.__next__) 方法抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration)，则必须在后续调用中继续抛出异常。不遵从此特性的实现被视为不正确。[^7]

如果容器支持不同类型的迭代，则可以提供额外的方法来专门请求这些迭代类型的迭代器(支持多种迭代形式的对象的一个例子是树结构，它支持 breadth-first 和 depth-first 两种遍历方式)。[^7]

Python 定义了多个迭代器对象，以支持对如下类型进行迭代：常规(general)序列类型和特殊(specific)序列类型、字典以及其它专业表单(specialized forms)。除迭代器协议的实现之外，其实特定类型并不重要。[^7]

```python
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值
```



### 3.1 迭代器与 for 循环

将迭代器用于 [`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环时，[`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环仍会调用 `iter()` 来处理迭代器对象，然后通过 `next()` 逐一获取每个元素，直至 `__next__` 抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration) 为止。注意：将某个迭代器对象传递给 [`iter()`](https://docs.python.org/3.7/library/functions.html#iter) 后，只会返回指向该迭代器的引用，并不会创建具备新id的迭代器对象。

```python
>>> aa = [1,2,3,]
>>> bb = iter(aa)
>>> bb
<list_iterator object at 0x000001B393436E48>
>>> cc = iter(bb)
>>> cc # bb和cc引用同一个对象
<list_iterator object at 0x000001B393436E48>
```

通常情况下，如果反复尝试将某个迭代器用于 `for` 循环，其实在第一次循环结束时就会耗尽该迭代器，之后只会反复使用这个已被耗尽的迭代器，看起来如同在使用一个空容器。[^4]

```python
>>> aa = [1,2,3,]
>>> bb = iter(aa)
>>> for i in bb:
	print(i)

	
1
2
3
>>> for i in bb:
	print(i)

	
>>> 
```

但是，如果在`__iter__` 中重置相关变量，则可让迭代器反复用于for循环，并且每次都有输出。

```python
# 请对比IteratorObjc修改前后的代码
# 修改前
class IteratorObjc:
    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        while self._count < 3:
            self._count += 1
            return self._count

# 修改后
class IteratorObjc:
    """
    在这种情况下，每次调用__iter__方法时，
    会返回实例对象自身，不会创建具备新id的迭代器对象。
    """
    def __iter__(self):
        # 重置_count，便可反复进行迭代
        self._count = 0
        # 调用时返回实例自身
        return self

    def __next__(self):
        while self._count < 3:
            self._count += 1
            return self._count

a_iterator = IterableObjc()
for i in a_iterator:
    print(i, end=',')
print()
for i in a_iterator: # 可重复输出
    print(i, end=',')
```

### 3.2 迭代器与内置函数

由于迭代器也属于 IterableObjc，所以迭代器也可直接用于如下内置函数：

- `any(iterable)`
- `class list([iterable])`
- `map(function, iterable, ...)`
- ....

通常情况下，如果反复将某个迭代器传递给内置函数。在第一次使用该迭代器时就会耗尽该迭代器，之后只会反复使用这个已被耗尽的迭代器，看起来如同在使用一个空容器。

```python
>>> aa = [1,2,3,]
>>> bb = iter(aa)
>>> list(bb)
[1, 2, 3]
>>> list(bb)
[]
```

但是，如果在`__iter__` 中重置相关变量，则可让迭代器反复用于内置函数。

```python
class IteratorObjc:
    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        while self._count < 3:
            self._count += 1
            return self._count


a_iterator = IterableObjc()
print(list(a_iterator))
print(list(a_iterator))
```

输出

```
[1, 2, 3]
[1, 2, 3]
```

### 3.3 itertools

> 10.1. [`itertools`](https://docs.python.org/3/library/itertools.html#module-itertools) — Functions creating iterators for efficient looping

[`itertools`](https://docs.python.org/3/library/itertools.html#module-itertools) 模块提供了众多用于创建迭代器的函数。下面简要介绍几个：

- `count()` 函数返回的迭代器可产生一串连续的整数，并且通过该迭代器可产生无限个整数。与内置函数 `range()` 不同，`count()` 不需要通过参数来设定上线。

  ```python
  >>> from itertools import count
  >>> counter = count(start=10)
  >>> next(counter)
  10
  >>> next(counter)
  11
  ```

- `cycle()` 函数会把所接受的可迭代对象转换为一个无限循环的迭代器。

  ```python
  >>> from itertools import cycle
  >>> colors = cycle(['red', 'white', 'blue'])
  >>> next(colors)
  'red'
  >>> next(colors)
  'white'
  >>> next(colors)
  'blue'
  >>> next(colors)
  'red'
  ```

- `islice()` 函数会截取输入迭代器的一部分，并把这部分作为输出迭代器返回

  ```python
  >>> from itertools import islice
  >>> colors = cycle(['red', 'white', 'blue'])  # infinite
  >>> limited = islice(colors, 0, 4)            # finite
  >>> for x in limited:                    # so safe to use for-loop on
  ...     print(x)
  red
  white
  blue
  red
  ```

## 4. 生成器

generator [^4][^7][^9]

本质上来说，生成器([generator](https://docs.python.org/3.7/glossary.html#term-generator))就是一个函数，它提供了一种实现迭代器协议的便捷方式。生成器与普通函数的区别在于它包含 [`yield`](https://docs.python.org/3.7/reference/simple_stmts.html#yield) 表达式，并且不需要定义 `__iter__()` 和 `__next__()`。也就是说，使用 [`yield`](https://docs.python.org/3.6/reference/simple_stmts.html#yield) 语句的函数或方法便可被称为生成器函数( *generator function* )。关于 `yield` 可参考 [The yield statement](https://docs.python.org/3.6/reference/simple_stmts.html#yield) 和  [the documentation for the yield expression](https://docs.python.org/3.7/reference/expressions.html#yieldexpr). 

```python
# 一个生成器函数的示例：
def generator_func():
    cont = 0
    while cont < 3:
        cont += 1
        yield cont
```

generator 在官方文档的语境中存在如下两种含义：

- 第一种用于指代生成器函数，**本文内容均采用这种含义**

- 第二种是用于指代  generator iterator(下一节将介绍此概念)。比如通过下面的代码可以看到 Python 将生成器函数描述为函数类型，但将 generator iterator 描述为 Generator 类型。因此，当我们在文档中遇到 generator 时，一定要根据上下文来判断其具体所指的对象。

  ```python
  # 关于生成器在不同语境中的含义：
  from collections import abc
  import types
  def generator_func():
      cont = 0
      while cont < 3:
          cont += 1
          yield cont
  
  
  g_iterator = generator_func()
  assert isinstance(generator_func, types.FunctionType) # 无异常
  assert isinstance(g_iterator, abc.Generator) # 无异常
  ```

### 4.1 generator iterator

[generator-iterator](https://docs.python.org/3.7/glossary.html#term-generator-iterator) 是通过生成器函数创建的实例对象 (下文中简称为 g_iterator)，该对象自动支持 [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 和 [`__next__()`](https://docs.python.org/3.7/reference/expressions.html#generator.__next__) 方法，属于迭代器。g_iterator 适用于任何需要迭代器的场景。注意，通过生成器函数创建 g_iterator 时，并不会执行生成器函数体中的任何代码：

```python
def generator_func():
    print("生成器函数")
    cont = 0
    while cont < 3:
        cont += 1
        yield cont


g_iterator = generator_func()
# 不会打印"生成器函数"
```

细节上来讲，g_iterator 用于执行函数体：通过调用 `g_iterator.__next__()` 方法，可继续执行函数体。如果在执行过程中遇到了 [`yield`](https://docs.python.org/3.6/reference/simple_stmts.html#yield) 语句，便会暂停执行并返回指定变量；如果在遇到 [`return`](https://docs.python.org/3.6/reference/simple_stmts.html#return) 语句或者函数体已执行完毕时，便会抛出 [`StopIteration`](https://docs.python.org/3.6/library/exceptions.html#StopIteration) ，表明 g_iterator 对象已被耗尽。

简单来说，[`yield`](https://docs.python.org/3.7/reference/simple_stmts.html#yield) 用于暂停 g_iterator  的执行，并会记住当前位置的执行状态(包括局部变量和待处理的 try 语句)。当 g_iterator  恢复执行时，便会从之前中断的位置开始执行(普通函数每次调用时，都会从头开始重新执行)

如果生成器函数中使用了 `return` 语句时，返回值被包含在 `StopIteration.value` 中。如果使用 `for` 语句，则拿不到 `return` 的返回值。如果想要拿到返回值，则必须捕获 `StopIteration` 异常。

```python
>>> def fib(max):
...     n, a, b = 0, 0, 1
...     while n < max:
...         yield b
...         a, b = b, a + b
...         n = n + 1
...     return '我是返回值'
...
>>> f = fib(3)
>>> next(f)
1
>>> next(f)
1
>>> next(f)
2
>>> next(f)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration: 我是返回值
```

如果将 g_iterator 对象传递给 [`iter()`](https://docs.python.org/3.7/library/functions.html#iter)，只会返回指向 g_iterator 自身的引用，并不会创建具备新id的迭代器对象。

```python
class Generator:
    def __iter__(self):#生成器函数
        cont = 0
        while cont < 3:
            cont += 1
            yield cont


a_generator = Generator()

# 通过同一个generator可创建不同的generator iterator。
# 例如g_iter1和g_iter2是两个具备不同标识符id的generator iterator
g_iter1 = iter(a_generator)
g_iter2 = a_generator.__iter__()
print("g_iter1的id是:{0}, 类型是:{1}".format(id(g_iter1), type(g_iter1)))
print("g_iter2的id是:{0}, 类型是:{1}\n".format(id(g_iter2), type(g_iter2)))

# 对同一个generator iterator依次执行这两种方法，均返回带有同一id的对象
print(id(g_iter1.__iter__()))
print(id(iter(g_iter1)))

"""输出：
g_iter1的id是:2742184172272, 类型是:<class 'generator'>
g_iter2的id是:2742184172624, 类型是:<class 'generator'>

2742184172272
2742184172272
"""
```



### 4.2 生成器表达式

generator expression[^4]

该表达式同样会返回一个 generator iterator。该表达式与常规表达式一样，会使用 [`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 循环来定义一个循环变量 `i` 及其范围；也可使用 `if` 对 `i` 进行筛选。该组合表达式可为封闭(enclosing)函数生成值：

```python
sum(i*i for i in range(10))  
# sum of squares 0, 1, 4, ... 81; result 285
```

**注意，没有元组推导式，元括弧用于创建生成器表达式：**

```python
>>> lazy_squares = (x * x for x in numbers)
>>> lazy_squares
<generator object <genexpr> at 0x10d1f5510>
>>> next(lazy_squares)
1
>>> list(lazy_squares)
[4, 9, 16, 25, 36]
```

#### 4.2.1 对比其他常规表达式

列表推导式用于构建一个列表：

```python
>>> numbers = [1, 2, 3, 4, 5, 6]
>>> [x * x for x in numbers]
[1, 4, 9, 16, 25, 36]
```

集合推导式用于构建一个集合：

```python
>>> {x * x for x in numbers}
{1, 4, 36, 9, 16, 25}
```

字典推导式用于构建一个字典：

```python
>>> {x: x * x for x in numbers}
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36}
```

## 5. isinstance

通过 `isinstance()` 进行实例测试时：

- ContainerObjc 属于 [`Container`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Container) 
- IterableObjc 属于 [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable) 
- iterator 属于 [`Generator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Generator) 和 [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable) 
- generator iterator 属于 [`Generator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Generator) 和 [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable) 

```python
from collections import abc

# 容器 ContainerObjc
class ContainerObjc(object):
    def __contains__(self, item):
        pass
assert isinstance(ContainerObjc(), abc.Container) # 无异常

# 可迭代对象 IterableObjc 
class IterableObjc:
    def __iter__(self):
        pass
assert isinstance(IterableObjc(), abc.Iterable) # 无异常

# 迭代器 iterator 
class IteratorObjc:
    def __iter__(self):
        pass

    def __next__(self):
        pass
assert isinstance(IteratorObjc(), abc.Iterator) # 无异常

# 生成器函数返回的generator iterator
def generator_func():
    yield "生成器函数"
assert isinstance(generator_func(), abc.Generator) # 无异常

# 生成器表达式返回的generator iterator
generator_expr = (i for i in range(10))
assert isinstance(generator_expr, abc.Generator) # 无异常
```

------

注脚：

[^1]: 语言参考 - [3.1. Objects, values and types](https://docs.python.org/3.7/reference/datamodel.html#objects-values-and-types)
[^2]: 标准库 8.4. [`collections.abc`](https://docs.python.org/3.6/library/collections.abc.html#module-collections.abc) — Abstract Base Classes for Containers
[^3]: [Iterables vs. Iterators vs. Generators](https://nvie.com/posts/iterators-vs-generators/) | [完全理解 Python 迭代对象、迭代器、生成器](http://python.jobbole.com/87805/)
[^4]: [Glossary 术语表](https://docs.python.org/3.7/glossary.html)
[^5]: [iter(*object*[, *sentinel*])](https://docs.python.org/3.7/library/functions.html#iter) 
[^6]: 语言参考 - [8.3. The `for` statement](https://docs.python.org/3.7/reference/compound_stmts.html#the-for-statement)
[^7]: 标准库 - [4.5. terator Types](https://docs.python.org/3.7/library/stdtypes.html#iterator-types)
[^8]: 语言参考 - [3.3.7. Emulating container types](https://docs.python.org/3.7/reference/datamodel.html#emulating-container-types)
[^9]: 语言参考 -[3.2. The standard type hierarchy](https://docs.python.org/3.7/reference/datamodel.html#the-standard-type-hierarchy)
[^10]: [Python迭代器，生成器--精华中的精华](https://www.cnblogs.com/deeper/p/7565571.html)

扩展阅读：

- [Use More Iterators](https://nvie.com/posts/use-more-iterators/)

