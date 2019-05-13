# BeautifulSoup
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

## 概述

[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) 是一个可以从 HTML 或 XML 文件中提取数据的 Python 库。它能够通过你喜欢的转换器实现惯用的文档导航、查找、修改文档的方式。

如需了解 Beautiful Soup 的使用方法，直接阅读官方文档即可。

相关资源:

- Home: https://www.crummy.com/software/BeautifulSoup/
- PyPI: https://pypi.org/project/beautifulsoup4/
- Docs-EN: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Docs-CN: https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

安装:

```shell
conda install beautifulsoup4
```

执行以下代码可验证是否安装成功:

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup('<p>Hello</p>', 'lxml')
print(soup.p.string) #> Hello
```

注意，安装时和导入时使用的库名称并不一定相同。比如在安装 BeautifulSoup4 时，使用的名称是 `beautifulsoup4`；而在导入时，使用的名称却是 `bs4` (路径为 `~\Anaconda3\envs\spider\Lib\site-packages\bs4`)。

Beautiful Soup 支持 Python 标准库中的 HTML [解析器](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id9)，同时还支持一些第三方的解析器(如 [lxml](http://lxml.de/))。详见:

- <https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id9>
- <https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#id49>

如需了解 CSS 选择器，可参考:

- <http://www.w3school.com.cn/css/css_selector_type.asp>

