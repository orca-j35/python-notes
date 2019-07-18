# \_\_import\_\_
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考：
>
> - [importlib.import_module(name, package=None)](https://docs.python.org/3.7/library/importlib.html#importlib.import_module)
> - [Python in a Nutshell 2nd](https://learning.oreilly.com/library/view/python-in-a/0596001886/) -> 8.Core Builts-ins -> Built-in Types
> - [importlib — Python 的模块载入机制](https://pythoncaff.com/docs/pymotw/importlib-pythons-import-mechanism/209)
> - [【Python学习笔记】1. import reload 以及`__import__`注意点](https://www.cnblogs.com/MaggieXiang/archive/2013/06/05/3118156.html)

🔨 \_\_import\_\_(*name*, *globals=None*, *locals=None*, *fromlist=()*, *level=0*) -> module_object

Note: [`__import__`](https://docs.python.org/3.7/library/functions.html#__import__) 与 [`importlib.import_module()`](https://docs.python.org/3.7/library/importlib.html#importlib.import_module) 不同，`__import__` 属于在日常 Python 编程中不需要的高级函数。

事实上 [`import`](https://docs.python.org/3.7/reference/simple_stmts.html#import) 语句同样会调用 `__import__` 函数，因此可通过替换 `__import__` 函数(导入 [`builtins`](https://docs.python.org/3.7/library/builtins.html#module-builtins) 模块，并重新为 `builtins.__import__` 赋值)来改变 `import` 语句的语义，但是强烈建议你不要这样去做，因为利用导入钩子(*import* *hooks*)可以以更容易的方式来达到相同的目的(见 [PEP 302](https://www.python.org/dev/peps/pep-0302))，而且代码会假设正在使用默认的导入实现，因此不会导致代码问题。

由于 `__import__()` 适用于 Python 解释器，而非一般用途，所以不鼓励直接使用 `__import__()`。如果需要以编程方式导入模块，最好使用 [`importlib.import_module()`](https://docs.python.org/3.7/library/importlib.html#importlib.import_module)。

与 `import` 语句不同，如果在交互模式下重复使用 `__import__` 函数加载同一模块，则会反复重载该模块，效果与使用 `importlib.reload ` 类似。但在脚本模式下则不会对模块进行重复加载。

并不会重复加载同一模块。在导入模块时，首先会搜索 [`sys.modules`](https://docs.python.org/3/library/sys.html#sys.modules)——先前导入过的模块均会被缓存在 `sys.modules` 中。

*Changed in version 3.3:* Negative values for *level* are no longer supported (which also changes the default value to 0).

参数说明：

- *name* - 被导入的模块的名称
- *globals* & *locals* - 在使用相对导入时，用于确定 *name* 模块在包中的路径。在进行相对导入时，通常会将 *globals* 设置为 `globals()`，并将 *locals* 设置为 `locals()`。在标准实现中并没有使用 *locals* 参数，仅使用 *globals* 来确定 [`import`](https://docs.python.org/3.7/reference/simple_stmts.html#import) 语句中的 *name* 模块在包中的路径。
- *fromlist* - 用于设置需要从 *name* 中导入的对象名或子模块名。
- *level* - 用于决定是使用绝对(*absolute*)导入，还是使用相对(*relative*)导入：
  - `0` (默认值) 表示仅会执行绝对导入
  - 正整数表示被搜索的父目录相对于调用 `__import__()` 的模块的目录的数量(see [**PEP 328**](https://www.python.org/dev/peps/pep-0328) for the details)：`1` 表示调用 `__import__()` 的模块所在目录，依此类推。


## 绝对导入

假设存在如下文件目录及代码：

```python
top_pkg/
	__init__.py
	pkg_a/
		__init__.py
		a_1.py
		a_2.py
	pkg_b/
		__init__.py
		b_1.py
		b_2.py
main.py -> import top_pkg
		-> import top_pkg.pkg_a
    	-> from top_pkg.pkg_b import b_1,b_2
```

`main.py` 中的 `import top_pkg` 语句经编译后的字节码类似于以下代码：

```python
top_pkg = __import__('top_pkg', globals(), locals(), [], 0)
```

`main.py` 中的 `import top_pkg.pkg_a` 语句类似于以下代码：

```python
top_pkg = __import__('top_pkg.pkg_a', globals(), locals(), [], 0)
```

Note: 此时 `__import__` 依然会返回顶层模块 `top_pkg`，`pkg_a` 将被绑定到 `top_pkg`。如果在 *fromlist* 给出了 `'pkg_a'` ，则会返回 `top_pkg.pkg_a`，如：

```python
top_pkg = __import__('top_pkg.pkg_a', globals(), locals(), ['pkg_a'], 0)
print(pkg_a)
#Out: <module 'top_pkg.pkg_a' from '~\\pkg\\top_pkg\\pkg_a\\__init__.py'> 
```

`main.py` 中的代码 `from top_pkg.pkg_b import b_1,b_2` 经编译后的字节码类似于以下代码：

```python
_temp = __import__('top_pkg.pkg_b', globals(), locals(), ['b_1', 'b_2'], 0)
b_1 = _temp.b_1
b_2 = _temp.b_2
```

此时，`__import__` 返回的对象是 `top_pkg.pkg_b`。

## 相对导入

假设存在如下文件目录及代码：

```python
top_pkg/
	__init__.py
	pkg_a/
		__init__.py
		a_1.py -> from . import a_2
		a_2.py
	pkg_b/
		__init__.py
		b_1.py
		b_2.py
main.py -> import top_pkg.pkg_a.a_1
```

在 `a_1.py` 中使用的相对导入语句 `from . import a_2` 与如下语句等效：

```python
# in a_1.py
# from . import a_2
a_2 = __import__('a_2', globals(), locals(), (), 1)
```

在进行相对导入时，还可通过设置 *globals* 字典中的 `__package__` (或 `__name__`)值来改变父包名(或模块自己的名称)，从而改变相对导入的路径。比如，通过将 `__package__` 设置为 `top_pkg.pkg_b` 从而实现在 `a_1.py` 中导入 `top_pkg.pkg_b.b_1.py`：

```python
# in a_1.py
b_1 = __import__('b_1', globals={'__package__': 'top_pkg.pkg_b'}, level=1)
```

tips：在进行相对导入时，如果模块存在 `__package__` 属性，那么将基于此属性进行相对导入；如果不存在此属性，才会使用模块的 `__name__` 属性来完成相对导入。

## 利用 `__import__` 实现延迟导入

```python
class LazyImport:
    def __init__(self, module_name):
        self.module_name = module_name
        self.module = None

    def __getattr__(self, name):
        if self.module is None:
            self.module = __import__(self.module_name)
        return getattr(self.module, name)


string_ = LazyImport("string")
print(string_.ascii_lowercase)
```



## importlib.import_module()

🔨 importlib.import_module(*name*, *package=None*)

If you simply want to import a module (potentially within a package) by name, use [`importlib.import_module()`](https://docs.python.org/3.7/library/importlib.html#importlib.import_module).

Import a module. The *name* argument specifies what module to import in absolute or relative terms (e.g. either `pkg.mod` or `..mod`). If the name is specified in relative terms, then the *package* argument must be set to the name of the package which is to act as the anchor for resolving the package name (e.g. `import_module('..mod', 'pkg.subpkg')`will import `pkg.mod`).

The [`import_module()`](https://docs.python.org/3.7/library/importlib.html#importlib.import_module) function acts as a simplifying wrapper around[`importlib.__import__()`](https://docs.python.org/3.7/library/importlib.html#importlib.__import__). This means all semantics of the function are derived from [`importlib.__import__()`](https://docs.python.org/3.7/library/importlib.html#importlib.__import__). The most important difference between these two functions is that [`import_module()`](https://docs.python.org/3.7/library/importlib.html#importlib.import_module) returns the specified package or module (e.g. `pkg.mod`), while [`__import__()`](https://docs.python.org/3.7/library/functions.html#__import__) returns the top-level package or module (e.g. `pkg`).

If you are dynamically importing a module that was created since the interpreter began execution (e.g., created a Python source file), you may need to call [`invalidate_caches()`](https://docs.python.org/3.7/library/importlib.html#importlib.invalidate_caches)in order for the new module to be noticed by the import system.

*Changed in version 3.3:* Parent packages are automatically imported.

