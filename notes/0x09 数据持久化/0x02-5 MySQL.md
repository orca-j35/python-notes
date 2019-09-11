# MySQL
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 🚧 2019年9月2日

## 概述

相关资源:

- Home: https://www.mysql.com/cn/
- MySQL Reference Manuals: http://dev.mysql.com/doc/
  - MySQL 8.0 Reference Manual: https://dev.mysql.com/doc/refman/8.0/en/
- MySQL client/server protocol: http://dev.mysql.com/doc/internals/en/client-server-protocol.html
- Download: https://dev.mysql.com/downloads/mysql/
  - For Windows: https://dev.mysql.com/downloads/windows/installer/8.0.html
- 教程:
  - 廖雪峰: https://www.liaoxuefeng.com/wiki/1177760294764384
  - 廖雪峰 Python 教程: https://www.liaoxuefeng.com/wiki/1016959663602400/1017801397501728
  - 《 SQL 必知必会 》
  - runoob: http://www.runoob.com/mysql/mysql-tutorial.html

MySQL 官方提供了以下几个版本的 MySQL 数据库:

- [MySQL Community Edition](https://www.mysql.com/products/community/): 社区开源版本(GPL)
- [MySQL Standard Edition](https://www.mysql.com/products/standard/): 标准版 (commercial)
- [MySQL Enterprise Edition](https://www.mysql.com/products/enterprise/): 企业版 (commercial)
- [MySQL Cluster Carrier Grade Edition](https://www.mysql.com/products/cluster/): 集群版 (commercial)

上述版本的功能和价格依次递增，但增加的功能主要是监控、集群等管理功能，各版本中基本的 SQL 功能是完全一样的。所以使用 MySQL 的好处是可以先利用社区版进行学习、开发、测试，需要部署的时候，可以选择付费的高级版本，或者云服务商提供的兼容版本，而不需要对应用程序本身做改动。



### Install on Windows

> 参考:
>
> - [安装MySQL - 廖雪峰 SQL 教程](https://www.liaoxuefeng.com/wiki/001508284671805d39d23243d884b8b99f440bfae87b0f4000/00150916716600634d1020c90304a6aaa5f37248006f900000)
> - 《python3网络爬虫开发实战》-> MySQL 的安装

在 [MySQL Installer](https://dev.mysql.com/downloads/installer/) 中可获取 Windows 版本的 MySQL (如, `mysql-installer-community.msi`)。安装过程中始终选用默认配置即可，一路 next 便可完成安装。安装程序会自动在 Windows 中将 MySQL 设置为服务。在安装完成后，便可直接使用 MySQL 客户端连接 MySQL 服务器。

在安装过程中需记住自己的配置（比如下面这些），以便今后使用：

- 默认端口: 3306
- root 密码: orca_j35
- Windows Service Name: MySQL80

配置信息可使用 MySQLInstaller.exe 进行修改。

在 "计算机管理"->"服务和应用程序"->"服务" 中可查看 MySQL 服务(名称是 MySQL80)是否启动。可以在"服务"中关闭 MySQL 服务，或禁止其自动启动。



### 可视化管理工具

适用于 MySQL 的可视化管理工具:

- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) - 在 MySQL 安装包中自带该工具
- [MySQL-Front](http://www.mysqlfront.de/) - 用于MySQL数据库服务器的 Windows 前端程序。在连接本地 MySQL 数据库时，需将主机设置为 `localhost` 或 `127.0.0.1`
- [navicat](https://www.navicat.com.cn/) - 破解参考 [1](https://github.com/Deltafox79/Navicat_Keygen) , [2](https://www.jianshu.com/p/5f693b4c9468?mType=Group) (目前能够顺利破解 12.1 版)



## DB-API Drivers

> 参考:
>
> - https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python
> - https://stackoverflow.com/questions/4960048/how-can-i-connect-to-mysql-in-python-3-on-windows
> - https://stackoverflow.com/questions/384471/mysql-db-lib-for-python-3-x

本小节会介绍一些遵循数据库 API 规范(v2.0)的 MySQL 数据库驱动模块。

MySQL 服务器以独立的进程运行，并通过网络对外服务，数据库驱动模块的功能便是连接 MySQL 服务器。



### Connector/Python

MySQL 官方提供的驱动器，纯 Python 实现

相关资源:

- [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/)
- [MySQL Connector/Python X DevAPI Reference Documentation](https://dev.mysql.com/doc/dev/connector-python/8.0/)
- GitHub - https://github.com/mysql/mysql-connector-python
- PyPI - https://pypi.org/project/mysql-connector-python
- [Download Connector/Python](https://dev.mysql.com/downloads/connector/python/)

推荐使用 `pip` (或 `conda` )安装 Connector/Python

```shell
pip install mysql-connector-python

# 某些教程可能会使用下述命令进行安装,
# pip install mysql-connector-python --allow-external mysql-connector-python
# 这种做法是错误的,因为自1.0版起,pip已弃用如下选项:
# --allow-external,--allow-all-external,--allow-unverified 
```

下面的代码用于测试是否安装成功:

```python
# 需保持mysql服务开启
import mysql.connector
cnx = mysql.connector.connect(user='scott', password='password',
                              host='127.0.0.1',
                              database='employees')
cnx.close()
```

⚠: 在 Windows 中还可使用 [MySQL Installer](https://dev.mysql.com/downloads/windows/installer/8.0.html) (或[独立的 MSI Installer](https://dev.mysql.com/downloads/connector/python/))来安装 Connector/Python。Installer 会检查本机中 Python 的路径，并将 Connector/Python 置于 `~\PythonX.Y\Lib\site-packages\` 中。不推荐使用这种方式安装，因为这会导致 `pip` (或 `conda` )无法管理此包。

在检索过程中感觉有用，但是没有完整阅读过的资料:

- [MySQL Python connector API详解](https://www.history-of-my-life.com/archives/222) 



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



#### 提示

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

pymysql 模块中的 connection 对象和 cursor 对象均支持上下文管理( `with` 语句)，详见源代码。

pymysql 模块提供了 `DictCursor` 对象，可以将查询结果以字典形式返回。

pymysql 模块采用 `pyformat` 风格的参数标记，例如 `...WHERE name=%(name)s`。



#### 创建数据库

以下 SQL 语句会创建一个名为 test 的数据库：

```mysql
CREATE DATABASE `test` CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci';
```

为了获取更好的兼容性，建议在 MySQL 中使用 utf8mb4 字符集而非 utf8 字符集。

示例代码：

```python
import pymysql

connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='orca_j35',
    charset='utf8mb4',
)

try:
    with connection.cursor() as cursor:
        cursor.execute(
            "CREATE DATABASE `test` CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci';"
        )
finally:
    connection.close()
```

⚠- 在创建数据库时，无需为 connect 构造器提供 database 参数，也无需执行 commit 操作。



#### 创建 table

首先需要在数据库中创建如下 table：

```mysql
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
# NOT NULL - 表示字段不为null
# IF NOT EXISTS - 详见"IF NOT EXIETS"小节
# 请使用 utf8mb4 字符集
```

示例 - 创建 table：

```python
import pymysql

conn = connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='orca_j35',
    charset='utf8mb4',
    database='test',
)

try:
    with connection.cursor() as cursor:
        # Create a database
        sql = '''CREATE TABLE IF NOT EXISTS `users1` (
                `id` int(11) NOT NULL AUTO_INCREMENT,
                `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
                PRIMARY KEY (`id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'''

finally:
    connection.close()
```

⚠- 在创建表格时，无需执行 commit 操作。



#### 插入和检索数据

示例 - 向 table 中插入数据：

```python
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='orca_j35',
                             charset='utf8mb4',
                             database='test',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # 插入一条新的record, 并使用参数标记%s来传递字段值
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. 
    # So you must commit to save your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
```

输出：

```
{'password': 'very-secret', 'id': 1}
```

⚠- 在修改表格时，需执行 commit 操作。

示例 - 动态构造 SQL 插入语句：

```python
import pymysql

conn = connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='orca_j35',
    charset='utf8mb4',
    database='test',
)

try:
    with connection.cursor() as cursor:
        # 当data发生改变时,INSERT语句中插入的字段会动态变化
        data = {'email': '"webmaster@python.org"', 'password': '"very-secret"'}
        table = '`users`'
        sql = "INSERT INTO {table} ({keys}) VALUES ({values})".format(
            table=table,
            keys=', '.join(data.keys()),
            values=', '.join(data.values()),
        )
        print(sql)
        cursor.execute(sql)

    connection.commit()

    with connection.cursor() as cursor:

        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org', ))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
```



##### 防止重复插入相同数据

> 参考: 
>
> - [13.2.11.6 Subqueries with EXISTS or NOT EXISTS](https://dev.mysql.com/doc/refman/8.0/en/exists-and-not-exists-subqueries.html) 
> - [13.2.6.1 INSERT ... SELECT Syntax](https://dev.mysql.com/doc/refman/8.0/en/insert-select.html) 
> - [MySQL防止重复插入相同记录 insert if not exists](https://blog.csdn.net/fly910905/article/details/79634483) 
> - 《SQL 必知必会》15.1.3 插入检索出的数据 
> - https://blog.csdn.net/qq907177955/article/details/80589015 

在插入（*insert*）数据时，有时需要先查询是否已存在相同的 record，然后再进行插入。我们可以使用下面这个 SQL 语句模板来达到这一目的。

```mysql
INSERT INTO `table_name` (field_1, field_2, ..., field_n) 
SELECT 
	field_1_value, 
	field_2_value, 
	..., 
	field_n_value
FROM
	DUAL
WHERE
	NOT EXISTS (
		SELECT
			field
		FROM
			TABLE
		WHERE
			field = ?
        )
```

示例 - 使用 `NOT EXISTS` 和子查询来防止插入相同的数据：

```mysql
mysql> SELECT * FROM `user`;
+------+----+---------------------+-----+
| name | id | time                | age |
+------+----+---------------------+-----+
| 小明 |  1 | 2019-08-13 15:14:31 |   1 |
| 小红 |  2 | 2019-08-08 15:14:40 |   2 |
| 小刚 |  3 | 2019-08-24 15:14:45 |   3 |
| 小灿 |  4 | 2019-09-20 15:14:49 |   4 |
+------+----+---------------------+-----+
4 rows in set (0.03 sec)

mysql> INSERT INTO `user` ( `name`, age ) SELECT
'小明',
99 
FROM
	DUAL 
WHERE
	NOT EXISTS ( SELECT `name` FROM `user` WHERE `name` = '小明' );
Query OK, 0 rows affected (0.00 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM `user`;
+------+----+---------------------+-----+
| name | id | time                | age |
+------+----+---------------------+-----+
| 小明 |  1 | 2019-08-13 15:14:31 |   1 |
| 小红 |  2 | 2019-08-08 15:14:40 |   2 |
| 小刚 |  3 | 2019-08-24 15:14:45 |   3 |
| 小灿 |  4 | 2019-09-20 15:14:49 |   4 |
+------+----+---------------------+-----+
4 rows in set (0.05 sec)
```

##### ON DUPLICATE KEY UPDATE

> 参考：[13.2.6.2 INSERT ... ON DUPLICATE KEY UPDATE Syntax](https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html)

如果指定了 `ON DUPLICATE KEY UPDATE` 子句，并且被插入的内容将导致 UNIQUE 索引或 PRIMARY KEY 出现重复值，则会使用 `ON DUPLICATE KEY UPDATE` 子句中的内容来更新 UNIQUE 索引或 PRIMARY KEY 中相应的字段。如果被插入的内容不会导致 UNIQUE 索引或 PRIMARY KEY 出现重复值，则会插入一个新的 record。

例如，如果字段 a 是 UNIQUE 索引，并且已存在 `a=1` 的 record，则下述两个语句等效：

```mysql
INSERT INTO t1 (a,b,c) VALUES (1,2,3)
  ON DUPLICATE KEY UPDATE c=c+1;

UPDATE t1 SET c=c+1 WHERE a=1;
```

示例 - 遇到已存在的主键时，则更新其中的字段：

```python
import pymysql

conn = connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='orca_j35',
    charset='utf8mb4',
    database='test',
)

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        
    # 如果主键已经存在，则会执行更新操作
    with connection.cursor() as cursor:
        sql = (
            "INSERT INTO `users` (id, email, password) VALUES (% s, % s, % s)"
            "ON DUPLICATE KEY UPDATE email = % s, password = % s")
        cursor.execute(
            sql, (1, 'whale@python.org', '123', 'whale@python.org', '123'))

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `users`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
```

输出：

```
(1, 'orca@python.org', 'very-secret')
(1, 'whale@python.org', '123')
```



#### 更新数据

```python
import pymysql

conn = connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='orca_j35',
    charset='utf8mb4',
    database='test',
)

try:
    with connection.cursor() as cursor:
        data = {'email': '"orca@python.org"', 'password': '"very-secret"'}
        table = '`users`'
        sql = "INSERT INTO {table} ({keys}) VALUES ({values})".format(
            table=table,
            keys=', '.join(data.keys()),
            values=', '.join(data.values()),
        )
        cursor.execute(sql)

    connection.commit()

    with connection.cursor() as cursor:
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('orca@python.org', ))
        result = cursor.fetchone()
        print(result)
    
    # 更新数据
    with connection.cursor() as cursor:
        sql = "UPDATE `users` SET password = '123' WHERE email = 'orca@python.org';"
        cursor.execute(sql)
        
    with connection.cursor() as cursor:
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('orca@python.org', ))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
```

输出：

```
(17, 'very-secret')
(17, '123')
```

#### 删除数据

```mysql
mysql> SELECT * FROM users;
+----+-----------------+-------------+
| id | email           | password    |
+----+-----------------+-------------+
|  1 | orca@python.org | very-secret |
+----+-----------------+-------------+
1 row in set (0.03 sec)

mysql> DELETE FROM users WHERE email = 'orca@python.org';
Query OK, 1 row affected (0.01 sec)
mysql> SELECT * FROM users;
Empty set
```



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

## 数据库编码方案

> 参考:
>
> - https://my.oschina.net/xsh1208/blog/1052781
> - https://www.infoq.cn/article/in-mysql-never-use-utf8-use-utf8

注释: MySQL 中使用"数据库字符集"一词来表示所采用的编码方案。

MySQL 中的"utf8 字符集"与 Unicode 中的 UTF-8 编码方案并不等价，"utf8 字符集"最多支持 3 字节编码，"UTF-8 编码方案"最多支持 4 字节编码。也就是说，MySQL 中的"utf8 字符集"的最大字符长度是 3 个字节，如果遇到 4 字节的宽字符便会出现插入异常。

与关字符集相关的文档如下:

> [Unicode Support in **MySQL 8.0 Reference Manual**](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode.html)
>
> - [The utf8mb4 Character Set (4-Byte UTF-8 Unicode Encoding)](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf8mb4.html)
> - [The utf8mb3 Character Set (3-Byte UTF-8 Unicode Encoding)](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf8mb3.html)
> - [The utf8 Character Set (Alias for utf8mb3)](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf8.html)
> - [The ucs2 Character Set (UCS-2 Unicode Encoding)](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-ucs2.html)
> - [The utf16 Character Set (UTF-16 Unicode Encoding)](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf16.html)
> - [The utf16le Character Set (UTF-16LE Unicode Encoding)](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf16le.html)
> - [The utf32 Character Set (UTF-32 Unicode Encoding)](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf32.html)
> - [Converting Between 3-Byte and 4-Byte Unicode Character Sets](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-conversion.html) 

三个字节的 UTF-8 最大能编码的 Unicode 字符是 `0xffff`，也就是 Unicode 中的基本多文种平面(BMP)。任何不在基本多文本平面的 Unicode字符，都无法使用 Mysql 的 utf8 字符集存储。包括 Emoji 表情和很多不常用的汉字，以及任何新增的 Unicode 字符等等。

要在 Mysql 中保存 4 字节长度的 UTF-8 编码，需要使用 utf8mb4 字符集，但只有 5.5.3 版本以后的才支持(查看版本: `select version();`)。**为了获取更好的兼容性，在 MySQL 中总应使用 utf8mb4 字符集而非 utf8 字符集。**对于 CHAR 类型数据，utf8mb4 会多消耗一些空间，根据 Mysql 官方建议，使用 VARCHAR 替代 CHAR。

使用 MySQL 时，我们会在 3 个地方遇到字符集: 数据库的字符集，表的字符集，字段的字符集。当我们通过数据库驱动操作字段时，需要使用与字段一直的字符集。

在 MariaDB 中也存在类似问题。

## SQL 补充

本节会对本文中出现的某些 SQL 语句进行解释。

### AUTO_INCREMENT

> 参考:
>
> - [Mysql中的auto_increment关键字详解](https://blog.csdn.net/liu16659/article/details/80847195)

在创建 tab 时，可以使用 AUTO_INCREMENT 来设置"自动递增"。

```mysql
create table mydatabase.test
(id int not null AUTO_INCREMENT PRIMARY key,
name varchar(20)) AUTO_INCREMENT  = 3;

# 第一个AUTO_INCREMENT表示id支持自动递增
# AUTO_INCREMENT = 3 表示自动递增的初始值是3

insert into mydatabase.test(name) VALUES
('littlelawson'),
('shakespere');

select * from mydatabase.test

drop table mydatabase.test;
```

结果：

```
| id   | name         |
| ---- | ------------ |
| 3    | littlelawson |
| 4    | shakespere   |
```

### SELECT VERSION()

查看当前数据库的版本

```python
import pymysql

conn = connection = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',
    password='orca_j35',
    charset='utf8mb4',
    database='test',
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print(result)
        #> ('8.0.15',)
finally:
    connection.close()
```

### IF NOT EXISTS

> 参考：[mysql中,创建表的时候指定if not exists参数的作用?](https://www.cnblogs.com/chuanzhang053/p/9169323.html) 
>
> 相关文档：[17.4.1.6 Replication of CREATE ... IF NOT EXISTS Statements](https://dev.mysql.com/doc/refman/8.0/en/replication-features-create-if-not-exists.html)

在创建 table 时，如果数据库中已存在同名 table，便会报错（只要 table 相同就会报错，不考虑 table 的具体结构）。可使用 `IF NOT EXISTS` 语句来避免出现错误信息。

```mysql
mysql> CREATE TABLE test01 (id int);
Query OK, 0 rows affected (0.06 sec)

mysql> CREATE TABLE test01 (id int);
1050 - Table 'test01' already exists
mysql> CREATE TABLE if not EXISTS test01 (id01 int);
Query OK, 0 rows affected (0.00 sec)

mysql> show warnings;
+-------+------+-------------------------------+
| Level | Code | Message                       |
+-------+------+-------------------------------+
| Note  | 1050 | Table 'test01' already exists |
+-------+------+-------------------------------+
1 row in set (0.03 sec
```

虽然不会报错，但存在警告信息。



### FROM DUAL

> 参考:
>
> - https://dev.mysql.com/doc/refman/8.0/en/select.html
> - https://www.cnblogs.com/mingmingcome/p/9310371.html
> - https://www.jianshu.com/p/b8d1db32302e

[`SELECT`](https://dev.mysql.com/doc/refman/8.0/en/select.html) 可用来检索没有引用任何 table 的行计算，例如：

```sql
mysql> SELECT 1 + 1;
        -> 2
```

在没有引用 table 的情况下，你可以为 `SELECT` 设置一个虚拟（*dummy*）表名——`DUAL`：

```mysql
mysql> SELECT 1 + 1 FROM DUAL;
        -> 2
```

`DUAL` 纯粹是为了方便哪些需要在 `SELECT` 语句后使用 `FROM` 或其它子句的人而提供的。MySQL 可能会忽略这些子句。如果没有引用 table，MySQL 并不需要 `FROM DUAL` 语句。

DUAL 表中并没有任何数据：

```mysql
mysql> SELECT * FROM DUAL;
1096 - No tables used
```



### EXISTS or NOT EXISTS

> 参考:
>
> - [13.2.11.6 Subqueries with EXISTS or NOT EXISTS](https://dev.mysql.com/doc/refman/8.0/en/exists-and-not-exists-subqueries.html) 

如果子查询（*subquery*）获取到的内容不是为空，那么 `EXISTS` 子查询将返回 TRUE，`NOT EXIST` 子查询将返回 FALSE，例如：

```mysql
SELECT column1 FROM t1 WHERE EXISTS (SELECT * FROM t2);
```

> ❓：什么是子查询？
>
> 子查询是位于 `SELECT` 语句中的 `SELECT` 语句，例如：
>
> ```mysql
> SELECT * FROM t1 WHERE column1 = (SELECT column1 FROM t2);
> ```
>
> 相关文档：[13.2.11 Subquery Syntax](https://dev.mysql.com/doc/refman/8.0/en/subqueries.html)

### 查看变量

示例 - 查看变量名中包含 `char` 的变量：

```mysql
mysql> show variables like '%char%';
+--------------------------+---------------------------------------------------------+
| Variable_name            | Value                                                   |
+--------------------------+---------------------------------------------------------+
| character_set_client     | utf8mb4                                                 |
| character_set_connection | utf8mb4                                                 |
| character_set_database   | utf8mb4                                                 |
| character_set_filesystem | binary                                                  |
| character_set_results    | utf8mb4                                                 |
| character_set_server     | utf8mb4                                                 |
| character_set_system     | utf8                                                    |
| character_sets_dir       | C:\Program Files\MySQL\MySQL Server 8.0\share\charsets\ |
+--------------------------+---------------------------------------------------------+
8 rows in set (0.05 sec)
```



