# bool

class bool([*x*])

该内置函数本质上是在调用 [bool](https://docs.python.org/3.7/library/functions.html#bool) 类的构造函数，从而获得一个布尔(bool)对象。bool 类仅有 `False` 和 `True` 两个实例 (详见 [Boolean Values](https://docs.python.org/3.7/library/stdtypes.html#bltin-boolean-values))。[bool](https://docs.python.org/3.7/library/functions.html#bool) 类是 [int](https://docs.python.org/3.7/library/functions.html#int) 类的子类(详见 [Numeric Types — int, float, complex](https://docs.python.org/3.7/library/stdtypes.html#typesnumeric))，但不能为 bool 类创建子类。

Tips：在数值上下文中(numeric contexts) ：`False` 被视作 0，`True` 被视作 1。

```python
>>> 1 + True
2
```

对于`bool()` ，如果省略 *x* 参数，则会返回 `False`。

```python
>>> bool() 
False
```

如果存在 *x* 参数，`bool()` 会使用标准[真值测试](https://docs.python.org/3.7/library/stdtypes.html#truth)对 *x* 进行转换。当 *x* 的真值为 false 时，`bool()` 会返回 `False` ；反之则返回 `True`。

```python
>>> bool(1)
True
>>> bool(0)
False
>>> bool("False") # 非空字符串始终为True
True
>>> bool([0, 0])
True
>>> bool([])
False
>>> bool(2+2)
True
```

## what's false object

默认情况下，对象的真值为 true，除非存在以下两种情况：

- 对象中定义了 [`__bool__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__bool__) 方法，并且该方法返回 `False` 
- 对象中定义了 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 方法，并且该方法返回 `0` 

如果同时定义了上述两种方法， [`__bool__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__bool__) 的优先级高于 [`__len__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__len__) 。

```python
>>> class Cls():
    def __bool__(self):
        return True

    def __len__(self):
        return 0

>>> a_cls = Cls()
>>> bool(a_cls)
True
```

下面是真值为 false 的内置对象：

- 常量 `None` 和 `False` 被定义为 false
- 任何等于 0 的数值类型：`0`, `0.0`, `0j`, `Decimal(0)`, `Fraction(0, 1)`
- 空序列(sequences)和集合(collections)： `''`, `()`, `[]`, `{}`, `set()`, `range(0)`

