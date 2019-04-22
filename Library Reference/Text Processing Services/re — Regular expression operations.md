# re — Regular expression operations
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 参考:
>
> - [`re`](https://docs.python.org/3/library/re.html#module-re) — Regular expression operations
> - [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html#regex-howto)
>
> 工具:
>
> - https://regex101.com/
> - If you have [`tkinter`](https://docs.python.org/3/library/tkinter.html#module-tkinter) available, you may also want to look at [Tools/demo/redemo.py](https://github.com/python/cpython/tree/3.7/Tools/demo/redemo.py), a demonstration program included with the Python distribution. It allows you to enter REs and strings, and displays whether the RE matches or fails. `redemo.py` can be quite useful when trying to debug a complicated RE.

本笔记覆盖了标准库文档「[`re`](https://docs.python.org/3/library/re.html#module-re) — Regular expression operations」中的如下三个部分:

- Module Contents
- Regular Expression Objects
- Match Objects

如果想了解「Regular Expression Syntax」可阅读笔记﹝[re — 正则表达式语法.md](./re — 正则表达式语法.md)﹞。

Note: 在本笔记中我会使用 `Style without quotes` 来表示正则表达式(*Regular* *Expression* - RegEx)，同时会使用 `'Style without quotes'` 来表示被匹配的字符串。例如，可使用正则表达式 `hello` 来匹配字符串 `'hello'`。

See also: 第三方模块 [regex](https://pypi.org/project/regex/) 的 API 与标准库 `re` 模块兼容，同时还提供了一些额外的功能，对 Unicode 的支持也更加全面。

## Module Contents

[Regular Expression Objects](https://docs.python.org/3/library/re.html#re-objects) 中提供的大多数方法都可用作模块级别的函数。模块级别的函数无需预先编译正则表达式对象，但会失掉一些微调参数。

本节将介绍 `re` 模块中定义的函数、常量、异常。部分函数是已编译的正则表达式的全功能方法的简化版本。

*Changed in version 3.6:* Flag constants are now instances of `RegexFlag`, which is a subclass of [`enum.IntFlag`](https://docs.python.org/3/library/enum.html#enum.IntFlag).

### re.compile()🔨

🔨re.compile(*pattern*, *flags=0*)

该函数可将正则表达式 *pattern* 编译为正则表达式对象([*regular* *expression* *object*](https://docs.python.org/3/library/re.html#re-objects)) —— `re.Pattern`

*flag* 用于设置正则表达式对象的行为，可利用 `|` 运算符(bitwise OR)将多个 flag 组合使用。

```python
p = re.compile('ab*', re.IGNORECASE)
```

如果需要多次使用某个 pattern 进行匹配，可利用 `re.compile()` 将其编译为 `re.Pattern` 对象，然后再使用该 `re.Pattern` 对象进行匹配，这样便可省略每次匹配时编译 pattern 的过程，如:

```python
prog = re.compile(pattern)
result = prog.match(string)
```

直接调用 `re.match()` 函数也可以完成匹配，但是每次都要重新编译 pattern，如:

```python
result = re.match(pattern, string)
```

> Note: The compiled versions of the most recent patterns passed to [`re.compile()`](https://docs.python.org/3/library/re.html#re.compile)and the module-level matching functions are cached, so programs that use only a few regular expressions at a time needn’t worry about compiling regular expressions.

### Flag 常量

flag 常量用于向 `compile()` 函数传递 *flag* 参数。对同一个 flag 常量而言，其短名称和长名称在使用过程中完全等效。

#### re.A & re.ASCII🚩

如果使用了 `re.A` flag，那么下述特殊序列将执行 ASCII-only 匹配，不再执行 full-Unicode 匹配。该 flag 仅对 Unicode pattern 有意义，byte pattern 将忽略该 flag。

```
 \w, \W, \b, \B, \d, \D, \s, \S 
```

`re.A` 对应于内联 flag `(?a)`。

> Note that for backward compatibility, the `re.U` flag still exists (as well as its synonym `re.UNICODE` and its embedded counterpart `(?u)`), but these are redundant in Python 3 since matches are Unicode by default for strings (and Unicode matching isn’t allowed for bytes).



#### re.DEBUG🚩

显式已编译表达式的调试信息，没有对应的内联 flag。



#### re.I & re.IGNORECASE🚩

如果使用了 `re.I` flag，那么在执行匹配时将不会区分大小写，因此像 `[A-Z]` 这样的表达式也可以匹配到小写字母。对应于内联 flag `?i`。

> Full Unicode matching (such as `Ü` matching `ü`) also works unless the [`re.ASCII`](https://docs.python.org/3/library/re.html#re.ASCII)flag is used to disable non-ASCII matches. The current locale does not change the effect of this flag unless the [`re.LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) flag is also used.
>
> Note that when the Unicode patterns `[a-z]` or `[A-Z]` are used in combination with the [`IGNORECASE`](https://docs.python.org/3/library/re.html#re.IGNORECASE) flag, they will match the 52 ASCII letters and 4 additional non-ASCII letters: ‘İ’ (U+0130, Latin capital letter I with dot above), ‘ı’ (U+0131, Latin small letter dotless i), ‘ſ’ (U+017F, Latin small letter long s) and ‘K’ (U+212A, Kelvin sign). If the [`ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag is used, only letters ‘a’ to ‘z’ and ‘A’ to ‘Z’ are matched.



#### re.L & re.LOCALE🚩

如果使用了 `re.L` flag，那么将根据当前环境(*locale*)来设置 `\w`, `\W`, `\b`, `\B`，并且还会设置是否区分大小写。不鼓励使用该 flag，因为环境机制非常不可靠。环境机制一次仅处理一种 "culture"，且仅适用于 8-bit 环境。默认情况下，Python 3 中已为 Unicode(str) pattern 启用了 Unicode 匹配。

*Changed in version 3.6:* [`re.LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) can be used only with bytes patterns and is not compatible with [`re.ASCII`](https://docs.python.org/3/library/re.html#re.ASCII).

*Changed in version 3.7:* Compiled regular expression objects with the [`re.LOCALE`](https://docs.python.org/3/library/re.html#re.LOCALE) flag no longer depend on the locale at compile time. Only the locale at matching time affects the result of matching.

#### re.M & re.MULTILINE🚩

如果使用了 `re.M` flag，则会影响 `^` 和 `$` 的行为:

- the pattern character `'^'` matches at the beginning of the string and at the beginning of each line (immediately following each newline).

  By default, `'^'` matches only at the beginning of the string

- The pattern character `'$'` matches at the end of the string and at the end of each line (immediately preceding each newline). 

  By default, `'$'` only at the end of the string and immediately before the newline (if any) at the end of the string.

对应于内联 flag `?m`。

#### re.S & re.DOTALL🚩

如果使用了 `re.S` flag，元字符 `.` 将可以匹配包括换行符(*newline*)在内的所有字符；如果没有使用 `re.S`，`.` 将匹配除换行符以外的所有字符。对应于内联 flag `?s`。

#### re.X & re.VERBOSE🚩

如果使用了 `re.X` flag，则可以以更易读的方式来编写正则表达式 pattern。 `re.X` flag 允许在视觉上拆分 pattern，并且可以为每个部分添加注释。对应于内联 flag `?x`。

如果使用了 `re.X` 则会忽略 pattern 中的空白符(*whitespace*)，但以下几种情况除外:

- whitespace in a character class `[]`
- when preceded by an unescaped backslash
- within tokens like `*?`, `(?:` or `(?P<...>`

`#` 用于添加注释，规则如下:

> When a line contains a `#` that is not in a character class and is not preceded by an unescaped backslash, all characters from the leftmost such `#` through the end of the line are ignored.

示例 - 以下两个用于匹配十进制数的正则表达式对象完全等效:

```python
a = re.compile(r"""\d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.X)
b = re.compile(r"\d+\.\d*")
```

### re.search()🔨

🔨re.search(*pattern*, *string*, *flags=0*)

> Scan through *string* looking for the first location where the regular expression *pattern* produces a match, and return a corresponding [match object](https://docs.python.org/3/library/re.html#match-objects). Return `None` if no position in the string matches the pattern; note that this is different from finding a zero-length match at some point in the string.
>
> If you want to locate a match anywhere in *string*, use [`search()`](https://docs.python.org/3/library/re.html#re.search) instead (see also [search() vs. match()](https://docs.python.org/3/library/re.html#search-vs-match)).

```python
# 在整个string中查找与pattern匹配的部分，
# 如果存在与pattern匹配的部分，则返回match对象
re.search('super', 'superstition')
#> <re.Match object; span=(0, 5), match='super'>
re.search('super', 'insuperable')
#> <re.Match object; span=(2, 7), match='super'>

# 如果不存在与pattern匹配的部分，则返回None
re.search('super', 'hero')
#> re.search('super', 'hero')
# 注意匹配失败与零宽度匹配的区别
re.search('\w?', '!')
#> <re.Match object; span=(0, 0), match=''>
```

### re.match()🔨

🔨re.match(*pattern*, *string*, *flags=0*)

> If zero or more characters at the beginning of *string* match the regular expression *pattern*, return a corresponding [match object](https://docs.python.org/3/library/re.html#match-objects). Return `None` if the string does not match the pattern; note that this is different from a zero-length match.
>
> Note that even in [`MULTILINE`](https://docs.python.org/3/library/re.html#re.MULTILINE) mode, [`re.match()`](https://docs.python.org/3/library/re.html#re.match) will only match at the beginning of the string and not at the beginning of each line.
>
> If you want to locate a match anywhere in *string*, use [`search()`](https://docs.python.org/3/library/re.html#re.search) instead (see also [search() vs. match()](https://docs.python.org/3/library/re.html#search-vs-match)).

```python
# 检查pattern是否与string的前n个字符匹配
# 如果匹配成功，则返回mathch对象
re.match('super', 'superstition')
#> <re.Match object; span=(0, 5), match='super'>

# 如果匹配失败，则返回None
re.match('super', 'hero')
#> None

# 注意匹配失败与零宽度匹配的区别
re.match('\w?', '!')
#> <re.Match object; span=(0, 0), match=''>


# 不能从中间开始匹配，必须从第一个字符开始就匹配
re.match('super', 'insuperable')
#> None

# re.M对match()没有影响
re.match('super', 'hero\nsuper',flags=re.M)
#> None
```

### re.fullmatch()🔨

🔨re.fullmatch(*pattern*, *string*, *flags=0*)

> If the whole *string* matches the regular expression *pattern*, return a corresponding [match object](https://docs.python.org/3/library/re.html#match-objects). Return `None` if the string does not match the pattern; note that this is different from a zero-length match.

```python
# 检查pattern和string是否完全匹配
# 如果完全匹配则返回match对象，否则返回None
re.fullmatch('super','super')
#> <re.Match object; span=(0, 5), match='super'>
re.fullmatch('super','super!')
#> None
```

*New in version 3.4.*

### re.split()🔨

🔨re.split(*pattern*, *string*, *maxsplit=0*, *flags=0*)

> Split *string* by the occurrences of *pattern*. If capturing parentheses are used in *pattern*, then the text of all groups in the pattern are also returned as part of the resulting list. If *maxsplit*is nonzero, at most *maxsplit* splits occur, and the remainder of the string is returned as the final element of the list.
>

```python
# 使用pattern来拆分string
re.split(r'\W+', 'hi~hi~hi!')
#> ['hi', 'hi', 'hi', '']

# 如果pattern中包含捕获组，那么在结果中将包含这些捕获组
re.split(r'i(\W+)', 'hi~hi~hi!')
#> ['h', '~', 'h', '~', 'h', '!', '']

# maxsplit用于设置拆分次数的上限，会将未参与拆分的部分设为列表的最后一项
re.split(r'\W+', 'hi~hi~hi!',1)
#> ['hi', 'hi~hi!']

# 还可设置flag
re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
#> ['0', '3', '9']

# re.split比str.split更灵活
'a b   c'.split(' ') # str.split无法识别连续的空格
#> ['a', 'b', '', '', 'c']
re.split(r'\s+', 'a b   c')
#> ['a', 'b', 'c']
```

> If there are capturing groups in the separator and it matches at the start of the string, the result will start with an empty string. The same holds for the end of the string:
>

```python
re.split(r'(\W+)', '...words, words...')
#> ['', '...', 'words', ', ', 'words', '...', '']
re.split(r'\W+', '...words, words...')
#> ['', 'words', 'words', '']
```

> That way, separator components are always found at the same relative indices within the result list.
>
> Empty matches for the pattern split the string only when not adjacent to a previous empty match.
>

```python
re.split(r'\b', 'Words, words, words.')
#> ['', 'Words', ', ', 'words', ', ', 'words', '.']
re.split(r'\W*', '...words...')
#> ['', '', 'w', 'o', 'r', 'd', 's', '', '']
re.split(r'(\W*)', '...words...')
#> ['', '...', '', '', 'w', '', 'o', '', 'r', '', 'd', '', 's', '...', '', '', '']
```

*Changed in version 3.1:* Added the optional flags argument.

*Changed in version 3.7:* Added support of splitting on a pattern that could match an empty string.

### re.findall()🔨

🔨re.findall(*pattern*, *string*, *flags=0*)

> Return all non-overlapping matches of *pattern* in *string*, as a list of strings. The *string* is scanned left-to-right, and matches are returned in the order found. If one or more groups are present in the pattern, return a list of groups; this will be a list of tuples if the pattern has more than one group. Empty matches are included in the result.

```python
# 返回pattern在string中的所有非重叠匹配
re.findall(r'\w+', 'hi~hi~hi!')
#> ['hi', 'hi', 'hi']

# 如果patter中存在group，则返回group列表
re.findall(r'(\w+)', 'hi~hi~hi!')
#> ['hi', 'hi', 'hi']
re.findall(r'(\w+)(\W)', 'hi~hi~hi!')
#> [('hi', '~'), ('hi', '~'), ('hi', '!')]

# 结果中包含空匹配
re.findall(r'\w*', 'hi~hi~hi!')
#> ['hi', '', 'hi', '', 'hi', '', '']
```

*Changed in version 3.7:* Non-empty matches can now start just after a previous empty match.

### re.finditer()🔨

🔨re.finditer(*pattern*, *string*, *flags=0*)

> Return an [iterator](https://docs.python.org/3/glossary.html#term-iterator) yielding [match objects](https://docs.python.org/3/library/re.html#match-objects) over all non-overlapping matches for the RE *pattern* in *string*. The *string* is scanned left-to-right, and matches are returned in the order found. Empty matches are included in the result.

```python
# 该函数会将返回一个迭代器，
# 其中包含了pattern在string中的所有非重叠匹配
list(re.finditer(r'(\w+)(\W)', 'hi~hi~hi!'))
'''Out:
[<re.Match object; span=(0, 3), match='hi~'>,
 <re.Match object; span=(3, 6), match='hi~'>,
 <re.Match object; span=(6, 9), match='hi!'>]
'''
```

*Changed in version 3.7:* Non-empty matches can now start just after a previous empty match.

### re.sub()🔨

🔨re.sub(*pattern*, *repl*, *string*, *count=0*, *flags=0*)

> Return the string obtained by replacing the leftmost non-overlapping occurrences of *pattern* in *string* by the replacement *repl*. If the pattern isn’t found, *string* is returned unchanged. 

```python
# 将pattern在string中的所有非重叠匹配替换为repl
re.sub(r'(blue|white|red)',r'colour', 'blue socks and red shoes')
#> 'colour socks and colour shoes'
# 如果在string没有匹配到pattern则会原样返回string
re.sub(r'\d','%','hello')
#> 'hello'
```

> *repl* can be a string or a function; if it is a string, any backslash escapes in it are processed. That is, `\n` is converted to a single newline character, `\r` is converted to a carriage return, and so forth. Unknown escapes of ASCII letters are reserved for future use and treated as errors. Other unknown escapes such as `\&` are left alone. Backreferences, such as `\6`, are replaced with the substring matched by group 6 in the pattern. For example:

```python
# 如果repl是字符串，则会处理其中的转义序列
re.sub(r'def\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*\(\s*\):',
       r'static PyObject*\npy_\1(void)\n{',
       'def myfunc():')
#> 'static PyObject*\npy_myfunc(void)\n{'
```

> If *repl* is a function, it is called for every non-overlapping occurrence of *pattern*. The function takes a single [match object](https://docs.python.org/3/library/re.html#match-objects) argument, and returns the replacement string. For example:
>

```python
# 如果repl是函数，则会在每个非重叠处调用该函数
# repl函数的输入参数是match对象，返回用于替换的字符串
def dashrepl(matchobj):
    if matchobj.group(0) == '-': return ' '
    else: return '-'
re.sub('-{1,2}', dashrepl, 'pro----gram-files')
#> 'pro--gram files'
re.sub(r'\sAND\s', ' & ', 'Baked Beans And Spam', flags=re.IGNORECASE)
#> 'Baked Beans & Spam'
```

> The *pattern* may be a string or a [pattern object](https://docs.python.org/3/library/re.html#re-objects).

```python
# pattern可以是字符串或pattern对象
p = re.compile('(blue|white|red)')
p.sub('colour', 'blue socks and red shoes')
#> 'colour socks and colour shoes'
```

> The optional argument *count* is the maximum number of pattern occurrences to be replaced; *count* must be a non-negative integer. If omitted or zero, all occurrences will be replaced. 

```python
# count用于设置替换次数
p = re.compile('(blue|white|red)')
p.sub('colour', 'blue socks and red shoes', count=1)
#> 'colour socks and red shoes'
```

> Empty matches for the pattern are replaced only when not adjacent to a previous empty match. Empty matches for the pattern are replaced when adjacent to a previous non-empty match.

```python
# 只有不相邻的空匹配才会被替换
re.sub('x*', '-', 'abxd')
#> '-a-b--d-'
```

> In string-type *repl* arguments, in addition to the character escapes and backreferences described above, `\g<name>` will use the substring matched by the group named `name`, as defined by the `(?P<name>...)` syntax. `\g<number>` uses the corresponding group number; `\g<2>` is therefore equivalent to `\2`, but isn’t ambiguous in a replacement such as `\g<2>0`.`\20` would be interpreted as a reference to group 20, not a reference to group 2 followed by the literal character `'0'`. The backreference `\g<0>` substitutes in the entire substring matched by the RE.

```python
# 在repl中引用命名组和编号组的方法
re.sub(r'(?P<quote>\w\d)',
       r'\1-\g<1>-\g<quote>',
       'a1 b1 c1')
#> 'a1-a1-a1 b1-b1-b1 c1-c1-c1'
```

*Changed in version 3.1:* Added the optional flags argument.

*Changed in version 3.5:* Unmatched groups are replaced with an empty string.

*Changed in version 3.6:* Unknown escapes in *pattern* consisting of `'\'` and an ASCII letter now are errors.

*Changed in version 3.7:* Unknown escapes in *repl* consisting of `'\'` and an ASCII letter now are errors.

### re.subn()🔨

🔨re.subn(*pattern*, *repl*, *string*, *count=0*, *flags=0*)

`re.subn()` 与 `re.sub()` 执行相同的操作，但返回值是一个元组:

```python
# new_string的值与re.sub相同
# number_of_subs_made表示执行替换的次
(new_string, number_of_subs_made)
```

示例:

```python
re.subn('(blue|white|red)','colour', 'blue socks and red shoes')
#> ('colour socks and colour shoes', 2)
re.subn('(blue|white|red)','colour','no colours at all')
#> ('no colours at all', 0)
```

*Changed in version 3.1:* Added the optional flags argument.

*Changed in version 3.5:* Unmatched groups are replaced with an empty string.

### re.escape()🔨

🔨re.escape(*pattern*)

> Escape special characters in *pattern*. This is useful if you want to match an arbitrary literal string that may have regular expression metacharacters in it. For example:
>

```python
# 该函数用于转义pattern中的特殊字符串
>>> print(re.escape('python.exe'))
python\.exe

>>> legal_chars = string.ascii_lowercase + string.digits + "!#$%&'*+-.^_`|~:"
>>> print('[%s]+' % re.escape(legal_chars))
[abcdefghijklmnopqrstuvwxyz0123456789!\#\$%\&'\*\+\-\.\^_`\|\~:]+

>>> operators = ['+', '-', '*', '/', '**']
>>> print('|'.join(map(re.escape, sorted(operators, reverse=True))))
/|\-|\+|\*\*|\*
```

> This functions must not be used for the replacement string in [`sub()`](https://docs.python.org/3/library/re.html#re.sub) and [`subn()`](https://docs.python.org/3/library/re.html#re.subn), only backslashes should be escaped. For example:
>

```python
# 该函数不能用作sub()和subn()中的替换字符串，因为repl函数的输入参数是match对象
>>> digits_re = r'\d+'
>>> sample = '/usr/sbin/sendmail - 0 errors, 12 warnings'
>>> print(re.sub(digits_re, digits_re.replace('\\', r'\\'), sample))
/usr/sbin/sendmail - \d+ errors, \d+ warnings
```

*Changed in version 3.3:* The `'_'` character is no longer escaped.

*Changed in version 3.7:* Only characters that can have special meaning in a regular expression are escaped.

### re.purge()🔨

🔨re.purge()

清除正则表达式缓存。

### re.error()⚠

⚠*exception* re.error(*msg*, *pattern=None*, *pos=None*)

> Exception raised when a string passed to one of the functions here is not a valid regular expression (for example, it might contain unmatched parentheses) or when some other error occurs during compilation or matching. It is never an error if a string contains no match for a pattern. The error instance has the following additional attributes:
>
> - `msg`
>
>   The unformatted error message.
>
> - `pattern`
>
>   The regular expression pattern.
>
> - `pos`
>
>   The index in *pattern* where compilation failed (may be `None`).
>
> - `lineno`
>
>   The line corresponding to *pos* (may be `None`).
>
> - `colno`[¶](https://docs.python.org/3/library/re.html#re.error.colno)
>
>   The column corresponding to *pos* (may be `None`).

```python
re.findall('(\w','abc')
#> error: missing ), unterminated subpattern at position 0

try:
    re.findall('\w(\w','abc')
except re.error as ex:
    print(ex.msg) #> missing ), unterminated subpattern
    print(ex.pattern) #> \w(\w
    print(ex.pos) #> 2
    print(ex.lineno) #> 1
    print(ex.colno) #> 3
```

*Changed in version 3.5:* Added additional attributes.

## Regular Expression Objects

正则表达式经 `re.compile()` 编译后可得到正则表达式对象([*regular* *expression* *object*](https://docs.python.org/3/library/re.html#re-objects))，该对象支持如下方法和属性。

*Changed in version 3.7:* Added support of [`copy.copy()`](https://docs.python.org/3/library/copy.html#copy.copy) and [`copy.deepcopy()`](https://docs.python.org/3/library/copy.html#copy.deepcopy). Compiled regular expression objects are considered atomic.

### Pattern.search()🔨

🔨Pattern.search(*string*[, *pos*[, *endpos*]])

> Scan through *string* looking for the first location where this regular expression produces a match, and return a corresponding [match object](https://docs.python.org/3/library/re.html#match-objects). Return `None` if no position in the string matches the pattern; note that this is different from finding a zero-length match at some point in the string.
>
> The optional second parameter *pos* gives an index in the string where the search is to start; it defaults to `0`. This is not completely equivalent to slicing the string; the `'^'`pattern character matches at the real beginning of the string and at positions just after a newline, but not necessarily at the index where the search is to start.
>
> The optional parameter *endpos* limits how far the string will be searched; it will be as if the string is *endpos* characters long, so only the characters from *pos* to `endpos - 1` will be searched for a match. If *endpos* is less than *pos*, no match will be found; otherwise, if *rx* is a compiled regular expression object, `rx.search(string, 0, 50)` is equivalent to`rx.search(string[:50], 0)`.

```python
>>> pattern = re.compile("d")
>>> pattern.search("dog")     # Match at index 0
<re.Match object; span=(0, 1), match='d'>
>>> pattern.search("dog", 1)  # No match; search doesn't include the "d"
```

### Pattern.match()🔨

🔨Pattern.match(*string*[, *pos*[, *endpos*]])

> If zero or more characters at the *beginning* of *string* match this regular expression, return a corresponding [match object](https://docs.python.org/3/library/re.html#match-objects). Return `None` if the string does not match the pattern; note that this is different from a zero-length match.
>
> The optional *pos* and *endpos* parameters have the same meaning as for the [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search)method.

```python
>>> pattern = re.compile("o")
>>> pattern.match("dog")      # No match as "o" is not at the start of "dog".
>>> pattern.match("dog", 1)   # Match as "o" is the 2nd character of "dog".
<re.Match object; span=(1, 2), match='o'>
```

> If you want to locate a match anywhere in *string*, use [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search) instead (see also [search() vs. match()](https://docs.python.org/3/library/re.html#search-vs-match)).

### Pattern.fullmatch()🔨

🔨Pattern.fullmatch(*string*[, *pos*[, *endpos*]])

> If the whole *string* matches this regular expression, return a corresponding [match object](https://docs.python.org/3/library/re.html#match-objects). Return `None` if the string does not match the pattern; note that this is different from a zero-length match.
>
> The optional *pos* and *endpos* parameters have the same meaning as for the [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search)method.

```python
>>> pattern = re.compile("o[gh]")
>>> pattern.fullmatch("dog")      # No match as "o" is not at the start of "dog".
>>> pattern.fullmatch("ogre")     # No match as not the full string matches.
>>> pattern.fullmatch("doggie", 1, 3)   # Matches within given limits.
<re.Match object; span=(1, 3), match='og'>
```

### Pattern.split()🔨

🔨Pattern.split(*string*, *maxsplit=0*)

> Identical to the [`split()`](https://docs.python.org/3/library/re.html#re.split) function, using the compiled pattern.

### Pattern.findall()🔨

🔨Pattern.findall(*string*[, *pos*[, *endpos*]])

> Similar to the [`findall()`](https://docs.python.org/3/library/re.html#re.findall) function, using the compiled pattern, but also accepts optional *pos* and *endpos* parameters that limit the search region like for [`search()`](https://docs.python.org/3/library/re.html#re.search).

### Pattern.finditer()🔨

🔨Pattern.finditer(*string*[, *pos*[, *endpos*]])

> Similar to the [`finditer()`](https://docs.python.org/3/library/re.html#re.finditer) function, using the compiled pattern, but also accepts optional *pos* and *endpos* parameters that limit the search region like for [`search()`](https://docs.python.org/3/library/re.html#re.search).

### Pattern.sub()🔨

🔨Pattern.sub(*repl*, *string*, *count=0*)

> Identical to the [`sub()`](https://docs.python.org/3/library/re.html#re.sub) function, using the compiled pattern.

### Pattern.subn()🔨

🔨Pattern.subn(*repl*, *string*, *count=0*)

> Identical to the [`subn()`](https://docs.python.org/3/library/re.html#re.subn) function, using the compiled pattern.

### Pattern.flags🔧

🔧Pattern.flags

> The regex matching flags. This is a combination of the flags given to [`compile()`](https://docs.python.org/3/library/re.html#re.compile), any `(?...)` inline flags in the pattern, and implicit flags such as `UNICODE` if the pattern is a Unicode string.

### Pattern.groups🔧

🔧Pattern.groups

> The number of capturing groups in the pattern.

### Pattern.groupindex🔧

🔧Pattern.groupindex

> A dictionary mapping any symbolic group names defined by `(?P<id>)` to group numbers. The dictionary is empty if no symbolic groups were used in the pattern.

### Pattern.pattern🔧

🔧Pattern.pattern

> The pattern string from which the pattern object was compiled.

## Match Objects

Match 对象的 boolean 值始终为 `True`。如果 string 与 pattern 不匹配， 那么 [`match()`](https://docs.python.org/3/library/re.html#re.regex.match) 和 [`search()`](https://docs.python.org/3/library/re.html#re.regex.search) 将返回 `None`，因此可以使用 `if` 语句来测试是否匹配成功:

```python
match = re.search(pattern, string)
if match:
    process(match)
```

*Changed in version 3.7:* Added support of [`copy.copy()`](https://docs.python.org/3/library/copy.html#copy.copy) and [`copy.deepcopy()`](https://docs.python.org/3/library/copy.html#copy.deepcopy). Match objects are considered atomic.

Match 对象支持以下方法和属性。

### expand()🔨

🔨Match.expand(*template*)

通过在 *template* 字符串上执行反斜杠替换来获得字符串。诸如 `\n` 之类的转义序列将被转换为适当的字符，数值反向引用(`\1`, `\2`)和名称反向引用(`\g<1>`, `\g<name>`)将被替换为对应 group 中的内容。

```python
import re
from re import Match

m = re.match(r'(.+) \1','the the')
m[1]
#> 'the'
m.expand(r'\1')
#> 'the'
m.expand(r'\n\r')
#> '\n\r'
```

> Return the string obtained by doing backslash substitution on the template string *template*, as done by the [`sub()`](https://docs.python.org/3/library/re.html#re.Pattern.sub) method. Escapes such as `\n` are converted to the appropriate characters, and numeric backreferences (`\1`, `\2`) and named backreferences (`\g<1>`, `\g<name>`) are replaced by the contents of the corresponding group.
>
> *Changed in version 3.5:* Unmatched groups are replaced with an empty string.

### group()🔨

🔨Match.group([*group1*, *...*])

返回实参列表中给出的 group，可分为以下情况:

- If there is a single argument, the result is a single string; 
- if there are multiple arguments, the result is a tuple with one item per argument. 
- Without arguments, *group1* defaults to zero (the whole match is returned). 

> If a *groupN* argument is zero, the corresponding return value is the entire matching string; if it is in the inclusive range [1..99], it is the string matching the corresponding parenthesized group. If a group number is negative or larger than the number of groups defined in the pattern, an [`IndexError`](https://docs.python.org/3/library/exceptions.html#IndexError) exception is raised. 

```python
>>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
>>> m.group()
'Isaac Newton'
>>> m.group(0)       # The entire match
'Isaac Newton'
>>> m.group(1)       # The first parenthesized subgroup.
'Isaac'
>>> m.group(2)       # The second parenthesized subgroup.
'Newton'
>>> m.group(1, 2)    # Multiple arguments give us a tuple.
('Isaac', 'Newton')
```

如果在正则表达式中使用 `(?P<name>...)` 语法，那么 *groupN* 可以是以字符串表示的 group 名称。如果 pattern 中没有名为 *groupN* 的 group 名，则会抛出 [`IndexError`](https://docs.python.org/3/library/exceptions.html#IndexError) 异常。

```python
import re

m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
m.group('first_name'),m.group(1)
#> ('Malcolm', 'Malcolm')
m.group('last_name'),m.group(2)
#> ('Reynolds', 'Reynolds')
m.group('Undefined_name')
#> IndexError: no such group
```

> If a group is contained in a part of the pattern that did not match, the corresponding result is `None`. 

```python
import re

m = re.match(r"(\w+)(\d)*", "Malcolm")
print(m.group(2))
#> None
```

> If a group is contained in a part of the pattern that matched multiple times, the last match is returned.

```python
import re
# If a group matches multiple times, only the last match is accessible
m = re.match(r"(..)+", "a1b2c3")
m.group(1)
#> 'c3'
```

### \_\_getitem\_\_()🔨

🔨Match.\_\_getitem\_\_(*g*)

> This is identical to `m.group(g)`. This allows easier access to an individual group from a match:

```python
>>> m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
>>> m[0]       # The entire match
'Isaac Newton'
>>> m[1]       # The first parenthesized subgroup.
'Isaac'
>>> m[2]       # The second parenthesized subgroup.
'Newton'
```

*New in version 3.6.*

### groups()🔨

🔨Match.groups(*default*=*None*)

> Return a tuple containing all the subgroups of the match, from 1 up to however many groups are in the pattern. The *default* argument is used for groups that did not participate in the match; it defaults to `None`.

```python
>>> m = re.match(r"(\d+)\.(\d+)", "24.1632")
# 返回所有分组
>>> m.groups()
('24', '1632')
```

> If we make the decimal place and everything after it optional, not all groups might participate in the match. These groups will default to `None` unless the *default* argument is given:

```python
>>> m = re.match(r"(\d+)\.?(\d+)?", "24")
>>> m.groups()      # Second group defaults to None.
('24', None)
>>> m.groups('0')   # Now, the second group defaults to '0'.
('24', '0')
```

### groupdict()🔨

🔨Match.groupdict(*default*=*None*)

> Return a dictionary containing all the *named* subgroups of the match, keyed by the subgroup name. The *default* argument is used for groups that did not participate in the match; it defaults to `None`. For example:

```python
import re
m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)(?P<num>\d)?", "Malcolm Reynolds")
m.groupdict()
#> {'first_name': 'Malcolm', 'last_name': 'Reynolds', 'num': None}
# default用于设置未匹配group的值
m.groupdict(0)
#> {'first_name': 'Malcolm', 'last_name': 'Reynolds', 'num': 0}
```

### start() & end()🔨

🔨Match.start([*group*])
🔨Match.end([*group*])

获取 *group* 起点和终点的索引值。

> Return the indices of the start and end of the substring matched by *group*; *group* defaults to zero (meaning the whole matched substring). Return `-1` if *group* exists but did not contribute to the match. 

```python
import re
m = re.match(r"(\w+) (\w+)(?P<num>\d)?", "0123 4567")
# 返回group起点和终点的索引值
m.start(1),m.end(1)
#> (0, 4)
m.start(2),m.end(2)
#> (5, 9)
# 未匹配group将返回-1
m.start(3),m.end(3)
#> (-1, -1)
```

> For a match object *m*, and a group *g* that did contribute to the match, the substring matched by group *g* (equivalent to `m.group(g)`) is

```python
m.string[m.start(g):m.end(g)] # 等效于m.group(g)
```

> Note that `m.start(group)` will equal `m.end(group)` if *group* matched a null string. For example, after `m = re.search('b(c?)', 'cba')`, `m.start(0)` is 1, `m.end(0)` is 2, `m.start(1)` and `m.end(1)` are both 2, and `m.start(2)` raises an [`IndexError`](https://docs.python.org/3/library/exceptions.html#IndexError) exception.

An example that will remove *remove_this* from email addresses:

```python
>>> email = "tony@tiremove_thisger.net"
>>> m = re.search("remove_this", email)
>>> email[:m.start()] + email[m.end():]
'tony@tiger.net'
```

### span()🔨

🔨Match.span([*group*])

For a match *m*, return the 2-tuple `(m.start(group), m.end(group))`. Note that if *group* did not contribute to the match, this is `(-1, -1)`. *group* defaults to zero, the entire match.

```python
import re

m = re.match(r"(\w+) (\w+)(?P<num>\d)?", "0123 4567")
m.span()
#> (0, 9)
m.span(2)
#> (5, 9)
m.start(2),m.end(2)
#> (5, 9)
```

### pos🔧 

🔧Match.pos

> The value of *pos* which was passed to the [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search) or [`match()`](https://docs.python.org/3/library/re.html#re.Pattern.match) method of a [regex object](https://docs.python.org/3/library/re.html#re-objects). This is the index into the string at which the RE engine started looking for a match.

在 [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search) 和 [`match()`](https://docs.python.org/3/library/re.html#re.Pattern.match) 中 pos 参数用于确定搜索和匹配的起点，编译后的 Regular Expression Objects 对象支持 pos 参数。

```python
pattern = re.compile("d")
pattern.search("dog-doge",0)
#> <re.Match object; span=(0, 1), match='d'>
pattern.search("dog-doge",1)
#> <re.Match object; span=(4, 5), match='d'>
m = pattern.search("dog-doge",1)
m.pos
#> 1
```

### endpos🔧

🔧Match.endpos

> The value of *endpos* which was passed to the [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search) or [`match()`](https://docs.python.org/3/library/re.html#re.Pattern.match) method of a [regex object](https://docs.python.org/3/library/re.html#re-objects). This is the index into the string beyond which the RE engine will not go.

在 [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search) 和 [`match()`](https://docs.python.org/3/library/re.html#re.Pattern.match) 中 endpos 参数用于确定搜索和匹配的终点，编译后的 Regular Expression Objects 对象支持 endpos 参数。

### lastindex🔧

🔧Match.lastindex

> The integer index of the last matched capturing group, or `None` if no group was matched at all. For example, the expressions `(a)b`, `((a)(b))`, and `((ab))` will have `lastindex == 1` if applied to the string `'ab'`, while the expression `(a)(b)` will have `lastindex == 2`, if applied to the same string.

```python
m = re.search("((a)(b))","ab")
m.groups()
#> ('ab', 'a', 'b')
m.lastindex
#> 1
m = re.search("(a)(b)","ab")
m.groups()
#> ('a', 'b')
m.lastindex
#> 2
```

### lastgroup🔧

🔧Match.lastgroup

> The name of the last matched capturing group, or `None` if the group didn’t have a name, or if no group was matched at all.

```python
m = re.search("(a)(?P<test>b)","ab")
m.lastgroup
#> 'test'
```

### re🔧

🔧Match.re

The [regular expression object](https://docs.python.org/3/library/re.html#re-objects) whose [`match()`](https://docs.python.org/3/library/re.html#re.Pattern.match) or [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search) method produced this match instance.

```python
m = re.search("(a)(?P<test>b)","ab")
m.re
#> re.compile(r'(a)(?P<test>b)', re.UNICODE)
```

### string🔧

🔧Match.string

The string passed to [`match()`](https://docs.python.org/3/library/re.html#re.Pattern.match) or [`search()`](https://docs.python.org/3/library/re.html#re.Pattern.search).

```python
m = re.search("(a)(?P<test>b)","ab")
m.string
#> 'ab'
```

