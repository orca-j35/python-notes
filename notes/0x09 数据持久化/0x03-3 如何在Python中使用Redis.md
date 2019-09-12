# 如何在Python中使用Redis
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本文参考自 [How to Use Redis With Python](https://realpython.com/python-redis/)

教程内容简介：

- 从源代码安装 Redis 并了解生成的二进制文件的用途
- 了解一点和 Redis 相关的知识，包括语法、协议和 design
- 掌握 redis-py，同时看看它如何实现 Redis 协议
- 设置 Amazon ElastiCache Redis 服务器实例，并与之通信

## 从源代码安装 Redis

本节内容针对 Mac OS X 或 Linux 展开。如果你使用的是 Windows，则应安装 Redis 的 Microsoft [分支](https://github.com/MicrosoftArchive/redis)。目前 Windows 版本远低于 Linux 版本，最好在 Linux 上使用 Redis。

在 Linux 上安装 Redis 时，请交叉参考：

- https://redis.io/download 
- [Installing Redis From Source](https://realpython.com/python-redis/#installing-redis-from-source) 
- [Redis quickstart guide](https://redis.io/topics/quickstart) 

我尝试在 Windows 10 的 WSL 中安装 Redis，但未能成功安装。



## 配置 Redis

> 在 Linux 上配置 Redis 的详细过程，请参考：
>
> - [Configuring Redis](https://realpython.com/python-redis/#configuring-redis) 
> - [Redis quickstart guide](https://redis.io/topics/quickstart) 

Redis 具备高度的可配置性，虽然 Redis 支持开箱即用，但还是让我们来配置一下与"数据库持久性"和"基本安全"相关的一些基本选项。先创建一个 `.conf` 配置文件：

```shell
$ sudo su root
$ mkdir -p /etc/redis/
$ touch /etc/redis/6379.conf
```

以下是 `/etc/redis/6379.conf` 中的配置项，在之后的教程中会逐步介绍这些配置选项。

```
# /etc/redis/6379.conf

port              6379
daemonize         yes
save              60 1
bind              127.0.0.1
tcp-keepalive     300
dbfilename        dump.rdb
dir               ./
rdbcompression    yes
```

如果要将 Redis 用于生产环境，请务必阅读配置示例，以熟悉各种配置细节，并对配置进行调整：

- 适用于 Linux 的配置示例，请查看 Redis 源代码中的 [`redis.conf`](http://download.redis.io/redis-stable/redis.conf) 文件。
- 适用于 Windows 的配置示例，请查看安装目录中的 `C:\Redis\redis.windows-service.conf` 文件。

一些教程（包括 Redis 官方文档中的部分内容）也许会建议你运行 Shell 脚本 `install_server.sh` （位于 [`redis/utils/install_server.sh`](http://download.redis.io/redis-stable/utils/install_server.sh)）。你可以将这种方法视为一种更全面的替代方案，但请注意有关 `install_server.sh` 的一些细节：

- It will not work on Mac OS X—only Debian and Ubuntu Linux.
- It will inject a fuller set of configuration options into `/etc/redis/6379.conf`.
- It will write a System V [`init` script](https://bash.cyberciti.biz/guide//etc/init.d) to `/etc/init.d/redis_6379` that will let you do `sudo service redis_6379 start`.

在 [Redis quickstart guide](https://redis.io/topics/quickstart) 中也包含与 Redis 配置相关的部分（https://redis.io/topics/quickstart#installing-redis-more-properly）：

- Set **daemonize** to yes (by default it is set to no).
- Set the **pidfile** to `/var/run/redis_6379.pid` (modify the port if needed).
- Change the **port** accordingly. In our example it is not needed as the default port is already 6379.
- Set your preferred **loglevel**.
- Set the **logfile** to `/var/log/redis_6379.log`
- Set the **dir** to /var/redis/6379 (very important step!)

但之前给出的配置选项应该足以满足本教程的需求。

> **Security Note:** A few years back, the author of Redis pointed out security vulnerabilities in earlier versions of Redis if no configuration was set. Redis 3.2 (the current version 5.0.3 as of March 2019) made steps to prevent this intrusion, setting the `protected-mode` option to `yes` by default.
>
> We explicitly set `bind 127.0.0.1` to let Redis listen for connections only from the localhost interface, although you would need to expand this whitelist in a real production server. The point of `protected-mode` is as a safeguard that will mimic this bind-to-localhost behavior if you don’t otherwise specify anything under the `bind` option.



## 介绍 Redis

本节将为你提供足够多的 Redis 知识，并概述其设计（*design*）和基本用法。

### Getting Started

Redis 拥有 client-server 体系结构（*architecture* ），并使用 request-response 模型（*model*）。这意味着默认情况下 client 会使用 TCP 协议在 6379 端口上连接 Redis 服务器。client 在进行请求操作（比如执行 reading, writing, getting, setting, updating）时，server 便会响应这些请求。

client-server 应用程序的特点是，多个 client 可与同一个 server 进行通信。每个 client 在各自的 socket 上执行（通常是阻塞）读取，并等待服务器响应。

在 Linux 中成功安装 Redis 后，在其 `src` 目录中包含以下可执行文件：

- **redis-server** is the Redis Server itself.
- **redis-sentinel** is the Redis Sentinel executable (monitoring and failover).
- [**redis-cli**](https://redis.io/topics/rediscli) is the command line interface utility to talk with Redis.
- **redis-benchmark** is used to check Redis performances.
- **redis-check-aof** and **redis-check-dump** are useful in the rare event of corrupted data files.

client 程序 redis-cli 的运行方式与 Python 类似，当你在命令行中运行 redis-cli 时，便会进入交互式 REPL（Read Eval Print Loop）模式。

在运行 clinet 程序时，需要先启动 redis-server，这样 clinet 程序才能与 server 进行通讯。开发过程中我们通常会在 localhost（IPv4 address `127.0.0.1`）上启动服务器，这也是默认配置。在启动 Redis 服务器时，我们还可以向其传递配置文件，这好比将配置文件中的所有 key-value 对设置为命令行参数。

```shell
$ redis-server /etc/redis/6379.conf
31829:C 07 Mar 2019 08:45:04.030 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
31829:C 07 Mar 2019 08:45:04.030 # Redis version=5.0.3, bits=64, commit=00000000, modified=0, pid=31829, just started
31829:C 07 Mar 2019 08:45:04.030 # Configuration loaded
```

配置项 `daemonize` 值为 yes，表示 server 在后台运行。也可以在启动 redis-server 时，使用命令行参数 `--daemonize yes`。

在 redis-server 成功运行后，便可启动 redis-cli 了。在命令行中键入 redis-cli 后，便会进入交互式 REPL 模式，如下：

```
127.0.0.1:6379>
```

可以使用 `PING` 命令来和服务器之间的连接状态，如果返回 `PONG` 则表示一切正常：

```
127.0.0.1:6379> PING
PONG
```

注意：Redis 命令不区分大小写。

在 Linux 中，还有另一种检测服务器状态的方法：使用 `pgrep` 来搜索 Redis 服务器的进程 ID

```shell
$ pgrep redis-server
26983
```

要终止 Redis 服务器，请使用命令 `pkill redis-server`。在Mac OS X上，还可以使用 `redis-cli shutdown`。

接下来，我们将会看到一些常见的 Redis 命令，并且会将它们与纯 Python 中的类似对象进行比较。

### Redis as a Python Dictionary

Redis 是 Remote Dictionary Service 的缩写，即远程字典服务，特点如下：

- Redis 以 key-value 对形式存储数据，并支持数百种[附加命令](https://redis.io/commands)（如 GET、SET、DEL）
- Redis 中的 key 始终是字符串
- Redis 中的 value 有多种可选数据类型。本教程会介绍一些基本的 value 数据类型：string、list、hashes、sets 。高级 value 数据类型有 [geospatial items](https://redis.io/commands#geo) 和 [stream](https://redis.io/commands#stream) 
- 大多数 Redis 命令的时间复杂度是 $O(1)$ ，道理和在 Python 字典或 hash 表中检索数据一致

官方将 Redis 称为数据结构服务器（*data structure server*），是因为相较于 [memcached](https://www.memcached.org/) 这样的 key-value store 而言，Redis 支持 key-value 数据类型不只是 string-string。Redis 中的 value 可以是字符串（*String*）、哈希（*Hash*）、 列表（*list*）、 集合（set）、有序集合（*sorted set*）和位图（*bitmaps*）等类型。

为了便于读者理解 Redis 中的 key-value，这里先用我们熟知的 Python 字典来进行对比介绍。我们的第一个 demo 数据库（ID 0）是 string-string 映射 country-capital_city：

```shell
127.0.0.1:6379> SET Bahamas Nassau
OK
127.0.0.1:6379> SET Croatia Zagreb
OK
127.0.0.1:6379> GET Croatia
"Zagreb"
127.0.0.1:6379> GET Japan
(nil)
```

在纯 Python 上述映射可表示为：

```python
>>> capitals = {}
>>> capitals["Bahamas"] = "Nassau"
>>> capitals["Croatia"] = "Zagreb"
>>> capitals.get("Croatia")
'Zagreb'
>>> capitals.get("Japan")  # None
```

这里使用 `capitals.get("Japan")` 而不是 `capitals["Japan"]`，是因为当 key 不存在时，Redis 将返回 `nil`（不会抛出 error）。这样的工作方式与 `dict.get()` 更加类似。

Redis 允许在一条命令中设置（[`MSET`](https://redis.io/commands/mset)）或获取（[`MGET`](https://redis.io/commands/mget)）多个 key-value 对：

```shell
127.0.0.1:6379> MSET Lebanon Beirut Norway Oslo France Paris
OK
127.0.0.1:6379> MGET Lebanon Norway Bahamas
1) "Beirut"
2) "Oslo"
3) "Nassau"
```

在纯 Python 可使用 `dict.update()` 近似模拟上述命令：

```python
>>> capitals.update({
...     "Lebanon": "Beirut",
...     "Norway": "Oslo",
...     "France": "Paris",
... })
>>> [capitals.get(k) for k in ("Lebanon", "Norway", "Bahamas")]
['Beirut', 'Oslo', 'Nassau']
```

使用 `.get()` （而不是 `.__getitem__()`）来模仿 Redis 的行为，是因为当 key 不存在时 Redis 会返回 null-like 值。

Redis 中的 [`EXISTS`](https://redis.io/commands/exists) 命令被用来检查 key 是否存在：

```shell
127.0.0.1:6379> EXISTS Norway
(integer) 1
127.0.0.1:6379> EXISTS Sweden
(integer) 0
```

在纯 Python 中可使用成员测试 `in` 来模拟 `EXISTS` 命令，成员测试 `in` 对应 `dict.__contains__()` 方法。

```python
>>> "Norway" in capitals
True
>>> "Sweden" in capitals
False
```

上述三个示例意在展示 Redis 命令与纯 Python 中类似功能的区别：

| Redis                                        | Python                                                       |
| -------------------------------------------- | ------------------------------------------------------------ |
| SET Bahamas Nassau                           | capitals["Bahamas"] = "Nassau"                               |
| GET Croatia                                  | capitals.get("Croatia")                                      |
| MSET Lebanon Beirut Norway Oslo France Paris | capitals.update( {  "Lebanon": "Beirut", "Norway": "Oslo", "France": "Paris",  } ) |
| MGET Lebanon Norway Bahamas                  | [capitals[k] for k in ("Lebanon", "Norway", "Bahamas")]      |
| EXISTS Norway                                | "Norway" in capitals                                         |

注意：目前并没有在 Python 中使用 Redis 客户端。

Python Redis 客户端库 redis-py 封装了与 Redis 服务器通讯的 TCP 连接，并将原始命令发送给服务器。原始命令是经过 [REdis Serialization Protocol](https://redis.io/topics/protocol) (RESP) 协议处理的字节序列。redis-py 在接受到来自服务的原始回复信息后，会按照 RESP 协议将其解析回 Python 对象，如 `bytes`、`int`，甚至是 `datetime.datetime`。

### More Data Types in Python vs Redis

再说一遍，Redis 中的 key 始终是 string，但是可用于 value 的数据类型（或数据结构）却不仅限于 string。

hash 是 string-stirng 映射，又称 field-value 对，应位于一个顶层 key 的下方。

下面为 'realpython' 键设置了三个 field-value 对。

```
127.0.0.1:6379> HSET realpython url "https://realpython.com/"
(integer) 1
127.0.0.1:6379> HSET realpython github realpython
(integer) 1
127.0.0.1:6379> HSET realpython fullname "Real Python"
(integer) 1
```

Redis hash 大致类似于经过一层嵌套的 Python 字典：

```python
data = {
    "realpython": {
        "url": "https://realpython.com/",
        "github": "realpython",
        "fullname": "Real Python",
    }
}
```

Redis 中的 field 类似于 `data` 内层字典中的 key，Redis 用术语 key 来描述 hash 结构顶层的键。因此，'realpython' 是 key，'url' 是 field，"https://realpython.com/" 是 value。

Redis 允许在一条命令中设置（[`MSET`](https://redis.io/commands/mset)）基本 string:string 键值对，[`HMSET`](https://redis.io/commands/hmset) 



## 待完工...:construction:

