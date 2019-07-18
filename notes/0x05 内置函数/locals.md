# locals

```
locals()
    Return a dictionary containing the current scope's local variables.
    
    NOTE: Whether or not updates to this dictionary will affect name lookups in
    the local scope and vice-versa is *implementation dependent* and not
    covered by any backwards compatibility guarantees.
```

🔨 locals()

该函数会返回当前本地作用域的本地符号表，本地符号表以字典形式记录了当前作用域中局部变量的分配关系。例如：

```python
def func():
    print(locals())
    update = 'new_field' # 向本地符号表新增变量
    print(locals())
func()
"""Out：
{}
{'update': 'new_field'}
"""
```

在函数块中调用 `locals()` 时，其返回的本地符号表中会包含自由变量；但是，在类块中调用 `locals()` 时，其返回的本地符号表中不会包含自由变量。

```python
def sum_(x, y):
    def inner():
        print(locals())
        return x + y # x和y是自由变量
    return inner()
sum_(1, 2)
"""Out:
{'x': 1, 'y': 2}
"""
```

注意：不要手动修改本地符号表中的内容。因为就算手动修改了本地符号表，也并不会影响解释器所使用的本地变量和自由变量的值，对本地符号表所做的手动修改均会被忽略。

```python
from pprint import pprint
def func():
    a_field = 'orca'
    pprint(locals())
    locals()['a_field'] = "j35" # 手动修改本地符号表中的变量
    pprint(locals())
    pprint(a_field)
func()
"""Out:
{'a_field': 'orca'}
{'a_field': 'orca'}
'orca'
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

## 应用示例

利用`locals()` 验证文件是否打开：

```
try:
	data = open('its.txt', "w")
	print("It's...", file=data)
except IOError as err:
	print('File error: ' + str(err))
finally:
	if 'data' in locals():
		data.close()
```

