# 处理 PDF 文档
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库



目前收集到如下用于处理 PDF 的库:

- [PDFMiner](https://github.com/euske/pdfminer) - A tool for extracting information from PDF documents. Python 2 only!
  
  - GitHub: <https://github.com/euske/pdfminer>
  - PyPI: <https://pypi.org/project/pdfminer/>
  - Docs: <https://euske.github.io/pdfminer/>
  
- pdfminer.six - PDFMiner.six is a fork of PDFMiner using [six](https://pypi.org/project/six/) for Python 2+3 compatibility(待测试)

  - GitHub: <https://github.com/pdfminer/pdfminer.six>
  - PyPI: <https://pypi.org/project/pdfminer.six/>

  [pdfminer.six-i](https://pypi.org/project/pdfminer.six-i/) 好像也是由 [@pdfminer](https://github.com/pdfminer) 维护的分支，不过目前已找不到其 GitHub 仓库。(待测试)

  - PyPI: <https://pypi.org/project/pdfminer.six-i/#description>

- pdfminer3 - gwk/pdfminer3 is a Python 3.7 fork of pdfminer/pdfminer.six, which is in turn derived from euske/pdfminer. (待测试)

  - PyPI: <https://pypi.org/project/pdfminer3/>
  - GitHub: <https://github.com/gwk/pdfminer3>

- pdfminer3k - 似乎年久失修，上次在 PyPI 上的 release 的时间是 Jun 21, 2011。《Python 网络爬虫权威指南（第 2 版）》的 7.4 节有介绍这个库的使用方法。

  - PyPI: <https://pypi.org/project/pdfminer3k/>
  - GitHub: <https://github.com/jaepil/pdfminer3k>

- [PyPDF2](https://github.com/mstamy2/PyPDF2) - A library capable of splitting, merging and transforming PDF pages.
  - PyPI: <https://github.com/mstamy2/PyPDF2>
  - GitHub: <https://github.com/mstamy2/PyPDF2>
  - Home: <http://mstamy2.github.io/PyPDF2/>
  - Docs: <https://pythonhosted.org/PyPDF2/>
  - 如果你对 PyPDF2, PyPDF3, PyPDF4 之间的关系感到困惑，可以看看这里 - [State of PyPDF2 and Future Plans](https://github.com/mstamy2/PyPDF2/wiki/State-of-PyPDF2-and-Future-Plans)
  - PyPDF4 - <https://pypi.org/project/PyPDF4/>
  
- [ReportLab](https://www.reportlab.com/opensource/) - Allowing Rapid creation of rich PDF documents.

- pdfplumber - Plumb a PDF for detailed information about each text character, rectangle, and line. Plus: Table extraction and visual debugging. Works best on machine-generated, rather than scanned, PDFs. Built on [`pdfminer`](https://github.com/euske/pdfminer) and [`pdfminer.six`](https://github.com/goulu/pdfminer). 🧀

  详见笔记﹝pdfplumber.md﹞

  - GitHub: <https://github.com/jsvine/pdfplumber>

  

相关参考:

- [Python：解析PDF文本及表格——pdfminer、tabula、pdfplumber 的用法及对比](https://www.cnblogs.com/gl1573/p/10064438.html)
- [手把手教你如何用Python从PDF文件中导出数据](http://www.sohu.com/a/278505885_197042) - PDFMiner
- [python3-用 pdfminer.six 的 pdf2txt.py 工具提取pdf全部内容](https://blog.csdn.net/m0_37952030/article/details/85041434)
- [使用python pdfminer3k读取pdf](https://www.jianshu.com/p/742a28decc58)
- [深入学习python解析并读取PDF文件内容的方法](https://www.cnblogs.com/wj-1314/p/9429816.html) - PDFMiner