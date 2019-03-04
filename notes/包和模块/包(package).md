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

## 1. 概述

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

### 1.1 \_\_init\_\_.py

每个包目录下都必需包含一个 `__ini__.py` 文件，该文件向 Python 表明这是一个内含模块的包，否则 Python 会将该包目录视为普通目录。`__init__.py` 中的内容可以为空，也用于执行包的初始化代码，或者设置 `__all__ ` 变量(详见后文 `from Package import *` 小节)。

另外，`__init__.py` 可被视为一个模块，其名称即是包名。如下例中，`__init__.py` 的名称便是 `mycompany`

```
- <some folder present in the sys.path>/
    - mycompany/
        - __init__.py
        - abc.py
        - xyz.py
```

### 1.2 多级目录

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

### 1.3 避免命名冲突

通过 Package 按目录对模块进行组织，可以有效避免命名冲突。

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

## 2. 包导入

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

### 2.1 import...as...

在使用 `import item.subitem.subsubitem` 这样的语法时，除了最后一个之外都必需是包；最后一项可以是模块或包，但不能是倒数第二项中的类、函数或变量。

包用户可以从包中导入单个模块，例如：

```python
import sound.effects.echo
```

上面的代码会加载指定的子模块 `echo`，但在使用该模块时必需使用完全限定名(*full* *name*)：

```python
sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)
# echofilter() 不能使用非完全限定名
```

还可使用 `as` 来重命名被导入的模块：

```python
import sound.effects.echo as echo_
echo_.echofilter(input, output, delay=0.7, atten=4)
```

### 2.2 from...import...as...

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

### 2.3 from Package import *

使用 `from sound.effects import *` 时，表示我们希望找到包中现存的所有子模块，并将它们全部导入。然而这样做可能会花费很多时间，并且导入子模块可能会产生不必要的副作用(这些副作用只有在显式导入子模块时才会发生)。 为了避免出现上述问题，根据包是否包含 `__all__` 属性， `from sound.effects import *` 会表现出两种不同的工作方式。

#### 含 `__all__`

解决上述问题的的唯一方法是让包作者为包提供显式索引。`import` 语句遵循如下约定：如果在包的 `__init__.py` 中定义了名为 `__all__` 的列表，那么在使用 `from package import *` 语句时，只会导入 `__all__` 中列出的模块。例如，当 `sound/effects/__init__.py` 包含以下代码时：

```python
__all__ = ["echo", "surround", "reverse"]
```

此时 `from sound.effects import *` 将从 `sound` 包中导入三个指定的子模块。

```python
from sound.effects import *
print(echo)
print(surround)
print(reverse)
'''Out:
<module 'sound.effects.echo' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\echo.py'>
<module 'sound.effects.surround' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\surround.py'>
<module 'sound.effects.reverse' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\reverse.py'>
'''
```

#### 不含 `__all__`

如果包作者认为 `from Package import *` 不适用于他的包，那么包作者可选择不支持 `__all__`。如果未定义 `__all__`，那么 `from sound.effects import *` 语句并不会将 `sound.effects` 包中所有子模块导入到当前命名空间中。此时 `from sound.effects import *` 仅会导入 `sound.effects` 包中定义的名称。也就是说会运行 `sound.effects` 包中 `__init__.py` 内的初始化代码，并导入其中定义的所有名称——这些名称包括通过 `__init__.py` 定义的全部名称，及显式加载的子模块。示例：

```python
# 当 sound/effects/__init__.py 包含以下代码：
from sound.effects import echo
effects_say = 'say: effects_ package'
print('run effects.__init__')
```

导入效果：

```python
from sound.effects import *
print(effects_say)
print(echo)
'''Out:
run effects.__init__
say: effects_ package
<module 'sound.effects.echo' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\echo.py'>
'''
```

同时还会加载由前面的 [`import`](https://docs.python.org/3.7/reference/simple_stmts.html#import) 语句显式导入的 `sound.effects` 包中的子模块。例如(`sound/effects/__init__.py` 中不包含任何代码)：

```python
import sound.effects.echo
import sound.effects.surround
from sound.effects import *
print(echo)
print(surround)
'''Out:
<module 'sound.effects.echo' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\echo.py'>
<module 'sound.effects.surround' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\surround.py'>
'''
```

从上面这个示例中可以看到 `echo` 模块和 `surround` 模块被导入到了当前命名空间中。因为它们是 `sound.effects` 包的子模块，且由前面的 `import` 语句显式导入，因此在执行 `from sound.effects import *` 后，这两个模块会被导入到当前命名空间中(在一定义 `__all__` 的情况下同样有效)。

另外，还会加载 `sound/__init__.py` 中显式导入的 `sound.effects` 包中的子模块。例如：

```python
# 当 sound/__init__.py 包含以下代码：
from sound.effects import reverse
import sound.effects.surround
print('run sound.__init__')

# 当 sound/effects/__init__.py 包含以下代码：
from sound.effects import echo
effects_say = 'say: effects_ package'
print('run effects.__init__')
```

导入效果：

```python
from sound.effects import *
print(effects_say)
print(echo)
print(reverse)
print(surround)
# print(sound.effects) 抛出异常，不可调用
'''Out:
run effects.__init__
run sound.__init__
say: effects_ package
<module 'sound.effects.echo' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\echo.py'>
<module 'sound.effects.reverse' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\reverse.py'>
<module 'sound.effects.surround' from 'c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound\\effects\\surround.py'>
'''
```

### 2.4 包内引用(相对导入)

使用包内引用(*Intra*-*package* *References*)的前提是存在包结构，也就是说每个包目录必需包含 `__init__.py`。

如果在包中使用了子包结构(比如下面的 `sound` 包)，首先可以使用绝对(*absolute*)导入来引用兄弟包中的子模块。例如，当模块 `sound.filters.vocoder` 需要 `sound.effects` 包中的 `echo` 模块时，可使用 `from sound.effects import echo`。

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
              surround.py # <--
              reverse.py
              ...
      filters/   # Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
```

其次，还可以使用 `from module import name` 形式的导入语句来完成相对(*relative*)导入。在相对导入中会使用前导点号 `.` 来表示当前包和父包。例如，在 `surround` 模块中，我们可以使用如下语句：

```python
from . import echo # 在当前包中导入指定模块
from .. import formats # 在父包中导入指定子包
from ..filters import equalizer # 在父包中的子包中导入指定模块
```

注意，相对导入基于当前模块名。由于主模块的名称始终是 `"__main__"` ，因此 Python 应用程序的主模块(入口模块)必需始终使用绝对导入。另外，与主模块同目录的其它模块同样不能使用相对导入，因为主模块目录下的模块的 `__package__` 值均为 `''`，也就是说没有已知父包——即使在主目录下包含 `__init__.py` 也不行。例如：

```python
# 目录结构
pkg/ # 当前目录
	main.py # 主模块(入口)，代码如下
    	import MA
		print(f"in {__name__},and {__package__ if __package__ != '' else 'null str'}")
    MA.py # 代码如下
        import MB
        print(f"in {__name__},and {__package__ if __package__ != '' else 'null str'}")
    MB.py # 代码如下
		print(f"in {__name__},and {__package__ if __package__ != '' else 'null str'}")
    __init__.py # 代码如下
    	print(f"in {__name__},and {__package__ if __package__ != '' else 'null str'}")
```

执行效果:

```bash
$ python main.py
in MB,and null str
in MA,and null str
in __main__,and None

$ python -m main
in MB,and null str
in MA,and null str
in __main__,and null str
```

如果将 `MA.py` 中的代码改为

```python
from . import MB
print(f"in {__name__},and {__package__ if __package__ != '' else 'null str'}")
```

执行效果如下：

```
$ python main.py
Traceback (most recent call last):
--snip--
ImportError: attempted relative import with no known parent package
    
$ python -m main
Traceback (most recent call last):
--snip--
ImportError: attempted relative import with no known parent package
```

## 3. Packages in Multiple Directories

> 相关内容:
>
> - 笔记﹝Import-related 模块属性﹞
> - [5.4.5. module.`__path__`](https://docs.python.org/3/reference/import.html#module-path)

包支持一个名为 [`__path__`](https://docs.python.org/3.7/reference/import.html#__path__) 的特殊属性。在包的 `__init__.py` 中的代码被执行前，包的 `__path__` 属性将被初始化为一个包含 `__init__.py` 目录名的列表。例如： 

```python
# 目录结构
pkg/ # 当前目录
	main.py # 主模块(入口)，代码如下
    	import sound.effects
    sound/ 
        __init__.py
        	print(f'{__name__}:{__path__}')
        effects/
        	__init__.py
            	print(f'{__name__}:{__path__}')
```

执行效果:

```
$ python main.py
sound:['c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\pkg\\sound']
sound.effects:['c:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模
块\\pkg\\sound\\effects']
```

`__path__` 变量可以被修改，修改此变量后将会影响之后对包中包含的模块和子包的搜索。

该属性可用于扩展包中的模块集，不过该功能并不常用。

## 4. 术语

参考: [Glossary](https://docs.python.org/3.7/glossary.html#glossary)

### package

A Python [module](https://docs.python.org/3.7/glossary.html#term-module) which can contain submodules or recursively, subpackages. Technically, a package is a Python module with an `__path__` attribute.

See also [regular package](https://docs.python.org/3.7/glossary.html#term-regular-package) and [namespace package](https://docs.python.org/3.7/glossary.html#term-namespace-package).