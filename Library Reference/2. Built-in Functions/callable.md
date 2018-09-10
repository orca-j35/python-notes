# callable

callable(*object*)

该函数用于检测 *object* 是否可被调用：如果 *object* 可以被调用，便返回 [`True`](https://docs.python.org/3.7/library/constants.html#True)；否则返回 [`False`](https://docs.python.org/3.7/library/constants.html#False)。即便该函数的返回值是 `True`，在调用 *object* 时也可能会失败；但如果该函数的返回值是 `False`，则调用 *object* 时一定会失败。

类也属于可调用对象，当我们调用某个类时，其实是在调用类的构造函数。另外，如果类中定义了 [`__call__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__call__) 方法，那么由该类创建的实例也属于可调用对象。

New in version 3.2: 该函数最初在 Python 3.0 中被移除，但是又在 Python 3.2 被加入。

一些不可调用对象的示例：

```python
>>> callable(61)
False
>>> callable('鲸')
False
```

一些可调用对象的示例：

```python
>>> callable(print)
True
>>> callable(lambda x:x+1)
True
# 定义一个类，不含__call__方法
>>> class Cls: pass 

>>> callable(Cls) # 其是是在调用类的构造函数
True
>>> callable(Cls())
False
# 定义一个类，包含__call__方法
>>> class Cls_has_call: 
	def __call__(self):pass

>>> callable(Cls_has_call())
True
```

## \_\_call\_\_

object.\_\_call\_\_(*self*[, *args*...])

该函数用于[模拟可调用对象](https://docs.python.org/3.7/reference/datamodel.html#emulating-callable-objects)，当我们像调用函数一样调用类实例时，便会调用该方法。如果类中定义了该方法，那么在调用类实例 x 时：`x(arg1,arg2, ...)` 与  `x.__call__(arg1, arg2, ...)` 等效果。