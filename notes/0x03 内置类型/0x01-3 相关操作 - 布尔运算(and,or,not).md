

# 布尔运算(and, or, not)

Boolean Operations - and, or, not

> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 本小节涵盖了 [Boolean Operations — and, or, not](https://docs.python.org/3.7/library/stdtypes.html#boolean-operations-and-or-not) 中的全部内容
>
> 相关笔记：
>
> - 『真值测试.md』
> - 『表达式和运算符.md』-> 布尔运算符

下面是布尔运算(*Boolean operations*)，优先级从上至下依次增加：

| Operation | Result                                     | Notes |
| --------- | ------------------------------------------ | ----- |
| `x or y`  | if *x* is false, then *y*, else *x*        | (1)   |
| `x and y` | if *x* is false, then *x*, else *y*        | (2)   |
| `not x`   | if *x* is false, then `True`, else `False` | (3)   |

Notes:

1. This is a short-circuit operator, so it only evaluates the second argument if the first one is false.
2. This is a short-circuit operator, so it only evaluates the second argument if the first one is true.
3. `not` has a lower priority than non-Boolean operators, so `not a == b` is interpreted as `not (a == b)`, and `a == not b` is a syntax error.

