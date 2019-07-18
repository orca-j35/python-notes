# urllib - URL handling modules
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

用于处理 URL 的模块被集中放置在标准库中的 `urllib` 包中:

- [`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) - 用于打开并读取 URL

  详见笔记﹝urllib.request - Extensible library for opening URLs.md﹞

  为了遵守标准的消息格式，通过 POST 发送的二进制数据应首先使用 [`base64`](https://pymotw.com/3/base64/index.html#module-base64) 进行编码，因此 HTTP POST 请求通常会使用 `urllib` 进行"表单编码(*form* *encoded*)"

- [`urllib.error`](https://docs.python.org/3/library/urllib.error.html#module-urllib.error) - 包含由 `urllib.request` 抛出的异常

  详见笔记﹝urllib.error - Exception classes raised by urllib.request.md﹞

- [`urllib.parse`](https://docs.python.org/3/library/urllib.parse.html#module-urllib.parse) -- 用于解析 URL，可对 URL 字符串执行拆分和重组等操作

  详见笔记﹝urllib.parse - Parse URLs into components.md﹞

- [`urllib.robotparser`](https://docs.python.org/3/library/urllib.robotparser.html#module-urllib.robotparser) - 用于解析网站提供的 `robots.txt` 文件，行为良好的爬虫会利用 `robots.txt` 来判断网站可被爬取的部分。

  详见笔记﹝urllib.robotparser - Parser for robots.txt.md﹞



