# print

🔨 print(**objects*, *sep=' '*, *end='\n'*, *file=sys.stdout*, *flush=False*)

该函数用于将 *objects* 打印至文本流 *file*，其中 *sep*、*file*、*flush* 均是 *keyword-only* 参数，*objects* 是 *var-positional* 参数。如果 *objects* 为空，`print()` 将会只打印 *end*。

在 `print()` 函数中，所有非关键字实参均会先转换为字符串(类似于 `str()`)， 然后再写入到流中。正是由于该函数会先将非关键字实参转换为文本字符串，所以它不能用于二进制模式的文件对象。在使用二进制模式的文件对象时，请使用 `file.write(...)`。

```python
>>> print(b'absd')
b'absd'
```

Changed in version 3.3: Added the *flush* keyword argument.

**参数说明：**

- *sep* - string inserted between *objects*, must be given as keyword arguments. if it is not present or `None`, a space will be used.  

  ```python
  >>> print(1,2,3,4,5,sep='-')
  1-2-3-4-5
  >>> print(1,2,3,4,5)
  1 2 3 4 5
  >>> print(1,2,3,4,5,sep=None)
  1 2 3 4 5
  ```

- *end* - string appended after the last value, must be given as keyword arguments.  if it is not present or `None`, a newline will be used.  

  ```python
  >>> print(1,2,3,4,5,end='!!!!!')
  1 2 3 4 5!!!!!
  >>> print(1,2,3,4,5)
  1 2 3 4 5
  >>> print(1,2,3,4,5,end=None)
  1 2 3 4 5
  >>> print(end='@')
  @
  ```

- *file* - a file-like object (stream), must be given as keyword arguments. 

  The *file* argument must be an object with a `write(string)` method; if it is not present or `None`, [`sys.stdout`](https://docs.python.org/3.7/library/sys.html#sys.stdout) will be used. 

  ```python
  class Cls(object):
      def __init__(self):
          self.values = []
  	# file-like对象是指定义了write(string)方法的对象
      def write(self, value):
          self.values.append(value)
  
  
  x = Cls()
  i = [1, 2, 3]
  j = ['a', 'b', 'c']
  print(i, j, range(5), file=x)
  print(x.values)
  # Out: ['[1, 2, 3]', ' ', "['a', 'b', 'c']", ' ', 'range(0, 5)', '\n']
  # 注意观察输出序列的结构
  ```

- *flush* - whether to forcibly flush the stream —— 立即把内容输出到流文件，不做缓存。

  Whether output is buffered is usually determined by *file*, but if the *flush* keyword argument is true, the stream is forcibly flushed.

  ```python
  >>> f_object = open('test.txt','w',encoding='utf8')
  # 此时test.txt中没有何内容
  >>> print('1', end=',', file=f_object)
  >>> print('2',file=f_object)
  # 此时test.txt中仍然没有何内容，会先将输出至文件对象的数据进行缓存，
  # 待文件对象关闭时，才会将缓存的数据写入文件对象
  >>> f_object.close()
  # 此时test.txt中出现: '1,2'
  
  >>> f_object = open('test.txt','w',encoding='utf8')
  >>> # 此时test.txt中没有何内容
  >>> print('1',file=f_object,flush=True)
  # 此时test.txt中出现: '1'
  # flush=True时不会缓存数据，会立即把内容输出到流文件,不用等文件对象关闭后再写入
  >>> f_object.close()
  ```
