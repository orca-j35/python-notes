# ascii

ascii(*object*)

类似于 [`repr()`](https://docs.python.org/3.7/library/functions.html#repr)，该函数会返回一个用于描述 *object* 的可打印(printable)的字符串。与 [`repr()`](https://docs.python.org/3.7/library/functions.html#repr)  的不同之处在于，`ascii()` 在获取 `__repr__()` 的返回值之后，会使用转义序列 (`\x`, `\u` , `\U`) 来表示其中的非 ASCII 码字符。`ascii()` 返回的字符串类似于 Python 2 中的 `repr()` 函数返回的字符串。 

```python
class Cls:
    def __repr__(self):
        # ascii与repr都会调用__repr__，
        # 但ascii会转义其中的非ASCII字符
        return "调用__repr__"

    def __str__(self):
        # ascii不会调用__str__
        return "调用__str__"


a_cls = Cls()
print("repr 的返回值:{0}".format(repr(a_cls)))
print("ascii的返回值:{0}".format(ascii(a_cls)))
```

输出

```
repr 的返回值:调用__repr__
ascii的返回值:\u8c03\u7528__repr__
```

**如何表示非 ASCII 码字符？**

补充一点有关 Unicode 的知识：每个 Unicode 字符都有一个指定的代码点(code point)，在 Unicode 字符集中一般表示为 `U+XXXX` ，其中 XXXX 是由 4 个或更多个16进制数字表示的序列。在 Python 3 中：`\u` 转义序列用于插入码点范围在 `U+0000` ~ `U+FFFF` 之间的 Unicode 字符。`\U` 转义序列用于插入码点范围在 `U+10000` 及以上的字符。

`ascii()` 会将非 ASCII 码字符划分为三段，分别使用不同的转义序列表示：

- `\xhh` 转义序列用于表示码点范围在`U+007F` ~ `U+00FF` 之间的 Unicode 字符。
- `\uxxxx` 转义序列用于表示码点范围在`U+0100` ~ `U+FFFF` 之间的 Unicode 字符。
- `\Uxxxxxxxx` 转义序列用于表示码点范围在 `U+10000` 及以上的字符。

 `U+0000` ~ `U+007E` 之间的 Unicode 字符对应于 ASCII 码，这部分内容不会被 `ascii()` 转义。

示例代码：

```python
print(ascii('µ')) # U+007F ~ U+00FF
print(ascii('鲸')) # U+0100 ~ U+FFFF 
print(ascii("😊")) # U+10000
```

输出:

```
'\xb5'
'\u9cb8'
'\U0001f60a'
```

最后在对比一下 `repr()`：

```python
print(repr('µ'))
print(repr('鲸'))
print(repr("😊"))
```

输出：

```
'µ'
'鲸'
'😊'
```

## what's printable

可打印(printable)是指通过 `print()` 函数可获得预期输出，例如：

```python
>>> ascii('鲸')
"'\\u9cb8'"
>>> print(ascii('鲸'))
'\u9cb8'
```

因为 `ascii('鲸')` 的返回值是可打印(printable)字符串，所有需要在转义字符 `\u` 前，再添加一个反斜线(`\`)，才能保证 `print` 函数输出预期字符串。也就是说可打印字符串是通过增加 `\` 来去掉转义字符的特殊含义的字符串。因此，当用户通过 `print` 打印一个可打印字符串时，便可输出一个用户可读的"转义字符串"。