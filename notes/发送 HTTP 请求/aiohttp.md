# aiohttp
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

requests 属于阻塞式 HTTP 请求库，当我们通过 requests 发出请求后，只有等服务器响应之后才会继续执行后续代码。

aiohttp 属于异步 HTTP Client/Server，Python3.5 中引入了 `async/await` 关键字，使得回调的写法更加直观和人性化。aiohttp 的异步操作借助于 `async/await` 关键字，使得写法变得更加简洁，架构更加清晰。

相关资源:

- Home: https://aiohttp.readthedocs.io
- PyPI: https://pypi.org/project/aiohttp/
- GitHub: https://github.com/aio-libs/aiohttp
- Docs-EN: https://aiohttp.readthedocs.io/en/stable/

aiohttp 官方还推荐 [cchardet](https://aiohttp.readthedocs.io/en/stable/glossary.html#term-cchardet)(字符编码检测库)和 [aiodns](https://aiohttp.readthedocs.io/en/stable/glossary.html#term-aiodns)(异步 DNS 解析库):

- cchardet: cChardet is high speed universal character encoding detector - binding to charsetdetect.

  https://pypi.org/project/cchardet/

  https://github.com/PyYoshi/cChardet

- chardet: The Universal Character Encoding Detector

  https://pypi.org/project/chardet/

- aiodns: DNS resolver for asyncio.

  https://pypi.org/project/aiodns

  https://github.com/saghul/aiodns

安装:

```shell
conda install aiohttp
conda install -c conda-forge cchardet
# conda和anaconda.org中都没有aiodns包
```

如果需要用到 DNS 异步解析的话，还可以考虑 [Pycares](https://pypi.org/project/pycares/)。