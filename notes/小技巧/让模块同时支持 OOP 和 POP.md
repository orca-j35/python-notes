>转载须注明出处：简书@[Orca_J35](https://www.jianshu.com/u/5e6f798c903a) | GitHub@[orca-j35](https://github.com/orca-j35)

提供一个让模块同时支持"面向对象"和"面向过程"的思路。
如果需要一个更详细的示例，可以参考内置模块 `turtle`，该模块同时支持 OOP 和 POP。

先创建一个名为 test_module 的模块：

```python
# file_name: test_module.py
__all__ = ['Cls', 'func']
class Cls(object):
    def func(self):
        print("Orca_J35")

instance = Cls()
exec('func = instance.func', globals())
```

然后导入并使用该模块：

```python
# file_name: test.py
from hello import *
func() # 使用POP方式
"""Out:
Orca_J35
"""
```
