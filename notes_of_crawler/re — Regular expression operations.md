# re — Regular expression operations
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`re`](https://docs.python.org/3/library/re.html#module-re) — Regular expression operations
> - [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html#regex-howto)
>
> 工具:
>
> - [在线正则表达式测试 - 开源中国](http://tool.oschina.net/regex)

Note: 在本笔记中我会使用 `Style without quotes` 来表示正则表达式(*Regular* *Expression* - RE)，同时会使用 `'Style without quotes'` 来表示被匹配的字符串。例如，可使用正则表达式 `hello` 来匹配字符串 `'hello'`。

在 [Regular Expression Objects](https://docs.python.org/3/library/re.html#re-objects) 中提供的大多数方法都可用作模块级别的函数。模块级别的函数无需预先编译正则表达式对象，同时会失掉一些微调参数。

See also: 第三方模块 [regex](https://pypi.org/project/regex/) 的 API 与标准库 `re` 模块兼容，同时还提供了一些额外的功能，对 Unicode 的支持也更加全面。

