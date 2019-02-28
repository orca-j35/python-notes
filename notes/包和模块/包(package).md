# 包(package)
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [6. Modules - The Python Tutorial](https://docs.python.org/3.7/tutorial/modules.html#modules)
>   - [6. 模块](https://learnku.com/docs/tutorial/3.7.0/modules/3508#c776ac) | [6. 模块](http://www.pythondoc.com/pythontutorial3/modules.html)
> - [模块 - 廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014318447437605e90206e261744c08630a836851f5183000)
> - byte of python - 模块
>
> 扩展阅读:
>
> - [5.2. Packages](https://docs.python.org/3/reference/import.html#packages)

包作为放置模块的文件夹，是按目录组织来模块的方法，使用 "dotted module names"(`.module_name`)来构造 Python 模块所属命名空间。比如，模块名 `A.B` 用于指定包 `A` 中的子模块 `B`。

在不同的包中可使用相同的模块名，从而避免模块名冲突。但是在命名模块时不能和标准库中模块名发生冲突，否则将无法正常导入标准库中的模块。

示例 - 设计了一个用于处理声音文件和声音数据的模块包：

```
sound/                  # Top-level package
      __init__.py       # Initialize the sound package
      formats/   # Subpackage for file format conversions
              __init__.py
              wavread.py
              wavwrite.py
              aiffread.py
              aiffwrite.py
              auread.py
              auwrite.py
              ...
      effects/  # Subpackage for sound effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/   # Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
```



## \_\_init\_\_.py

每个包目录下都必需包含一个 `__ini__.py` 文件，该文件向 Python 表明这是一个内含模块的包，否则 Python 会将该包目录视为普通目录。`__init__.py` 中的内容可以为空，也用于执行包的初始化代码，或者设置 `__all__ ` 变量(详见后文 `from Package import *` 小节)。

另外，`__init__.py` 可被视为一个模块，其名称即是包名。如下例中，`__init__.py` 的名称便是 `mycompany`

```
- <some folder present in the sys.path>/
    - mycompany/
        - __init__.py
        - abc.py
        - xyz.py
```

### 多级目录

Packages 可以拥有多级目录结构。

```
- <some folder present in the sys.path>/
    - mycompany/
        - __init__.py
        - abc.py
        - xyz.py
        - web/
        	- __init__.py
        	www.py
        	utils.py
```

两个 `utils.py` 的模块名分别是 `mycompany.utils` 和 `mycompany.web.utils` 。
`mycompany.web` 也是一个模块，该模块对应 `mycompany.web.__init__.py` 文件。

### 避免命名冲突

通过 Package 按目录对模块进行组织。
可以有效避免命名冲突。

```
- <some folder present in the sys.path>/
    - mycompany/
        - __init__.py
        - abc.py
        - xyz.py
```

当 `abc.py` 和 `xyz.py` 与其它模块名冲突时，可将这两个模块放入包中。
只要顶层包 `mycompany` 保证唯一性，即可有效避免模块冲突。
注意：此时模块的名称发生了改变：`abc.py` 变为 `mycompany.abc.py` 。

## 包导入

在导入包时，Python 会搜索 `sys.path` 中的目录，找到包中的子目录。

示例 - 设计了一个用于处理声音文件和声音数据的模块包：

```
sound/                  # Top-level package
      __init__.py       # Initialize the sound package
      formats/   # Subpackage for file format conversions
              __init__.py
              wavread.py
              wavwrite.py
              aiffread.py
              aiffwrite.py
              auread.py
              auwrite.py
              ...
      effects/  # Subpackage for sound effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/   # Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
```

### import...as...

包用户可以从包中导入单个模块，例如：

```python
import sound.effects.echo
```

上面的代码会加载指定的子模块 `echo`，但在使用该模块时必需使用完全限定名(*full* *name*)：

```python
sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)
# echofilter() 不能使用非完全限定名
```

在使用 `import item.subitem.subsubitem` 这样的语法时，除了最后一个之外都必需是包；最后一项可以是模块或包，但不能是倒数第二项中的类、函数或变量。

还可使用 `as` 来重命名被导入的模块：

```python
import sound.effects.echo as echo_
echo_.echofilter(input, output, delay=0.7, atten=4)
```

### from...import...as...

使用 `from package import item` 时，`item` 可以是包的子模块(或子包)，也可以是包中定义的其它名称(如函数、类、变量)。`import` 语句会先测试在包中是否定义了指定的 `item`；如果在包中没有定义 `item` ，则会假定 `item` 是一个模块并尝试加载它。假如完全找不到 `item`，则会抛出 [`ImportError`](https://docs.python.org/3.7/library/exceptions.html#ImportError) 异常。

#### 加载子模块

另一种导入子模块的的方法是：

```python
from sound.effects import echo
```

上面的代码会加载指定的子模块 `echo`，并且可以不使用前缀包：

```python
echo.echofilter(input, output, delay=0.7, atten=4)
```

可使用 `as` 来重命名被导入的模块：

```python
from sound.effects import echo as echo_
echo_.echofilter(input, output, delay=0.7, atten=4)
```

#### 加载子模块中属性

还可以直接加载所需的函数或变量：

```python
from sound.effects.echo import echofilter
```

上面的代码会加载子模块 `echo` 中的 `echofilter()` 函数：

```python
echofilter(input, output, delay=0.7, atten=4)
```

可使用 `as` 来重命名被导入的函数或变量：

```python
from sound.effects.echo import echofilter as echofilter_
echofilter_(input, output, delay=0.7, atten=4)
```

### from Package import *







现在来仔细研究下 `from sound.effects import *` 语句。
理想情况下，我们希望 `sound.effects` 被以某种方式发送到文件系统，然后查找 Package 中存在子模块，并将其全部导入。这可能需要很长的时间，并且当子模块被明确导入时，这些子模块可能会产生不必要的副作用。

对于包作者而言，唯一的解决方案就是提供明确的包索引。
 [`import`](https://docs.python.org/3/reference/simple_stmts.html#import) 语句遵循如下约定：如果某个包的 `__init__.py` 中定义了名为 `__all__` 的列表。当遇到 `from packageimport *` 时，则将该列表视为应导入的模块名称的列表。当新版本的包被发布时，包作者应该保存对此表的更新。如果认为 importing * from package 没什么用处的话，包作者也可不支持该列表。
示例： `sound/effects/__init__.py`  若包含如下代码：

```
__all__ = ["echo", "surround", "reverse"]
```

这表示 `from sound.effects import *` 将会导入 `sound` 包的三个子模块。

如果没有定义 `__all__` ， `from sound.effects import *` 并不会将 `sound.effects` 包中所有子模块导入到当前命名空间中；该代码只能保证 `sound.effects` 包被导入(possibly running any initialization code in `__init__.py`)，然后导入包中定义的任何名称。这包括通过 `__init__.py` 定义的任何名称 (and submodules explicitly明确 loaded)。还同时包含任何之前通过  [`import`](https://docs.python.org/3/reference/simple_stmts.html#import) 语句明确加载的 package 的子模块。

考虑如下代码：

```
import sound.effects.echo
import sound.effects.surround
from sound.effects import *
```

In this example, the `echo` and `surround` modules are imported in the current namespace because they are defined in the `sound.effects` package when the `from...import` statement is executed. (This also works when `__all__` is defined.)

Although certain modules are designed to export only names that follow certain patterns when you use `import *`, it is still considered bad practice in production code.

Remember, there is nothing wrong with using `from Package import specific_submodule`! In fact, this is the recommended notation unless the importing module needs to use submodules with the same name from different packages.

#### Intra-package References

When packages are structured into subpackages (as with the `sound` package in the example), you can use absolute imports to refer to submodules of siblings packages. For example, if the module `sound.filters.vocoder` needs to use the `echo` module in the `sound.effects` package, it can use `from sound.effects import echo`.

You can also write relative相对 imports, with the `from module import name` form of import statement. These imports use leading dots to indicate the current and parent packages involved in the relative import. From the `surround` module for example, you might use:

```
from . import echo #从当前模块所在文件夹导入echo
from .. import formats
from ..filters import equalizer
```

Note that relative imports are based on the name of the current module. Since the name of the main module is always `"__main__"`, modules intended for use as the main module of a Python application must always use absolute imports.

1. 文件夹中必须有 `__init__.py` 文件，该文件可以为空，但必须存在该文件。

2. 如果模块的某个文件夹中的 `.py` 文件使用了相对导入，那么该文件夹中的 `.py` 文件都不可作为顶层模块来执行（即不能作为主函数的入口）。否则相对导入不能正常运行。因为顶层模块不在被视作 package，所以解释器无法正确解释相对路径。使用 `-m` 也不行

    

### Packages in Multiple Directories

Packages support one more special attribute, [`__path__`](https://docs.python.org/3/reference/import.html#__path__). 
This is initialized to be a list containing the name of the directory holding the package’s `__init__.py` before the code in that file is executed. 在该文件中的代码被执行之前，它被初始化为包含保存包的 `__init__.py` 的目录的名称的列表。 
This variable can be modified; doing so affects future searches for modules and subpackages contained in the package.

While this feature is not often needed, it can be used to extend the set of modules found in a package.

```
>>> import learn_py

>>> learn_py.__path__
['C:\\Users\\iwhal\\Documents\\learn_py']
```



## 术语

参考: [Glossary](https://docs.python.org/3.7/glossary.html#glossary)

### package

A Python [module](https://docs.python.org/3.7/glossary.html#term-module) which can contain submodules or recursively, subpackages. Technically, a package is a Python module with an `__path__` attribute.

See also [regular package](https://docs.python.org/3.7/glossary.html#term-regular-package) and [namespace package](https://docs.python.org/3.7/glossary.html#term-namespace-package).