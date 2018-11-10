# globals

```
globals()
    Return the dictionary containing the current scope's global variables.
    
    NOTE: Updates to this dictionary *will* affect name lookups in the current
    global scope and vice-versa.
```

🔨 globals()

该函数会返回当前模块的全局符号表，全局符号表以字典形式记录了模块最外层的全局变量的分配关系。例如：

```python
>>> from pprint import pprint
>>> pprint(globals())
{'__annotations__': {},
 '__builtins__': <module 'builtins' (built-in)>,
 '__doc__': None,
 '__loader__': <class '_frozen_importlib.BuiltinImporter'>,
 '__name__': '__main__',
 '__package__': None,
 '__spec__': None,
 'pprint': <function pprint at 0x0000024FD8BEB268>}
```

注意：`globals()` 总是会返回当前模块的全局符号表。比如，当我们在函数定义中调用 `globals()` 时，它始终会返回函数定义所在模块的全局符号表，而不会返回调用该函数的模块的全局符号表。
示例 - `other` 模块中的 `def id_of_globals()` 函数始终会返回 `other` 模块的全局符号表，即使在 `main` 模块中调用 `def id_of_globals()` 函数，也是如此：

```python
# in other.py
print("globals of other:", id(globals()))
def id_of_globals():
    print("globals of other:", id(globals()))
```

```python
# in main.py
import other
other.id_of_globals()
print("globals of main:", id(globals()))
"""Out:
globals of other: 2341407132192
globals of other: 2341407132192
globals of main: 2341406892536
"""
```

当位于模块的最外层(全局作用域)时，本地符号表和全局符号表相等，此时 `globals()` 和 `locals()` 等效。

```python
# At the outermost layer of the module
print(id(globals()))
print(id(locals()))
"""Out:
2784089268728
2784089268728
"""
```

如果对全局符号表做出修改，则会影响解释器所使用的全局变量，反之亦然：

```python
>>> globals()['update'] = "orca_j35"
>>> update
'orca_j35'
>>> del update
>>> globals().get('update','not to exist')
'not to exist'
```

