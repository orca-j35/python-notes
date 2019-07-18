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
> - [What are variable annotations in Python 3.6?](https://stackoverflow.com/questions/39971929/what-are-variable-annotations-in-python-3-6)
>
> - [**PEP 484**](https://www.python.org/dev/peps/pep-0484) - Type Hints
>
>   Definition of a standard meaning for annotations: type hints.
>
> - [**PEP 526**](https://www.python.org/dev/peps/pep-0526) - Syntax for Variable Annotations
>
>   Ability to type hint variable declarations, including class variables and instance variables
>
> - What’s New In Python 3.6 -> [PEP 526: Syntax for variable annotations](https://docs.python.org/3.7/whatsnew/3.6.html?highlight=annotation#pep-526-syntax-for-variable-annotations)

变量注解([*variable* *annotation*](https://docs.python.org/3.7/glossary.html#term-variable-annotation))用于为变量或类属性提供注解。

在对变量或类进行注解时，可以不进行赋值操作：

```python
class C:
    field: 'annotation'

print(C.__annotations__) #> {'field': 'annotation'}
```

通常会将变量注解用作类型提示([*type* *hint*](https://docs.python.org/3.7/glossary.html#term-type-hint))，例如下面这个变量期望获得 [`int`](https://docs.python.org/3.7/library/functions.html#int) 类型的值：

```python
from typing import Dict, ClassVar, get_type_hints
class Starship:
    hitpoints: int = 50
    stats: ClassVar[Dict[str, int]] = {}
    primes: List[int] = []
    shield: int = 100
    captain: str
    def __init__(self, captain: str) -> None:
        ...

assert get_type_hints(Starship) == {'hitpoints': int,
                                    'stats': ClassVar[Dict[str, int]],
                                    'shield': int,
                                    'captain': str}

assert get_type_hints(Starship.__init__) == {'captain': str,
                                             'return': None}
```

变量注解的语法在 [Annotated assignment statements](https://docs.python.org/3.7/reference/simple_stmts.html#annassign) 中进行了解释。

See [function annotation](https://docs.python.org/3.7/glossary.html#term-function-annotation), [**PEP 484**](https://www.python.org/dev/peps/pep-0484) and [**PEP 526**](https://www.python.org/dev/peps/pep-0526), which describe this functionality.

### 函数注解

> 参考:
>
> - [Python 的函数注解](https://segmentfault.com/a/1190000005173184)
> - [4.7.7. Function Annotations](https://docs.python.org/3/tutorial/controlflow.html#function-annotations)
>
> 扩展阅读:
>
> - [**PEP 3107**](https://www.python.org/dev/peps/pep-3107) - Function Annotations
>
>   The original specification for function annotations.
>
> - [**PEP 484**](https://www.python.org/dev/peps/pep-0484) - Type Hints
>
>   Definition of a standard meaning for annotations: type hints.
>
> - [**PEP 526**](https://www.python.org/dev/peps/pep-0526) - Syntax for Variable Annotations
>
>   Ability to type hint variable declarations, including class variables and instance variables
>
> - [**PEP 563**](https://www.python.org/dev/peps/pep-0563) - Postponed Evaluation of Annotations
>
>   Support for forward references within annotations by preserving annotations in a string form at runtime instead of eager evaluation.
>
> - [variable annotation](https://docs.python.org/3.7/glossary.html#term-variable-annotation)

函数注解([*function* *annotation*](https://docs.python.org/3.7/glossary.html#term-function-annotation))用于为函数形参或返回值提供注解，在 [Function definitions](https://docs.python.org/3.7/reference/compound_stmts.html#function) 对函数注解的语法进行了解释。

```python
def dog(name:str, age:(1, 99), species:'品种') -> tuple:
    return (name, age, species)
```

- `: expression`：用于对参数逐个进行注解，可对任何参数进行注解，包括 `*args` 和 `**kwargs` 
- “`-> expression`”：用于对返回值进行注解。

任何有效的 Python 表达式均可被用作注解，注解的存在不会改变函数的语义。

通常会将函数注解用作类型提示([*type* *hint*](https://docs.python.org/3.7/glossary.html#term-type-hint))，例如下面这个函数期望获得两个 [`int`](https://docs.python.org/3.7/library/functions.html#int) 类型的实参，并且还应该具备 [`int`](https://docs.python.org/3.7/library/functions.html#int) 类型的返回值：

```python
def sum_two_numbers(a: int, b: int) -> int:
   return a + b
```

函数注解以字典的形式被存储在该函数的 `__annotations__` 属性中，对函数的其它部分没有任何影响。

```python
In [7]: dog.__annotations__
Out[7]: {'age': (1, 99), 'name': str, 'return': tuple, 'species': '品种'}
```

### 类型提示

> 扩展阅读:
>
> - [`typing`](https://docs.python.org/3.7/library/typing.html#module-typing) — Support for type hints
>
> - [**PEP 484**](https://www.python.org/dev/peps/pep-0484) - Type Hints
>
>   Definition of a standard meaning for annotations: type hints.
>
> - What’s New In Python 3.5 -> [PEP 484 - Type Hints](https://docs.python.org/3.7/whatsnew/3.5.html?highlight=annotation#pep-484-type-hints)

类型提示([*type* *hint*](https://docs.python.org/3.7/glossary.html#term-type-hint))其实就是一个注解，该注解用于指定变量、类属性、函数形参、函数返回值期望的类型。

类型提示是可选的，并不要求强制实施，但它对静态类型分析工具很有用，并且可以帮助 IDE 完成代码补全和代码重构。

可使用 [`typing.get_type_hints()`](https://docs.python.org/3.7/library/typing.html#typing.get_type_hints) 访问全局变量、类属性、函数的类型提示，但是不能访问本地变量的类型提示。





