# lambda
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:﹝流畅的 Python﹞-> 5.3 匿名函数 
>
> 扩展阅读: [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html#functional-programming-howto) -> [Small functions and the lambda expression](https://docs.python.org/3/howto/functional.html#small-functions-and-the-lambda-expression)

Lambda 表达式的语法如下：

```
lambda_expr        ::=  "lambda" [parameter_list] ":" expression
lambda_expr_nocond ::=  "lambda" [parameter_list] ":" expression_nocond
```

Lambda 表达式(也称 lambda 表单)被用于创建匿名函数，可用于任何需要函数对象的地方。使用 `lambda` 表达式创建的函数不能包含语句或注释。

表达式 `lambda parameters: expression` 会产生一个匿名函数对象，其行为与通过以下方式定义的函数相同：(`parameter_list` 的相关语法需查看 [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function) 。)

```python
# lambda parameters: expression 等效于
def <lambda>(parameter_list):
    return expression
```

`lambda` 句法只是语法糖，它与 `def` 语句一样，都会创建函数对象，并且同样可以为匿名函数指定函数名。

由于 `lambda` 属于表达式而非语句，所以在 `lambda` 函数的定义体中只能使用纯表达式。换句话说，`lambda` 函数的定义体中不能赋值，也不能使用 `while` , `try` , `return` 等语句。`lambda` 函数的返回值就是 `expression` 的结果。

`lambda` 函数同样支持闭包：(关于闭包，详见﹝闭包.md﹞)

```python
def to_hex(x):
    return lambda y:hex(x+y) # 将匿名函数用作返回值
avg = to_hex(10)
avg(2) #> '0xc'
avg.__code__.co_varnames #> ('y',)
avg.__code__.co_freevars #> ('x',)
avg.__closure__ #> (<cell at 0x000002DC44F16348: int object at 0x000000005833C810>,)
avg.__closure__[0].cell_contents #> 10
```

## 使用场景

在参数列表中最适合使用匿名函数，例如：

```python
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=lambda word: word[::-1])
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
```

除了作为参数传给高阶函数之外，Python 很少使用匿名函数。由于句法上的限制，非平凡的 `lambda` 表达式要么难以阅读，要么无法写出。