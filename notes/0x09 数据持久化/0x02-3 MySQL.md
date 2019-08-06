# MySQL
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

相关资源:

- Home: https://www.mysql.com/cn/
- Download: https://dev.mysql.com/downloads/mysql/
  - For Windows: https://dev.mysql.com/downloads/windows/installer/8.0.html
- 教程 - 廖雪峰: https://www.liaoxuefeng.com/wiki/001508284671805d39d23243d884b8b99f440bfae87b0f4000
- 教程 - runoob: http://www.runoob.com/mysql/mysql-tutorial.html

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

在 [MySQL Installer](https://dev.mysql.com/downloads/installer/) 中可获取 Windows 版本的 MySQL(如, `mysql-installer-community.msi`)。安装过程中始终选用默认配置即可，一路 next 便可完成安装。安装程序会自动在 Windows 中将 MySQL 设置为服务。在安装完成后，便可直接使用 MySQL 客户端连接 MySQL 服务器。

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

相关资源:

- GitHub - https://github.com/PyMySQL/PyMySQL/
- PyPI - https://pypi.org/project/PyMySQL/
- Docs - https://pymysql.readthedocs.io/en/latest/

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

❓PyMySQL 也为 MySQLdb 提供了类似的接口，执行如下初始化操作即可:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

在调用 `pymysql.install_as_MySQLdb()` 后，几乎完全兼容 `MySQLdb`

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

该库是 MySQLdb ([MySQLdb1](https://github.com/farcepest/MySQLdb1)) 的分支，虽然 MySQLdb 不支持 Python3，但 mysqlclient 支持 Python3。

相关资源:

- GitHub - https://github.com/PyMySQL/mysqlclient-python
- PyPI - https://pypi.org/project/mysqlclient/
- Docs - https://mysqlclient.readthedocs.io/

```
pip install mysqlclient
```

该包依赖 MySQLConnector/C 或 MSVC，安装过程详见 [GitHub](https://github.com/PyMySQL/mysqlclient-python)。