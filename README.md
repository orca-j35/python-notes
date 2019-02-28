# python_notes
Python 学习笔记

本笔记的目录结构：

- Language Reference - 「[Library Reference](https://docs.python.org/3.7/library/index.html)」的笔记
- Library Reference - 「[Language Reference](https://docs.python.org/3.7/reference/index.html)」的笔记
- notes - 已整理的笔记
- notes_of_PyQt -  PyQt 的笔记
- notes_of_crawler - 爬虫的笔记
- 待整理笔记 - 待整理的笔记

学习工具：

- [pythontutor](http://www.pythontutor.com/index.html)：可视化 Python 代码的执行过程

- [Thonny](http://thonny.org/)：Python IDE for beginners

- [zeal](https://zealdocs.org/)：文档查询

  - There is a VSCode plugin available at <https://github.com/deerawan/vscode-dash>.
  - https://kapeli.com/dash

- [jupyter](https://jupyter.org/)

- [ipython](https://ipython.org/index.html)

  jupyter 和 ipython 的关系 -- IPython is a growing project, with increasingly language-agnostic components. IPython 3.x was the last monolithic release of IPython, containing the notebook server, qtconsole, etc. As of IPython 4.0, the language-agnostic parts of the project: the notebook format, message protocol, qtconsole, notebook web application, etc. <u>have moved to new projects under the name [Jupyter](https://jupyter.org/).</u> IPython itself is focused on interactive Python, part of which is providing a Python kernel for Jupyter.

阅读建议：

- [The Best Python Books](https://realpython.com/best-python-books/)：由 [realpython](https://realpython.com) 提供的推荐阅读列表

- [What tutorial should I read?](https://sopython.com/wiki/What_tutorial_should_I_read%3F)：由 [sopython](https://sopython.com/) 提供的推荐阅读列表

- [Rreal Python](https://realpython.com/tutorials/all/)：提供了大量教程，覆盖面很广。阅读过其中一篇的译文：[Python 3.7 中的新特性](https://pythonfun.top/cool-new-features-in-python-3.7-trp/)，感觉挺不错的

- [Think Python 2e](https://greenteapress.com/wp/think-python-2e/)：免费书籍，该书的 GitHub 仓库是 [ThinkPython2](https://github.com/AllenDowney/ThinkPython2/tree/master/code)

  该书有如下中文译本：

  - [ThinkPython2-CN](http://codingpy.com/books/thinkpython2/)：该译本的 GitHub 仓库是 [ThinkPython-CN](https://github.com/bingjin/ThinkPython2-CN)
  - 像计算机科学家一样思考Python 第2版：目前在销售的中文译本

- [Python Crash Course](https://ehmatthes.github.io/pcc/)：[作者的网站](https://ehmatthes.github.io/pcc/)提供了示例代码、速查列表、勘误等内容

  - [Geany IDE](https://www.geany.org/Main/HomePage)
  - 中文译本：Python编程 从入门到实践

- Python Cookbook：[出版商的页面](http://shop.oreilly.com/product/0636920027072.do)中提供了示例代码和勘误信息

  - 中文译本：[《Python Cookbook》3rd Edition](https://python3-cookbook.readthedocs.io/zh_CN/latest/copyright.html)，该译本的 GitHub 仓库是 [python3-cookbook](https://github.com/yidao620c/python3-cookbook)

- [The Hitchhiker's Guide to Python!](https://docs.python-guide.org/)

  该指南有如下中文译本：

  - [Python最佳实践指南!](https://pythonguidecn.readthedocs.io/zh/latest/)，该译本的 GitHub 仓库是 [Python-Guide-CN](https://github.com/Prodesire/Python-Guide-CN)
  - [Python 最佳实践指南 2018](https://pythoncaff.com/docs/python-guide/2018) 

- [Python 3 Module of the Week](https://pymotw.com/3/index.html)

  - 中文翻译：[Python 3 标准库实例教程](https://pythoncaff.com/docs/pymotw)
  - 英文勘误：[View Errata](http://www.oreilly.com/catalog/errata.csp?isbn=0636920032519)

- [Effective Python: 59 Ways to Write Better Python](https://effectivepython.com/)

  - 中文译本：Effective Python 编写高质量Python代码的59个有效方法

- [Fluent Python: Clear, Concise, and Effective Programming](http://shop.oreilly.com/product/0636920032519.do)

  - 中文译本：流畅的 Python
  - GitHub 仓库是 [fluentpython/example-code](https://github.com/fluentpython/example-code)

- [Effective Computation in Physics: Field Guide to Research with Python](http://shop.oreilly.com/product/0636920033424.do)

  - 中文译本：[Python 物理学高效计算](https://www.epubit.com/book/detail/33360)
  - GitHub 仓库是：[physics-codes/examples](https://github.com/physics-codes/examples)

- [byte-of-python](https://python.swaroopch.com/)：免费书籍，该书的 GitHub 仓库是 [byte-of-python](https://github.com/swaroopch/byte-of-python)

  - 中文译本：[简明 Python 教程](https://bop.mol.uno/)，该译本的 GitHub 仓库是 [byte-of-python](https://github.com/LenKiMo/byte-of-python)

- [The Python Tutorial](https://docs.python.org/3.7/tutorial/index.html)：官方教程

  - 中文译本：[Python 官方文档：入门教程](https://learnku.com/docs/tutorial/3.7.0)
  - 中文译本：[Python 入门指南](http://www.pythondoc.com/pythontutorial3/index.html)

- [Learn Python 3 the Hard Way](https://learnpythonthehardway.org/python3/)：此教程存在 Stack Overflow 较多争议，部分人认为它不适合初学者，该教程有一个进阶版 [Learn More Python the Hard Way](https://learncodethehardway.org/more-python-book/)。

  - 中文译本：[笨办法学Python 3](https://item.jd.com/12372646.html?dist=jd)，在网络上流传的中文译本都是旧版本，最好直接购买纸质书。

- Intermediate Python：这本书更像是一本学习笔记，汇总了很多知识点，该书的 GitHub 仓库是 [intermediatePython](https://github.com/yasoob/intermediatePython)，在线阅读地址是 [http://book.pythontips.com](http://book.pythontips.com/)，作者博客 [Python Tips](https://pythontips.com/)

  - 中文译本的 GitHub 仓库是 [interpy-zh](https://github.com/eastlakeside/interpy-zh)，在线阅读[Python进阶](http://interpy.eastlakeside.com/)

- [Intermediate Python](https://leanpub.com/intermediatepython)：与上一本书同名，没有发现中文 译本

爬虫：

- Python3 网络爬虫开发实战：作者[崔庆才](https://cuiqingcai.com/author/cqcre)，GitHub [仓库](https://github.com/Python3WebSpider)，GitBook [预览](https://germey.gitbooks.io/python3webspider/content/)
  - 该作者还提供了一套付费视频教程 [Python3网络爬虫实战案例](https://cuiqingcai.com/4320.html) 和两套免费教程 [爬取知乎所有用户详细信息](https://edu.hellobi.com/course/163)、[Python3爬虫三大案例实战分享](https://edu.hellobi.com/course/156) -- 视频资源在 B 站上均有

一些有趣的东西：

- https://jakevdp.github.io/

博客：

- [欢乐蟒](https://pythonfun.top/)：翻译了一些技术文章，比如 [Python 3.7 中的新特性](https://pythonfun.top/cool-new-features-in-python-3.7-trp/) 
- [Python 之旅](http://funhacks.net/2017/01/03/explore_python/)：内容层次清晰，有作者自己的理解，很不错 - [在线阅读](https://funhacks.net/explore-python/)
- [Python 之禅](https://foofish.net/)：博客
- [Python 学习之旅](https://segmentfault.com/blog/python3)：有几篇总结性的文章很不错
- [Python Reference (The Right Way) - DRAFT](https://python-reference.readthedocs.io/en/latest/index.html)：适用于Python 2.7.X，提供了有关内置函数、列表推导式、容器数据、运算符、语句等的快速参考
- [〖十月狐狸〗](https://www.cnblogs.com/sesshoumaru/)：提供了 Python 3.6 中所有内置函数的笔记
- [Yixiaohan](https://github.com/Yixiaohan)/[codeparkshare](https://github.com/Yixiaohan/codeparkshare) 整理并推荐了一些学习资料

杂项：

- [Cool New Features in Python 3.7](https://realpython.com/python37-new-features/) ：详细讲述了 3.7 版本的新功能
- [Python快速教程](https://www.cnblogs.com/vamei/archive/2012/09/13/2682778.html)：没仔细看，感觉内容比较丰富