# sum

```
sum(iterable, start=0, /)
    Return the sum of a 'start' value (default: 0) plus an iterable of numbers
    
    When the iterable is empty, return the start value.
    This function is intended specifically for use with numeric values and may
    reject non-numeric types.
```

🔨 sum(*iterable*[, *start*])

该函数会将 *start* 与 *iterable* 中的各项从左至右逐一相加，并返回求和结果。*iterable* 中的元素均是数值类型；*start* 的默认值是 0，不能以非数值作为 *start* 的实参。sum 函数大致等效于如下代码：

```python
def sum_(iterable, start=0):
    for i in iterable:
        start += i
    return start
```

示例：

```python
>>> sum(range(10))
45
>>> sum((1.5,2.5,3.5,4.5))
12.0
>>> sum((complex(1,-1),complex(2,-2)))
(3-3j)
>>> sum([],10) # 如果iterable为空，则返回start
10
>>> sum((1,2,3,4),2)
12
```

注意 - sum 函数专门用于数值计算，会拒绝非数值类型。

```python
>>> sum([1,2,3],[1,])
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    sum([1,2,3],[1,])
TypeError: can only concatenate list (not "int") to list
>>> sum((1,2,3,'4'))
Traceback (most recent call last):
  File "<pyshell#11>", line 1, in <module>
    sum((1,2,3,'4'))
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

提示 - 在某些情况下，sum 函数并非最理想的方案，例如：

- 在连接由字符串组成的序列时，最有效方式是调用 `''.join(sequence)` 方法

  ```python
  >>> '-'.join(['hello','world'])
  'hello-world'
  ```

- 当加数是具备扩展精度(*extended precision*)的浮点数时，需使用 [`math.fsum()`](https://docs.python.org/3.7/library/math.html#math.fsum) 

  ```python
  >>> sum([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
  0.9999999999999999
  >>> fsum([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1])
  1.0
  ```

- 在连接一系列可迭代对象时，需要使用 [`itertools.chain()`](https://docs.python.org/3.7/library/itertools.html#itertools.chain)

  ```python
  def chain(*iterables):
      # chain('ABC', 'DEF') --> A B C D E F
      for it in iterables:
          for element in it:
              yield element
  ```


