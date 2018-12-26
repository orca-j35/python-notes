

# 布尔类型(bool)

Boolean Values

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本笔记涵盖了 [Boolean Values](https://docs.python.org/3.7/library/stdtypes.html#boolean-values) 中的全部内容，并进行了扩展
>
> 相关笔记：
>
> - 『真值测试.md』
> - 『bool.md』
> - 『3.2. 标准类型层次.md』

布尔值包含两个常量对象 `False` 和 `True`，用于表示真值。

[bool](https://docs.python.org/3.7/library/functions.html#bool) 类是 [int](https://docs.python.org/3.7/library/functions.html#int) 类的子类(详见 [Numeric Types — int, float, complex](https://docs.python.org/3.7/library/stdtypes.html#typesnumeric))，但不能为 bool 类创建子类。

```python
issubclass(bool,int) #> True
```

因为 bool 是 int 的子类，所以 bool 同样支持 int 类型支持的操作，详见笔记『数值类型(int,float,complex).md』和『numbers - Numeric abstract base classes.md』

在数值上下文中（e.g., 被用作算数运算符的操作数时），`False` 和 `True` 的行为与整数 0 和 1 类似：

```python
False + True + True #> 2
```

如果将 bool 值转换为字符串，会得到  `"False"` 或 `"True"` ，而非 `'0'` 或 `'1'`。

```python
str(True),repr(False) #> ('True', 'False')
```

内置函数 `bool()` 用于获取对象的布尔值。

## 布尔意义

Python 中的所有对象均具备布尔意义。
默认情况下，对象的真值为 `True`，除非存在以下两种情况：

- 对象中定义了 [`__bool__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__bool__) 方法，并且该方法返回 `False` 
- 对象中定义了 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 方法，并且该方法返回 `0` 

如果同时定义了上述两种方法， [`__bool__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__bool__) 的优先级高于 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 。如果类定义中不包含 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 和 [`__bool__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__bool__)，则该类的所有实例均为真。

下面是真值为 false 的内置对象：

- 常量 `None` 和 `False` 被定义为 false
- 任何等于 0 的数值类型：`0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0, 1)`
- 空序列(*sequences*)和集合(*collections*)： `''`, `()`, `[]`, `{}`, `set()`, `range(0)`



