# re — 正则表达式语法
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html#regex-howto) 🍰
> - [learn-regex — GitHub](https://github.com/ziishaned/learn-regex) 🍰
> - [`re`](https://docs.python.org/3/library/re.html#module-re) — Regular expression operations 🍰
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

## raw 字符串和 `\`

反斜线字符( `\` )在正则表达式中有以下两种用法:

- 表示特殊格式 - 比如，使用 `\w` 来匹配字符和字母
- 用来屏蔽元字符或特殊序列的含义 - 比如，使用 `\\` 来匹配 `'\'`，使用 `\.` 来匹配 `'.'`

正则表达式中 `\` 字符的用法与 Python 在 string literals 中用法有冲突，例如：

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

### 任意字符 `.`

在默认情况下 `.` (*Dot*) 用于匹配除换行符之外的单个任意字符串。如果设置 [`DOTALL`](https://docs.python.org/3/library/re.html#re.DOTALL) flag，则会匹配包括换行符在内的单个任意字符。

```python
re.findall(r".ar", "The car parked in the garage.")
#> ['car', 'par', 'gar']
```

### 锚点 `^`  `###  

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
#> ['The', 'the']
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

### 量词 `{m}` `{m,n}` `{m,n}?`

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

### 转义符 `\`

`\` 有如下两种功能:

- 表示特殊序列 - 比如，使用 `\w` 来匹配字符和字母
- 用来屏蔽元字符或特殊序列的含义 - 比如，使用 `\\` 来匹配 `'\'`，使用 `\.` 来匹配 `'.'`

```python
re.findall(r"\.\\", ".\\")
#> ['.\\']
re.findall("[fcm]at\.?",'The fat cat sat on the mat.')
#> ['fat', 'cat', 'mat.']
```

建议在 pattern 中使用 raw 字符串，否则会出现以下问题:

> If you’re not using a raw string to express the pattern, remember that Python also uses the backslash as an escape sequence in string literals; if the escape sequence isn’t recognized by Python’s parser, the backslash and subsequent character are included in the resulting string. However, if Python would recognize the resulting sequence, the backslash should be repeated twice. This is complicated and hard to understand, so it’s highly recommended that you use raw strings for all but the simplest expressions.

### 字符集 `[]`

`[]` 表示一组字符，有以下两种用法:

- 直接在 `[]` 中列出需要的字符，例如 `[amk]` 可匹配 `'a'`, `'m'`, `'k'`

- 在 `[]` 给出字符集的范围，例如:

  - `[a-z]` will match any lowercase ASCII letter, 
  - `[0-5][0-9]` will match all the two-digits numbers from `00` to `59`
  - `[0-9A-Fa-f]` will match any hexadecimal digit. 

  在下述两种情况中，`-` 被用于匹配字面值 `'-'`:

  - If `-` is escaped (e.g. `[a\-z]`) 
  - if it’s placed as the first or last character (e.g. `[-a]` or `[a-]`)

在 `[]` 中的元字符不再拥有特殊含义，仅匹配相应的字面值，例如:

```python
re.findall("[(+*)]",'(+*)')
#> ['(', '+', '*', ')']
```

在 `[]` 中可使用像 `\w` 或 `\s` 这样的字符集类(注意，`\w` 或 `\s` 代表的字符集依赖于  [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) 或 [`LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) flag)。

```python
re.findall("[\w]",'abc')
#> ['a', 'b', 'c']
```

如果在字符集后放置量词，则会重复匹配该字符集:

```python
re.findall(r'[a-zA-Z][0-9a-zA-Z]{0,19}','orca')
#> ['orca']
```

如果需要在字符集中匹配 `']'`，可以使用 `\]` 或将 `]` 置于字符集的起始位置:\

```python
re.findall(r"[()[\]{}]", "[]")
#> ['[', ']']
re.findall(r"[]()[{}]", "[]")
#> ['[', ']']
```

> Support of nested sets and set operations as in [Unicode Technical Standard #18](https://unicode.org/reports/tr18/)might be added in the future. This would change the syntax, so to facilitate this change a [`FutureWarning`](https://docs.python.org/3/library/exceptions.html#FutureWarning) will be raised in ambiguous cases for the time being. That includes sets starting with a literal `'['` or containing literal character sequences `'--'`, `'&&'`, `'~~'`, and `'||'`. To avoid a warning escape them with a backslash.

*Changed in version 3.7:* [`FutureWarning`](https://docs.python.org/3/library/exceptions.html#FutureWarning) is raised if a character set contains constructs that will change semantically in the future.

#### 否定字符集 `[^]`

可以在 `[]` 中使用 `^` 来设置一个否定字符集，此时将匹配否定字符集中未包含的所有字符。例如:

- `[^5]` will match any character except `'5'`
- `[^^]` will match any character except `'^'`. `^` has no special meaning if it’s not the first character in the set.

```python
re.findall("[^^5]",'^456abc')
#> ['4', '6', 'a', 'b', 'c']
```

仅当 `^` 被用作 `[]` 中的第一个字符时，才具备特殊含义。



### 或运算 `|`

例如，`(?:T|t)he|car` 将匹配 `(?:T|t)he` 或 `car`:

```python
re.findall(r"(?:T|t)he|car", "The car is parked in the garage.")
#> ['The', 'car', 'the']
```

注意，可以在 group 中使用 `|` 

> `A|B`, where *A* and *B* can be arbitrary REs, creates a regular expression that will match either *A* or *B*. An arbitrary number of REs can be separated by the `'|'` in this way. 
>
> This can be used inside groups (see below) as well. 
>
> As the target string is scanned, REs separated by `'|'` are tried from left to right. When one pattern completely matches, that branch is accepted. This means that once *A* matches, *B* will not be tested further, even if it would produce a longer overall match. In other words, the `'|'` operator is never greedy. To match a literal `'|'`, use `\|`, or enclose it inside a character class, as in `[|]`.

### 捕获组 `(...)`

捕获组(*capturing* *group*)是一组被置于括号中 sub-pattern，在执行匹配后可检索 group 捕获到的内容:

```python
m = re.match(r"(ab.) \1", "abc abc")
m.groups()
#> ('abc',)
```

可使用 `\number` 来引用 group 捕获到的内容(详见﹝[`\number`](#`\number`)﹞小节):

```python
# 会使用第一次匹配到的内容进行二次匹配，
# 并不是重复使用(ab.)进行匹配
re.match(r"(ab.) \1", "abc abc")
#> <re.Match object; span=(0, 7), match='abc abc'>
re.match(r"(ab.) \1", "abc abd")
#> None
```

如果在 group 后放置量词，则会重复匹配该 sub-pattern:

```python
m = re.match(r"(ab.)*", "abcabd")
m
#> <re.Match object; span=(0, 6), match='abcabd'>
m.groups()
#> ('abd',)
```

在 group 中可使用 `|`:

```python
re.findall(r"(c|g|p)ar", "The car is parked in the garage.")
#> ['c', 'p', 'g']
```

如果需要匹配 `'('` 或 `')'`，可采用以下两种方法:

- use `\(` or `\)`
- enclose them inside a character class: `[(]`, `[)]`

#### 非捕获组 `(?:...)`

非捕获组(*Non*-*capturing* *group*) 与捕获组的区别如下:

- 通过 `(?:...)` 匹配到的子字符串不能单独检索
- 不可使用 `\number` 来引用 `(?:...)` 匹配到的子字符串

```python
m = re.match(r"(ab.)-(?:ab.)", "abc-abc")
m.groups()
#> ('abc',)
```

#### 命名组 `(?P<name>...)`

命名组 `(?P<name>...)` 类似于编号组 `(...)`，但是命名组可通过组名 `name` 来访问捕获到的子字符串。组名 `name` 必须是有效的 Python 标识符，并且在同一个 pattern 中不可重复定义相同的组名。命名组是对编号组的扩展，我们仍然通过组号来操作命名组。比如，可使用 `\number` 来引用命名组捕获到的内容:

```python
# 会使用命名组匹配到的内容进行二次匹配，
# 并不是重复使用正则表达式 ab. 进行匹配
re.match(r"(?P<quote>ab.) \1 (?P=quote)", "abc abc abc")
#> <re.Match object; span=(0, 7), match='abc abc'>
re.match(r"(?P<quote>ab.) (?P=quote)", "abc abd")
#> None
```

在下面的表格中展示了在不同 context 中引用命名组的方法——假设 pattern 为 `(?P<quote>['"]).*?(?P=quote)`，可匹配用单引号(或双引号)引用的字符串。

| Context of reference to group “quote”                   | Ways to reference it                                         |
| :------------------------------------------------------ | :----------------------------------------------------------- |
| in the same pattern itself                              | - `(?P=quote)` (as shown)<br />- `\1`                        |
| when processing match object *m*                        | - `m.group('quote')`<br />- `m.group(1)`<br />- `m.end('quote')` (etc.) |
| in a string passed to the *repl* argument of `re.sub()` | - `\g<quote>`<br />- `\g<1>`<br />- `\1`                     |

#### 引用命名组 `(?P=name)`

用于引用命名组匹配到的内容

```python
# 会使用命名组匹配到的内容进行二次匹配，
# 并不是重复使用正则表达式 ab. 进行匹配
re.match(r"(?P<quote>ab.) \1 (?P=quote)", "abc abc abc")
#> <re.Match object; span=(0, 7), match='abc abc'>
re.match(r"(?P<quote>ab.) (?P=quote)", "abc abd")
#> None
```



### 扩展符号 `(?...)`

`(?...)` 被称为扩展符号，如 `(?aiLmsux)`, `(?:...)`, `(?aiLmsux-imsx:...)` 等。扩展符号的含义和语法取决于 `?` 后面的第一个字符。在扩展符号的中只有 `(?P<name>...)` 会创建 group，其余扩展符号均不会创建 group。

以下是当前支持的扩展符号:

#### `(?aiLmsux)`

可使用 `'a'`, `'i'`, `'L'`, `'m'`, `'s'`, `'u'`, `'x'` 中的一个或多个来组建该扩展符号，并将其置于 pattern 的开始处，例如:

```python
re.match(r"(?a)\w", "鲸")
#> None
re.match(r'\w','鲸')
#> <re.Match object; span=(0, 1), match='鲸'>
```

`'a'`, `'i'`, `'L'`, `'m'`, `'s'`, `'u'`, `'x'` 表示相应的 flage:

- [`re.A`](https://docs.python.org/3/library/re.html#re.A) (ASCII-only matching)
- [`re.I`](https://docs.python.org/3/library/re.html#re.I) (ignore case)
- [`re.L`](https://docs.python.org/3/library/re.html#re.L) (locale dependent)
- [`re.M`](https://docs.python.org/3/library/re.html#re.M) (multi-line)
- [`re.S`](https://docs.python.org/3/library/re.html#re.S) (dot matches all)
- `re.U` (Unicode matching)
- [`re.X`](https://docs.python.org/3/library/re.html#re.X) (verbose)

需要使用 flag 时，我们通常会向 [`re.compile()`](https://docs.python.org/3/library/re.html#re.compile) 函数传递 flag 参数。但是，我们还可以直接在正则表达式中使用 `(?aiLmsux)` 来设置 flag，这样便无需使用 `re.compile()` 函数。

```python
# 以下两种方法等效
re.match(r"(?a)\w", "a")
#> <re.Match object; span=(0, 1), match='a'>
r = re.compile(r'(?a)\w',flags=re.A)
r.match('a')
#> <re.Match object; span=(0, 1), match='a'>
```



#### `(?:...)`

详见﹝[非捕获组 `(?:...)`](#非捕获组 `(?:...)`)﹞小节



#### `(?aiLmsux-imsx:...)`

`(?aiLmsux-imsx:...)` 由两部分构成，其用法与 `(?aiLmsux)` 类似

- `-` 前的部分可由 `'a'`, `'i'`, `'L'`, `'m'`, `'s'`, `'u'`, `'x'` 中 0 个或多个组成，表示添加相应的 flag
- `-` 后的部分可由  `'i'`, `'m'`, `'s'`, `'x'` 中的 1 或多个组成，表示移除相应 flag。注: `-` 及其之后的部分为可选部分

> The letters `'a'`, `'L'` and `'u'` are mutually exclusive when used as inline flags, so they can’t be combined or follow `'-'`. Instead, when one of them appears in an inline group, it overrides the matching mode in the enclosing group. In Unicode patterns `(?a:...)`switches to ASCII-only matching, and `(?u:...)` switches to Unicode matching (default). In byte pattern `(?L:...)` switches to locale depending matching, and `(?a:...)` switches to ASCII-only matching (default). This override is only in effect for the narrow inline group, and the original matching mode is restored outside of the group.

*New in version 3.6.*

*Changed in version 3.7:* The letters `'a'`, `'L'` and `'u'` also can be used in a group.

#### `(?P<name>...)`

详见﹝[命名组 `(?P<name>...)`](#命名组 `(?P<name>...)`)﹞小节



#### `(?P=name)`

详见﹝[引用命名组 `(?P=name)`](#引用命名组 `(?P=name)`)﹞小节



#### `(?#...)`

`(?#...)` 用于提供注释，其中的内容不参与匹配:

```python
re.match(r"(?#comment)\w", "V")
#> <re.Match object; span=(0, 1), match='V'>
```

#### 零宽度断言(前后预查)

| Symbol | Description         |
| ------ | ------------------- |
| ?=     | Positive Lookahead  |
| ?!     | Negative Lookahead  |
| ?<=    | Positive Lookbehind |
| ?<!    | Negative Lookbehind |



##### `(?=...)`

`(?=...)` 被称为 Positive Lookahead Assertion，仅当 `(?=...)` 部分匹配成功后，才会匹配 `(?=...)` 之前的部分，并且 `(?=...)` 本身不会消耗任何字符串，也不会出现在匹配结果中。例如:

```python
# 只有在\sfat匹配成功时，才会匹配[T|t]he
re.findall(r"[T|t]he(?=\sfat)", "The fat cat sat on the mat.")
#> ['The']
# 注意对比下面这两句代码
re.findall('[0-9\.]+(?=%)','4.44% and 10.88%')
#> ['4.44', '10.88']
re.findall('[0-9\.]*(?=%)','4.44% and 10.88%')
#> ['4.44', '', '10.88', '']
```



##### `(?!...)`

`(?!...)` 被称为 Negative Lookahead Assertion，仅当 `(?!...)` 部分匹配失败后，才会匹配 `(?!...)` 之前的部分，并且 `(?!...)` 本身不会消耗任何字符串，也不会出现在匹配结果中。例如:

```python
# 只有在\sfat匹配失败时，才会匹配[T|t]he
re.findall(r"[T|t]he(?!\sfat)", "The fat cat sat on the mat.")
#> ['the']
re.findall(r".(?!ab)", "cab")
#> ['a', 'b']
```



##### `(?<=...)`

`(?<=...)` 被称为 Positive Lookbehind Assertion，仅当 `(?<=...)` 部分匹配成功后，才会匹配 `(?<=...)` 之后的部分，并且 `(?<=...)` 不会出现在匹配结果中。例如:

```python
re.findall(r"(?<=[T|t]he\s).at", "The fat cat sat on the mat.")
#> ['fat', 'mat']
```

`(?<=...)` 只能表示固定长度的字符串，比如允许使用 `(?<=abc)` 或 `(?<=a|b)`，但不能使用 `(?<=a*)` 或 `(?<=a{3,4})`:

```python
re.findall(r"(?<=a|b).", "abab")
#> ['b', 'a', 'b']
re.findall(r"(?<=a*).", "abab")
#> error: look-behind requires fixed-width pattern
```

> Note: That patterns which start with positive lookbehind assertions will not match at the beginning of the string being searched; you will most likely want to use the [`search()`](https://docs.python.org/3/library/re.html#re.search) function rather than the [`match()`](https://docs.python.org/3/library/re.html#re.match) function:

```python
re.search('(?<=abc)def', 'abcdef')
#> <re.Match object; span=(3, 6), match='def'>
re.match('(?<=abc)def', 'abcdef')
#> None
```

*Changed in version 3.5:* Added support for group references of fixed length.



##### `(?<!...)`

`(?<!...)` 被称为 Negative Lookbehind Assertion，仅当 `(?<!...)` 部分匹配失败后，才会匹配 `(?<!...)` 之后的部分，并且 `(?<!...)` 不会出现在匹配结果中。例如:

```python
re.findall(r"(?<![T|t]he\s).at", "The fat cat sat on the mat.")
#> ['cat', 'sat']
```

`(?<!...)` 只能表示固定长度的字符串，比如允许使用 `(?<!abc)` 或 `(?<!a|b)`，但不能使用 `(?<!a*)` 或 `(?<!a{3,4})`:

```python
re.findall(r"(?<!a).", "abc")
#> ['a', 'c']
re.findall(r"(?<!a*).", "abc")
#> error: look-behind requires fixed-width pattern
```

> Note: Patterns which start with negative lookbehind assertions may match at the beginning of the string being searched.

```python
re.match(r"(?<!a).", "abc")
#> <re.Match object; span=(0, 1), match='a'>
re.search(r"(?<!a).", "abc")
#> <re.Match object; span=(0, 1), match='a'>
```



#### `(?(id/name)yes-pattern|no-pattern)`

如果存在具备给定 id 或 name 的 group，则尝试匹配 `yes-pattern`；如果不存在相应的 group，则尝试匹配 `no-pattern`。另外，`no-pattern` 属于可选部分，可省略。

> 示例 - `(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)` is a poor email matching pattern, which will match with `'<user@host.com>'` as well as `'user@host.com'`, but not with `'<user@host.com'` nor `'user@host.com>'`.

```python
re.match(r"(<)*(\w+@\w+(?:.\w+)+)(?(1)>|$)", "<user@host.com>")
#> <re.Match object; span=(0, 15), match='<user@host.com>'>
re.match(r"(<)*(\w+@\w+(?:.\w+)+)(?(1)>|$)", "user@host.com")
#> <re.Match object; span=(0, 13), match='user@host.com'>
re.match(r"(<)*(\w+@\w+(?:.\w+)+)(?(1)>|$)", "<user@host.com")
#> None
re.match(r"(<)*(\w+@\w+(?:.\w+)+)(?(1)>|$)", "user@host.com>")
#> None
```

在使用 `(?(id/name)yes-pattern|no-pattern)` 时，需要注意 `match()`,  `search()`, `findall()` 之间的区别。`match()` 必须从最右侧起完全匹配，而 `search()` 和 `findall()` 则可以从任意位置开始匹配。例如:

```python
re.match(r"(<)*(\w+@\w+(?:.\w+)+)(?(1)>|$)", "<user@host.com")
#> None
re.search(r"(<)*(\w+@\w+(?:.\w+)+)(?(1)>|$)", "<user@host.com")
#> <re.Match object; span=(1, 14), match='user@host.com'>
re.findall(r"(<)*(\w+@\w+(?:.\w+)+)(?(1)>|$)", "<user@host.com")
#> [('', 'user@host.com')]
```

可以看到 `search()` 和 `findall()` 会将 `user@host.com` 作为匹配对象。



## special sequences

特殊序列由 `\` 和字符组成，正则表达式解析器可接收以下两种特殊序列:

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

如果 `\` 后的字符不是 ASCII 数字和字母，则以此构建的正则表达式将匹配第二个字符，例如 `\$` 将匹配 `$`

```python
re.findall(r'\$\鲸','$鲸')
#> ['$鲸']
```

### `\number`

可使用 `\number` 来引用 group 捕获到的内容:

```python
# 会使用第一次匹配到的内容进行二次匹配，
# 并不会重复使用(ab.)进行匹配
re.match(r"(ab.) \1", "abc abc")
#> <re.Match object; span=(0, 7), match='abc abc'>
re.match(r"(ab.) \1", "abc abd")
#> None
```

group 编号从 1 开始，`\number` 可引用编号为 1~99 的 group。

如果出现以下两种情况，则会将 `\number` 视为一个八进制数:

- `\number` 左侧第一位数为 0
- `\number` 是 3 位八进制数

此时不会将 `\number` 解释为 group 编号，而是会将其解释为该八进制数对应的字符，例如:

```python
re.findall(r'\070\176','8~')
#> ['8~']
```

在 `[]` 中的 `\number` 不再拥有特殊含义，此时 `\number` 将被解释为八进制数对应的字符，例如:

```python
re.findall(r'[\70\176]','8~')
#> ['8', '~']
```

### `\A`

`\A` 表示从字符串的第一个字符开始匹配:

> `\A` 和 `^` 的区别:
>
> When not in `MULTILINE` mode, `\A` and `^` are effectively the same. In `MULTILINE` mode, they’re different: `\A` still matches only at the beginning of the string, but `^` may match at any location inside the string that follows a newline character.

```python
re.findall(r'^[T|t]he',
           'The car is parked in the garage,\n'
           'the plane is parked at the airport',
          flags=re.MULTILINE)
#> ['The', 'the']
re.findall(r'\A[T|t]he',
           'The car is parked in the garage,\n'
           'the plane is parked at the airport',
          flags=re.MULTILINE)
#> ['The']
```



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








