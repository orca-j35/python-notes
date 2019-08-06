# dbm - Unix Key-Value Databases
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本笔记仅作简要介绍，今后还需要补充下述连接中的内容:
>
> - https://pymotw.com/3/dbm/index.html
>
> 参考:
>
> - https://codingpy.com/books/thinkpython2/14-files.html#id7

**数据库**是一个用来存储数据的文件。 大多数的数据库采用类似字典的形式，即将键映射到值。 数据库和字典的最大区别是，数据库是存储在硬盘上（或者其他永久存储中）， 所以即使程序结束，它们依然存在。

`dbm`模块提供了一个创建和更新数据库文件的接口。 举个例子，我接下来创建建一个包含图片文件标题的数据库。

打开数据库和打开其它文件的方法类似：

```
>>> import dbm
>>> db = dbm.open('captions', 'c')
```

模式 `'c'` 代表如果数据库不存在则创建该数据库。 这个操作返回的是一个数据库对象，可以像字典一样使用它（对于大多数操作）。

当你创建一个新项时，`dbm` 将更新数据库文件。

```
>>> db['cleese.png'] = 'Photo of John Cleese.'
```

当你访问某个项时，`dbm` 将读取文件：

```
>>> db['cleese.png']
b'Photo of John Cleese.'
```

返回的结果是一个 **字节对象（bytes object）** ，这就是为什么结果以 `b` 开头。 一个字节对象在很多方面都和一个字符串很像。但是当你深入了解 Python 时， 它们之间的差别会变得很重要，但是目前我们可以忽略掉那些差别。

如果你对已有的键再次进行赋值，`dbm` 将把旧的值替换掉：

```
>>> db['cleese.png'] = 'Photo of John Cleese doing a silly walk.'
>>> db['cleese.png']
b'Photo of John Cleese doing a silly walk.'
```

一些字典方法，例如 `keys` 和 `items` ，不适用于数据库对象，但是 `for` 循环依然适用：

```
for key in db:
    print(key, db[key])
```

与其它文件一样，当你完成操作后需要关闭文件：

```
>>> db.close()
```