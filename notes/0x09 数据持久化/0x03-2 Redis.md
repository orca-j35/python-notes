# Redis
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 扩展阅读：https://realpython.com/python-redis/#ten-or-so-minutes-to-redis

Redis 是面向 key-value 型数据的高性能存储系统。因为值(*value*)可以是字符串(*String*), 哈希(*Map*), 列表(*list*), 集合(*sets*), 有序集合(*sorted sets)*和位图(*bitmaps*)等类型，所以又被称为数据结构服务器。Redis 最好的地方便是用于提供数据持久化功能(定时把内存中的数据写入文件)，从而不至于一旦宕机将造成数据丢失。而且相较于 Memcached ，它提供的值类型选择更为宽泛。

相关资源:

- Home: https://redis.io
- Home-CN: http://www.redis.cn
- GitHub: https://github.com/antirez/redis
- Docs: https://redis.io/documentation
- 在线互动教程: http://try.redis.io/
- 教程 - runoob: http://www.runoob.com/redis/redis-tutorial.html
- [Windows 上的 Redis 的缺点](https://redislabs.com/ebook/appendix-a/a-3-installing-on-windows/a-3-1-drawbacks-of-redis-on-windows/)

## Install on Windows

[在 Windows 中安装 Redis 的三种方法](https://github.com/ServiceStack/redis-windows)：

- Install Redis on Ubuntu on Windows, Use [Windows Subsystem for Linux (WSL)](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide)

- Running the latest version of Redis with Vagrant

- Running Microsoft's native port of Redis

  [MicrosoftArchive/redis](https://github.com/MicrosoftArchive/redis) 中提供了适用于 Windows 的安装包(如, [Redis-x64-3.2.100.msi](https://github.com/MicrosoftArchive/redis/releases/download/win-3.2.100/Redis-x64-3.2.100.msi))，但微软提供的版本远低于 Redis 官方释放的版本，比如目前微软的版本是 3.2，而 Redis 官方的版本是 5.0。

  安装过程中始终选用默认配置即可，一路 next 便可完成安装。安装程序会自动在 Windows 中将 Redis 设置为服务。在安装完成后，便可直接使用 Redis 客户端连接 Redis 服务器。

  如果不想通过安装器 [Redis-x64-3.2.100.msi](https://github.com/MicrosoftArchive/redis/releases/download/win-3.2.100/Redis-x64-3.2.100.msi) 进行安装，而是想通过 [Redis-x64-3.2.100.zip](https://github.com/MicrosoftArchive/redis/releases/download/win-3.2.100/Redis-x64-3.2.100.zip) 手动配置，可参考下面的连接:

  - http://www.runoob.com/redis/redis-install.html
  - https://www.cnblogs.com/weiqinl/p/6490372.html
  - https://www.cnblogs.com/sunxuchu/p/5463403.html
  - https://www.cnblogs.com/panchunting/p/Redis_On_Windows_Install.html 包含源代码的编译方法

  [How do I run Redis on Windows? - stackoverflow](https://stackoverflow.com/questions/6476945/how-do-i-run-redis-on-windows/10525215)



### 命令行程序

简要介绍一下 `<install directory>\Redis` 中的文件:

- redis-server.exe: 服务端程序

- redis-cli.exe: 客户端程序，用于连接服务端

- redis.conf: 配置文件

- redis-check-dump.exe: 本地数据库检查

- redis-check-aof.exe: 更新日志检查

- redis-benchmark.exe: 性能测试，用于模拟同时由 N 个客户端发送 M 个  SETs/GETs 查询，例如

  ```shell
  # 向redis服务器发送10万个请求，每个请求附带60个并发客户端
  redis-benchmark -n 100000 -c 60
  ```

## 管理工具

以下是适用于 MongoDB  的可视化管理工具:

- [Redis Desktop Manager](https://github.com/uglide/RedisDesktopManager/): 0.9.4 版本开始收费，官方不再提供下载，但是有第三方编译并提供了安装包，见 https://github.com/necan/RedisDesktopManager-Windows
  - Docs: http://docs.redisdesktop.com/en/latest/quick-start/
- [RedisStudio (Redis GUI Client)](https://github.com/cinience/RedisStudio): 无需安装，直接可用
- [Redis React](https://github.com/ServiceStackApps/RedisReact#download): Redis React is a simple user-friendly UI for browsing data in Redis servers. 无需安装，直接可用
- [redis-web-app](https://github.com/NetCoreWebApps/Redis): Redis Vue is a simple, lightweight, versatile Redis Admin UI developed using [Vue](https://vuejs.org/v2/guide/) and [ServiceStack .NET Core Web Apps](http://templates.servicestack.net/docs/web-apps). 

## Python Drivers

### Redis-Py

在 Python 中可通过 redis-py 来操作 Redis 数据库。

相关资源:

- GitHub: https://github.com/andymccurdy/redis-py
- PyPI: https://pypi.org/project/redis/
- Docs: https://redis-py.readthedocs.io/en/latest/

```shell
pip install redis
conda install redis-py
```

在 conda 中需使用 `redis-py`，如果使用 `redis` 则会安装 redis 数据库。

下面的代码用于测试是否安装成功:

```python
import redis
print(redis.VERSION)
```

## Redis-Dump

Redis-Dump 由 Ruby 实现的用于导入导出 Redis 数据的工具。需要先安装 Ruby 才能使用 Redis-Dump。

Ruby 相关资源:

- Home: http://www.ruby-lang.org/zh_cn/
- RubyInstaller: https://rubyinstaller.org/
- RubyGems: https://rubygems.org/

Redis-Dump 相关资源:

- GitHub: https://github.com/delano/redis-dump
- Docs:
  - http://delanotes.com/redis-dump/
  - https://www.rubydoc.info/gems/redis-dump/0.4.0/file/README.rdoc  
- Gem: https://rubygems.org/gems/redis-dump

安装 Redis-Dump

```shell
$ gem install redis-dump
```

测试安装，尝试调用以下命令：

```shell
redis-dump
redis-load
```



