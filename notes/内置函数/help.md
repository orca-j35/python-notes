# help

🔨 help([*object*])

调用内置帮助系统，用于交互模式。

如果未给出参数，则会在解释器控制台中启动交互式帮助系统。

```python
>>> help()

Welcome to Python 3.7's help utility!

If this is your first time using Python, you should definitely check out
the tutorial on the Internet at https://docs.python.org/3.7/tutorial/.

Enter the name of any module, keyword, or topic to get help on writing
Python programs and using Python modules.  To quit this help utility and
return to the interpreter, just type "quit".

To get a list of available modules, keywords, symbols, or topics, type
"modules", "keywords", "symbols", or "topics".  Each module also comes
with a one-line summary of what it does; to list the modules whose name
or summary contain a given string such as "spam", type "modules spam".

help> oct
Help on built-in function oct in module builtins:

oct(number, /)
    Return the octal representation of an integer.
    
    >>> oct(342391)
    '0o1234567'

help> quit # 退出内置帮助系统

You are now leaving help and returning to the Python interpreter.
If you want to ask for help on a particular object directly from the
interpreter, you can type "help(object)".  Executing "help('string')"
has the same effect as typing a particular string at the help> prompt.
```

如果参数是字符串，则查找该字符串对应的模块、函数、类、方法、关键字或文档主题的名称，并在控制台中打印相应的帮助页面。

如果将其它任何类型的对象用作参数，则会生成该对象的帮助页面。

该函数通过 [`site`](https://docs.python.org/3.7/library/site.html#module-site) 模块添加到内置命名空间。

**Changed in version 3.4**: Changes to [`pydoc`](https://docs.python.org/3.7/library/pydoc.html#module-pydoc) and [`inspect`](https://docs.python.org/3.7/library/inspect.html#module-inspect) mean that the reported signatures for callables are now more comprehensive and consistent.