# frozenset
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记:『集合类型(set, frozenset).md』

🔨 *class* set([*iterable*])

🔨 *class* frozenset([*iterable*])

构造器 `set()` 和 `frozenset()` 拥有相同的工作方式，可分为以下两种情况：

- 如果未指定 *iterable*，将构建一个空 set (或 frozenset)对象：

  ```python
  # set() -> new empty set object
  set() #> set()
  frozenset() #> frozenset()
  ```

- 如果给定了 *iterable* 参数，则会用 *iterable* 中的元素构建一个 set (或 frozenset)对象。*iterable* 中的元素必须都是可哈希对象，`set()` (或 `frozenset()`) 会自动剔除 *iterable* 中的重复项。

  ```python
  # set(iterable) -> new set object
  set([1,2,2,3]) #> {1, 2, 3}
  set('abracadabra') #> {'a', 'b', 'c', 'd', 'r'}
  frozenset([1,2,2,3]) #> frozenset({1, 2, 3})
  ```

集合中的元素必须是可哈希([*hashable*](https://docs.python.org/3.7/glossary.html#term-hashable))对象，如果想构建一个内含集合(*set*)对象的 set，内层的集合必须是 frozenset 对象。

```python
{1,2,frozenset((3,4))} #> {1, 2, frozenset({3, 4})}
```

注意：`{}` 将构造一个空字典，并不会构建空集合。

有关集合类型(set, frozenset)的详细介绍，请阅读『集合类型(set, frozenset).md』

