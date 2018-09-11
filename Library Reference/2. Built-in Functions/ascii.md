# ascii

ascii(*object*)

类似于 [`repr()`](https://docs.python.org/3.7/library/functions.html#repr)，该函数会返回一个用于描述 *object* 的可打印(printable)的字符串。与 [`repr()`](https://docs.python.org/3.7/library/functions.html#repr)  的不同之处在于，`ascii()` 在获取 `__repr__()` 的返回值之后，会使用"可打印转义序列" (`'\\x'`, `'\\u'` , `'\\U'`) 来表示其中的非 ASCII 码字符。`ascii()` 返回的字符串类似于 Python 2 中的 `repr()` 函数返回的字符串。 

```python
class Cls:
    def __repr__(self):
        # ascii与repr都会调用__repr__，
        # 但ascii会将其中的非ASCII字符显示为"可打印转义序列"
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

## 如何表示非ASCII字符

补充一点有关 Unicode 的知识：每个 Unicode 字符都有一个指定的代码点(code point)，在 Unicode 字符集中一般表示为 `U+XXXX` ，其中 XXXX 是由 4 个或更多个16进制数字表示的序列。在 Python 3 中：`\u` 转义序列用于插入码点范围在 `U+0000` ~ `U+FFFF` 之间的 Unicode 字符。`\U` 转义序列用于插入码点范围在 `U+10000` 及以上的字符。

`ascii()` 会将非 ASCII 码字符划分为三段，分别使用不同的"可打印转义序列"表示：

- `'\\xhh'` 转义序列用于表示码点范围在`U+0080` ~ `U+00FF` 之间的 Unicode 字符。
- `'\\uxxxx'` 转义序列用于表示码点范围在`U+0100` ~ `U+FFFF` 之间的 Unicode 字符。
- `'\\Uxxxxxxxx'` 转义序列用于表示码点范围在 `U+10000` 及以上的字符。

示例代码：

```python
print(ascii('µ')) # U+0080 ~ U+00FF
print(ascii('鲸')) # U+0100 ~ U+FFFF 
print(ascii("😊")) # U+10000 以上
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

## 如何表示ASCII字符

`U+0000` ~ `U+007E` 之间的 Unicode 字符对应于 ASCII 字符。

如果某个字符对应于 ASCII 中的可见将字符，则会直接显示该字符：

```python
>>> ascii('a\x41')
"'aA'"
```

如果某个字符对应于 ASCII 中的不可见将字符，但该字符拥有"独立转义序列"，则将该"独立转义序列"显示为"可打印转义序列"：

```python
>>> ascii('\n')
"'\\n'"
```

如果某个字符是 ASCII 中的不可见将字符，且没有"独立转义序列"，则会以"可打印十六进制转义序列"`'\\xhh'` 表示该不可见字符：

```python
>>> ascii('\x01')
"'\\x01'"
```

## what's printable

可打印(printable)是指通过 `print()` 函数可获得预期输出，例如：

```python
>>> ascii('鲸')
"'\\u9cb8'"
>>> print(ascii('鲸'))
'\u9cb8' # 我们希望看到一个用户可读的"可打印转义序列"
```

因为 `ascii('鲸')` 的返回值是可打印(printable)字符串，所以需要在转义序列 `\u` 前，再添加一个反斜线(`\`)，才能保证 `print` 函数输出预期字符串。也就是说"可打印字符串"是通过增加 `\` 来去掉转义序列的特殊含义的字符串。因此，当用户通过 `print` 打印一个可打印字符串时，便可输出一个用户可读的"可打印转义序列"。