# struct - Interpret bytes as packed binary data
> GitHub@[orca-j35](https://github.com/orca-j35)，所有笔记均托管于 [python_notes](https://github.com/orca-j35/python_notes) 仓库

Working with Binary Data Record Layouts
`struct` 模块为处理可变长度的二进制记录格式，提供了  `pack()` 和 `unpack()` 函数。

c 语言中，可使用 struct 和 union 处理字节，并进行字节和 int/float 的转换。
但是准确的说，Python 中没有专门用于处理字节的数据类型。
不过 `b'str'` 可表示字节，所以字节数组可视为二进制字符串。

利用 `pack` 将整型转换为 `bytes` ，`>` 表示按照 big-endian 排序

```
>>> import struct
>>> struct.pack('>I', 10240099)
b'\x00\x9c@c'
```

利用 `unpack` 把 `bytes` 转换为相应数据类型：

```
>>> struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
(4042322160, 32896)
```

下面的示例展示了，在不使用 `zipfile` 模块的情况下，如何在 ZIP 文件中遍历头信息。`'H'` 表示 2 字节的无符号短整型；`'I'` 表示 4 字节的无符号整型；`'<'` 表示标准字节尺寸，并按照 little-endian byte 排序。ZIP 文件采用 little-endian 储存布局。

```
import struct

with open('myfile.zip', 'rb') as f:
    data = f.read()

start = 0
for i in range(3):     # show the first 3 file headers
    start += 14
    fields = struct.unpack('<IIIHH', data[start:start+16])
    crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

    start += 16
    filename = data[start:start+filenamesize]
    start += filenamesize
    extra = data[start:start+extra_size]
    print(filename, hex(crc32), comp_size, uncomp_size)

    start += extra_size + comp_size     # skip to the next header
```

输出头文件：

```
b'abc.txt' 0x3c483b96 55 59
b'' 0x3b964b02 3619912 3866624
```

利用 `struct` 分析 `.bmp` 图像，该图像格式采用 little-endian 储存方式。
头文件结构：

1. `cc` is `'BM'` 表示Windows位图，is `'BA'` 表示 OS/2位图。
2. 接下来的6个 `I` 分别表示位图大小/保留位(始终为0)/实际图像的偏移量/Header的字节数/图像宽度/图像高度
3. 最后的 2 个 `HH` ，第一个始终为1，第二个表示颜色数。

```
# 读入前30个字节
>>> s = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'

>>> struct.unpack('<ccIIIIIIHH', s)
(b'B', b'M', 691256, 0, 54, 40, 640, 360, 1, 24)
```

