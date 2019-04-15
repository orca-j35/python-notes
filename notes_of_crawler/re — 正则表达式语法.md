# re — 正则表达式语法
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html#regex-howto) 🍰
> - [learn-regex — GitHub](https://github.com/ziishaned/learn-regex)
> - https://github.com/ziishaned/learn-regex
> - [`re`](https://docs.python.org/3/library/re.html#module-re) — Regular expression operations
> - [正则表达式 - 廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143193331387014ccd1040c814dee8b2164bb4f064cff000)
> - http://www.runoob.com/regexp/regexp-syntax.html
> - http://www.runoob.com/regexp/regexp-metachar.html
>
> 工具:
>
> - https://regex101.com/
> - [在线正则表达式测试 - 开源中国](http://tool.oschina.net/regex)

Note: 在本笔记中我会使用 `Style without quotes` 来表示正则表达式(*Regular* *Expression* - RE)，同时会使用 `'Style without quotes'` 来表示被匹配的字符串。例如，可使用正则表达式 `hello` 来匹配字符串 `'hello'`。

RE pattern 和 string 可以是 Unicode string([`str`](https://docs.python.org/3/library/stdtypes.html#str)) ，也可以是 8-bit string([`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes))。但是，Unicode string 和 8-bit string 不能混用：

- 不能将 Unicode string 同 bytes pattern 进行匹配，反之亦然
- 在进行替换时，用于替换的字符串也必须与 pattern 和 search 的字符串具有相同的类型。

正则表达式主要有以下两个应用场景：

- 检查 string 是否同 pattern 相匹配(例如检查 Email 地址的格式是否正确)
- 在字符串中执行替换操作(例如将所有美国拼写改为英国拼写)

正则表达式可拼接使用:

> if *A* and *B* are both regular expressions, then *AB* is also a regular expression. In general, if a string *p*matches *A* and another string *q* matches *B*, the string *pq* will match AB. This holds unless *A*or *B* contain low precedence operations; boundary conditions between *A* and *B*; or have numbered group references. Thus, complex expressions can easily be constructed from simpler primitive expressions like the ones described here. For details of the theory and implementation of regular expressions, consult the Friedl book [[Frie09\]](https://docs.python.org/3/library/re.html#frie09), or almost any textbook about compiler construction.

构建正则表达式的字符分为普通字符和特殊字符:

- Most ordinary characters, like `'A'`, `'a'`, or `'0'`, are the simplest regular expressions; they simply match themselves. You can concatenate ordinary characters, so `last` matches the string `'last'`. 
- Some characters, like `'|'` or `'('`, are special. Special characters either stand for classes of ordinary characters, or affect how the regular expressions around them are interpreted.

重复修饰符(*repetition* *qualifiers* - `*`, `+`, `?`, `{m,n}`, etc)不能直接嵌套使用:

> This avoids ambiguity with the non-greedy modifier suffix `?`, and with other modifiers in other implementations. To apply a second repetition to an inner repetition, parentheses may be used. For example, the expression `(?:a{6})*` matches any multiple of six `'a'` characters.

## raw 字符串和 `'\'`

反斜线字符( `'\'` )在正则表达式中有以下两种用法:

- 表示特殊格式 - 比如，使用 `\w` 来匹配字符和字母
- 用来屏蔽特殊字符的含义 - 比如，使用 `\\` 来匹配 `'\'`，使用 `\.` 来匹配 `'.'`

正则表达式中 `'\'` 字符的用法与 Python 在 string literals 中用法有冲突，例如：

```python
# 当我们在utf-8编码的文本文件中看到一个反斜线'\'字符时
# 如果我们将该字符读取到Python解释器中，则会得到下面这个字符串
s = '\\'
# 如果我们要使用正则表达式来匹配s，那么pattern字符串应为
pattern = '\\\\'
```

建议在 pattern 中使用 raw 字符串，例如:

```python
# 当我们在utf-8编码的文本文件中看到'\n'时，如果我们将其读取到Python解释器中，则会得到如下字符串
s1 = '\\n'
# 如果我们要使用正则表达式来匹配s1，那么pattern字符串如下
p1 = '\\\\n'
re.match('\\\\n','\\n') # or re.match(r'\\n','\\n')
#> <re.Match object; span=(0, 2), match='\\n'>

# 当我们在utf-8编码的文本文件中看到'\s'时，如果我们将其读取到Python解释器中，则会得到如下字符串
s2 = '\\s'
# 如果我们要使用正则表达式来匹配s1，那么pattern字符串如下
p2 = '\\\\s'
re.match('\\\\s','\\s') # or re.match(r'\\s','\\s')
#> <re.Match object; span=(0, 2), match='\\s'>

# 还可以思考以下示例
re.match('\\\\s','\s') # or re.match(r'\\s','\s')
#> <re.Match object; span=(0, 2), match='\\s'>
re.match('\\\s','\s')
#> <re.Match object; span=(0, 2), match='\\s'>
```

通过上面的示例，可以看到如果在 pattern 中使用普通字符串的话，可能需要大量使用 `\`，这会大大降低 pattern 的可读性，因此我们需要在 pattern 中使用 raw 字符串，以减少 `\` 的用来。raw 字符串中不会对 `\` 进行特殊处理(例如， `r"\n"` 表示两个字符 `'\'` 和 `'n'` ，而 `"\n"` 则被视作一个换行符。

```python
r'\n','\n'
#> ('\\n', '\n')
```



## metacharacters

> 参考:
>
> - https://docs.python.org/3/howto/regex.html#more-metacharacters
> - 

元字符(*metacharacters*)的完整列表如下(在标准库文档中，有时会将"元字符"称为"特殊字符"):

```
. ^ $ * + ? { } [ ] \ | ( )
```

我们可以将多个元字符组合使用，例如 `*?`、`{m,n}?`。

如果要使用元字符的字面值，只需在元字符前添加 `\` 即可:

```python
re.findall(r"\.ar", "car.ar")
#> ['.ar\\k']
```

### `.`

在默认情况下 `.` (*Dot*) 用于匹配除换行符之外的单个任意字符串。如果设置 [`DOTALL`](https://docs.python.org/3/library/re.html#re.DOTALL) flag，则会匹配包括换行符在内的单个任意字符。

```python
re.findall(r".ar", "The car parked in the garage.")
#> ['car', 'par', 'gar']
```

### 锚点 `^`  `$`

📌`^` (Caret)表示匹配字符串的第一个字符:

```python
re.findall(r'[Tt]he','The car is parked in the garage.')
#> ['The', 'the']
re.findall(r'^[Tt]he','The car is parked in the garage.')
#> ['The']
```

如果设置了 [`MULTILINE`](https://docs.python.org/3/library/re.html#re.MULTILINE) flag，则会在每个换行符后进行匹配:

```python
re.findall(r'^[T|t]he',
           'The car is parked in the garage,\n'
           'the plane is parked at the airport',
          flags=re.MULTILINE)
3> ['The', 'the']
```

📌`$` 表示匹配字符串的最后一个字符，或是匹配字符串末尾处换行符的前一个字符。如果设置了 [`MULTILINE`](https://docs.python.org/3/library/re.html#re.MULTILINE) flag，则会在每个换行符前进行匹配。

```python
re.findall(r'\wat$','The fat cat sat\n on the mat\n')
#> ['mat']
re.findall(r'\wat$','The fat cat sat\n on the mat\n',flags=re.MULTILINE)
#> ['sat', 'mat']
```

> Note: searching for a single `$` in `'foo\n'` will find two (empty) matches: one just before the newline, and one at the end of the string.

### 重复匹配 `*`  `+`  `?`

📌`*` 表示重复匹配 0 到多次，且采用贪婪匹配(*greedy*)

> Causes the resulting RE to match 0 or more repetitions of the preceding RE, as many repetitions as are possible. `ab*` will match ‘a’, ‘ab’, or ‘a’ followed by any number of ‘b’s.

```python
re.findall(r'ab*','a ab abbb')
#> ['a', 'ab', 'abbb']
```

📌`+` 表示重复匹配 1 到多次，且采用贪婪匹配(*greedy*)

> Causes the resulting RE to match 1 or more repetitions of the preceding RE. `ab+` will match ‘a’ followed by any non-zero number of ‘b’s; it will not match just ‘a’.

```python
re.findall(r'ab+','a ab abbb')
#> ['ab', 'abbb']
```

📌`?` 表示重复匹配 0 或 1 次，且采用贪婪匹配(*greedy*)

> Causes the resulting RE to match 0 or 1 repetitions of the preceding RE. `ab?` will match either ‘a’ or ‘ab’.

```python
re.findall(r'ab?','a ab abbb')
#> ['a', 'ab', 'ab']
```

### 惰性匹配 `*?`, `+?`, `??`

`*` , `+` , `?` 均采用贪婪匹配，它们会匹配尽可能多的文本。可以使用 `?` 后缀将贪婪匹配转换为惰性(*lazy*)匹配。

```python
re.findall(r"<.*>",'<a> b <c>')
#> ['<a> b <c>']
re.findall(r"<.*?>",'<a> b <c>')
#> ['<a>', '<c>']
```

### `{m}` `{m,n}` `{m,n}?`

📌`{m}` 用于设定准确的重复匹配的次数

> Specifies that exactly *m* copies of the previous RE should be matched; fewer matches cause the entire RE not to match. For example, `a{6}` will match exactly six `'a'` characters, but not five.

```python
re.findall(r'a{6}','a'*6)
#> ['aaaaaa']
re.findall(r'a{6}','a'*5)
#> []
```

📌`{m,n}` 重复匹配为 m~n 次(包含 n)，且采用贪婪匹配(*greedy*)。可以省略 m 或 n —— `{,n}` 表示 `{0,n}`，`{m,}` 表示 m 到无穷大。

> Causes the resulting RE to match from *m* to *n* repetitions of the preceding RE, attempting to match as many repetitions as possible. For example, `a{3,5}` will match from 3 to 5 `'a'` characters. Omitting *m* specifies a lower bound of zero, and omitting *n*specifies an infinite upper bound. As an example, `a{4,}b` will match `'aaaab'` or a thousand `'a'` characters followed by a `'b'`, but not `'aaab'`. The comma may not be omitted or the modifier would be confused with the previously described form.

```python
re.findall(r'a{3,5}','a'*4)
#> ['aaaa']
re.findall(r'<.{1,6}>','<a> b <c>')
#> ['<a>', '<c>']
```

📌`{m,n}?` 重复匹配为 m~n 次(包含 n)，且采用惰性匹配。

> Causes the resulting RE to match from *m* to *n* repetitions of the preceding RE, attempting to match as *few* repetitions as possible. This is the non-greedy version of the previous qualifier. For example, on the 6-character string `'aaaaaa'`, `a{3,5}` will match 5 `'a'` characters, while `a{3,5}?` will only match 3 characters.

```python
re.findall(r'<.{0,}>','<a> b <c>')
#> ['<a> b <c>']
re.findall(r'<.{0,}?>','<a>b<c>')
#> ['<a>', '<c>']
```

### `\`

`\` 有如下两种功能:

- 

反斜线字符( `'\'` )在正则表达式中有以下两种用法:

- 表示特殊格式 - 比如，使用 `\w` 来匹配字符和字母
- 用来屏蔽特殊字符的含义 - 比如，使用 `\\` 来匹配 `'\'`，使用 `\.` 来匹配 `'.'`

### `[]`



### `|`



### `(...)`



### `(?...)`



### `(?aiLmsux)`



### `(?:...)`



### `(?aiLmsux-imsx:...)`



### `(?P<name>...)`



### `(?P=name)`



### `(?#...)`



### `(?=...)`



### `(?!...)`



### `(?<=...)`



### `(?<!...)`



### `(?(id/name)yes-pattern|no-pattern)`



## special sequences

The special sequences consist of `'\'` and a character from the list below. If the ordinary character is not an ASCII digit or an ASCII letter, then the resulting RE will match the second character. For example, `\$` matches the character `'$'`.

正则表达式解析器可接收以下两种特殊序列:

- Python 字符串字面值转义序列:

  ```
  \a      \b      \f      \n
  \r      \t      \u      \U
  \v      \x      \\
  ```

- 正则表达式特有的特殊序列:

  ```
  \A      \b      \B      \d
  \D      \s      \S      \w
  \W      \Z      \number
  ```

示例:

```python
import re
re.match('\n','\n') # or re.match(r'\n','\n')
#> <re.Match object; span=(0, 1), match='\n'>
re.match('\w','h') # or re.match(r'\w','h')
#> <re.Match object; span=(0, 1), match='h'>
```



### `\number`

Matches the contents of the group of the same number. Groups are numbered starting from 1. For example, `(.+) \1` matches `'the the'` or `'55 55'`, but not `'thethe'` (note the space after the group). This special sequence can only be used to match one of the first 99 groups. If the first digit of *number* is 0, or *number* is 3 octal digits long, it will not be interpreted as a group match, but as the character with octal value *number*. Inside the`'['` and `']'` of a character class, all numeric escapes are treated as characters.

### `\A`

Matches only at the start of the string.

### `\b`

Matches the empty string, but only at the beginning or end of a word. A word is defined as a sequence of word characters. Note that formally, `\b` is defined as the boundary between a `\w` and a `\W` character (or vice versa), or between `\w` and the beginning/end of the string. This means that `r'\bfoo\b'` matches `'foo'`, `'foo.'`, `'(foo)'`, `'bar foo baz'`but not `'foobar'` or `'foo3'`.By default Unicode alphanumerics are the ones used in Unicode patterns, but this can be changed by using the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag. Word boundaries are determined by the current locale if the [`LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) flag is used. Inside a character range, `\b` represents the backspace character, for compatibility with Python’s string literals.

### `\B`

Matches the empty string, but only when it is *not* at the beginning or end of a word. This means that `r'py\B'` matches `'python'`, `'py3'`, `'py2'`, but not `'py'`, `'py.'`, or `'py!'`. `\B` is just the opposite of `\b`, so word characters in Unicode patterns are Unicode alphanumerics or the underscore, although this can be changed by using the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag. Word boundaries are determined by the current locale if the [`LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) flag is used.

### `\d`

For Unicode (str) patterns:Matches any Unicode decimal digit (that is, any character in Unicode character category [Nd]). This includes `[0-9]`, and also many other digit characters. If the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag is used only `[0-9]` is matched.For 8-bit (bytes) patterns:Matches any decimal digit; this is equivalent to `[0-9]`.

### `\D`

Matches any character which is not a decimal digit. This is the opposite of `\d`. If the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag is used this becomes the equivalent of `[^0-9]`.

### `\s`

For Unicode (str) patterns:Matches Unicode whitespace characters (which includes `[ \t\n\r\f\v]`, and also many other characters, for example the non-breaking spaces mandated by typography rules in many languages). If the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag is used, only `[ \t\n\r\f\v]` is matched.For 8-bit (bytes) patterns:Matches characters considered whitespace in the ASCII character set; this is equivalent to `[ \t\n\r\f\v]`.

### `\S`

Matches any character which is not a whitespace character. This is the opposite of `\s`. If the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag is used this becomes the equivalent of `[^ \t\n\r\f\v]`.

### `\w`

For Unicode (str) patterns:Matches Unicode word characters; this includes most characters that can be part of a word in any language, as well as numbers and the underscore. If the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag is used, only `[a-zA-Z0-9_]` is matched.For 8-bit (bytes) patterns:Matches characters considered alphanumeric in the ASCII character set; this is equivalent to `[a-zA-Z0-9_]`. If the [`LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) flag is used, matches characters considered alphanumeric in the current locale and the underscore.

### `\W`

Matches any character which is not a word character. This is the opposite of `\w`. If the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag is used this becomes the equivalent of `[^a-zA-Z0-9_]`. If the [`LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) flag is used, matches characters considered alphanumeric in the current locale and the underscore.

### `\Z`

Matches only at the end of the string.

Most of the standard escapes supported by Python string literals are also accepted by the regular expression parser:

```
\a      \b      \f      \n
\r      \t      \u      \U
\v      \x      \\
```

(Note that `\b` is used to represent word boundaries, and means “backspace” only inside character classes.)

`'\u'` and `'\U'` escape sequences are only recognized in Unicode patterns. In bytes patterns they are errors. Unknown escapes of ASCII letters are reserved for future use and treated as errors.

Octal escapes are included in a limited form. If the first digit is a 0, or if there are three octal digits, it is considered an octal escape. Otherwise, it is a group reference. As for string literals, octal escapes are always at most three digits in length.

*Changed in version 3.3:* The `'\u'` and `'\U'` escape sequences have been added.

*Changed in version 3.6:* Unknown escapes consisting of `'\'` and an ASCII letter now are errors.








