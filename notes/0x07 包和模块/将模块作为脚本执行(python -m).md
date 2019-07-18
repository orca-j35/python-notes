# 将模块作为脚本执行(python -m)

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考: 
>
> - [1. Command line and environment](https://docs.python.org/3/using/cmdline.html#command-line-and-environment) -> [-m module-name](https://docs.python.org/3/using/cmdline.html#cmdoption-m)
> - [python 自问自答：python -m参数？](https://www.cnblogs.com/xueweihan/p/5118222.html)
>
> 相关笔记:﹝\_\_main\_\_ - Top-level script environment.md﹞
>
> 扩展阅读:
>
> - [`runpy.run_module()`](https://docs.python.org/3/library/runpy.html#runpy.run_module) - Equivalent functionality directly available to Python code
> - [**PEP 338**](https://www.python.org/dev/peps/pep-0338) – Executing modules as scripts
> - [充分理解 python -m mod](https://www.jianshu.com/p/934db39a9b6d)
>
> 注意：本笔记使用 Python 3.7
>
> *Changed in version 3.1:* Supply the package name to run a `__main__` submodule.
>
> *Changed in version 3.4:* namespace packages are also supported

⌨ `python -m <module-name> [arg] ... `

该命令会在 [`sys.path`](https://docs.python.org/3/library/sys.html#sys.path) 中搜索 module-name 模块，并将其作为 [`__main__`](https://docs.python.org/3/library/__main__.html#module-__main__) 模块执行(如果存在 module-name 的话)——也就是说会将模块以脚本方式执行。

由于 module-name 表示模块名，因此 module-name 中不能包含文件扩展名(`.py`)。module-name 应是一个有效的绝对 Python 模块名，但是实现可能不会强制执行此操作「e.g., 可能会允许你使用包含连字符 `-` (*hyphen*)的名称」。

还允许使用 package 名称(including namespace packages)。如果提供的是 package 名，而非普通模块名，解释器便会将 `<pkg>.__main__` 作为主模块执行。利用此行为可将传递给解释器的目录或 zipfiles 作为脚本参数处理。详见笔记﹝\_\_main\_\_ - Top-level script environment.md﹞

Note: 该选项不能与以 C 编写的内置模块和扩展模块一起使用，因为这些模块没有 Python 模块文件。但是，即使原始源文件不可用，这些模块还是可用于预编译模块。

使用了 `-m` 选项后，[`sys.argv`](https://docs.python.org/3/library/sys.html#sys.argv) 中的第一个元素将被设置为相应模块文件的完整路径(while the module file is being located, the first element will be set to `"-m"`)。与 [`-c`](https://docs.python.org/3/using/cmdline.html#cmdoption-c) 选项一样，当前目录将被添加至 [`sys.path`](https://docs.python.org/3/library/sys.html#sys.path) 的开头。

标准库中的许多模块都包含当其作为脚本执行时，才会执行的代码。一个例子是timeit 模块：

```python
python -mtimeit -s 'setup here' 'benchmarked code here'
python -mtimeit -h # for details
```

示例 - `-m` 和直接运行 `.py` 的区别：

```bash
# in Python 3.7
# 当前目录: ~\\GitHub\\python_notes\\notes\\模块\\devel-m
'''code of main.py
import os, sys
print('> in main.py, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...\n')
else:
    print('I am being imported from another module...\n')

print(f'os.getcwd: {os.getcwd()}\n'
      f'sys.argv: {sys.argv}\n'
      f'sys.path: {sys.path}')
'''
# 注意对比以下三中情况
# 直接执行main.py脚本
$ python main.py
> in main.py, and say:
This program is being run by itself...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_-m
sys.argv: ['main.py']
sys.path: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_-m', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']

# 将main模块当作脚本执行
$ python -m main
> in main.py, and say:
This program is being run by itself...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_-m
sys.argv: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_-m\\main.py']
sys.path: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_-m', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']

# 导入模块
# ''表示当前目录
$ python
Python 3.7.1 ...
>>> import main
> in main.py, and say:
I am being imported from another module...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_-m
sys.argv: ['']
sys.path: ['', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
```

`''` 表示当前目录

## 需使用 `-m` 的场景

### 示例代码和目录结构

目录结构如下：

```python
'''
devel_-m/ -> 当前目录
    pkg/
    	__init__.py
    	run.py
    pkg1/
    	__init__.py
    	moduleA.py
'''
```

`pkg/__init__.py` 中的代码：

```python
import os, sys
print(f'> in {__package__}.__init__, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...\n')
else:
    print('I am being imported from another module...\n')

print(f'os.getcwd: {os.getcwd()}\n'
      f'sys.argv: {sys.argv}\n'
      f'sys.path: {sys.path}')
print('=================')
```
`pkg/run.py.py` 中的代码：

```python
import os, sys
print(f'> in {__package__}.run, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...\n')
else:
    print('I am being imported from another module...\n')

print(f'os.getcwd: {os.getcwd()}\n'
      f'sys.argv: {sys.argv}\n'
      f'sys.path: {sys.path}')
print('=================')
from pkg1 import moduleA
```
`pkg1/__init__.py` 中的代码：

```python
print(f'> in {__package__}.__init__, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...')
else:
    print('I am being imported from another module...')
print('=================')
```
`pkg1/moduleA.py` 中的代码：

```python
print(f'> in {__package__}.moduleA, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...')
else:
    print('I am being imported from another module...')
print('=================')
```

### python xxx.py

当我们在 `devel_-m` 目录下执行 `python pkg/run.py` 命令时，会抛出异常。因为，此时 `sys.path[0]` 中存放的是 `run.py` 所在的目录(即，`~/devel_-m/pkg`)，无法通过 `sys.path[0]` 找到名为 `pkg1` 的包。执行过程如下：

```python
iwhal@LAPTOP-AR0R702R MINGW64 ~/Documents/GitHub/python_notes/notes/包和模块/devel_-m (master)
$ python pkg/run.py
> in None.run, and say:
This program is being run by itself...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_-m
sys.argv: ['pkg/run.py']
sys.path: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_-m\\pkg', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
=================
Traceback (most recent call last):
  File "pkg/run.py", line 12, in <module>
    from pkg1 import moduleA
ModuleNotFoundError: No module named 'pkg1'
```

### python -m xxx.py

当我们在 `devel_-m` 目录下执行 `python -m pkg.run` 命令时，不会抛出异常。因为，此时 `sys.path[0]` 中存放的是 `pkg` 所在的目录(即，`~/devel_-m`)，可通过 `sys.path[0]` 找到名为 `pkg1` 的包。执行过程如下：

```python
iwhal@LAPTOP-AR0R702R MINGW64 ~/Documents/GitHub/python_notes/notes/包和模块/devel_-m (master)
$ python -m pkg.run
> in pkg.__init__, and say:
I am being imported from another module...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_-m
sys.argv: ['-m']
sys.path: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_-m', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
=================
> in pkg.run, and say:
This program is being run by itself...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_-m
sys.argv: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_-m\\pkg\\run.py']
sys.path: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_-m', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
=================
> in pkg1.__init__, and say:
I am being imported from another module...
=================
> in pkg1.moduleA, and say:
I am being imported from another module...
=================
```

通过 `python -m` 执行包中的模块时，会先执行包的 `__init__.py` 脚本(在本例中是 `pkg.__init__`)。因此，`sys.path[0]` 会存放包所在的目录(在本例中是  `~/devel_-m`，在此目录中可找到名为 `pkg1` 的包)。

如果在脚本中导入了其它模块，那么保证该脚本顺利执行的前提是在 `sys.path` 中可找到该模块(详见笔记﹝模块搜索路径.md﹞)。



