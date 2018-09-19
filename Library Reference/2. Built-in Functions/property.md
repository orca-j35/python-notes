# property

🔨class property(*fget=None*, *fset=None*, *fdel=None*, *doc=None*)

> 为了避免混淆 attribute 和 property，本文将 attribute 译作属性，但 property 保留单词形式。

该内置函数其实是 `property` 类的构造函数，用于创建 property 对象，各个参数的含义如下：

- *fget* : 一个函数对象，用于返回字段的值
- *fset* : 一个函数对象，用于设置字段的值
- *fdel* : 一个函数对象，用于删除字段
- *doc* : 一个字符串，用于为字段创建文档字符串

property 对象用于管理某个实例字段，可根据实际需求控制该字段的访问权限：

- 可读字段，需正确设置 *fget* 参数；不可读字段，需 *fget=None*
- 可写字段，需正确设置 *fset* 参数；不可写字段，需 *fset=None*
- 可删除字段，需正确设置 *fdel*  参数；不可删除字段，需 *fdel=None*

tips: 该内置函数只能创建属于实例的 property 对象，不能创建属于类的 property 对象。

property 对象的典型用法如下：

```python
class C:
    def __init__(self):
        self._x = None

    def getx(self): # getter
        return self._x

    def setx(self, value): # setter
        self._x = value

    def delx(self): # deleter
        del self._x

    x = property(getx, setx, delx, "I'm the 'x' property.")
```









🔨class property(object)