# locals

the global names in a module; 

the local names in a function invocation.

在对象内部，本地作用域

类定义会在本地作用域中放置另一个命名空间。

Python 中一切皆是对象，当我们创建对象时，便会创建一个本地作用域



`locals`()

Update and return a dictionary representing the current local symbol table. Free variables are returned by [`locals()`](https://docs.python.org/3.7/library/functions.html#locals) when it is called in function blocks, but not in class blocks.

Note

 

The contents of this dictionary should not be modified; changes may not affect the values of local and free variables used by the interpreter.



