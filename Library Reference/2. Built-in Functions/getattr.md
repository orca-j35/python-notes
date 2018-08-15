### getattr

getattr(*object*, *name*[, *default*])

该函数用于获取 *object* 中名为 *name* 的属性(*name* 以字符串表示)，也就是说 `getattr(x, 'foobar')` 等效于 `x.foobar`。
如果 *object* 中含有 *name* 属性，则返回该属性；如果 *object* 没有 *name* 属性，则返回 *default*(如果提供)，否则抛出 [`AttributeError`](https://docs.python.org/3.7/library/exceptions.html#AttributeError) 异常。
对于字段属性，会直接返回值；对于方法属性，会返回其引用(通过引用可调用方法属性)。

Tips：该函数属于反射操作；使用 `object.__class__` 的 `__mro__` 属性提供方的法解析顺序(MRO)列表，在继承链中搜索 *name* 属性。

一个简单的示例：

```python
>>> class Foo:
...     def __init__(self, x):
...         self.x = x
...
>>> f = Foo(10)
>>> getattr(f, 'x')
10
>>> f.x
10
>>> getattr(f, 'y', 'bar')
'bar'
```

另一个较复杂的示例：

```python
class Cls:
    class_field = "类字段"

    def __init__(self):
        self.instance_field = "实例字段"

    def instance_method(self):
        print("实例方法")

    @staticmethod
    def static_method():
        print("静态方法")

    @classmethod
    def class_method(cls):
        print("类方法")


a_instance = Cls()
print("以下属性均可使用：", '\n',
      getattr(Cls, "class_field"), '\n',
      getattr(Cls, "static_method"), '\n',
      getattr(Cls, "class_method"), '\n',
      getattr(a_instance, "instance_field"), '\n',
      getattr(a_instance, "instance_method"))

print("存在default参数：", '\n',
      getattr(a_instance, "extra_field", "没有该属性!"), '\n',)
```

输出：

```
以下属性均可使用：
 类字段
 <function Cls.static_method at 0x000001CEBC5F6730>
 <bound method Cls.class_method of <class '__main__.Cls'>>
 实例字段
 <bound method Cls.instance_method of <__main__.Cls object at 0x000001CEBC5F9550>>

存在default参数：
 没有该属性!
```

