# abs

abs(*x*) 

返回一个数的绝对值。
如果实参(argument)是整数或浮点数，则会返回其绝对值。
如果实参是复数(complex number)，则会返回复数的模(magnitude)

示例：

```python
>>> abs(-3)
3
>>> abs(-3.4)
3.4
>>> abs(3+4j) # 复数
5.0
```

另一个示例：

```python
>>> abs(0x10)
16
>>> abs(0b10)
2
>>> abs(0o20)
16
```

## \_\_abs\_\_

> 相关笔记:『3.3. Special method names.md』-> 3.3.8. Emulating numeric types

🔨 object.`__abs__`(*self*)

`__abs__` 用于实现 `abs()`。调用 `abs(x)` 时，便会调用 `x.__abs__()`。

```python
class ExampleCls:
    def __abs__(self):
        return 'orac_j35'
abs(ExampleCls()) #> 'orac_j35'
```