# PyCharm
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

一直显示 connecting to console

```
1、打开Anaconda cmd(也就是Anaconda Prompt，在启动栏Anaconda目录里应该有)
2、输入echo %PATH% 获得PATH value
如果是使用win7系统，在电脑的cmd中输入 echo %PATH% > path_val.txt
3、在PyCharm中, files -> Settings -> Build, Execution, Deployment -> Console -> Python Console -> 点击Environment variables的文件夹符号
4、点击+号，增加新的Environment Variable； name中输入PATH ，value中复制输入前边通过echo %PATH% 的结果
5、点击OK，然后点击apply
6、完成
```

