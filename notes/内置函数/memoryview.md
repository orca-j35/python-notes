# memoryview
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库
>
> 相关笔记:
>
> - 『二进制序列类型(bytes, bytearray, memoryview)』-> Memory Views

🔨*class* memoryview(*obj*)

该函数会创建一个引用自 *obj* 的内存视图([*memoryview*](https://docs.python.org/3.7/library/stdtypes.html#memoryview))对象。内存视图对象允许 Python 代码访问支持缓冲区协议([*buffer* protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects))的对象的内部数据，且无需拷贝。

*obj* 必须支持缓冲区协议([*buffer* *protocol*](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects))。支持缓冲区协议的内置对象有 [bytes](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray)。[bytes](https://docs.python.org/3.7/library/stdtypes.html#bytes) 和 [bytearray](https://docs.python.org/3.7/library/stdtypes.html#bytearray) 由 [memoryview](https://docs.python.org/3.7/library/stdtypes.html#memoryview) 提供支持，内存视图使用缓冲区协议([buffer protocol](https://docs.python.org/3.7/c-api/buffer.html#bufferobjects))访问来访问其它二进制对象的内存，且无需拷贝。

示例 - 使用内存视图对象修改一个短整型有符号整数数组的数据。

```python
from array import array

numbers = array('h', [-2, -1, 0, 1, 2]) # 'h'表示signed short
memv = memoryview(numbers) 
len(memv) #> 5
# 转换成列表形式
memv.tolist() #> [-2, -1, 0, 1, 2]
# 转换成无符号字符类型
memv_oct = memv.cast('B')       
memv_oct.tolist() #> [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
# 修改第3个元素的高位字段
memv_oct[5] = 4                 
numbers #> array('h', [-2, -1, 1024, 1, 2])
```



