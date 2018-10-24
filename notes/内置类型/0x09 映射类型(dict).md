# 映射类型(dict)

> 本节涵盖了 [Mapping Types — dict](https://docs.python.org/3.7/library/stdtypes.html#dict) 中的所有知识点，并进行了扩展。

映射([*mapping*](https://docs.python.org/3/glossary.html#term-mapping))对象会将可哈希([*hashable*](https://docs.python.org/3/glossary.html#term-hashable))值映射到任意对象。映射属于可变对象。目前只有一种标准的映射类型，即字典(*dictionary*)。如果想要了解其它容器类型，可以参考内置类型 ([list](https://docs.python.org/3.7/library/stdtypes.html#list)、[set](https://docs.python.org/3.7/library/stdtypes.html#set)、[tuple](https://docs.python.org/3.7/library/stdtypes.html#tuple)) 以及 [collections](https://docs.python.org/3.7/library/collections.html#module-collections) 模块。

所有可哈希对象均可用作字典的键(*key*)，，所有不可哈希的对象均不能用作字典的键。不可哈希的对象包括列表、字典以及任何**可变类型**。两个相等可哈希对象的哈希值相等，即便这两个对象具备不同的 id

如果两个具备不同 id 的可哈希对象拥有相同的哈希值，那么在 key 中可以互换使用：

```python
>>> hash(a)
-6299899980521991026
>>> b = range(10)
>>> hash(b)
-6299899980521991026
>>> a is b
False
>>> dict_ = {a:'range对象'}
>>> dict_[b]
'range对象'
```



测试是否是可哈希对象 isinstance



可变对象通过值来测试相等性，不可变对象

(如，列表、字典或任何可变类型)

唯一需要的属性是比较相等的对象具有相同的哈希值，即便对象具备不同的id





A dictionary’s keys are *almost* arbitrary values. Values that are not [hashable](https://docs.python.org/3.7/glossary.html#term-hashable), that is, values containing lists, dictionaries or other mutable types (that are compared by value rather than by object identity) may not be used as keys. Numeric types used for keys obey the normal rules for numeric comparison: if two numbers compare equal (such as `1` and `1.0`) then they can be used interchangeably to index the same dictionary entry. (Note however, that since computers store floating-point numbers as approximations it is usually unwise to use them as dictionary keys.)





在别的编程语言中 dict 也被称作 联合内存(associative memories) 或联合数组(associative arrays)。

- key ：是 [hashable](https://docs.python.org/3/glossary.html#term-hashable) 值。包含列表、字典或其它可变类型的值，不能用作 key。用作 key 的 Numeric 类型，遵循数字比较的一般规则：如果两个数相等，那么在引用相同字典条目时，可互换（例如1和1.0）。（注意：由于计算机将浮点数存储为近似值，因此将浮点数用于 key 是不明智的做法。