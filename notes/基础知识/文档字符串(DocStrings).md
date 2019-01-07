# 文档字符串
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

DocStrings - Documentation Strings

> 参考
>
> - 《数据结构(Python语言描述)》-> 5.1.4 先验条件、后验条件、异常和文档
> - [4.7.6. Documentation Strings](https://docs.python.org/3/tutorial/controlflow.html#documentation-strings)
>   - [4. 深入 Python 流程控制](https://pythoncaff.com/docs/tutorial/3.7.0/controlflow/2041)

如果模块、类或函数定义中的起始语句是字符串，那么该字符串会被视作文档字符串(*DocStrings*)。通过 `__doc__` 属性，可直接获取文档字符的内容。`help()` 函数和 `pydoc` 命令均通过获取对象的 `__doc__` 属性，来提供帮助信息。

文档字符串格式要求如下：

- 文档字符串的缩进必须与定义中的所有其它语句保持一致。
- 虽然可以是 `"..."` 或 `"""..."""` 字符串，但通常是`"""..."""` 多行字符串。
- 如果将 `"""..."""` 用作文档字符串，那么第一行将被视作文档字符的标题，用于概述了对象的用途，并以大写字母开头，同时以点号结尾；第二行是空白行，用于从视觉上将概述部分与其余部分进行分割；从第三行开始是详细记录程序的文档，例如调用约定和副作用等。

Python 解析器不会从 Python 中的多行字符串文字中删除缩进，因此处理文档的工具必须剥离缩进。这点是使用以下的约定完成的。字符串第一行后面的第一个非空行决定了整个文档字符串的缩进量(我们不能使用第一行，因为它通常与字符串的开头引号相邻，所以它的缩进在字符串文字中是不明显的)。每行不应该当有不足的缩进，但是如果有前导空白将会全部清除。由制表符扩展成的空白应该测试是否可用(一般被兑换成 8 个空格)。

以下是个多行文档字符串的例子：

```python
def print_max(x, y):
    '''Prints the maximum of two numbers.

    The two values must be integers.
    '''
    # convert to integers, if possible
    x = int(x)
    y = int(y)

    if x > y:
        print(x, 'is maximum')
    else:
        print(y, 'is maximum')

print_max(3, 5)
print(print_max.__doc__)
```

输出：

```
5 is maximum
Prints the maximum of two numbers.

    The two values must be integers.    
```

