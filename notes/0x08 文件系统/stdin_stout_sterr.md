# stdin_stout_sterr
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> ❗待整理
>
> 参考:
>
> - https://docs.python.org/3/library/sys.html#sys.stdin



想要用交互方式读取用户输入，可从文件 `sys.stdin` 中读取。
如果要将数据输出到屏幕上，可以写入文件 `sys.stdout` 中。`print` 在输出数据时，默认使用 `sys.stdout` 。

```
import sys
sys.stdout.write("Enter youe name:")
name = sys.stdin.readline()
```

[File objects](https://docs.python.org/3/glossary.html#term-file-object) used by the interpreter for standard input, output and errors:

- `sys.stdin` is used for all interactive input (including calls to [`input()`](https://docs.python.org/3/library/functions.html#input));
- `sys.stdout` is used for the output of [`print()`](https://docs.python.org/3/library/functions.html#print) and [expression](https://docs.python.org/3/glossary.html#term-expression) statements and for the prompts of [`input()`](https://docs.python.org/3/library/functions.html#input);
- The interpreter’s own prompts and its error messages go to `sys.stderr`.

