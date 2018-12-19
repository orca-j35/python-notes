# divmod

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

```
divmod(x, y, /)
    Return the tuple (x//y, x%y).  Invariant: div*y + mod == x.
```

🔨 divmod(*a*, *b*)

在调用该函数时，需使用两个数值作为实参 —— Py2.3 版本之前不允使用理复数。
函数的返回值是一个元组，由 *a* 除以 *b* 的商(*quotient*)和余数(*remainder*)构成。
也就是说，divmod(*a*, *b*) 的返回值等于 `(a // b, a % b)`，例如：

```python
>>> divmod(5,2)
(2, 1)
>>> divmod(-5,2)
(-3, 1)
>>> divmod(5.5,2)
(2.0, 1.5)
>>> divmod(5.5,-2)
(-3.0, -0.5)
>>> divmod(1+2j,1+0.5j)
((1+0j), 1.5j)
```

模运算 `a % b` 的结果的符号总与第二个操作数 *b* 的符号相同。

## \_\_divmod\_\_ & \_\_rdivmod\__

> 相关笔记:『3.3. Special method names.md』-> 3.3.8. Emulating numeric types

🔨 object.`__divmod__`(*self*, *other*)

🔨 object.`__rdivmod__`(*self*, *other*)

[`__divmod__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__divmod__) 应等效于使用 [`__floordiv__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__floordiv__) 和 [`__mod__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__mod__)，与 [`__truediv__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__truediv__) 无关。如果该方法不支持某些类型的参数，则应在遇到这些类型的参数时返回 `NotImplemented`。

以上两个内置方法用于实现 `divmod()`，`__rdivmod__` 是 `__divmod__` 的反射(交换)操作。只有当左操作数"不支持"相应操作，并且操作数是"不同类型"时，才会调用反射方法。

"不支持"的意思是类中不包含相应方法，或虽实现了相应方法但返回值是 `NotImplemented`。

如果需要强制回退至右操作数的反射方法，则不应将左操作数的方法设置为 `None`。`None` 会显示阻止回退操作，并将 `None` 直接用作返回值。

对于相同类型的操作数，如果非反射方法失效(例如， [`__add__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__add__))，则认为操作数不支持相应的操作，并不会调用反射方法。