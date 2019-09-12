# Redis
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>



## 概述

Redis（*Remote Dictionary Server*）是一个 in-memory 数据结构项目，它实现了一个具有[可选持久性](https://en.wikipedia.org/wiki/Redis#Persistence)的分布式 in-memory 键值（*key-value*）数据库。Redis 通常被称为数据结构服务器，因为值（*value*）可以是 字符串（*String*）、哈希（*Hash*）、 列表（*list*）、 集合（set）、有序集合（*sorted set*）和位图（*bitmaps*）等类型。

Redis 最好的地方就是用来提供数据[持久化](https://en.wikipedia.org/wiki/Redis#Persistence)功能（定时把内存中的数据写入文件），从而不至于一旦宕机将造成数据丢失。而且相较于 [memcached](https://www.memcached.org/)，Redis 提供的值类型选择更为宽泛。

相关资源:

- Home: https://redis.io
- Home-CN: http://www.redis.cn
- GitHub: https://github.com/antirez/redis
- Docs: https://redis.io/documentation
- 在线互动教程: http://try.redis.io/ 
- 教程 - runoob: http://www.runoob.com/redis/redis-tutorial.html



### Install on Windows

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
  
  [Windows 上的 Redis 的缺点](https://redislabs.com/ebook/appendix-a/a-3-installing-on-windows/a-3-1-drawbacks-of-redis-on-windows/)



### 命令行程序

简要介绍一下 `<install directory>\Redis` 中的文件:

- redis-server.exe - 服务端程序

- redis-cli.exe - 客户端程序，用于连接服务端，cli 的意思是 command line interface

- redis.conf - 配置文件

- redis-check-dump.exe - 本地数据库检查

- redis-check-aof.exe - 更新日志检查

- redis-benchmark.exe - 性能测试，用于模拟同时由 N 个客户端发送 M 个  SETs/GETs 查询，例如

  ```shell
  # 向redis服务器发送10万个请求，每个请求附带60个并发客户端
  redis-benchmark -n 100000 -c 60
  ```

### 配置文件



### 可视化管理工具

以下是适用于 MongoDB  的可视化管理工具:

- [Redis Desktop Manager](https://github.com/uglide/RedisDesktopManager/): 0.9.4 版本开始收费，官方不再提供下载，但是有第三方编译并提供了安装包，见 https://github.com/necan/RedisDesktopManager-Windows
  - Docs: http://docs.redisdesktop.com/en/latest/quick-start/
- [RedisStudio (Redis GUI Client)](https://github.com/cinience/RedisStudio): 无需安装，直接可用
- [Redis React](https://github.com/ServiceStackApps/RedisReact#download): Redis React is a simple user-friendly UI for browsing data in Redis servers. 无需安装，直接可用
- [redis-web-app](https://github.com/NetCoreWebApps/Redis): Redis Vue is a simple, lightweight, versatile Redis Admin UI developed using [Vue](https://vuejs.org/v2/guide/) and [ServiceStack .NET Core Web Apps](http://templates.servicestack.net/docs/web-apps). 



### 学习路线

如果对 Redis 相关的知识点有所遗忘，可以依次参考下述资料：

1. 通过在线互动教程 http://try.redis.io/，了解 Redis 最主要的功能
2. https://github.com/andymccurdy/redis-py，了解 redis-py 的相关知识
3. [How to Use Redis With Python](https://realpython.com/python-redis/)，了解如何使用 Redis 和 redis-py
4. [Redis Documentation](http://redis.io/documentation)
5. [Command Reference](http://redis.io/commands)
6. [Implement a Twitter Clone in Redis](http://redis.io/topics/twitter-clone)
7. [Introduction to Redis Data Types](http://redis.io/topics/data-types-intro)



## 使用入门

> 参考：
>
> - http://try.redis.io/

### 简单数据结构

`SET` 命令用来存储 key-value 对，下面这个例子会将值 `"fido"` 存储到 `"server:name"` 键中：

```shell
C:\Redis>redis-cli
127.0.0.1:6379> SET server:name "fido"
OK
127.0.0.1:6379> GET server:name
"fido"
```

Redis 将永久存储我们的数据，可以使用 `GET` 命令取回我们需要的数据。

`DEL` 命令用于删除目标键值对。

`SETNX` 仅在 key 不存在时，才会将其设置为目标值。

`INCR` 会以原子方式递增 key 中存放的数值。

```shell
C:\Redis>redis-cli
127.0.0.1:6379> SET server:name "fido"
OK
127.0.0.1:6379> GET server:name
"fido"
127.0.0.1:6379> SET connections 10
OK
127.0.0.1:6379> INCR connections
(integer) 11
127.0.0.1:6379> INCR connections
(integer) 12
127.0.0.1:6379> DEL connections
(integer) 1
127.0.0.1:6379> INCR connections
(integer) 1
```

> There is something special about [INCR](http://try.redis.io/#help). Why do we provide such an operation if we can do it ourself with a bit of code? After all it is as simple as:
>
> ```
> x = GET count
> x = x + 1
> SET count x
> ```
>
> The problem is that doing the increment in this way will only work as long as there is a single client using the key. See what happens if two clients are accessing this key at the same time:
>
> 1. Client A reads *count* as 10.
> 2. Client B reads *count* as 10.
> 3. Client A increments 10 and sets *count* to 11.
> 4. Client B increments 10 and sets *count* to 11.
>
> We wanted the value to be 12, but instead it is 11! This is because incrementing the value in this way is not an atomic operation. Calling the [INCR](http://try.redis.io/#help) command in Redis will prevent this from happening, because it *is* an atomic operation. Redis provides many of these atomic operations on different types of data.

`EXPIRE` 被用来设置 key-value 的生存周期，`TTL` 被用来查看生存周期的剩余时限：

```shell
> SET resource:lock "Redis Demo"
OK
> EXPIRE resource:lock 120
(integer) 1
# 将在120秒后删除resource:lock键
> TTL resource:lock
(integer) 112
# after 112s
> TTL resource:lock
(integer) -2
# -2表示该key并不存在
```

`TTL keyname` 等于 -1 时，表示该 key 永远存在。当 `SET` 某个 key 时，会重设其 `TTL`：

```shell
> SET resource:lock "Redis Demo 1"
OK
> EXPIRE resource:lock 120
(integer) 1
> TTL resource:lock
(integer) 108
> SET resource:lock "Redis Demo 2"
OK
> TTL resource:lock
(integer) -1
```

### 复杂数据结构

Redis 同样支持复杂数据结构。

#### List

首先让我们来看看 list 的使用方法，list 时一系列有序值，与 list 交互的重要命令有 RPUSH, LPUSH, LLEN, LRANGE, LPOP, RPOP。

`RPUSH` 从列表右侧插入新值，`LPUSH` 从列表左侧插入新值

```shell
> RPUSH friends "Alice"
(integer) 1
> RPUSH friends "Bob"
(integer) 2
> LPUSH friends "Sam"
(integer) 3
```

`LRANGE` 获取列表的子集

> It takes the index of the first element you want to retrieve as its first parameter and the index of the last element you want to retrieve as its second parameter. A value of -1 for the second parameter means to retrieve elements until the end of the list.

```
LRANGE friends 0 -1 => 1) "Sam", 2) "Alice", 3) "Bob"
LRANGE friends 0 1 => 1) "Sam", 2) "Alice"
LRANGE friends 1 2 => 1) "Alice", 2) "Bob
```

`LLEN` 返回当前列表的长度

```
    LLEN friends => 3
```

`LPOP` 从列表中删除第一个元素并返回它。

```
    LPOP friends => "Sam"
```

`RPOP` 从列表中删除最后一个元素并返回它。

```
    RPOP friends => "Bob"
```

此时，列表中现在只有一个元素:

```
    LLEN friends => 1
    LRANGE friends 0 -1 => 1) "Alice"
```

#### Set

集合类似于列表，除了它没有特定的顺序，每个元素只能出现一次。使用集合的一些重要命令是SADD，SREM，SISMEMBER，SMEMBERS和SUNION。

`SADD` 将给定的值添加到集合中。


    SADD superpowers "flight"
    SADD superpowers "x-ray vision"
    SADD superpowers "reflexes"
`SREM` 从集合中移除给定值。


    SREM superpowers "reflexes"

`SISMEMBER` 测试给定的值是否在集合中。如果有值，则返回1;如果没有，则返回0。


    SISMEMBER superpowers "flight" => 1
    SISMEMBER superpowers "reflexes" => 0
`SMEMBERS` 返回此集合的所有成员的列表。


    SMEMBERS superpowers => 1) "flight", 2) "x-ray vision"
`SUNION` 组合两个或多个集合并返回所有元素的列表。


    SADD birdpowers "pecking"
    SADD birdpowers "flight"
    SUNION superpowers birdpowers => 1) "pecking", 2) "x-ray vision", 3) "flight"


#### Sorted Sets

集合是一种非常方便的数据类型，但由于它们未排序，因此无法解决许多问题。这就是 Redis 1.2引入 Sorted Sets 的原因。

有序集类似于常规集，但是每个值都会关联一个 score。score 被用来对集合中的元素进行排序

    ZADD hackers 1940 "Alan Kay"
    ZADD hackers 1906 "Grace Hopper"
    ZADD hackers 1953 "Richard Stallman"
    ZADD hackers 1965 "Yukihiro Matsumoto"
    ZADD hackers 1916 "Claude Shannon"
    ZADD hackers 1969 "Linus Torvalds"
    ZADD hackers 1957 "Sophie Wilson"
    ZADD hackers 1912 "Alan Turing"
在这些示例中，score 是出生年份，值是着名黑客的名字。

```
ZRANGE hackers 2 4 => 1) "Claude Shannon", 2) "Alan Kay", 3) "Richard Stallman"
```



#### Hash

哈希是字符串字段和字符串值之间的映射，因此它们是表示对象的完美数据类型（例如：具有多个字段的用户，如姓名，姓氏，年龄等）：

```
    HSET user:1000 name "John Smith"
    HSET user:1000 email "john.smith@example.com"
    HSET user:1000 password "s3cret"
```

要获取保存的数据，请使用 `HGETALL`：

```
    HGETALL user:1000
```

你也可以一次设置多个字段:

```
  HMSET user:1001 name "Mary Jones" password "hidden" email "mjones@example.com"
```

如果你只需要一个字段值，这也是可能的:

```
    HGET user:1001 name => "Mary Jones"
```

散列字段中的数值处理与简单字符串中的数字值完全相同，并且存在以原子方式递增此值的操作。

```
    HSET user:1000 visits 10
    HINCRBY user:1000 visits 1 => 11
    HINCRBY user:1000 visits 10 => 21
    HDEL user:1000 visits
    HINCRBY user:1000 visits 1 => 1
```

扩展阅读 [full list of Hash commands](http://redis.io/commands#hash) 

## Redis-Py

redis.io 推荐使用 redis-py 来操作 Redis 数据库。除了 redis-py 之外，还有一些用来操作  Redis 数据库的 Python 驱动器，详见 https://redis.io/clients#python

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

### 建立连接

Redis 类为所有 Redis 命令提供 Python 接口，并提供 Redis 协议的实现。Connection 和 Pipeline 源于 Redis 实例，实现了如何将命令发送和接收到 Redis 服务器

```python
# in Python3
>>> import redis
>>> r = redis.Redis(host='localhost', port=6379, db=0)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
>>> r.set('whale', '鲸')
True
>>> r.get('whale')
b'\xe9\xb2\xb8'
```

默认情况下，在 Python 3 中响应结果是 `bytes` 类型，在 Python 2 中响应结果是 `str` 类型。对响应结果的解码操作由用户完成。

可以通过 `redis.Redis()` 构造器设置编码方案：

```python
r = redis.Redis(host='localhost', port=6379, db=0, encoding='utf-8')
```

如果需要自动解码所有响应结果，可以在 `redis.Redis()` 构造器设置 `decode_responses=True`。此时，所有响应结果都会使用预设编码方案来解码：

```python
>>> r = redis.Redis(host='localhost', port=6379, db=0, encoding='utf-8', decode_responses=True)
>>> r.set('whale', '鲸')
True
>>> r.get('whale')
'鲸'
```

####  Redis 和 StrictRedis

> 参考：https://github.com/andymccurdy/redis-py#upgrading-from-redis-py-2x-to-30

redis-py 3.0 引入了许多新功能，并不兼容 redis-py 2.0。redis-3.0 已不再支持旧版本中的 "Redis" 客户端类，并且将之前的 "StrictRedis" 客户端类重命名为 "Redis"。"StrictRedis" 现在是 "Redis" 的别名，两者等效。

#### Connection Pools

> 详见：https://github.com/andymccurdy/redis-py#connection-pools

在幕后，redis-py 使用连接池来管理与 Redis 服务器的连接。默认情况下，您创建的每个 Redis 实例将依次创建自己的连接池。您可以通过将已创建的连接池实例传递给 Redis 类的 connection_pool 参数来覆盖此行为并使用现有连接池。您可以选择执行此操作以实现客户端分片，或者对如何管理连接进行更精细的控制。

```python
>>> pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
>>> r = redis.Redis(connection_pool=pool)
```

通过观察源码可以发现，Redis 内其实就是用 host 和 port 等参数构造了一个 ConnectionPool，所以直接将 ConnectionPool 当作参数传给 Redis 也一样。

另外，ConnectionPool 还支持通过 URL 来构建。URL 的格式支持有如下 3 种：

```
redis://[:password]@host:port/db  
rediss://[:password]@host:port/db  
unix://[:password]@/path/to/socket.sock?db=db
```

这 3 种 URL 分别表示创建 Redis TCP 连接、Redis TCP+SSL 连接、Redis UNIX socket 连接。我们只需要构造上面任意一种 URL 即可，其中 password 部分如果有则可以写，没有则可以省略。下面再用 URL 连接演示一下：

```
url = 'redis://:foobared@localhost:6379/0'  
pool = ConnectionPool.from_url(url)  
redis = Redis(connection_pool=pool)
```

这里我们使用第一种连接字符串进行连接。首先，声明一个 Redis 连接字符串，然后调用 `from_url()` 方法创建 ConnectionPool，接着将其传给 Redis 即可完成连接，所以使用 URL 的连接方式还是比较方便的。



### API

[Redis 官方文档](https://redis.io/commands)提供了每个命令的详细释义，redis-py 遵循官方命令的语法，只需按照官方语法来使用 redis-py 即可。不过现实并不总是完美的，以下是一些列外情况：

> - **SELECT**: 未实现。 See the explanation in the Thread Safety section below.
> - **DEL**: 'del' 是 Python 语法中的保留关键字。因此 redis-py 使用 'delete' 进行替代。
> - **MULTI/EXEC**: These are implemented as part of the Pipeline class. The pipeline is wrapped with the MULTI and EXEC statements by default when it is executed, which can be disabled by specifying transaction=False. See more about Pipelines below.
> - **SUBSCRIBE/LISTEN**: Similar to pipelines, PubSub is implemented as a separate class as it places the underlying connection in a state where it can't execute non-pubsub commands. Calling the pubsub method from the Redis client will return a PubSub instance where you can subscribe to channels and listen for messages. You can only call PUBLISH from the Redis client (see [this comment on issue #151](https://github.com/andymccurdy/redis-py/issues/151#issuecomment-1545015) for details).
> - **SCAN/SSCAN/HSCAN/ZSCAN**: The *SCAN commands are implemented as they exist in the Redis documentation. In addition, each command has an equivilant iterator method. These are purely for convenience so the user doesn't have to keep track of the cursor while iterating. Use the scan_iter/sscan_iter/hscan_iter/zscan_iter methods for this behavior.

在 redis-py 3.0 中，这三个命令（MSET、MSETNX 和 ZADD）将接受一个名为 mapping 的位置参数，并且该参数是 `dict` 类型。对于 MSET 和 MSETNX 而言，mapping 是 key-names -> values 组成的字典；对于 ZADD 而言，mapping 是 element-names -> score 组成的字典。

MSET, MSETNX 和 ZADD 的声明如下：

```
def mset(self, mapping):
def msetnx(self, mapping):
def zadd(self, name, mapping, nx=False, xx=False, ch=False, incr=False):
```

详见，https://github.com/andymccurdy/redis-py#mset-msetnx-and-zadd



### SSL 连接

> 参考：https://github.com/andymccurdy/redis-py#ssl-connections

redis-py 3.0 已将 `Redis` 构造器的 `ssl_cert_reqs` 选项的默认值从 `None` 改为 `'required'`。从远程 SSL 终端接受证书时会强制执行 hostname 验证。如果在终端没有在 cert 上正确设置 hostname，则会导致 redis-py 3.0 抛出 `ConnectionError`。

```python
class Redis(object):
    # --snip--
    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, socket_timeout=None,
                 socket_connect_timeout=None,
                 socket_keepalive=None, socket_keepalive_options=None,
                 connection_pool=None, unix_socket_path=None,
                 encoding='utf-8', encoding_errors='strict',
                 charset=None, errors=None,
                 decode_responses=False, retry_on_timeout=False,
                 ssl=False, ssl_keyfile=None, ssl_certfile=None,
                 ssl_cert_reqs='required', ssl_ca_certs=None,
                 max_connections=None):
    # --snip--
    
```

> This check can be disabled by setting ssl_cert_reqs to None. Note that doing so removes the security check. Do so at your own risk.
>
> It has been reported that SSL certs received from AWS ElastiCache do not have proper hostnames and turning off hostname verification is currently required.



### 输入数据

> 参考：https://github.com/andymccurdy/redis-py#encoding-of-user-input

redis-py 3.0 可接受的用户数据只能是 bytes、strings、numbers (ints, longs and floats)。如果试图将 key 或 value 指定为其它任何类型的对象都会抛出 `DataError`。



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

RedisDump 提供了强大的 Redis 数据的导入和导出功能，现在就来看下它的具体用法。

RedisDump 提供了两个可执行命令：redis-dump 用于导出数据，redis-load 用于导入数据。

### redis-dump

首先，可以输入如下命令查看所有可选项：

```
redis-dump -h
```

运行结果如下：

```
Usage: redis-dump [global options] COMMAND [command options]       -u, --uri=S                      Redis URI (e.g. redis://hostname[:port])      -d, --database=S                 Redis database (e.g. -d 15)      -s, --sleep=S                    Sleep for S seconds after dumping (for debugging)      -c, --count=S                    Chunk size (default: 10000)      -f, --filter=S                   Filter selected keys (passed directly to redis' KEYS command)      -O, --without_optimizations      Disable run time optimizations      -V, --version                    Display version      -D, --debug          --nosafe
```

其中 - u 代表 Redis 连接字符串，-d 代表数据库代号，-s 代表导出之后的休眠时间，-c 代表分块大小，默认是 10000，-f 代表导出时的过滤器，-O 代表禁用运行时优化，-V 用于显示版本，-D 表示开启调试。

我们拿本地的 Redis 做测试，运行在 6379 端口上，密码为 foobared，导出命令如下：

```
redis-dump -u :foobared@localhost:6379
```

如果没有密码的话，可以不加密码前缀，命令如下：

```
redis-dump -u localhost:6379
```

运行之后，可以将本地 0 至 15 号数据库的所有数据输出出来，例如：

```
{"db":0,"key":"name2","ttl":-1,"type":"string","value":"Durant","size":6}  {"db":0,"key":"name3","ttl":-1,"type":"string","value":"Durant","size":6}  {"db":0,"key":"name4","ttl":-1,"type":"string","value":"HelloWorld","size":10}  {"db":0,"key":"name5","ttl":-1,"type":"string","value":"James","size":5}  {"db":0,"key":"name6","ttl":-1,"type":"string","value":"James","size":5}  {"db":0,"key":"age","ttl":-1,"type":"string","value":"1","size":1}  {"db":0,"key":"age2","ttl":-1,"type":"string","value":"-5","size":2}
```

每条数据都包含 6 个字段，其中 db 即数据库代号，key 即键名，ttl 即该键值对的有效时间，type 即键值类型，value 即内容，size 即占用空间。

如果想要将其输出为 JSON 行文件，可以使用如下命令：

```
redis-dump -u :foobared@localhost:6379 &gt; ./redis_data.jl
```

这样就可以成功将 Redis 的所有数据库的所有数据导出成 JSON 行文件了。

另外，可以使用 - d 参数指定某个数据库的导出，例如只导出 1 号数据库的内容：

```
redis-dump -u :foobared@localhost:6379 -d 1 &gt; ./redis.data.jl
```

如果只想导出特定的内容，比如想导出以 adsl 开头的数据，可以加入 - f 参数用来过滤，命令如下：

```
redis-dump -u :foobared@localhost:6379 -f adsl:* &gt; ./redis.data.jl
```

其中 - f 参数即 Redis 的 keys 命令的参数，可以写一些过滤规则。

### redis-load

同样，我们可以首先输入如下命令查看所有可选项：

```
redis-load -h
```

运行结果如下：

```
redis-load --help    Try: redis-load [global options] COMMAND [command options]       -u, --uri=S                      Redis URI (e.g. redis://hostname[:port])      -d, --database=S                 Redis database (e.g. -d 15)      -s, --sleep=S                    Sleep for S seconds after dumping (for debugging)      -n, --no_check_utf8      -V, --version                    Display version      -D, --debug          --nosafe
```

其中 - u 代表 Redis 连接字符串，-d 代表数据库代号，默认是全部，-s 代表导出之后的休眠时间，-n 代表不检测 UTF-8 编码，-V 表示显示版本，-D 表示开启调试。

我们可以将 JSON 行文件导入到 Redis 数据库中：

```
< redis_data.json redis-load -u :foobared@localhost:6379
```

这样就可以成功将 JSON 行文件导入到数据库中了。

另外，下面的命令同样可以达到同样的效果：

```
cat redis_data.json | redis-load -u :foobared@localhost:6379
```

本节中，我们不仅了解了 redis-py 对 Redis 数据库的一些基本操作，还演示了 RedisDump 对数据的导入导出操作。由于其便捷性和高效性，后面我们会利用 Redis 实现很多架构，如维护代理池、Cookies 池、ADSL 拨号代理池、Scrapy-Redis 分布式架构等，所以 Redis 的操作需要好好掌握。

