# divmod

```
divmod(x, y, /)
    Return the tuple (x//y, x%y).  Invariant: div*y + mod == x.
```

🔨 divmod(*a*, *b*)

在调用该函数时，需使用两个数值作为实参 —— Py2.3 版本之前不允使用理复数。
函数的返回值是一个元组，由 *a* 除以 *b* 的商(*quotient*)和余数(*remainder*)构成。
也就是说，divmod(*a*, *b*) 的返回值等于 `(a // b, a % b)`，例如：

```python
>>> divmod(5,2)
(2, 1)
>>> divmod(-5,2)
(-3, 1)
>>> divmod(5.5,2)
(2.0, 1.5)
>>> divmod(5.5,-2)
(-3.0, -0.5)
>>> divmod(1+2j,1+0.5j)
((1+0j), 1.5j)
```

模运算 `a % b` 的结果的符号总与第二个操作数 *b* 的符号相同。
