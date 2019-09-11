# 如何在Python中使用Redis
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本文翻译自 [How to Use Redis With Python](https://realpython.com/python-redis/)，但我只翻译了重要的部分，一些引导性的语言并没有翻译

教程内容简介：

- 从源代码安装 Redis 并了解生成的二进制文件的用途
- 了解一点和 Redis 相关的知识，包括语法、协议和 design
- 掌握 redis-py，同时看看它如何实现 Redis 协议
- 设置 Amazon ElastiCache Redis 服务器实例，并与之通信

## 从源代码安装 Redis

本节内容针对 Mac OS X 或 Linux 展开。如果你使用的是 Windows，则应安装 Redis 的 Microsoft [分支](https://github.com/MicrosoftArchive/redis)。Windows 版本远低于 Linux 版本，最好在 Linux 上使用 Redis。

首先，你需要下载包含 Redis 源代码的压缩包（*tarball）：

```shell
$ redisurl="http://download.redis.io/redis-stable.tar.gz"
$ curl -s -o redis-stable.tar.gz $redisurl
```

接下来，切换到 `root` 并将源代码解压至 `/usr/local/lib/`：

```shell
$ sudo su root
$ mkdir -p /usr/local/lib/
$ chmod a+w /usr/local/lib/
$ tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
```

--snip--
我手上这台 Windows 只有 WSL，目前无法成功安装，先跳过这部分内容，详见 https://realpython.com/python-redis/#installing-redis-from-source

## 配置 Redis

Redis 具备高度的可配置性。虽然它开箱即用，但我们需要设置一下与数据库持久性和基本安全相关的基本配置选项：

```shell
$ sudo su root
$ mkdir -p /etc/redis/
$ touch /etc/redis/6379.conf
```

将以下内容写入 `/etc/redis/6379.conf`，在之后的教程中会逐步介绍这些配置选项。

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



## 待完工...:construction:

