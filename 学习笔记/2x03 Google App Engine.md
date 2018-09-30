# Google App Engine

[TOC]

本章内容来自 《head first python》

GAE 使一组 Web 应用开发技术，允许在 Google 的云计算基础设施上托管 Web 应用。
GAE 会持续监视正在运行的 Web 应用，根据 Web 应用当前的活动，调整所需的资源来服务 Web 应用的页面。如果业务很忙，GAE 会增加 Web 应用的可用资源，如果没有太多业务，GAE 则会减少资源，直到有另外的活动要求再次增加资源。

GAE 还允许访问 Google 的 BigTable 技术：这是一组数据库技术，利用这种技术，可以非常轻松的存储 Web 应用的数据。Google 还会定期备份 Web 应用的数据，将 Web 应用复制到地理位置分散的多个 Web 服务器上，并保证 App Engine 随时都可以正常运行。

Python 可以编写 GAE 程序。

Google 提供的 Web 托管服务，每月处理的页面访问量在 5000000 内免费。

## 安装

https://cloud.google.com/appengine/docs/standard/python/download 

在页面的最下方选择下载原始的 App Engine SDK for Python。

## 构建web应用

Google 云中 GAE 支持标准的 CGI 或 Python 的 WSGI 环境。构建与 GAE 兼容的 Web 应用，需要一个用于存放Web应用的文件夹，然后将执行代码和配置文件存放在该文件夹中。

例如构建一个用于测试的应用结构：

```
.../mygaetest/
		syahello.py
		app.yaml #配置文件，用于告诉google云有关web
```

app.yaml 是配置文件，用于告诉google云有关web应用运行时的环境信息。

```
application: mygaetest #用于标示web应用，与文件夹同名
version: 1 #用于标识web应用的当前版本
runtime: python #告诉GAE应用使用Py编写并在Py上运行
api_version: 1 #指示所面向的GAE版本

handlers:#可以把这一部认为是一个顶层Web应用路由机制
- url: /.* #此项告诉GAE将对Web应用的所有请求路由到syahello.py程序
  script: sayhello.py
```

syahello.py 是 CGI 脚本：

```
print('Content-type: text/plain\n')
print('Hello from Head First Python on GAE!')
```

GAE SDK 包含一个测试 Web 服务器。
使用 Google App Engine Launcher 时，要在首选项中设置好相应Py版本的路径。

## MCV 模式

App Engine 使用模型-视图-控制器(MVC)模式。

GAE 的 Web 应用的**模型组件**使用一个被称为 datastore (数据存储)的后台数据存储工具。该工具建立在 BigTable 技术基础上，提供了一个 NoSQL API，另外还使用GQL(goolgle's query language ) 提供了一个类SQL的API。

GAE 的**视图**使用了 Django 项目的模板系统（Django 是一种 Py 的 web 框架技术）。另外，GAE 还包含 Django 的表单构建技术。

**控制器** 可以使用 CGI 或 WSGI 标准。

### 对数据建模

GAE 将存储在 datastore 中的数据项称为属性 properties，在模型代码中定义。
可以把属性property认为是一种定义数据库模式中数据名称和类型的方法：每个属性就像是列类型，列类型与一行中存储的一块数据相关联，App Engine 将行称为一个实体entity。或说将”行“对应到”实体“，将”列“ 对应到”属性“。实体对应“数据行”，属性对应“数据值”。

与 SQL 数据库类似，GAE datastore 属性也有特定的预声明类型，比如：

• db.StringProperty: a string of up to 500 characters
• db.Blob: a byte string (binary data)
• db.DateProperty: a date
• db.TimeProperty: a time,
• db.IntegerProperty: a 64-bit integer
• db.UserProperty: a Google account 

[完整的声明列表](https://cloud.google.com/appengine/docs/standard/python/datastore/typesandpropertyclasses?csw=1)

| id   | name  | dob        |
| ---- | ----- | ---------- |
| 1    | james | 2002-03-14 |
| 2    | sarah | 2002-06-17 |
| 3    | vera  | 2002-12-25 |

id 列可储存为 db.IntegerProperty
name 列可存储为 db.StringProperty
dob 列可存储为 db.DateProperty

### 模板

Django 的模板可以将数据替换到 HTML 中，另外还可以执行条件也循环代码。
Django 使用 `{{name}}` 语句完成变量替换

```
# header.html
<html>
<head>
<title>{{ title }}</title>
</head>
<body>
<h1>{{ title }}</h1>

# footer.html
<p>
{{ links }}
</p>
</body>
</html>

# form_start.html
<form method="POST" action="/">
<table>

#form_end.html
<tr><th>&nbsp;</th><td><input type="submit" value="{{ sub_title }}"></td></tr>
</table>
</form>
```

使用模板

```
from google.appengine.ext.webapp import template
html = template.render('templates/header.html', {'title': 'Report a Possible Sighting'})
```

### 表单验证框架

GAE 还使用了 Django 的表单验证框架 From Validation Framework。
当给定一个数据模型时，GAE 可以使用这个框架生成必要的 HTML，从而在 HTML 表中显示表单域。



















