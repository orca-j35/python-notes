# README
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

目标: 抓取猫眼电影 TOP100 榜中的内容

目标站点: 

```
https://maoyan.com/board/4
```

存储格式:

```json
{
    'index':'排名'
    'image':'图片'
    'title':'名称'
    'actor':'主演'
    'time':'上映时间'
    'score':'分数'
}
```

URL 规律:

```
https://maoyan.com/board/4?offset=0  对应1~10
https://maoyan.com/board/4?offset=10 对应11~20
https://maoyan.com/board/4?offset=20 对应21~30
...
```

