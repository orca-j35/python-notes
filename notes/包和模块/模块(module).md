# 模块(module)
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考: 
>
> - [6. Modules - The Python Tutorial](https://docs.python.org/3.7/tutorial/modules.html#modules)
>   - [6. 模块](https://learnku.com/docs/tutorial/3.7.0/modules/3508#c776ac) | [6. 模块](http://www.pythondoc.com/pythontutorial3/modules.html)
> - [模块 - 廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014318447437605e90206e261744c08630a836851f5183000)
> - byte of python - 模块
> - 数据结构(python语言描述) ->  1.1.1 程序和模块

## 1. 概述

模块(*module*)是包含 Python 代码的 `.py` 文件，是代码的组织单元。模块拥有自己命名空间可以包含任意 Python 对象(如，语句、函数定义和类定义)。利用 `dir()` 函数可列出模块包含的属性名，详见笔记﹝dir.md﹞

简短的 Python 程序也称为脚本(*script*)，可以包含在单个模块之中。较为复杂的程序通常会包含一个主模块和一个或多个支持模块——主模块包含了程序执行的起点，支持模块则包含了函数定义和类定义。

模块等级的语句被用于初始化模块，会在第一次导入(*import*) 模块「或直接运行模块」时被执行，例如：

- 模块中位于函数定义和方法定义之外的语句会被执行
- 模块等级的"函数定义"和"类定义"语句会将"函数名"和"类名"导入模块的全局符号表中。

每个模块都有自己的私有"符号表"(*private* *symbol* *table*)，在模块中定义的所有函数都会将模块的"私有符号"表当作"全局符号表"使用。因此，模块的作者可以在模块内部使用全局变量，且无需担心它与某个用户的全局变量意外冲突。模块的用于可以使用 `modname.itemname` 来访问模块的全局变量。

示例 - module_1.py 和 module_2.py 位于同一目录下：

```python
# code of module_1.py
import module_2
print("in 模块1")
class ClassDef(object):
    print("模块1：类定义")
    def meth_def(args):
        print("模块1：方法定义")
def fun_def(args):
    print("模块1：函数定义")
print(dir())
print(dir(module_2))
print('out 模块1')

#  code of module_2.py
print("in 模块2")
class ClassDef(object):
    print("模块2：类定义")
    def meth_def(args):
        print("模块2：方法定义")
def fun_def(args):
    print("模块2：函数定义")
print('out 模块2')
```

运行 `module_1.py` 输出如下：

```python
in 模块2
模块2：类定义
out 模块2
in 模块1
模块1：类定义
['ClassDef', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'fun_def', 'module_2']
['ClassDef', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'fun_def']
out 模块1
```

通过上面这个示例，可以观察到在不同的模块中可以使用相同的函数名和变量名，但尽量不要与 [内置函数](https://docs.python.org/3/library/functions.html#built-in-functions) 冲突。

## 2. 模块的属性

模块中的属性可分为以下三类：

- 公共属性(*public*) - 以 `xxx` 命名，不以 `_` 开头
- 私有属性(*private*) - 以 `_xxx` 或 `__xxx` 命名
- 特殊属性 - 以 `__xxx__` 命名

以上三类属性均可通过 `module.attribute_name` 直接访问，Python 并不能限制对私有属性的访问，但我们"不应该"访问这些属性。模块和类不同，类会自动修改 `__xxx` 变量的名称，但是模块不会。

示例 - 私有属性的使用：

```python
def _private_1(name): # 私有属性
    return 'Hello, %s' % name

def _private_2(name): # 私有属性
    return 'Hi, %s' % name

def greeting(name): # 公共属性
    if len(name) > 3:
        return _private_1(name)
    else:
        return _private_2(name)
```

`greeting()` 是公共函数，其内部逻辑被两个私有函数进行了隐藏。在调用 `greeting()` 函数时，不用关心模块内部私有函数的实现细节。这是一种非常有用的代码封装和抽象的方法：将外部不需要引用的函数全部定义成私有，只有外部需要引用的函数才定义为公共。

## 3. 模块的注释

示例 - 展示模块注释的使用方法：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''A test module.'''

__author__ = 'orca-j35'
__version__ = '0.1'

import sys

def test():
    args = sys.argv
    if len(args)==1:
        print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

if __name__=='__main__':
    test()
```

- 第 1 行注释可以让该脚本直接在 Unix/Linux/Mac 上运行
- 第 2 行注释表示该脚本使用标准 UTF-8 编码
- 第4行是文档字符串，详见笔记﹝文档字符串.md﹞
- 第6行使用 `__author__` 变量表示作者名
- 第7行使用 `__version__` 变量表示版本

通过模块的 `__doc__` 属性或 `help()` 函数，可访问访问模块的文档注释。

## 4. 导入模块

> 相关笔记：
>
> - ﹝包(package).md﹞-> 2. 包导入
>
> 扩展阅读：
>
> - [PEP 328 -- Imports: Multi-Line and Absolute/Relative](https://www.python.org/dev/peps/pep-0328/)
> - [PEP 366 -- Main module explicit relative imports](https://www.python.org/dev/peps/pep-0366/)
> - [7.11. The `import` statement](https://docs.python.org/3.7/reference/simple_stmts.html#the-import-statement)

### import...as...

此方法用于在当前模块中导入另一个模块，被导入的模块名会被添加到当前模块的全局符号表中，但并不会将被导入模块中的属性添加到当前模块的全局符号表中。

例如，在 `A` 模块中导入 `B` 模块后，`B` 模块的名称会被放置到 `A` 模块的全局符号表中：

```python
>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__']
>>> import sys
>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'sys']
```

如果某函数很常用，还可为其分配本地名称：

```python
>>> path_=sys.path
>>> dir()
['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'path_', 'sys']
```

还可使用 `as` 来重命名被导入的模块：

```python
import sys as sys_rename
sys_rename.path
```

### from...import...as...

此方法用于将另一个模块中的特定属性导入当前模块的符号表中，但不会向当前模块的符号表中添加被导入模块的名称。

警告：应该尽量避免使用 `from..import` 语句，而是使用 `import` 语句。这样可避免命名冲突，并且也更易阅读。

```python
>>> from math import sqrt
>>> print("Square root of 16 is", sqrt(16))
>>> math
Traceback (most recent call last):
  File "<pyshell#2>", line 1, in <module>
    math
NameError: name 'math' is not defined
```

还可使用 `as` 来重命名被导入的属性：

```python
>>> from math import sqrt as sqr
>>> sqr(16)
4.0
```

### from...import *

此方法会将另一个模块中的所有属性(以 `_` 开头的属性除外)导入当前模块的符号表中。

在大多数情况下，不要使用该方法。因为它可能会向解释器中引入了一些使用者未知的名称，这可能会与当前符号表中已定义的名称相冲突。另外，该方法还会影响程序的可读性。

## 5. 模块重载

> 参考:
>
> - [【Python学习笔记】1. import reload 以及__import__注意点](https://www.cnblogs.com/MaggieXiang/archive/2013/06/05/3118156.html)
> - [5.3.1. The module cache](https://docs.python.org/3/reference/import.html#the-module-cache)

出于效率的原因，每个模块在每个解释器会话中只会导入一次。因此，重复使用 `import` 语句并不会重复加载同一模块。在导入模块时，首先会搜索 [`sys.modules`](https://docs.python.org/3/library/sys.html#sys.modules)——先前导入过的模块均会被缓存在 `sys.modules` 中。如果在 `sys.modules` 中已包含被导入的模块，便会直接使用该模块，不会再次进行导入。例如：

```python
# 以下两个脚本在同一个目录中
main.py -> import test
		-> import os
		-> print(id(os),'in main.py')
test.py -> import os
		-> print(id(os),'in test.py')
```

执行效果：

```python
$ python main.py
2103924143912 in test.py
2103924143912 in main.py
```

因此，在修改模块后，必须重新启动解释器，或对模块进行重载:

```python
import importlib
importlib.reload(modulename)
# 必需先加载模块，然后才能使用reload，如
import os
importlib.reload(os)
```

`reload` 会对已加载的模块进行重载，但是原模块已产生的实例会继续使用旧模块，新产生的实例会使用重载后的模块。模块经 `reload` 重载后，原有内存地址不会发生改变。

`reload` 不支持对通过 `from...import...` 语句导入的模块进行重载。

## 6. 执行模块

可通过以下两种方式来执行 Python 模块：

- ⌨ `python <module-name>.py [arg] ... `
- ⌨ `python -m <module-name> [arg] ... `

在执行模块时，以上两种方法均会将 `__name__` 设置为 `"__main_"`，详见笔记﹝将模块作为脚本执行(python -m).md﹞

## 7. 编译 python 文件

> 对旧版本的 Python 而言，通常会在 `.py` 文件所在目录下创建相应的 `.pyc` 文件。
>
> 如果 Python 没有相应目录的写入权限，则无法创建 `.pyc` 文件。
>
> 编译得到的 `.pyc` 文件中存放的是字节码(*bytecode*)，而非本地计算机的机器语言。在执行 `.pyc` 文件时，仍然需要将字节码翻译为计算机的本地语言。在执行 `.py` 文件时，Python 会先将源代码转换为字节码，然后再将字节码翻译为计算机的本地语言。

为了提高模块的加载速度，Python 会在 `__pycache__` 目录下以 `module.version.pyc` 名字缓存每个模块编译后的版本，这里的 version 编码了文件编译后的格式；version 中通常包含了 Python 的版本号。例如，在 CPython 发布 3.3 中 `spam.py` 的编译版本将被缓存为 `__pycache__/spam.cpython-33.pyc`。这种命名约定允许由不同发布和不同版本的 Python 编译的模块同时存在。

Python 针对编译版本，特别检查源的修改日期，以查看它是否过期，并需要重新编译。这是一个完全自动的过程。此外，编译的模块是与平台无关的，因此可以在具有不同架构的系统之间共享相同的库。

Python 在两种情况下不检查缓存。首先，对于直接从命令行加载的模块，Python 总是重新编译并且不会储存结果。第二，如果没有源模块，它不检查缓存。要支持没有源文件（仅编译版）的分发，编译的模块必须位于源目录中，并且不能有源模块。

高级技巧:

- 您可以在 Python 命令中使用 [`-O`](../using/cmdline.html#cmdoption-O) or [`-OO`](../using/cmdline.html#cmdoption-OO) 开关来减小已编译模块的大小。  `-O` 开关删除 `assert` 语句， `-OO` 开关删除 `assert` 语句和 `__doc__` 字符串。由于一些程序可能依赖于这些变量的可用性，你应该只在确定无误的场合使用这一选项。“优化” 过的模块有一个 `opt-` 标签，并且通常较小。未来的版本可能会改变优化的效果。
- 程序从 `.pyc` 文件读取时不会比从 `.py` 文件读取时运行的更快；关于 `.pyc` 文件的唯一的一点是它们的加载速度。
- 模块 [`compileall`](../library/compileall.html#module-compileall) 可以为目录中的所有模块创建 `.pyc` 文件。
- 在 [**PEP 3147**](https://www.python.org/dev/peps/pep-3147)中有关于这个过程的更多细节，包括决策的流程图。

## 8. 标准模块

Python 还附带一个由标准模块构成的库，并该库撰写了独立文档(Python Library Reference)。部分标准模块被内置在解释器中，这些模块提供了对那些不属于语言核心但仍属于内置操作的访问方法，其目的在于提高效率或提供对操作系统的原生访问(如系统调用)。例如，[`winreg`](https://docs.python.org/3.7/library/winreg.html#module-winreg) 模块尽在 Windows 系统中提供。

另外，需要注意一下 [`sys`](https://docs.python.org/3.7/library/sys.html#module-sys) 模块，它被内置在所有 Python 解释器中。`sys` 中的变量 `sys.ps1` 和 `sys.ps2` 被用于定义主提示符和辅助提示符(这两个变量只在解释器的交互模式下有意义)：

```python
>>> import sys
>>> sys.ps1
'>>> '
>>> sys.ps2
'... '
>>> sys.ps1 = 'C> '
C> print('Yuck!')
Yuck!
C>
```

变量 `sys.path` 用于确定解释器的模块搜索路径，详见笔记﹝模块搜索路径.md﹞

## 7. 为模块构建"发布"

在 PyPI 上共享自己编写的模块时，需要为模块准备一个“发布”。
“发布 distribution” 是指一个文件集合，该集合会有效组织其中的文件，以允许构建/打包/发布模块。构建好 distribution 后，便可把相应的模块安装到本地 Py 副本中，也可以把模块上传到 PyPI。

利用发布工具允许将模块转换为可共享的包。

PyPI (Python Package Index) : Python 包索引是第三方 Python 模块的储存库

### 构建“发布”

- 首先将模块放入相应的文件夹中；

- 再在该文件夹中创建 `setup.py` 文件，此文件包含有关发布的元数据 metadata ，用于构建、安装和上传打包的 “发布”。

  ```
  from distutils.core import setup
  setup(
      name='nester',
      version='1.0.0',
      py_modules=['nester'],
      author='hfpython',
      author_email='zxcvb@xc.com',
      url='http://www.dad.com',
      description='A simple printer of nested lists'
  )
  ```

  此时，文件夹中只有两个文件

  ```
  - nester/
      - nester.py #源代码
      - setup.py #元数据
  ```

- 构建 ’发布‘，在命令行中输入 `python setup.py sdist` ，在mac中可能是 `python3 setup.py sdist ` 。

  ```
  C:\Users\iwhal\Desktop\learn_python\nester>python setup.py sdist
  running sdist
  running check
  warning: sdist: manifest template 'MANIFEST.in' does not exist (using default file list)
  
  warning: sdist: standard file not found: should have one of README, README.txt
  
  writing manifest file 'MANIFEST'
  creating nester-1.0.0
  making hard links in nester-1.0.0...
  hard linking nester.py -> nester-1.0.0
  hard linking setup.py -> nester-1.0.0
  creating dist
  Creating tar archive
  removing 'nester-1.0.0' (and everything under it)
  ```

  此时会增加相应文件：

  ```
  - nester/
      - nester.py #源代码
      - setup.py #元数据
      - MANIFEST #‘发布’中的文件列表
      - dist/
      	- nester-1.0.0.tar.gz #distribution package
  ```

### 将“发布”安装到本地

将’发布‘安装到本地的 Py 副本中： `python setup.py install` ，在mac中可能是 `sudo python3 setup.py install ` 

```
​```
C:\Users\iwhal\Desktop\learn_python\nester>python setup.py install
running install
running build
running build_py
creating build
creating build\lib
copying nester.py -> build\lib
running install_lib
copying build\lib\nester.py -> C:\Python361\Lib\site-packages
byte-compiling C:\Python361\Lib\site-packages\nester.py to nester.cpython-36.pyc
running install_egg_info
Writing C:\Python361\Lib\site-packages\nester-1.0.0-py3.6.egg-info
​```
```

此时会增加更多文件：

```
​```
- nester/
    - nester.py #源代码
    - setup.py #元数据
    - MANIFEST #‘发布’中的文件列表
    - dist/
    	- nester-1.0.0.tar.gz #distribution package
    - build/
    	- lib/
    		nester.py #源代码
​```
```

完成以上步骤后，便成功将模块安装到了本地 Py 副本中，此时只需要 `import nester` 便可正常使用该模块了。  

### 将“发布”上传到PyPI

在命令行中输入 `python setup.py register` ，登陆PyPI。
登陆完成后，输入 `python setup.py sdlist upload` ，上传发布。
注意，上传后得到`Server response (200): OK` ，才表示上传成功。

## 8. 术语

> 参考: [Glossary](https://docs.python.org/3.7/glossary.html#glossary)

### module

An object that serves as an organizational unit of Python code. Modules have a namespace containing arbitrary Python objects. Modules are loaded into Python by the process of [importing](https://docs.python.org/3.7/glossary.html#term-importing).

See also [package](https://docs.python.org/3.7/glossary.html#term-package).

### package

A Python [module](https://docs.python.org/3.7/glossary.html#term-module) which can contain submodules or recursively, subpackages. Technically, a package is a Python module with an `__path__` attribute.

See also [regular package](https://docs.python.org/3.7/glossary.html#term-regular-package) and [namespace package](https://docs.python.org/3.7/glossary.html#term-namespace-package).

### importing

The process by which Python code in one module is made available to Python code in another module.

