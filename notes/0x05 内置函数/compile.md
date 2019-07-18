# compile

🔨 compile(*source*, *filename*, *mode*, *flags=0*, *dont_inherit=False*, *optimize=-1*)

**Compile** source into a code object that can be executed by exec() or eval().

该函数会将 *source* 编译为 code 对象或 AST(Abstract Syntax Trees)对象。内置函数 `exec()` 和 `eval()` 可执行 code 对象。

如果需要了解如何使用 AST 对象，可阅读 [`ast`](https://docs.python.org/3.7/library/ast.html#module-ast) 模块的文档；如果想要将 Python 代码解析为 AST，请参阅 [`ast.parse()`](https://docs.python.org/3.7/library/ast.html#ast.parse)。

如果被编译的 *source* 无效，则会抛出  [`SyntaxError`](https://docs.python.org/3.7/library/exceptions.html#SyntaxError)；如果 *source* 是空字节，则会抛出 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError)。

注意：在 `'single'` 或 `'eval'` 模式下编译内含多行代码的字符串时，输入必须由至少一个换行符终止。这有助于在 [`code`](https://docs.python.org/3.7/library/code.html#module-code) 模块中检测语句的完整性。

警告：由于 Python 的 AST 编译器存在栈深度限制，所以在将大且复杂的字符串编译为 AST 对象时，可能会使 Python 解析式奔溃。

**Changed in version 3.2**: Allowed use of Windows and Mac newlines. Also input in `'exec'`mode does not have to end in a newline anymore. Added the *optimize* parameter.

**Changed in version 3.5:** Previously, [`TypeError`](https://docs.python.org/3.7/library/exceptions.html#TypeError) was raised when null bytes were encountered in *source*.

**参数说明：**

- *source* - The source code may represent a Python module, statement or expression.

  提供源代码，可以是普通字符串、byte 字符串或 AST 对象。

- *filename* - The filename will be used for run-time error messages.

  - 如果 *source* 是从某个文件中读取的，则应将 *filename* 设置为对应文件的名称；
  - 如果 *source* 并非是从某个文件中读取的，则应向其传递一些可识别的值——通常会使用 `'<string>'`。

  当出现运行时错误时，便会在回溯信息中使用 *filename*，例如：

  ```python
  source_code = 'x=y+1'
  code_obj = compile(source_code, '在这里使用-->filename', mode='exec')
  exec(code_obj)
  '''Out:
  Traceback (most recent call last):
    File "c:/Users/iwhal/Desktop/内置函数/compile.py", line 7, in <module>
      exec(code_obj)
    File "在这里使用-->filename", line 1, in <module>
  NameError: name 'y' is not defined
  '''
  ```

- *mode* -  The mode must be 'exec' to compile a module, 'single' to compile a single (interactive) statement, or 'eval' to compile an expression.

  - 如果 *source* 由语句序列组成，需使用 `mode = 'exec'`；
  - 如果 *source* 由单个表达式组成，需使用 `mode = 'eval'`；
  - 如果 *source* 由单个交互式语句组成，需使用 `mode = 'single'` 。

  当 `mode = 'single'` 时，如果 *source* 的执行结果不是 `None`，则会打印该结果：

  ```python
  code_obj = compile('input("single_请输入:")', '<string>', mode='single')
  exec(code_obj)  # eval(code_obj)等效
  code_obj = compile('input("exec_请输入:")', '<string>', mode='exec')
  exec(code_obj)  # eval(code_obj)等效
  code_obj = compile('input("eval_请输入:")', '<string>', mode='eval')
  eval(code_obj)  # exec(code_obj)等效
  '''Out:
  single_请输入:orca
  'orca'
  exec_请输入:orca
  eval_请输入:orca
  '''
  ```

  示例 - 展示三种模式的效果：

  ```python
  source_code = '''
  x="mode=exec"
  print(x)
  '''
  code_obj = compile(source_code, '<string>', mode='exec')
  exec(code_obj)
  eval(code_obj)  # 编译为code的语句也可被eval执行
  
  code_obj = compile('print("mode=eval")', '<string>', mode='eval')
  exec(code_obj)
  eval(code_obj)
  
  code_obj = compile('input("single_请输入:")', '<string>', mode='single')
  exec(code_obj)
  eval(code_obj)
  """Out:
  mode=exec
  mode=exec
  mode=eval
  mode=eval
  single_请输入:orca
  'orca'
  single_请输入:orca
  'orca'
  """
  ```

- *flags* - The flags argument, if present, controls which future statements influence the compilation of the code. 

  设置影响 *source* 编译的 [future 语句](https://docs.python.org/3.7/reference/simple_stmts.html#future)。

  Future statements are specified by bits which can be bitwise ORed together to specify multiple statements. The bitfield required to specify a given feature can be found as the `compiler_flag` attribute on the `_Feature` instance in the [`__future__`](https://docs.python.org/3.7/library/__future__.html#module-__future__) module. 

  如果不想通过 `_Feature`  实例来设置 *flags*，也可直接使用以下枚举值(两种方法等效)：

  ```python
  # from https://github.com/python/cpython/blob/3.7/Lib/__future__.py
  CO_NESTED            = 0x0010   # nested_scopes
  CO_GENERATOR_ALLOWED = 0        # generators (obsolete, was 0x1000)
  CO_FUTURE_DIVISION   = 0x2000   # division
  CO_FUTURE_ABSOLUTE_IMPORT = 0x4000 # perform absolute imports by default
  CO_FUTURE_WITH_STATEMENT  = 0x8000   # with statement
  CO_FUTURE_PRINT_FUNCTION  = 0x10000   # print function
  CO_FUTURE_UNICODE_LITERALS = 0x20000 # unicode string literals
  CO_FUTURE_BARRY_AS_BDFL = 0x40000
  CO_FUTURE_GENERATOR_STOP  = 0x80000 # StopIteration becomes RuntimeError in generators
  CO_FUTURE_ANNOTATIONS     = 0x100000  # annotations become strings at runtime
  ```

  关于 future 语句，可阅读『[使用 \_\_future\_\_](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386820023084e5263fe54fde4e4e8616597058cc4ba1000#0)』和『[Future statement definitions](https://docs.python.org/3.7/library/__future__.html#module-__future__)』

- *dont_inherit* - The dont_inherit argument, if true, stops the compilation inheriting the effects of any future statements in effect in the code calling compile; if absent or false these statements do influence the compilation, in addition to any features explicitly specified.

  - 如果 *flages* 和 *dont_inherit* 均保持默认值，则使用在调用 `compile()` 的代码中有效的 future 语句来编译 *source*。
  - 如果 *flages* 非零，且 *dont_inherit* 保持默认值，则会使用在调用 `compile()` 的代码中有效的 future 语句，以及 *flags* 中指定的 future 语句来编译 *source*。
  - 如果 `dont_inherit = Ture`，则会忽略在调用 `compile()` 的代码中有效的 future 语句，只使用 *flags* 中指定的 future 语句来编译 *source*。

- *optimize* - 设置编译器的优化级别

  The default value of `-1` selects the optimization level of the interpreter as given by [`-O`](https://docs.python.org/3.7/using/cmdline.html#cmdoption-o) options. Explicit levels are `0` (no optimization; `__debug__` is true), `1` (asserts are removed, `__debug__` is false) or `2` (docstrings are removed too).

一些示例：

```python

```

