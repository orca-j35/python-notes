# VSCode
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

如果 IntelliSense 或 IntelliCode 异常，可尝试进行如下设置:

```json
// Enables Jedi as IntelliSense engine instead of Microsoft Python Analysis Engine.
"python.jediEnabled": true,

// Enable Visual Studio IntelliCode completions for Python
"vsintellicode.python.completionsEnabled": fasle,
```

如果在用户设置界面中不会将"原始默认配置"显示为 JSON，可进行如下设置:

```json
// 控制在将设置编辑为 json 时是否使用拆分 json 编辑器。
"workbench.settings.useSplitJSON": true
```

如果想要查看"原始默认配置"，可在 `cmd +shift + p` 中搜索 `Open Raw Default Settings`，并打开相应条目。