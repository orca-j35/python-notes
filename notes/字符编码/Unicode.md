# Unicode

[TOC]













阐述为什么会存在码点，和编码模式

## 已编码字符集vs.编码模式

Unicode 标准中定义了一组已编码字符集(后文简称字符集)，字符集体现了抽象字符和

用 UCS 指代该字符集

### 码点vs.编码单元vs.编码模式

Unicode 标准中定义了一组

Unicode 定义了一组字符集，字符集中的每个字符拥有各自的码点。如果直接使用码点值存储字符数据，便会出现如下问题：

- 假设以固定长度存储码点，那么每个字符至少需要占用 3 个字节，对于字符集前端的字符(比如英文字母)，仅有最后一个字节携带有效信息，其余字节全是 0，会浪费存储空间。
- 如果以可变长度存储每个码点，则可能无法区分不同的码点：字母 'A' 和 'B' 的码点值是 0x41 和 0x42，汉字 '䅂' 的码点值是 0x4142，那么当内存中出现 0x4142 时，到底是表示 'A' 和 'B'，还是表示 '䅂' 喃？

为了解决上述问题，便需要通过"编码模式"在"码点"与"编码单元"的序列间建立起映射的关系，使得每个码点仅有唯一一个对应的"编码单元"序列。如果采用可变长度的"编码模式"，还可减少空间的浪费。比如在 UTF-8 编码模式下：

- 字母 'A' 被映射为一个编码单元 0x41
- 字母 'B' 被映射为一个编码单元 0x42 
- 汉字 '䅂' 被映射为三个代码单元，分别是 0xE4、0x85、0x82

因此在存储数据时，我们实际上存储的是"编码单元"序列，而非码点值。另外，不同的"编码模式"模式，所产生的"编码单元"序列也是不同的。



由"编码单元"构成的序列用于表示码点，

"编码单元"序列与码点间的映射关系由"编码模式"确定。

- 在 UTF-8 编码模式下，码点被映射为 1 至 4 个编码单元构成的序列，每个编码单元是 8 位。
- 在 UTF-16 编码模式下，每个编码单元是 16 位。小于 U+10000 的码点被映射为单个编码单元；大于 U+10000 的码点被映射为一对代码单元(也称代理对 surrogate pairs)。
- 在 UTF-32 编码模式下，每个编码单元是 32 位，每个码点都被映射为单个编码单元。
- 在 GB18030 编码模式下，由于编码单元很小，码点会被映射为 1 至 4 个编码单元构成的序列



> Unicode 仅是一组字符集，不是编码模式。

### 参考

- [Glossary of Unicode Terms - Unicode 官方术语表](https://www.unicode.org/glossary/)
- [Character encoding - 字符编码](https://en.wikipedia.org/wiki/Character_encoding)
- [Self-synchronizing code - 自同步编码](https://en.wikipedia.org/wiki/Self-synchronizing_code)
- [Code point - 码点](https://en.wikipedia.org/wiki/Code_point)

## 概述

在 Unicode 出现之前，已经有许多不同的标准：美国的 ASCII、西欧语言中的 ISO 8859-1、俄罗斯 KOI-8、中国的 GB 18030 和 BIG-5 等。这样就产生了下面两个问题：

1. 对于任意给定的代码值，在不同的编码方案下有可能对应不同的字母；
2. 采用大字符集的语言其编码长度有可能不同。例如，有些常用的字符采用单字节编码，而另一些字符则需要两个或更多个字节。













## UTF-8

- 在 UTF-8 编码模式下，码点被映射为 1 至 4 个编码单元构成的序列，每个编码单元是 8 位。


UTF-8 是一种 Unicode 的实现方式。其他实现方式还包括 UTF-16（字符用两个字节或四个字节表示）和 UTF-32（字符用四个字节表示），不过在互联网上基本不用。**重复一遍，这里的关系是，UTF-8 是 Unicode 的实现方式之一。**

UTF-8 是一种可变长度的编码方式。它可以使用1~4个字节表示一个符号，根据不同的符号而变化字节长度。编码方式如下：

```
   Unicode Char. number|        UTF-8 octet sequence
   range (hexadecimal) |              (binary)
   --------------------+---------------------------------------------
   0000 0000-0000 007F | 0xxxxxxx
   0000 0080-0000 07FF | 110xxxxx 10xxxxxx
   0000 0800-0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
   0001 0000-0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
```

可见 UTF-8 兼容 ASCII 码



## UTF-16

在 UTF-16 编码模式下，每个编码单元是 16 位：

- 小于 U+10000 的码点(BMP 部分)被映射为单个编码单元，UTF-16 编码值与码点值相同，不能省略前导 0；
- 大于 U+10000 的码点被映射为一对代码单元(也称代理对 surrogate pairs)。

### 代理对

surrogate pairs 

编码过程大致如下：

```
假设supplementary planes中的某个码点的十六进制值是x，显然：
x ∈ (0x1_0000~0x10_FFFF)
首先，将x的减去0x1_0000，得到y：
∴ y = x-0x1_0000 ∈ (0x00000~0xF_FFFF)
将 y 表示为二进制，并将高10位记作h，低十位记作l，可得：
y = 0bhhhh_hhhh_hhll_llll_llll
将y的高10位与高代理项的基准值0xD800相加，便可得高代理项high：
high = (y // 0x400)+0xD800
将y的低10位与低代理项的基准值0xDC00相加，便可得低代理项low：
low = (y % 0x400)+0xDC00
```

此时，由 high 和 low 构成的代理对，便是该码点在 UTF-16 下的编码。
由于，y "高 10 位"的最大值 0x3FF 加上 0xD800 等于 0xDBFF(低 10 位同理)，所以"代理对"完全能够表示所有的 supplementary planes。

"代理对"中的 high 和 low 会落入基本多语言级别中空闲的 2048 字节内，这段区域通常被称为代理区域(surrogate area)[U+D800 ~ U+DBFF用于第一个代码单元 high，U+DC00 ~ U+DFFF用于第二个代码单元 low]。这样的设计使得我们可以迅速判断某个代码单元是否是代码对中的一部分。

这样构成的编码值会落入基本多语言级别中空闲的 2048 字节内，通常被称为代理区域(surrogate area)[U+D800 ~ U+DBFF用于第一个代码单元，U+DC00 ~ U+DFFF用于第二个代码单元]。这样设计十分巧妙，我们可以从中迅速的知道一个代码单元是一个字符编码，还是一个辅助字符的第一或第二部分。

用 Python 描述计算过程如下，不考虑输入错误，仅大端模式：

```python
def get_surrogate_pairs(char_or_code):
    """char_or_code:单个字符或码点"""
    if isinstance(char_or_code, str):
        code_point = ord(char_or_code)
    else:
        code_point = char_or_code
    code_point -= 0x10000
    high_surrogate = (code_point // 0x400)+0xD800
    low_surrogate = (code_point % 0x400)+0xDC00
    print(hex(high_surrogate), hex(low_surrogate))


get_surrogate_pairs("𐐷")
get_surrogate_pairs(0x10FFFF)
```

输出：

```
0xd801 0xdc37
0xdbff 0xdfff
```



### UCS-2 vs. UTF-16 

UCS(Universal Coded Character Set通用编码字符集)

在 UCS-2 编码模式下，每个编码单元是 16 位。UCS-2 只能将小于 U+10000 的码点映射为单个编码单元，不能编码大于 U+10000 的码点，也就是说只能编码 BMP 中的码点。

UTF-16 扩展自 UCS-2，每个编码单元仍是 16 位。可将大于 U+10000 的编码被映射为一对编码单元，小于 U+10000 的码点与 UCS-2 映射方式相同(UTF-16 兼容  UCS-2)。

示例：Notepad++ 支持 UCS-2 编码，如果在 UCS-2 编码的文件保存辅助平面中的字符，再次打开该文件时会发现辅助字符会变为另一个 BMP 字符，字符信息发生了丢失。

## UTF-32

在 UTF-32 (也称 UCS-4) 编码模式下，采用 32 位编码单元，每个码点都被映射为单个编码单元。UTF-32 虽可编码所有 Unicode 码点，但是相比其它编码模式会占用更多的空间。







## ASCII 码

一个字节是 8 位，可表示 256 个不同的符号。

ASCII 码一共规定了128个字符的编码，比如空格`SPACE`是32（二进制`00100000`），大写的字母`A`是65（二进制`01000001`）。这128个符号（包括32个不能打印出来的控制符号），只占用了一个字节的后面7位，最前面的一位统一规定为`0`。

由80H到0FFH共128个字符,一般称为"扩充字符",这128个扩充字符是由IBM制定的,并非标准的ASCII码.这些字符是用来表示框线、音标和其它欧洲非英语系的字母。

## 通过码点查找字符

在 [Unicode.org](https://www.unicode.org/) 中，点选 [Code Charts](https://www.unicode.org/charts/) 后，便会进入搜索页面。

![Code_Charts](Unicode.assets/Code_Charts.jpg)

在搜索框中输入 Unicode 码点后，便会找到该码点所在的编码图表(code chart)。
下载编码图标的 PDF 文件，并在其中搜索目标码点即可。

通过这种方式可以查询到较为详细的信息，甚至会为非字符(noncharacters)提供必要的说明。本文中提及的 `U+FFFE` 就是一个典型的非字符。

注脚：

[^1]: https://en.wikipedia.org/wiki/Character_encoding#Terminology



 

