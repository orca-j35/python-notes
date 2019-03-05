# Import-related 模块属性
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [5.4.4. Import-related module attributes](https://docs.python.org/3.7/reference/import.html?highlight=__package__#import-related-module-attributes)
> - [class importlib.machinery.ModuleSpec(name, loader, *, origin=None, loader_state=None, is_package=None)](https://docs.python.org/3.7/library/importlib.html#importlib.machinery.ModuleSpec)
> - [模块的内置方法--Python提高班](https://segmentfault.com/a/1190000000494023)
>

在加载程序(*loader*)执行模块之前，导入机器会在加载期间根据模块的规范(*spec*)在每个模块对象上填充以下属性。

## `__name__`

> 相关笔记:﹝`__main__` - Top-level script environment.md﹞

`__name__` 属性必需被设置为模块的完全限定(*fully-qualified*)名——该名称用于在导入系统中对模块进行唯一标识。

如果直接运行某个模块(`python xxx.py` 或 `python -m xxx.py`)，此时该模块的 `__name__` 属性将被设置为 `'__main__'`；如果通过 `import` 语句导入某个模块，此时其 `__name__` 属性将被设置该模块的完全限定名称。

```python
# in main.py
print(__name__) #> __main__

import os
print(os.__name__) #> os
```

因为在导入模块时，同样会执行模块中所包含的代码，这一点与独立运行模块时相同。此时，我们可利用 `__name__` 来确定模块的运行状态(独立运行，或被导入)，从而控制程序的执行方式：

```python
# save as module_using_name.py
if __name__ == '__main__':
    print('This program is being run by itself')
else:
    print('I am being imported from another module')
```

## `__loader__`

`__loader__` 属性必需被设置为导入机器(*mport* *machinery*)在加载模块时使用的加载器(*loader*)对象。该属性主要用于内省(*introspection*)，但可用于其它特定于加载器的功能。例如，获取与加载器相关联的数据。

```python
>>> print(__loader__)
<class '_frozen_importlib.BuiltinImporter'>
```

## `__package__`

必需为模块设置 `__package__` 属性，该属性值必需是一个字符串。`__package__` 的值可能会与 `__name__` 的值相同，具体情况如下：

- 当模块是包时，其 `__package__` 的值将被设置为 `__name__`。
- 当模块不是包时：
  - 顶层模块的 `__package__` 属性将被设置为空字符串(`python -m xxx`)或 `None` (`python xxx.py`)；与顶层模块同目录的其余模块的 `__package__` 属性将被设置为空字符串
  - 子模块的 `__package__` 属性将被设置为父包的名称。

在进行相对导入时，如果存在 `__package__` 属性，那么将基于此属性进行导入；如果不存在此属性，才会使用模块的 `__name__` 属性来完成相对导入。

See [**PEP 366**](https://www.python.org/dev/peps/pep-0366) for further details.This attribute is used instead of `__name__` to calculate explicit relative imports for main modules, as defined in [**PEP 366**](https://www.python.org/dev/peps/pep-0366). It is expected to have the same value as `__spec__.parent`.

Changed in version 3.6: The value of `__package__` is expected to be the same as `__spec__.parent`.

## `__spec__`

> The `__spec__` attribute must be set to the module spec that was used when importing the module. Setting `__spec__` appropriately applies equally to [modules initialized during interpreter startup](https://docs.python.org/3.7/reference/toplevel_components.html#programs). The one exception is `__main__`, where `__spec__` is [set to None in some cases](https://docs.python.org/3.7/reference/import.html?highlight=__package__#main-spec).When `__package__` is not defined, `__spec__.parent` is used as a fallback.
>
> New in version 3.4.
>
> Changed in version 3.6: `__spec__.parent` is used as a fallback when `__package__` is not defined.

`__spec__` 属性必需被设置为导入模块时使用的模块规范(*spec*)。

## `__path__`

> 相关笔记: ﹝包(package).md﹞-> 3. Packages in Multiple Directories
>
> If the module is a package (either regular or namespace), the module object’s `__path__`attribute must be set. The value must be iterable, but may be empty if `__path__` has no further significance. If `__path__` is not empty, it must produce strings when iterated over. More details on the semantics of `__path__` are given [below](https://docs.python.org/3.7/reference/import.html?highlight=__package__#package-path-rules).Non-package modules should not have a `__path__` attribute.

## `__file__`

被加载的模块的路径

```python
>>> import os
>>> os.__file__
'/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/os.pyc'
```

## `__cached__`

> `__file__` is optional. If set, this attribute’s value must be a string. The import system may opt to leave `__file__` unset if it has no semantic meaning (e.g. a module loaded from a database).
>
> If `__file__` is set, it may also be appropriate to set the `__cached__` attribute which is the path to any compiled version of the code (e.g. byte-compiled file). The file does not need to exist to set this attribute; the path can simply point to where the compiled file would exist (see [**PEP 3147**](https://www.python.org/dev/peps/pep-3147)).
>
> It is also appropriate to set `__cached__` when `__file__` is not set. However, that scenario is quite atypical. Ultimately, the loader is what makes use of `__file__` and/or `__cached__`. So if a loader can load from a cached module but otherwise does not load from a file, that atypical scenario may be appropriate.

## `__doc__`

模块的文档注释，详见笔记﹝模块(module)﹞-> 3. 模块的注释

## `__all__`

用于控制导入的内容，可用于模块或包，详见笔记：

- ﹝包(package)﹞-> 2.3 from Package import *
- [7.11. The `import` statement](https://docs.python.org/3/reference/simple_stmts.html?highlight=__all__#the-import-statement)

