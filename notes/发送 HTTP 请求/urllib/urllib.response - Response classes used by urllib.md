# urllib.response - Response classes used by urllib
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

[`urllib.response`](https://docs.python.org/3/library/urllib.request.html#module-urllib.response) — Response classes used by urllib

The [`urllib.response`](https://docs.python.org/3/library/urllib.request.html#module-urllib.response) module defines functions and classes which define a minimal file like interface, including `read()` and `readline()`. The typical response object is an addinfourl instance, which defines an `info()` method and that returns headers and a `geturl()` method that returns the url. Functions defined by this module are used internally by the[`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) module.