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
> - [在线正则表达式测试 - 开源中国](http://tool.oschina.net/regex)

Note: 在本笔记中我会使用 `Style without quotes` 来表示正则表达式(*Regular* *Expression* - RegEx)，同时会使用 `'Style without quotes'` 来表示被匹配的字符串。例如，可使用正则表达式 `hello` 来匹配字符串 `'hello'`。

在 [Regular Expression Objects](https://docs.python.org/3/library/re.html#re-objects) 中提供的大多数方法都可用作模块级别的函数。模块级别的函数无需预先编译正则表达式对象，同时会失掉一些微调参数。

See also: 第三方模块 [regex](https://pypi.org/project/regex/) 的 API 与标准库 `re` 模块兼容，同时还提供了一些额外的功能，对 Unicode 的支持也更加全面。



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

