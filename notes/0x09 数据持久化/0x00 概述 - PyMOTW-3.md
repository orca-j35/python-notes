# 概述
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - https://pymotw.com/3/persistence.html
>
> 扩展阅读:
>
> - [pickle — Object Serialization](https://pymotw.com/3/pickle/index.html) - ﹝0x01-1 pickle - Python object serialization.md﹞
> - [shelve — Persistent Storage of Objects](https://pymotw.com/3/shelve/index.html)
> - [dbm — Unix Key-Value Databases](https://pymotw.com/3/dbm/index.html)
> - [sqlite3 — Embedded Relational Database](https://pymotw.com/3/sqlite3/index.html)
> - [xml.etree.ElementTree — XML Manipulation API](https://pymotw.com/3/xml.etree.ElementTree/index.html)
> - [csv — Comma-separated Value Files](https://pymotw.com/3/csv/index.html) - ﹝0x01-5 csv - PyMOTW-3.md﹞
>
> 

数据持久化涉及两个方面:

- 数据转换 - 如何将内存中对象转换为可存储的数据格式
- 数据存储 - 如何存储转换后的数据

标准库中已为我们提供了一些用于处理"数据转换"和"数据存储"的模块。

## 数据转换

在标准库中有两个用来处理"数据转换"的模块，它们可以将对象转换为可传输(或可存储)的格式，这一转换过程通常被称为序列化(*serializing*)。最常见到的情况是使用 [`pickle`](https://pymotw.com/3/pickle/index.html#module-pickle) 进行持久化，因为它常被集成到一些实际存储序列化数据标准库模块中，例如 `shelve`。另外还可以使用 `json` 进行持久化，`json` 常用于基于 Web 的应用程序，因为现有的 Web 服务器存储工具通常会使用 JSON 格式。

## 数据存储

将内存中对象转换为可存储的格式后，下一步便需要决定如何存储数据:

- 对于不需要检索的数据，可以使用一个简单的平面扁平文件(*flat*-*file*)来存储数据，将序列化后的对象一个接一个写入文件即可
- 对于需要检索的数据，可以将"键值对"存储到采用 DBM 格式变体的简单数据库中

使用 DBM 格式存储数据的最直接的方式是使用 [`shelve`](https://pymotw.com/3/shelve/index.html#module-shelve) 模块。打开 shelve 文件，并通过类似于字典的 API 来访问该文件即可。在保存对象时，`shelve` 模块会先 pickle 对象，然后再将二进制序列存入数据库中。

但是 `shelve` 有一个缺点，当我使用 `shelve` 的默认接口时，无法预先知道 `shelve` 会使用那种 DBM 格式。因为在你创建数据库时，`shelve` 会根据当前系统中可用的 DBM 库来选择一种 DBM 格式。如果应用程序不需要在具有不同 DBM 库的主机之间共享数据库文件，则格式无关紧要；但如果需要可移植性，请使用模块中的某个类以确保使用特定 DBM 格式。

对于使用 JSON 数据格式的 Web 应用程序，请使用 [`json`](https://pymotw.com/3/json/index.html#module-json) 和 [`dbm`](https://pymotw.com/3/dbm/index.html#module-dbm) 来提供持久性机制。直接使用 [`dbm`](https://pymotw.com/3/dbm/index.html#module-dbm) 的要比使用 `shelve` 麻烦一些，因为 DBM 数据库的键和值必须时字符串，并且在访问数据库中的值时不会自动重建对象。

[`sqlite3`](https://pymotw.com/3/sqlite3/index.html#module-sqlite3) 进程内关系数据库可用于大多数 Python 发行版，可用来存储比"键值对"更加复杂的数据结构。`sqlite3` 将其数据库存储在内存或本地文件中，并且所有访问都来自同一进程，因此不存在网络通信延迟。`sqlite3` 的紧凑特性使其特别适合嵌入桌面应用程序或 Web 应用程序的开发版本。

标准库中还有一些用来解析"标准格式"(如 XML/HTML)的模块，以便在 Python 程序和用其他语言编写的应用程序之间交换数据。[`xml.etree.ElementTree`](https://pymotw.com/3/xml.etree.ElementTree/index.html#module-xml.etree.ElementTree) 被用于解析 XML 文档，并为不同的应用程序提供了几种操作模式。除了解析工具，`ElementTree` 还包含一个接口，用于从内存中的对象创建格式良好的 XML 文档。

[`csv`](https://pymotw.com/3/csv/index.html#module-csv) 模块可以以电子表格或数据库应用程序生成的格式读取和写入表格数据，这使得它可以批量加载数据，或将数据从一种格式转换为另一种格式。





