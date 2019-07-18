# \_\_main\_\_ - Top-level script environment
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考: [`__main__` — Top-level script environment](https://docs.python.org/3/library/__main__.html)
>
> 相关笔记:﹝将模块作为脚本执行(python -m).md﹞

`'__main__'` 是执行顶层代码的 scope 的名称。当从标准输入、脚本或交互式提示符中读取时，模块的 `__name__` 属性等于 `'__main__'`。

模块可通过检查自己的 `__name__` 属性来确认自己是否运行在 main scope 中。这使得模块在作为脚本运行(或配合 `python -m` 运行)时，可以有选择的执行模块中的代码：

```python
if __name__ == '__main__':
    # This program is being run by itself...
    # execute only if run as a script or `python -m`
    main()
else:
    # I am being imported from another module...
```

对于 package 而言，通过提供 `__main__.py` 模块可实现相同的效果——当配合 `python -m` 运行 package 时(或直接执行 package 时)，便会执行 `__mian__.py`。

示例 - 展示为 package 提供 `__main__.py` 的效果：「使用了 `-m` 选项后，[`sys.argv`](https://docs.python.org/3/library/sys.html#sys.argv) 中的第一个元素将被设置为相应模块文件的完整路径(while the module file is being located, the first element will be set to `"-m"`)，详见笔记﹝将模块作为脚本执行(python -m).md﹞」

```bash
'''
devel_main/ -> 当前目录
	__init__.py
    __main__.py
    
# code of __init__.py:
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

# code of __main__.py
import os, sys
print(f'> in {__package__}.__main__, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...\n')
else:
    print('I am being imported from another module...\n')

print(f'os.getcwd: {os.getcwd()}\n'
      f'sys.argv: {sys.argv}\n'
      f'sys.path: {sys.path}')
print('=================')
'''

# 直接执行pkg时，仅会调用__main__.py
$ python pkg
> in .__main__, and say:
This program is being run by itself...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_main
sys.argv: ['pkg']
sys.path: ['pkg', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
=================

# 将pkg当作脚本执行，会先执行__init__.py，再执行__main__.py
$ python -m pkg
> in pkg.__init__, and say:
I am being imported from another module...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_main
sys.argv: ['-m']
sys.path: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_main', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib',
'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
=================
> in pkg.__main__, and say:
This program is being run by itself...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_main
sys.argv: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_main\\pkg\\__main__.py']
sys.path: ['C:\\Users\\iwhal\\Documents\\GitHub\\python_notes\\notes\\包和模块\\devel_main', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib',
'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
=================

# 将pkg作为模块导入时，仅会执行__init__.py
$ python
Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:57:15) [MSC v.1915 64 bit (AMD64)] on win32
>>> import pkg
> in pkg.__init__, and say:
I am being imported from another module...

os.getcwd: C:\Users\iwhal\Documents\GitHub\python_notes\notes\包和模块\devel_main
sys.argv: ['']
sys.path: ['', 'C:\\Python37\\python37.zip', 'C:\\Python37\\DLLs', 'C:\\Python37\\lib', 'C:\\Python37', 'C:\\Users\\iwhal\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Python37\\lib\\site-packages']
=================
>>>
```

`''` 表示当前目录