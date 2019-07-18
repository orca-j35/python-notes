# input

```python
input(prompt=None, /)
    Read a string from standard input.  The trailing newline is stripped.
    
    The prompt string, if given, is printed to standard output without a
    trailing newline before reading input.
    
    If the user hits EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return), raise EOFError.
    On *nix systems, readline is used if available.v 
```

🔨 input([*prompt*])

如果提供了 *prompt*，则会将其写入至标准输出，并且不会在其末尾添加换行符(*newline*)。然后程序会暂停运行，以等待用户输入。当用户按下回车键(Return or Enter)后，程序会恢复执行，并以字符串形式返回用户键入的内容(尾部换行符会被剥离)。

```python
>>> s = input('--> ')  
--> Monty Python's Flying Circus
>>> s  
"Monty Python's Flying Circus"
```

如果 `input()` 读取到了 EOF，则会抛出 [`EOFError`](https://docs.python.org/3.7/library/exceptions.html#EOFError) 异常；另外，还可以使用键盘中断。

```python
# EOF (*nix: Ctrl-D, Windows: Ctrl-Z+Return, IDLE shell: Ctrl-D)
>>> input('输入内容:')
输入内容:
Traceback (most recent call last):
  File "<pyshell#54>", line 1, in <module>
    input('输入内容:')
EOFError: EOF when reading a line

# 键盘中断是 Ctrl-C
>>> input('输入内容:')
输入内容:
Traceback (most recent call last):
  File "<pyshell#50>", line 1, in <module>
    input('输入内容:')
KeyboardInterrupt
```

该函数对应 Python 2 中的 `raw_input` 函数。

如果加载了 [`readline`](https://docs.python.org/3.7/library/readline.html#module-readline) 模块，则 `input()` 将使用该模块来提供复杂的行编辑功能和历史记录功能。





