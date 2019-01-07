# 注释和注解(Comment&Annotation)
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

## 注释

Comments

> 参考：﹝2. Lexical analysis.md﹞-> 2.1.3. 注释
>
> 扩展阅读：[*Code tells you how, comments should tell you why*](http://www.codinghorror.com/blog/2006/12/code-tells-you-how-comments-tell-you-why.html).

在 Python 中，注释以 hash ( `#` ) 字符开头，并延伸到物理行的结尾。除非调用了隐式行连接规则，否则注释便意味着结束当前逻辑行。语法分析会忽略注释，因为注释不属于语言符号(*tokens*)。注释可能出现在行的开头， 或跟在空格和代码后面， 但不会出现在字符串字面量中。因为，字符串字面值中的 hash 字符仅被视作单个字符，没有注释功能。

```python
# this is the first comment
spam = 1 # and this is the second comment
# ... and now a third!
text = "# This is not a comment because it's inside quotes."
```

在遇到以下场景时，最好考虑使用注释：

- explain assumptions 解释假设
- explain important decisions 解释重要的决定
- explain important details 解释重要的细节
- explain problems you're trying to solve 解释你想要解决的问题
- explain problems you're trying to overcome in your program, etc. 解释你在程序中尝试克服的问题，等。

## 注解

todo： [**PEP 484**](https://www.python.org/dev/peps/pep-0484) and [**PEP 526**](https://www.python.org/dev/peps/pep-0526), 

Annotations

> 参考：
>
> - [annotation](https://docs.python.org/3.7/glossary.html#term-annotation)
> - [variable annotation](https://docs.python.org/3.7/glossary.html#term-variable-annotation)
> - [function annotation](https://docs.python.org/3.7/glossary.html#term-function-annotation)
> - [type hint](https://docs.python.org/3.7/glossary.html#term-type-hint)

注解([*annotation*](https://docs.python.org/3.7/glossary.html#term-annotation))是与变量、类属性、函数形参、函数返回值相关联的标签，通常会将注解用作类型提示([*type* *hint*](https://docs.python.org/3.7/glossary.html#term-type-hint))

无法在运行时(*runtime*)访问局部变量的注解，但是会将全局变量、类属性和函数的注解分别存储到模块、类、函数的 `__annotations__` 属性中。

See [variable annotation](https://docs.python.org/3.7/glossary.html#term-variable-annotation), [function annotation](https://docs.python.org/3.7/glossary.html#term-function-annotation), [**PEP 484**](https://www.python.org/dev/peps/pep-0484) and [**PEP 526**](https://www.python.org/dev/peps/pep-0526), which describe this functionality.

### 变量注解

> 扩展阅读：
>
> - [PEP 526 -- Syntax for Variable Annotations](https://www.python.org/dev/peps/pep-0526/)
> - What’s New In Python 3.6 -> [PEP 526: Syntax for variable annotations](https://docs.python.org/3.7/whatsnew/3.6.html?highlight=annotation#pep-526-syntax-for-variable-annotations)

变量注解([*variable* *annotation*](https://docs.python.org/3.7/glossary.html#term-variable-annotation))用于为变量或类属性提供注解。

在对变量或类进行注解时，可以不进行赋值操作：

```python
primes: List[int] = []

captain: str  # Note: no initial value!

class Starship:
    stats: Dict[str, int] = {}
        

class C:
    field: 'annotation'

print(C.__annotations__) #> {'field': 'annotation'}
```

通常会将变量注解用作类型提示([*type* *hint*](https://docs.python.org/3.7/glossary.html#term-type-hint))，例如下面这个变量期望获得 [`int`](https://docs.python.org/3.7/library/functions.html#int) 类型的值：

```python
count: int = 0
```

变量注解的语法在 [Annotated assignment statements](https://docs.python.org/3.7/reference/simple_stmts.html#annassign) 中进行了解释。

See [function annotation](https://docs.python.org/3.7/glossary.html#term-function-annotation), [**PEP 484**](https://www.python.org/dev/peps/pep-0484) and [**PEP 526**](https://www.python.org/dev/peps/pep-0526), which describe this functionality.

### 函数注解

函数注解([function annotation](https://docs.python.org/3.7/glossary.html#term-function-annotation))用于为函数形参或返回值提供注解。

通常会将函数注解用作类型提示([*type* *hint*](https://docs.python.org/3.7/glossary.html#term-type-hint))，例如下面这个函数期望获得两个 [`int`](https://docs.python.org/3.7/library/functions.html#int) 类型的实参，并且还应该具备 [`int`](https://docs.python.org/3.7/library/functions.html#int) 类型的返回值：

```python
def sum_two_numbers(a: int, b: int) -> int:
   return a + b
```

在 [Function definitions](https://docs.python.org/3.7/reference/compound_stmts.html#function) 对函数注解的语法进行了解释。

See [variable annotation](https://docs.python.org/3.7/glossary.html#term-variable-annotation) and [**PEP 484**](https://www.python.org/dev/peps/pep-0484), which describe this functionality.

### 类型提示

类型提示([*type* *hint*](https://docs.python.org/3.7/glossary.html#term-type-hint))其实就是一个注解，该注解用于指定变量、类属性、函数形参、函数返回值期望的类型。

类型提示是可选的，并不要求强制实施，但它对静态类型分析工具很有用，并且可以帮助 IDE 完成代码补全和代码重构。

可使用 [`typing.get_type_hints()`](https://docs.python.org/3.7/library/typing.html#typing.get_type_hints) 访问全局变量、类属性、函数的类型提示，但是不能访问本地变量的类型提示。

See [`typing`](https://docs.python.org/3.7/library/typing.html#module-typing) and [**PEP 484**](https://www.python.org/dev/peps/pep-0484), which describe this functionality.

### 



“[Python 的函数注解](https://segmentfault.com/a/1190000005173184)”

Python 3.x 引入了函数注解。

https://www.python.org/dev/peps/pep-3107/

普通的自定义函数如下：

```
def dog(name, age, species):
    return (name, age, species)
```

添加函数注解后的代码：

```
def dog(name:str, age:(1, 99), species:'品种') -> tuple:
    return (name, age, species)
```

- `:` 冒号：用于对参数逐个进行注解，注解的内容可以是任何形式，比如参数的类型、作用、取值范围等等
- `->` ：用于定义返回注解 (Return annotations)

函数注解以字典的形式被存储在该函数的 `__annotations__` 属性中，对函数的其它部分没有任何影响。

```
In [7]: dog.__annotations__
Out[7]: {'age': (1, 99), 'name': str, 'return': tuple, 'species': '品种'}
```

默认参数的添加位置：

```
In [8]: def dog(name:str ='dobi', age:(1, 99) =3, species:'品种' ='Labrador') -> tuple:
   ...:     return (name, age, species)
   ...:

In [9]: dog()
Out[9]: ('dobi', 3, 'Labrador')
```

示例：

```
>>> def f(ham: str, eggs: str = 'eggs') -> str:
...     print("Annotations:", f.__annotations__)
...     print("Arguments:", ham, eggs)
...     return ham + ' and ' + eggs
...
>>> f('spam')
Annotations: {'ham': <class 'str'>, 'return': <class 'str'>, 'eggs': <class 'str'>}
Arguments: spam eggs
'spam and eggs'
```



