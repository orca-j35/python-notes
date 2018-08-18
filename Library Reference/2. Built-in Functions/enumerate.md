### enumerate

enumerate(*iterable*, *start=0*) 

该内置函数本质上来说是在调用 enumerate 类的构造函数，从而生成一个枚举(enumerate)对象。 *iterable* 必须是一个支持迭代(iteration)的对象，比如  sequence 和 [iterator](https://docs.python.org/3/glossary.html#term-iterator) 。

枚举对象也是一个迭代器(iterator)，每次调用其 [`__next__()`](https://docs.python.org/3.7/library/stdtypes.html#iterator.__next__)  方法时，便会产生(yield)一个元组——其中包含一个计数值(以start为起点，默认值是0)和一个通过 *iterable* 对象生成的值。例如：

```python
>>> e = enumerate([1, 2, 3], start=1) # 指定起始值
>>> next(e)
(1, 1)
>>> next(e)
(2, 2)
>>> next(e)
(3, 3)
>>> next(e)
Traceback (most recent call last):
  File "<pyshell#7>", line 1, in <module>
    next(e)
StopIteration
```

作为 enumerate 类的用户，我们不必了解实现细节，可把 enumerate 等效于如下代码：

```python
def enumerate(sequence, start=0):
    n = start
    for elem in sequence:
        yield n, elem
        n += 1
```

示例：

```python
>>> for i in enumerate((1, 2, 3)):print(i)

(0, 1)
(1, 2)
(2, 3)
```