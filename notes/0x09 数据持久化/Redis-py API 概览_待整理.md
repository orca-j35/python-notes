

# Redis-py API 概览

> 本笔记内容取自：https://python3webspider.cuiqingcai.com/5.3-fei-guan-xi-xing-shu-ju-ku-cun-chu#5-3-2redis-cun-chu
>
> 是直接复制过来的，并未仔细核对过

## 键操作

表 5-5 总结了键的一些判断和操作方法。

表 5-5 键的一些判断和操作方法

| 方　　法           | 作　　用                                      | 参数说明                   | 示　　例                         | 示例说明                        | 示例结果  |
| ------------------ | --------------------------------------------- | -------------------------- | -------------------------------- | ------------------------------- | --------- |
| exists(name)       | 判断一个键是否存在                            | name：键名                 | redis.exists('name')             | 是否存在 name 这个键            | True      |
| delete(name)       | 删除一个键                                    | name：键名                 | redis.delete('name')             | 删除 name 这个键                | 1         |
| type(name)         | 判断键类型                                    | name：键名                 | redis.type('name')               | 判断 name 这个键类型            | b'string' |
| keys(pattern)      | 获取所有符合规则的键                          | pattern：匹配规则          | redis.keys('n*')                 | 获取所有以 n 开头的键           | [b'name'] |
| randomkey()        | 获取随机的一个键                              |                            | randomkey()                      | 获取随机的一个键                | b'name'   |
| rename(src, dst)   | 重命名键                                      | src：原键名；dst：新键名   | redis.rename('name', 'nickname') | 将 name 重命名为 nickname       | True      |
| dbsize()           | 获取当前数据库中键的数目                      |                            | dbsize()                         | 获取当前数据库中键的数目        | 100       |
| expire(name, time) | 设定键的过期时间，单位为秒                    | name：键名；time：秒数     | redis.expire('name', 2)          | 将 name 键的过期时间设置为 2 秒 | True      |
| ttl(name)          | 获取键的过期时间，单位为秒，1 表示永久不过期 | name：键名                 | redis.ttl('name')                | 获取 name 这个键的过期时间      | 1        |
| move(name, db)     | 将键移动到其他数据库                          | name：键名；db：数据库代号 | move('name', 2)                  | 将 name 移动到 2 号数据库       | True      |
| flushdb()          | 删除当前选择数据库中的所有键                  |                            | flushdb()                        | 删除当前选择数据库中的所有键    | True      |
| flushall()         | 删除所有数据库中的所有键                      |                            | flushall()                       | 删除所有数据库中的所有键        | True      |



## 字符串操作

Redis 支持最基本的键值对形式存储，用法总结如表 5-6 所示。

表 5-6 键值对形式存储

| 方　　法                      | 作　　用                                                     | 参数说明                                                     | 示　　例                                                     | 示例说明                                                  | 示例结果                                      |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | --------------------------------------------------------- | --------------------------------------------- |
| set(name, value)              | 给数据库中键名为 name 的 string 赋予值 value                 | n ame：键名；value：值                                       | redis.set('name', 'Bob')                                     | 给 name 这个键的 value 赋值为 Bob                         | True                                          |
| get(name)                     | 返回数据库中键名为 name 的 string 的 value                   | name：键名                                                   | redis.get('name')                                            | 返回 name 这个键的 value                                  | b'Bob'                                        |
| getset(name, value)           | 给数据库中键名为 name 的 string 赋予值 value 并返回上次的 value | name：键名；value：新值                                      | redis.getset('name', 'Mike')                                 | 赋值 name 为 Mike 并得到上次的 value                      | b'Bob'                                        |
| mget(keys, *args)             | 返回多个键对应的 value 组成的列表                            | keys：键名序列                                               | redis.mget(['name', 'nickname'])                             | 返回 name 和 nickname 的 value                            | [b'Mike', b'Miker']                           |
| setnx(name, value)            | 如果不存在这个键值对，则更新 value，否则不变                 | name：键名                                                   | redis.setnx('newname', 'James')                              | 如果 newname 这个键不存在，则设置值为 James               | 第一次运行结果是 True，第二次运行结果是 False |
| setex(name, time, value)      | 设置可以对应的值为 string 类型的 value，并指定此键值对应的有效期 | n ame：键名；time：有效期；value：值                         | redis.setex('name', 1, 'James')                              | 将 name 这个键的值设为 James，有效期为 1 秒               | True                                          |
| setrange(name, offset, value) | 设置指定键的 value 值的子字符串                              | name：键名；offset：偏移量；value：值                        | redis.set('name', 'Hello') redis.setrange ('name', 6, 'World') | 设置 name 为 Hello 字符串，并在 index 为 6 的位置补 World | 11，修改后的字符串长度                        |
| mset(mapping)                 | 批量赋值                                                     | mapping：字典或关键字参数                                    | redis.mset({'name1': 'Durant', 'name2': 'James'})            | 将 name1 设为 Durant，name2 设为 James                    | True                                          |
| msetnx(mapping)               | 键均不存在时才批量赋值                                       | mapping：字典或关键字参数                                    | redis.msetnx({'name3': 'Smith', 'name4': 'Curry'})           | 在 name3 和 name4 均不存在的情况下才设置二者值            | True                                          |
| incr(name, amount=1)          | 键名为 name 的 value 增值操作，默认为 1，键不存在则被创建并设为 amount | name：键名；amount：增长的值                                 | redis.incr('age', 1)                                         | age 对应的值增 1，若不存在，则会创建并设置为 1            | 1，即修改后的值                               |
| decr(name, amount=1)          | 键名为 name 的 value 减值操作，默认为 1，键不存在则被创建并将 value 设置为 - amount | name：键名；amount：减少的值                                 | redis.decr('age', 1)                                         | age 对应的值减 1，若不存在，则会创建并设置为1            | 1，即修改后的值                              |
| append(key, value)            | 键名为 key 的 string 的值附加 value                          | key：键名                                                    | redis.append('nickname', 'OK')                               | 向键名为 nickname 的值后追加 OK                           | 13，即修改后的字符串长度                      |
| substr(name, start, end=-1)   | 返回键名为 name 的 string 的子字符串                         | name：键名；start：起始索引；end：终止索引，默认为1，表示截取到末尾 | redis.substr('name', 1, 4)                                   | 返回键名为 name 的值的字符串，截取索引为 1~4 的字符       | b'ello'                                       |
| getrange(key, start, end)     | 获取键的 value 值从 start 到 end 的子字符串                  | key：键名；start：起始索引；end：终止索引                    | redis.getrange('name', 1, 4)                                 | 返回键名为 name 的值的字符串，截取索引为 1~4 的字符       | b'ello'                                       |



## 列表操作

Redis 还提供了列表存储，列表内的元素可以重复，而且可以从两端存储，用法如表 5-7 所示。

表 5-7 列表操作

| 方　　法                 | 作　　用                                                     | 参数说明                                            | 示　　例                         | 示例说明                                                     | 示例结果           |
| ------------------------ | ------------------------------------------------------------ | --------------------------------------------------- | -------------------------------- | ------------------------------------------------------------ | ------------------ |
| rpush(name, *values)     | 在键名为 name 的列表末尾添加值为 value 的元素，可以传多个    | name：键名；values：值                              | redis.rpush('list', 1, 2, 3)     | 向键名为 list 的列表尾添加 1、2、3                           | 3，列表大小        |
| lpush(name, *values)     | 在键名为 name 的列表头添加值为 value 的元素，可以传多个      | name：键名；values：值                              | redis.lpush('list', 0)           | 向键名为 list 的列表头部添加 0                               | 4，列表大小        |
| llen(name)               | 返回键名为 name 的列表的长度                                 | name：键名                                          | redis.llen('list')               | 返回键名为 list 的列表的长度                                 | 4                  |
| lrange(name, start, end) | 返回键名为 name 的列表中 start 至 end 之间的元素             | name：键名；start：起始索引；end：终止索引          | redis.lrange('list', 1, 3)       | 返回起始索引为 1 终止索引为 3 的索引范围对应的列表           | [b'3', b'2', b'1'] |
| ltrim(name, start, end)  | 截取键名为 name 的列表，保留索引为 start 到 end 的内容       | name：键名；start：起始索引；end：终止索引          | ltrim('list', 1, 3)              | 保留键名为 list 的索引为 1 到 3 的元素                       | True               |
| lindex(name, index)      | 返回键名为 name 的列表中 index 位置的元素                    | name：键名；index：索引                             | redis.lindex('list', 1)          | 返回键名为 list 的列表索引为 1 的元素                        | b'2'               |
| lset(name, index, value) | 给键名为 name 的列表中 index 位置的元素赋值，越界则报错      | name：键名；index：索引位置；value：值              | redis.lset('list', 1, 5)         | 将键名为 list 的列表中索引为 1 的位置赋值为 5                | True               |
| lrem(name, count, value) | 删除 count 个键的列表中值为 value 的元素                     | name：键名；count：删除个数；value：值              | redis.lrem('list', 2, 3)         | 将键名为 list 的列表删除两个 3                               | 1，即删除的个数    |
| lpop(name)               | 返回并删除键名为 name 的列表中的首元素                       | name：键名                                          | redis.lpop('list')               | 返回并删除名为 list 的列表中的第一个元素                     | b'5'               |
| rpop(name)               | 返回并删除键名为 name 的列表中的尾元素                       | name：键名                                          | redis.rpop('list')               | 返回并删除名为 list 的列表中的最后一个元素                   | b'2'               |
| blpop(keys, timeout=0)   | 返回并删除名称在 keys 中的 list 中的首个元素，如果列表为空，则会一直阻塞等待 | keys：键名序列；timeout：超时等待时间，0 为一直等待 | redis.blpop('list')              | 返回并删除键名为 list 的列表中的第一个元素                   | [b'5']             |
| brpop(keys, timeout=0)   | 返回并删除键名为 name 的列表中的尾元素，如果 list 为空，则会一直阻塞等待 | keys：键名序列；timeout：超时等待时间，0 为一直等待 | redis.brpop('list')              | 返回并删除名为 list 的列表中的最后一个元素                   | [b'2']             |
| rpoplpush(src, dst)      | 返回并删除名称为 src 的列表的尾元素，并将该元素添加到名称为 dst 的列表头部 | src：源列表的键；dst：目标列表的 key                | redis.rpoplpush('list', 'list2') | 将键名为 list 的列表尾元素删除并将其添加到键名为 list2 的列表头部，然后返回 | b'2'               |



## 集合操作

Redis 还提供了集合存储，集合中的元素都是不重复的，用法如表 5-8 所示。

表 5-8 集合操作

| 方　　法                       | 作　　用                                                 | 参数说明                                  | 示　　例                                        | 示例说明                                                     | 示例结果                     |
| ------------------------------ | -------------------------------------------------------- | ----------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------ | ---------------------------- |
| sadd(name, *values)            | 向键名为 name 的集合中添加元素                           | name：键名；values：值，可为多个          | redis.sadd('tags', 'Book', 'Tea', 'Coffee')     | 向键名为 tags 的集合中添加 Book、Tea 和 Coffee 这 3 个内容   | 3，即插入的数据个数          |
| srem(name, *values)            | 从键名为 name 的集合中删除元素                           | name：键名；values：值，可为多个          | redis.srem('tags', 'Book')                      | 从键名为 tags 的集合中删除 Book                              | 1，即删除的数据个数          |
| spop(name)                     | 随机返回并删除键名为 name 的集合中的一个元素             | name：键名                                | redis.spop('tags')                              | 从键名为 tags 的集合中随机删除并返回该元素                   | b'Tea'                       |
| smove(src, dst, value)         | 从 src 对应的集合中移除元素并将其添加到 dst 对应的集合中 | src：源集合；dst：目标集合；value：元素值 | redis.smove('tags', 'tags2', 'Coffee')          | 从键名为 tags 的集合中删除元素 Coffee 并将其添加到键为 tags2 的集合 | True                         |
| scard(name)                    | 返回键名为 name 的集合的元素个数                         | name：键名                                | redis.scard('tags')                             | 获取键名为 tags 的集合中的元素个数                           | 3                            |
| sismember(name, value)         | 测试 member 是否是键名为 name 的集合的元素               | name：键值                                | redis.sismember('tags', 'Book')                 | 判断 Book 是否是键名为 tags 的集合元素                       | True                         |
| sinter(keys, *args)            | 返回所有给定键的集合的交集                               | keys：键名序列                            | redis.sinter(['tags', 'tags2'])                 | 返回键名为 tags 的集合和键名为 tags2 的集合的交集            | {b'Coffee'}                  |
| sinterstore(dest, keys, *args) | 求交集并将交集保存到 dest 的集合                         | dest：结果集合；keys：键名序列            | redis.sinterstore ('inttag', ['tags', 'tags2']) | 求键名为 tags 的集合和键名为 tags2 的集合的交集并将其保存为 inttag | 1                            |
| sunion(keys, *args)            | 返回所有给定键的集合的并集                               | keys：键名序列                            | redis.sunion(['tags', 'tags2'])                 | 返回键名为 tags 的集合和键名为 tags2 的集合的并集            | {b'Coffee', b'Book', b'Pen'} |
| sunionstore(dest, keys, *args) | 求并集并将并集保存到 dest 的集合                         | dest：结果集合；keys：键名序列            | redis.sunionstore ('inttag', ['tags', 'tags2']) | 求键名为 tags 的集合和键名为 tags2 的集合的并集并将其保存为 inttag | 3                            |
| sdiff(keys, *args)             | 返回所有给定键的集合的差集                               | keys：键名序列                            | redis.sdiff(['tags', 'tags2'])                  | 返回键名为 tags 的集合和键名为 tags2 的集合的差集            | {b'Book', b'Pen'}            |
| sdiffstore(dest, keys, *args)  | 求差集并将差集保存到 dest 集合                           | dest：结果集合；keys：键名序列            | redis.sdiffstore ('inttag', ['tags', 'tags2'])  | 求键名为 tags 的集合和键名为 tags2 的集合的差集并将其保存为 inttag | 3                            |
| smembers(name)                 | 返回键名为 name 的集合的所有元素                         | name：键名                                | redis.smembers('tags')                          | 返回键名为 tags 的集合的所有元素                             | {b'Pen', b'Book', b'Coffee'} |
| srandmember(name)              | 随机返回键名为 name 的集合中的一个元素，但不删除元素     | name：键值                                | redis.srandmember('tags')                       | 随机返回键名为 tags 的集合中的一个元素                       | Srandmember (name)           |



## 有序集合操作

有序集合比集合多了一个分数字段，利用它可以对集合中的数据进行排序，其用法总结如表 5-9 所示。

表 5-9 有序集合操作

| 方　　法                                                     | 作　　用                                                     | 参数说明                                                     | 示　　例                                    | 示例说明                                                     | 示例结果                            |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------- | ------------------------------------------------------------ | ----------------------------------- |
| zadd(name, *args, **kwargs)                                  | 向键名为 name 的 zset 中添加元素 member，score 用于排序。如果该元素存在，则更新其顺序 | name：键名；args：可变参数                                   | redis.zadd('grade', 100, 'Bob', 98, 'Mike') | 向键名为 grade 的 zset 中添加 Bob（其 score 为 100），并添加 Mike（其 score 为 98） | 2，即添加的元素个数                 |
| zrem(name, *values)                                          | 删除键名为 name 的 zset 中的元素                             | name：键名；values：元素                                     | redis.zrem('grade', 'Mike')                 | 从键名为 grade 的 zset 中删除 Mike                           | 1，即删除的元素个数                 |
| zincrby(name, value, amount=1)                               | 如果在键名为 name 的 zset 中已经存在元素 value，则将该元素的 score 增加 amount；否则向该集合中添加该元素，其 score 的值为 amount | name：键名；value：元素；amount：增长的 score 值             | redis.zincrby('grade', 'Bob', -2)           | 键名为 grade 的 zset 中 Bob 的 score 减 2                    | 98.0，即修改后的值                  |
| zrank(name, value)                                           | 返回键名为 name 的 zset 中元素的排名，按 score 从小到大排序，即名次 | name：键名；value：元素值                                    | redis.zrank('grade', 'Amy')                 | 得到键名为 grade 的 zset 中 Amy 的排名                       | 1                                   |
| zrevrank(name, value)                                        | 返回键为 name 的 zset 中元素的倒数排名（按 score 从大到小排序），即名次 | name：键名；value：元素值                                    | redis.zrevrank ('grade', 'Amy')             | 得到键名为 grade 的 zset 中 Amy 的倒数排名                   | 2                                   |
| zrevrange(name, start, end, withscores= False)               | 返回键名为 name 的 zset（按 score 从大到小排序）中 index 从 start 到 end 的所有元素 | name：键值；start：开始索引；end：结束索引；withscores：是否带 score | redis.zrevrange ('grade', 0, 3)             | 返回键名为 grade 的 zset 中前四名元素                        | [b'Bob', b'Mike', b'Amy', b'James'] |
| zrangebyscore (name, min, max, start=None, num=None, withscores=False) | 返回键名为 name 的 zset 中 score 在给定区间的元素            | name：键名；min：最低 score；max：最高 score；start：起始索引；num：个数；withscores：是否带 score | redis.zrangebyscore ('grade', 80, 95)       | 返回键名为 grade 的 zset 中 score 在 80 和 95 之间的元素     | [b'Bob', b'Mike', b'Amy', b'James'] |
| zcount(name, min, max)                                       | 返回键名为 name 的 zset 中 score 在给定区间的数量            | name：键名；min：最低 score；max：最高 score                 | redis.zcount('grade', 80, 95)               | 返回键名为 grade 的 zset 中 score 在 80 到 95 的元素个数     | 2                                   |
| zcard(name)                                                  | 返回键名为 name 的 zset 的元素个数                           | name：键名                                                   | redis.zcard('grade')                        | 获取键名为 grade 的 zset 中元素的个数                        | 3                                   |
| zremrangebyrank (name, min, max)                             | 删除键名为 name 的 zset 中排名在给定区间的元素               | name：键名；min：最低位次；max：最高位次                     | redis.zremrangebyrank ('grade', 0, 0)       | 删除键名为 grade 的 zset 中排名第一的元素                    | 1，即删除的元素个数                 |
| zremrangebyscore (name, min, max)                            | 删除键名为 name 的 zset 中 score 在给定区间的元素            | name：键名；min：最低 score；max：最高 score                 | redis.zremrangebyscore ('grade', 80, 90)    | 删除 score 在 80 到 90 之间的元素                            | 1，即删除的元素个数                 |



## 散列操作

Redis 还提供了散列表的数据结构，我们可以用 name 指定一个散列表的名称，表内存储了各个键值对，用法总结如表 5-10 所示。

表 5-10 散列操作

| 方　　法                     | 作　　用                                               | 参数说明                                   | 示　　例                                       | 示例说明                                             | 示例结果                                                     |
| ---------------------------- | ------------------------------------------------------ | ------------------------------------------ | ---------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| hset(name, key, value)       | 向键名为 name 的散列表中添加映射                       | name：键名；key：映射键名；value：映射键值 | hset('price', 'cake', 5)                       | 向键名为 price 的散列表中添加映射关系，cake 的值为 5 | 1，即添加的映射个数                                          |
| hsetnx(name, key, value)     | 如果映射键名不存在，则向键名为 name 的散列表中添加映射 | name：键名；key：映射键名；value：映射键值 | hsetnx('price', 'book', 6)                     | 向键名为 price 的散列表中添加映射关系，book 的值为 6 | 1，即添加的映射个数                                          |
| hget(name, key)              | 返回键名为 name 的散列表中 key 对应的值                | name：键名；key：映射键名                  | redis.hget('price', 'cake')                    | 获取键名为 price 的散列表中键名为 cake 的值          | 5                                                            |
| hmget(name, keys, *args)     | 返回键名为 name 的散列表中各个键对应的值               | name：键名；keys：键名序列                 | redis.hmget('price', ['apple', 'orange'])      | 获取键名为 price 的散列表中 apple 和 orange 的值     | [b'3', b'7']                                                 |
| hmset(name, mapping)         | 向键名为 name 的散列表中批量添加映射                   | name：键名；mapping：映射字典              | redis.hmset('price', {'banana': 2, 'pear': 6}) | 向键名为 price 的散列表中批量添加映射                | True                                                         |
| hincrby(name, key, amount=1) | 将键名为 name 的散列表中映射的值增加 amount            | name：键名；key：映射键名；amount：增长量  | redis.hincrby('price', 'apple', 3)             | key 为 price 的散列表中 apple 的值增加 3             | 6，修改后的值                                                |
| hexists(name, key)           | 键名为 name 的散列表中是否存在键名为键的映射           | name：键名；key：映射键名                  | redis.hexists('price', 'banana')               | 键名为 price 的散列表中 banana 的值是否存在          | True                                                         |
| hdel(name, *keys)            | 在键名为 name 的散列表中，删除键名为键的映射           | name：键名；keys：键名序列                 | redis.hdel('price', 'banana')                  | 从键名为 price 的散列表中删除键名为 banana 的映射    | True                                                         |
| hlen(name)                   | 从键名为 name 的散列表中获取映射个数                   | name：键名                                 | redis.hlen('price')                            | 从键名为 price 的散列表中获取映射个数                | 6                                                            |
| hkeys(name)                  | 从键名为 name 的散列表中获取所有映射键名               | name：键名                                 | redis.hkeys('price')                           | 从键名为 price 的散列表中获取所有映射键名            | [b'cake', b'book', b'banana', b'pear']                       |
| hvals(name)                  | 从键名为 name 的散列表中获取所有映射键值               | name：键名                                 | redis.hvals('price')                           | 从键名为 price 的散列表中获取所有映射键值            | [b'5', b'6', b'2', b'6']                                     |
| hgetall(name)                | 从键名为 name 的散列表中获取所有映射键值对             | name：键名                                 | redis.hgetall('price')                         | 从键名为 price 的散列表中获取所有映射键值对          | {b'cake': b'5', b'book': b'6', b'orange': b'7', b'pear': b'6'} |