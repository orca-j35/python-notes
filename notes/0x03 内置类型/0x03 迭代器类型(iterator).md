## 4.5. Iterator Types

Python 支持对容器进行迭代(iteration)。本节会使用两种不同的方法来实现迭代器；通过这两种方法便可使得用户定义(user-defined)类支持迭代。序列(Sequences)始终支持迭代方法，详细描述如下。

需要为容器对象定义一个方法，以使其支持迭代：

- `container.__iter__()`

  该方法会返回一个迭代器(iterator)对象。迭代器对象需要支持下面描述的迭代器协议。如果容器支持不同类型的迭代，则可以提供额外的方法来专门请求这些迭代类型的迭代器(支持多种迭代形式的对象的一个例子是树结构，它支持 breadth-first 和 depth-first 两种遍历方式)。 This method corresponds to the [`tp_iter`](https://docs.python.org/3.7/c-api/typeobj.html#c.PyTypeObject.tp_iter) slot of the type structure for Python objects in the Python/C API. 

迭代器对象自身需要支持以下两个方法，这两个共同构成了迭代器协议：

- `iterator.__iter__()`

  返回迭代器对象本身。必须拥有该方法，才能让容器和迭代器能够配合 [`for`](https://docs.python.org/3.7/reference/compound_stmts.html#for) 和 [`in`](https://docs.python.org/3.7/reference/expressions.html#in) 一同使用。This method corresponds to the [`tp_iter`](https://docs.python.org/3.7/c-api/typeobj.html#c.PyTypeObject.tp_iter) slot of the type structure for Python objects in the Python/C API. 

- `iterator.__next__()`

  返回容器中的下一个项。如果不再有可供返回的项，则会抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration) 异常。This method corresponds to the [`tp_iternext`](https://docs.python.org/3.7/c-api/typeobj.html#c.PyTypeObject.tp_iternext) slot of the type structure for Python objects in the Python/C API.

Python 定义了多个迭代器对象，以支持对如下类型进行迭代：常规(general)序列类型和特殊(specific)序列类型、字典以及其它专业表单(specialized forms)。除迭代器协议的实现之外，其实特定类型并不重要。

一旦迭代器的 [`__next__()`](https://docs.python.org/3.7/library/stdtypes.html#iterator.__next__) 方法抛出 [`StopIteration`](https://docs.python.org/3.7/library/exceptions.html#StopIteration)，则必须在后续调用中继续抛出异常。不遵从此特性的实现被视为以损坏。

### 4.5.1. Generator Types

生成器([generator](https://docs.python.org/3.7/glossary.html#term-generator))提供了一种实现迭代器协议的便捷方式。如果某个容器对象的 [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 方法以生成器的方式被实现，那么它将自动返回一个支持 [`__iter__()`](https://docs.python.org/3.7/reference/datamodel.html#object.__iter__) 和 [`__next__()`](https://docs.python.org/3.7/reference/expressions.html#generator.__next__) 方法的迭代器对象——从技术上将，该对象其实属于生成器对象。有关生成器的更多信息请查阅 [the documentation for the yield expression](https://docs.python.org/3.7/reference/expressions.html#yieldexpr). 
