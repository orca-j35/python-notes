# chr

chr( *i* )

*i* 是整数，表示某个 Unicode 码点的值。`chr()` 会返回该码点对应的 Unicode 字符。由于 Python 的内置类型中并不包含字符类型，所以返回值实际上是一个长度为 1 的字符串，并且其中仅包含对应的 Unicode 字符。 *i* 的取值范围是 0 ~ 1,114,111(0x10FFFF)，大于或小于该取值范围都会抛出 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError)。

```python
>>> chr(97),chr(0x61)
('a', 'a')
>>> chr(8364)
'€'
>>> chr(40120)
'鲸'
```

对于不可见 Unicode 字符，`chr` 会返回以下转义序列：

1. 如果"不可见字符"拥有"独立转义序列"，便会返回该"独立转义序列"：

   ```python
   >>> chr(0x0a)
   '\n'
   ```

2. 如果没有独立的转义序列，便会返回十六进制转义序列或 Unicode 转义序列：

   ```python
   # \xhh 用于显示 U+0000~U+00FF 间的不可见字符
   >>> chr(0x00)
   '\x00'
   # \uxxxx 用于显示 U+0100~U+FFFF 间的不可见字符
   >>> chr(0xD800)
   '\ud800'
   # \Uxxxxxxxx 用于显示 U+10000 之后的不可见字符
   >>> chr(0x1D800)
   '\U0001d800'
   ```

Tips：`chr()` 与 `ord()` 的功能正好相反。

```python
>>> chr(ord('a'))
'a'
>>> ord(chr(97))
97
```



