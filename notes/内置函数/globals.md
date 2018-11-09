# globals

```
globals()
    Return the dictionary containing the current scope's global variables.
    
    NOTE: Updates to this dictionary *will* affect name lookups in the current
    global scope and vice-versa.
```

🔨 globals()

该函数会返回一个表示当前全局符号表的字典。

该字典始终是当前模块(在函数或方法中，是定义它们的模块，而不是调用调用它们的模块)



Return a dictionary representing the current global symbol table. This is always the dictionary of the current module (inside a function or method, this is the module where it is defined, not the module from which it is called).



Updates to this dictionary will affect name lookups in the current global scope and vice-versa.

```python

```

