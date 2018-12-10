# setattr

🔨 setattr(*object*, *name*, *value*)

`setattr()` 对应于 `getattr()`，前者用于设置对象



This is the counterpart of [`getattr()`](https://docs.python.org/3.7/library/functions.html#getattr). The arguments are an object, a string and an arbitrary value. The string may name an existing attribute or a new attribute. The function assigns the value to the attribute, provided the object allows it. For example, `setattr(x,'foobar', 123)` is equivalent to `x.foobar = 123`.