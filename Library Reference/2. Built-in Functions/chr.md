# chr

chr( *i* )

*i* 是整数，表示一个 Unicode 码点。`chr()` 会返回该码点对应的 Unicode 字符。由于 Python 的内置类型中并不包含字符类型，所以返回值实际上是一个长度为 1 的字符串，其中仅包含对应的 Unicode 字符。另外， *i* 的取值范围是 0 ~ 1,114,111(0x10FFFF)，大于或小于该取值范围都会抛出 [`ValueError`](https://docs.python.org/3.7/library/exceptions.html#ValueError)。

```python
>>> chr(97),chr(0x61)
('a', 'a')
>>> chr(8364)
'€'
>>> chr(40120)
'鲸'
```

对于不可见 Unicode 字符，`chr` 会返回以下转义序列：

1. 如果"不可见字符"拥有独立的转义序列，便会返回该独立的转义序列

   ```python
   >>> chr(0x0a)
   '\n'
   ```

2. 如果没有独立的转义序列，便会返回十六进制转义序列或 Unicode 转义序列表示该字符

   ```python
   >>> chr(0x00)
   '\x00'
   >>> chr(0xD800)
   '\ud800'
   >>> chr(0x1D800)
   '\U0001d800'
   ```

----



- `\xhh` 转义序列用于表示码点范围在`U+007F` ~ `U+00FF` 之间的 Unicode 字符。
- `\uxxxx` 转义序列用于表示码点范围在`U+0100` ~ `U+FFFF` 之间的 Unicode 字符。
- `\Uxxxxxxxx` 转义序列用于表示码点范围在 `U+10000` 及以上的字符。

Tips：`chr()` 与 `ord()` 的功能正好相反。

```python
>>> chr(ord('a'))
'a'
>>> ord(chr(97))
97
```

表示

```

```

