# 查看Python的版本
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

可使用终端命令来查看 Python 的版本信息:

```shell
(base) C:\WINDOWS\system32>python -VV
Python 3.7.1 (default, Dec 10 2018, 22:54:23) [MSC v.1915 64 bit (AMD64)]

(base) C:\WINDOWS\system32>python -V
Python 3.7.1

(base) C:\WINDOWS\system32>python --version
Python 3.7.1
```

还可通过 `sys` 模块来查看 Python 的版本信息:

```python
import sys
sys.version
#> '3.7.2 (default, Feb 21 2019, 17:35:59) [MSC v.1915 64 bit (AMD64)]'
sys.version_info
#> sys.version_info(major=3, minor=7, micro=2, releaselevel='final', serial=0)
```

查看 pip 版本信息:

```shell
$ pip --version
```

