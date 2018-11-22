# exec

```
exec(source, globals=None, locals=None, /)
    Execute the given source in the context of globals and locals.
    
    The source may be a string representing one or more Python statements
    or a code object as returned by compile().
    The globals must be a dictionary and locals can be any mapping,
    defaulting to the current globals and locals.
    If only globals is given, locals defaults to it.
```

🔨 exec(*object*[, *globals*[, *locals*]])

**Exec**ute the given source in the context of globals and locals.

该函数支持动态执行 Python 代码，返回值是 `None`，各参数含义如下：

- *object* - 必选参数，有以下两种情况：

  - 可以是一个字符串，其内容是一组 Python 语句。`exec()` 会先将 *object* 中的内容解析为 Python 语句，然后执行这些语句(除非发生语法错误)[[1]](https://docs.python.org/3.7/library/functions.html#id2)，返回值是 `None`。

    ```python
    >>> exec('1+2+3+4')
    >>> print(exec("{1: 'a', 2: 'b'}"))
    None
    >>> x = 1
    >>> exec('x+=1')
    >>> x
    2
    ```

  - 还可以是一个 code 对象，`exec()` 会直接执行该 code 对象。

  In all cases, the code that’s executed is expected to be valid as file input (see the section “File input” in the Reference Manual). Be aware that the [`return`](https://docs.python.org/3.7/reference/simple_stmts.html#return) and [`yield`](https://docs.python.org/3.7/reference/simple_stmts.html#yield)statements may not be used outside of function definitions even within the context of code passed to the [`exec()`](https://docs.python.org/3.7/library/functions.html#exec) function.

- *globals* - 可选参数，表示全局变量表，必须是一个字典对象，默认使用当前全局变量表。如果仅提供 *globals*，但不提供 *locals*，则默认 *locals* 与 *globals* 相同。

  如果提供的 *globals* 字典中并不包含 `__builtins__` 键，则会在解析 *object* 之前将 `'__builtins__': <module 'builtins' (built-in)>` 插入到 *globals* 中。这意味着 *object* 通常具有对标准模块 [`builtins`](https://docs.python.org/3.7/library/builtins.html#module-builtins) 的全部访问权限。

  ```python
  >>> g = {}
  >>> g.keys()
  dict_keys([])
  # 由于会在解析object之前向d中插入'__builtins__': 'builtins'
  # 所以可以在object中直接使用内置函数
  >>> exec('print(1024)',g)
  1024
  # g中被添加了__builtins__键
  >>> g.keys()
  dict_keys(['__builtins__'])
  ```

  还可以通过 `__builtins__` 属性控制内置函数的可用性：

  ```python
  import builtins
  g = dict(__builtins__={'print': builtins.print})
  # 此时，只能使用print函数
  exec('print(999)', g)
  ```

- *locals* - 可选参数，表示局部变量表，可以是任何映射对象，默认使用当前局部变量表。如果仅提供 *globals*，但不提供 *locals*，则默认 *locals* 与 *globals* 相同。

  在没有显式传递 *locals* 参数时，会默认使用 `locals()` 来获取当前本地符号表。此时不要尝试手动修改本地符号表中的内容。因为就算手动修改了本地符号表，也并不会影响解释器所使用的本地变量和自由变量的值，对本地符号表所做的手动修改均会被忽略。如果需要在 `exec()` 返回后查看 *locals* 的状态，则必须显式传递 *locals* 参数。

  ```python
  def func():
      a_field = 'orca'
      print(locals())
      # 手动修改本地符号表中的变量，并不会影响到本地符号表
      locals()['a_field'] = "j35"
      # 同理，采用默认locals参数时，也无法手动修改本地符号表
      exec('a_field="j35"')
      print(locals())
  	# 只有采用显式locals参数时，才能观察到locals的变化
      local_dict = dict(__builtins__={})
      exec('a_field="j35"', local_dict)
      print(local_dict)
  func()
  """Out:
  {'a_field': 'orca'}
  {'a_field': 'orca'}
  {'__builtins__': {}, 'a_field': 'j35'}
  """
  ```

内置函数 `globals() ` 会返回当前全局字典，`locals()` 会返回当前本地字典，在向 `eval()` 或 `exec()` 传递参数时，可能会用到 `globals()` 和 `locals()`。在模块级别， `globals() ` 和 `locals()` 都会返回全局字典。


