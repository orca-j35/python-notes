# MySQL
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

相关资源:

- Home: https://www.mysql.com/cn/
- MySQL Reference Manuals: http://dev.mysql.com/doc/
- MySQL client/server protocol: http://dev.mysql.com/doc/internals/en/client-server-protocol.html
- Download: https://dev.mysql.com/downloads/mysql/
  - For Windows: https://dev.mysql.com/downloads/windows/installer/8.0.html
- 教程:
  - 廖雪峰: https://www.liaoxuefeng.com/wiki/001508284671805d39d23243d884b8b99f440bfae87b0f4000
  - runoob: http://www.runoob.com/mysql/mysql-tutorial.html

MySQL 官方提供了以下几个版本的 MySQL 数据库:

- [MySQL Community Edition](https://www.mysql.com/products/community/): 社区开源版本(GPL)
- [MySQL Standard Edition](https://www.mysql.com/products/standard/): 标准版 (commercial)
- [MySQL Enterprise Edition](https://www.mysql.com/products/enterprise/): 企业版 (commercial)
- [MySQL Cluster Carrier Grade Edition](https://www.mysql.com/products/cluster/): 集群版 (commercial)

上述版本的功能和价格依次递增，但增加的功能主要是监控、集群等管理功能，各版本中基本的 SQL 功能是完全一样的。所以使用 MySQL 的好处是可以先利用社区版进行学习、开发、测试，需要部署的时候，可以选择付费的高级版本，或者云服务商提供的兼容版本，而不需要对应用程序本身做改动。

## Install on Windows

> 参考:
>
> - [安装MySQL - 廖雪峰](https://www.liaoxuefeng.com/wiki/001508284671805d39d23243d884b8b99f440bfae87b0f4000/00150916716600634d1020c90304a6aaa5f37248006f900000)
> - 《python3网络爬虫开发实战》-> MySQL 的安装

在 [MySQL Installer](https://dev.mysql.com/downloads/installer/) 中可获取 Windows 版本的 MySQL (如, `mysql-installer-community.msi`)。安装过程中始终选用默认配置即可，一路 next 便可完成安装。安装程序会自动在 Windows 中将 MySQL 设置为服务。在安装完成后，便可直接使用 MySQL 客户端连接 MySQL 服务器。

在安装过程中需记住以下配置，以便今后使用(可通过 MySQLInstaller.exe 修改这些配置):

- 默认端口: 3306
- root 密码: orca_j35
- Windows Service Name: MySQL80

在 "计算机管理"->"服务和应用程序"->"服务" 中可查看 MySQL 服务(名称是 MySQL80)是否启动。可以在"服务"中关闭 MySQL 服务，或禁止其自动启动。

## 可视化管理工具

适用于 MySQL 的可视化管理工具:

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) - 在 MySQL 安装包中自带该工具
- [MySQL-Front](http://www.mysqlfront.de/) - 用于MySQL数据库服务器的 Windows 前端程序。在连接本地 MySQL 数据库时，需将主机设置为 `localhost` 或 `127.0.0.1`
- [navicat](https://www.navicat.com.cn/) - 破解参考 [1](https://github.com/Deltafox79/Navicat_Keygen) , [2](https://www.jianshu.com/p/5f693b4c9468?mType=Group) (目前能够顺利破解 12.1 版)

## Python Drivers

> 参考:
>
> - https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python
> - https://stackoverflow.com/questions/4960048/how-can-i-connect-to-mysql-in-python-3-on-windows
> - https://stackoverflow.com/questions/384471/mysql-db-lib-for-python-3-x

### Connector/Python

纯 Python 实现

相关资源:

- [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
- [MySQL Connector/Python X DevAPI Reference Documentation](https://dev.mysql.com/doc/dev/connector-python/8.0/)
- GitHub - https://github.com/mysql/mysql-connector-python
- PyPI - https://pypi.org/project/mysql-connector-python
- [Download Connector/Python](https://dev.mysql.com/downloads/connector/python/)

推荐使用 `pip` (或 `conda` )安装 Connector/Python

```shell
conda install mysql-connector-python
```

下面的代码用于测试连接器是否安装成功:

```python
# 需保持mysql服务开启
import mysql.connector
cnx = mysql.connector.connect(user='scott', password='password',
                              host='127.0.0.1',
                              database='employees')
cnx.close()
```

在 Windows 中还可使用 [MySQL Installer](https://dev.mysql.com/downloads/windows/installer/8.0.html)(或[独立的 MSI Installer](https://dev.mysql.com/downloads/connector/python/))来安装 Connector/Python。Installer 会检查本机中 Python 的路径，并将 Connector/Python 置于 `~\PythonX.Y\Lib\site-packages\` 中。不推荐使用这种方式安装，因为这会导致 `pip` (或 `conda` )无法管理此包。

### PyMySQL

纯 Python 实现

相关资源:

- GitHub - https://github.com/PyMySQL/PyMySQL/
- PyPI - https://pypi.org/project/PyMySQL/
- Docs - https://pymysql.readthedocs.io/en/latest/
- 邮件列表: https://groups.google.com/forum/#!forum/pymysql-users

```shell
python3 -m pip install PyMySQL
```

如果要使用 "sha256_password" 或 "caching_sha2_password" 进行身份验证，还需要按照其它依赖项:

```python
$ python3 -m pip install PyMySQL[rsa]
```

下面的代码用于测试是否安装成功:

```python
import pymysql
print(pymysql.VERSION)
```

在调用 `pymysql.install_as_MySQLdb()` 后，任何导入 MySQLdb 或 \_mysql 的应用都会在不知不觉中实际使用 PyMySQL，源代码如下:

```python
# in pymysql>__init__.py
def install_as_MySQLdb():
    """
    After this function is called, any application that imports MySQLdb or
    _mysql will unwittingly actually use pymysql.
    """
    sys.modules["MySQLdb"] = sys.modules["_mysql"] = sys.modules["pymysql"]
```

相关示例请参考官方文档。

### CyMySQL

CyMySQL 包含一个 Python MySQL 客户端库，CyMySQL 是 PyMySQL 的分支。PyMySQL 是一个纯 Python 数据库驱动，CyMySQL 使用了 Cython 加速，同时支持 Python2 和 Python3。CyMySQL 可以在没有 Cython 的情况下以纯 Python 驱动的方式工作。

相关资源:

- GitHub - https://github.com/nakagami/CyMySQL/
- PyPI - https://pypi.org/project/cymysql/#description
- Docs - 没有找到文档，似乎需要参考 PyMySQL 的文档



### MySQLdb

目前不支持 Python 3

相关资源:

- GitHub - https://github.com/farcepest/MySQLdb1
- PyPI - https://pypi.org/project/MySQL-python
- Docs - http://mysql-python.sourceforge.net/MySQLdb.html

```
pip install MySQL-python
```



### mysqlclient

该库是 MySQLdb ([MySQLdb1](https://github.com/farcepest/MySQLdb1)) 的分支，支持 Python3

相关资源:

- GitHub - https://github.com/PyMySQL/mysqlclient-python
- PyPI - https://pypi.org/project/mysqlclient/
- Docs - https://mysqlclient.readthedocs.io/

```
pip install mysqlclient
```

该包依赖 MySQLConnector/C 或 MSVC，安装过程详见 [GitHub](https://github.com/PyMySQL/mysqlclient-python)。

## 编码方案

> 参考:
>
> - https://my.oschina.net/xsh1208/blog/1052781
> - https://www.infoq.cn/article/in-mysql-never-use-utf8-use-utf8

MySQL 中使用"数据库字符集"一词来表示所采用的编码方案。

MySQL 中的"utf8 字符集"与 Unicode 中的 UTF-8 编码方案并不等价，"utf8 字符集"最多支持 3 字节编码，"UTF-8 编码方案"最多支持 4 字节编码。也就是说，MySQL 支持的"utf8 字符集"最大字符长度为 3 字节，如果遇到 4 字节的宽字符就会插入异常了。

三个字节的 UTF-8 最大能编码的 Unicode 字符是 0xffff，也就是 Unicode 中的基本多文种平面(BMP)。也就是说，任何不在基本多文本平面的 Unicode字符，都无法使用 Mysql 的 utf8 字符集存储。包括 Emoji 表情和很多不常用的汉字，以及任何新增的 Unicode 字符等等。

要在 Mysql 中保存 4 字节长度的 UTF-8 编码，需要使用 utf8mb4 字符集，但只有 5.5.3 版本以后的才支持(查看版本: `select version();`)。为了获取更好的兼容性，在 MySQL 中总应使用 utf8mb4 字符集而非 utf8 字符集。对于 CHAR 类型数据，utf8mb4 会多消耗一些空间，根据 Mysql 官方建议，使用 VARCHAR 替代 CHAR。

在 MariaDB 中也存在类似问题。