# 字符编码模式(CEF)

Character Encoding Form (CEF)

[TOC]

> 为了便于理解，需先了解如下术语：
>
> - ***Unicode 标量值*** (Scalar Value)：除开高代理码点(high-surrogate)和低代理码点(low-surrogat )之外的任何 Unicode 码点都是标量值，具体范围是 0x0 ~ 0xD7FF 和 0xE000 ~ 0x10FFFF。代理码点不能通过"编码模式"映射为"编码单元序列"，只有标量值可被映射为"编码单元序列"。(See definition D76 in [Section 3.9, Unicode Encoding Forms](http://www.unicode.org/versions/latest/ch03.pdf#G7404).)
>
> - ***编码单元***(code unit)：也称编码值(Code Value)，表示用于处理或交换编码文本的基本单元。Unicode 标准在 UTF-8 编码模式中使用 8-bit 编码单元；在 UTF-16 编码模式中使用 16-bit 编码单元；在 UTF-32 编码模式中使用 32-bit 编码单元。

**Unicode 字符编码模式**是指从"标量值"到"编码单元序列"的可逆映射，用于为每个标量值分别分配一个唯一的"编码单元序列"。根据"编码单元序列"的长度是否可变，可将Unicode 字符编码模式分为两类：

- 固定宽度 (*fixed width*) 编码模式：仅使用一个编码单元，但编码单元的位数不同。

  | Type                                                         | Each character encoded as | Notes                            |
  | ------------------------------------------------------------ | ------------------------- | -------------------------------- |
  | 16-bit ([UCS](https://www.unicode.org/reports/tr17/#UCS)-2)  | a single 16-bit quantity  | within a code space of 0..FFFF   |
  | 32-bit ([UCS](https://www.unicode.org/reports/tr17/#UCS)-4)  | a single 32-bit quantity  | within a code space 0..7FFFFFFF  |
  | 32-bit ([UTF](https://www.unicode.org/reports/tr17/#UTF)-32) | a single 32-bit quantity  | within a code space of 0..10FFFF |

- 可变宽度 (*variable width*) 编码模式："编码单元序列"的长度可变。如下：

  | Name                                                | Characters are encoded as                                    | Notes                        |
  | --------------------------------------------------- | ------------------------------------------------------------ | ---------------------------- |
  | [UTF](https://www.unicode.org/reports/tr17/#UTF)-8  | a mix of one to four 8-bit code units in Unicode and one to six code units in 10646 | used only with Unicode/10646 |
  | [UTF](https://www.unicode.org/reports/tr17/#UTF)-16 | a mix of one to two 16 bit code units                        | used only with Unicode/10646 |

## 1. 为什么需要 CEF

既然已经有了已编码字符集，那么通过获取"已编码字符"的码点值，计算机不就可以识别目标字符了么？为什么还需要"字符编码模式"喃？因为还存在如下问题：

1. 假设以固定长度存储码点，那么每个字符至少需要占用 3 个字节。对于码点值小于 0x0000FF 字符(如英文字母)，仅有最后一个字节携带有效信息，其余字节全是 0，会浪费存储空间。
2. 如果以可变长度存储每个码点，则可能无法区分不同的标量值：字母 'A' 和 'B' 的码点值是 0x41 和 0x42，汉字 '䅂' 的码点值是 0x4142，那么当出现数值 0x4142 时，到底是表示 'A' 和 'B'，还是表示 '䅂' 喃？由于二进制数据中并没有明确的"边界信息"，所有并不能对二者做出区分。
3. 通常计算机系统会以一个固定的 bit 长度来表示数值。假设某个系统以 8-bit 的无符号整数来存储字符信息，那么当标量值大于 0xFF 时，又该如何存储数据喃？

为了解决上述问题，便需要通过"字符编码模式"在"码点值"与"编码单元序列"间建立起映射的关系，使得每个码点仅有唯一一个对应的"编码单元"序列(解决第 2 个问题)。如果采用可变长度的"编码模式"，还可减少空间的浪费(解决第 1 个问题)。比如在 UTF-8 编码模式下：

- 字母 'A' 被映射为一个编码单元 0x41
- 字母 'B' 被映射为一个编码单元 0x42 
- 汉字 '䅂' 被映射为三个代码单元，分别是 0xE4、0x85、0x82。标量值通过 UTF-8 映射为"编码单元序列"后，拥有明确的边界信息，不会与其他编码单元混淆(解决第 2 个问题)。

可以看到汉字 '䅂' 被映射为三个代码单元，每个代码单元是 8-bit，这说明我们可以在 8-bit 的系统中使用"编码单元序列"来表示标量值大于 0xFF 字符数据(解决第 3 个问题)，可变宽度 编码模式正是基于这样的思路产生的。在可变宽度编码模式中，我们可以用代码单元(8-bit 或 16-bit)构成的序列来表示任意标量值。

## 2. UTF

**UTF** (*Unicode transformation format* ) 是将每个标量值分别映射到一个唯一字节序列的算法，属于"Unicode 字符编码模式"的具体实现方式。UTF 包含三中模式：UTF-8、UTF-16、UTF-32，且每种 UTF 算法都是可逆算法。

### 2.1 UTF-8 CEF

**UTF-8 编码模式** (Encoding Form)：一种 Unicode 编码模式，会为每个标量值分别分配一个唯一的无符号字节序列，该序列的长度是 1 ~ 4 字节(可变宽度)。另外，UTF-8 与 ASCII 兼容。 (See definition D92 in [Section 3.9, Unicode Encoding Forms](http://www.unicode.org/versions/latest/ch03.pdf#G7404).)

下表展示了 UTF-8 中比特位编码方式： 

| 标量值(2进制)              | 标量值(16进制)    | First Byte | Second Byte | Third Byte | Fourth Byte |
| -------------------------- | ----------------- | ---------- | ----------- | ---------- | ----------- |
| 00000000 0xxxxxxx          | 0x0000..0x007F    | 0xxxxxxx   |             |            |             |
| 00000yyy yyxxxxxx          | 0x0080..0x07FF    | 110yyyyy   | 10xxxxxx    |            |             |
| zzzzyyyy yyxxxxxx          | 0x0800..0xFFFF    | 1110zzzz   | 10yyyyyy    | 10xxxxxx   |             |
| 000uuuuu zzzzyyyy yyxxxxxx | 0x10000..0x10FFFF | 11110uuu   | 10uuzzzz    | 10yyyyyy   | 10xxxxxx    |

编码后的字节序列和标量值间的对应关系：

| 标量值             | First Byte | Byte Second | Third Byte | Fourth Byte |
| ------------------ | ---------- | ----------- | ---------- | ----------- |
| U+0000..U+007F     | 00..7F     |             |            |             |
| U+0080..U+07FF     | C2..DF     | 80..BF      |            |             |
| U+0800..U+0FFF     | E0         | A0..BF      | 80..BF     |             |
| U+1000..U+CFFF     | E1..EC     | 80..BF      | 80..BF     |             |
| U+D000..U+D7FF     | ED         | 80..9F      | 80..BF     |             |
| U+E000..U+FFFF     | EE..EF     | 80..BF      | 80..BF     |             |
| U+10000..U+3FFFF   | F0         | 90..BF      | 80..BF     | 80..BF      |
| U+40000..U+FFFFF   | F1..F3     | 80..BF      | 80..BF     | 80..BF      |
| U+100000..U+10FFFF | F4         | 80..8F      | 80..BF     | 80..BF      |

### 2.2 UTF-16 CEF

**UTF-16 编码模式** (Encoding Form)：一种 Unicode 编码模式，会为 U+0000..U+D7FF 和 U+E000..U+FFFF 中的每个标量值分别分配一个唯一的无符号 16-bit 编码单元(编码单元的值与 Unicode 标量值相等)；会为 U+10000..U+10FFFF 中的每个标量值分别分配一个唯一代理对。下表展示了 UTF-16 中比特位编码方式： (See definition D91 in [Section 3.9, Unicode Encoding Forms](http://www.unicode.org/versions/latest/ch03.pdf#G7404).)

| Scalar Value               | UTF-16                            |
| -------------------------- | --------------------------------- |
| xxxxxxx xxxxxxxxx          | xxxxxxxx xxxxxxxx                 |
| 000uuuuu xxxxxxxx xxxxxxxx | 110110wwwwxxxxxx 110111xxxxxxxxxx |

#### 2.2.1 代理对

surrogate pairs 

**代理对** (Surrogate Pair)：用于表示辅助平面中的标量值，由包含两个 16-bit 编码单元的序列构成。代理对中的第一个值被称作高代理(high-surrogate)编码单元，第二个值被称作低代理(low--surrogate)编码单元。(See definition D75 in [Section 3.8, Surrogates](http://www.unicode.org/versions/latest/ch03.pdf#G2630).)

将标量值映射为代理对的算法大致如下：

```
假设辅助平面中某个标量值的十六进制值是x，显然：
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

代理对由 high 和 low 构成了，high 表示高代理编码单元，low 表示地代理编码单元。"高代理编码单元"的值位于 0xD800 ~ 0xDBFF 之间，"低代理编码单元"的值位于 0xDC00 ~ 0xDFFF 之间。为了避免与拥有相同值的码点混淆，所以在 U+D800 ~ U+DFFF 内的码点是不能通过"编码模式"映射为"编码单元序列"的，只有标量值可被映射为"编码单元序列"。这样的设计目的是为了便于判断某个"编码单元"是否是代码对中的一部分。

用 Python 描述计算过程如下，不考虑输入错误：

```python
def get_surrogate_pairs(char_or_code):
    """char_or_code:单个字符或码点值"""
    if isinstance(char_or_code, str):
        code_point = ord(char_or_code)
    else:
        code_point = char_or_code
    code_point -= 0x10000
    high_surrogate = (code_point // 0x400)+0xD800
    low_surrogate = (code_point % 0x400)+0xDC00
    print(hex(high_surrogate), hex(low_surrogate))

get_surrogate_pairs("𐐷")
get_surrogate_pairs("𤭢")
get_surrogate_pairs(0x10FFFF) # 输出最大码点值的代理对
```

输出：

```
0xd801 0xdc37
0xd852 0xdf62
0xdbff 0xdfff
```

为了便于理解，再补充几个术语：

> ***代理码点*** (Surrogate Code Point)：位于 U+D800 ~ U+DFFF 之间的 Unicode 码点属于作代理码点，保留共 UTF-16 使用。UTF-16 使用一对代理编码单元"表示"辅助码点。
>
> ***高代理码点*** (High-Surrogate Code Point)：位于 U+D800 ~ U+DBFF 间的 Unicode 码点属于高代理码点。(See definition D71 in [Section 3.8, Surrogates](http://www.unicode.org/versions/latest/ch03.pdf#G2630).)
>
> ***高代理编码单元*** (High-Surrogate Code Unit)：位于 0xD800 ~ 0xDBFF 间的 16-bit 编码单元，在 UTF-16 中被用作代理对的第一个编码单元。(See definition D72 in [Section 3.8, Surrogates](http://www.unicode.org/versions/latest/ch03.pdf#G2630).)
>
> ***低代理码点*** (Low-Surrogate Code Point)：位于 U+DC00 ~ U+DFFF 间的 Unicode 码点属于低代理码点。(See definition D73 in [Section 3.8, Surrogates](http://www.unicode.org/versions/latest/ch03.pdf#G2630).)
>
> ***低代理编码单元*** (Low-Surrogate Code Unit)：位于 0xDC00~ 0xDFFF 间的 16-bit 编码单元，在 UTF-16 中被用作代理对的第二个编码单元。(See definition D74 in [Section 3.8, Surrogates](http://www.unicode.org/versions/latest/ch03.pdf#G2630).)

### 2.3 UTF-32 CEF

**UTF-32 编码模式** (Encoding Form)：一种 Unicode 编码模式，会为每个 Unicode 标量值分配一个唯一的无符号 32-bit 编码单元(编码单元的值与 Unicode 标量值相等)。(See definition D90 in [Section 3.9, Unicode Encoding Forms](http://www.unicode.org/versions/latest/ch03.pdf#G7404).)

UTF-32 虽可编码所有 Unicode 码点，但是相比其它编码模式会占用更多的空间。

## 3. UCS

***UCS*** - Universal Character Set 通用字符集，由 International Standard ISO/IEC 10646 所规定，与 Unicode 标准相同。

***UCS-2*** ：ISO/IEC 10646 编码模式，使用两个 8 位字节编码通用字符集，仅限于基本多语言平面，不能编码辅助平面。UCS-2 是固定宽度编码模式。tips：Notepad++ 支持 UCS-2 编码，如果在 UCS-2 编码的文件保存辅助平面中的字符，再次打开该文件时会发现辅助字符会变为另一个 BMP 字符，字符信息发生了丢失。

***UCS-4*** ：ISO/IEC 10646 编码模式：使用 4 个 8 位字节编码通用字符集，适用于所有平面。

## 4. 相关术语补充

以下内容直接翻译自 Unicode 术语表：

> - ***Unicode 编码模式*** (Unicode Encoding Form)：一种字符编码模式，用于为每个 Unicode 标量值(scalar value)分别分配一个唯一的"编码单元序列"。Unicode 标准定义了三种 Unicode 编码模式：UTF-8, UTF-16, and UTF-32。(See definition D79 in [Section 3.9, Unicode Encoding Forms](http://www.unicode.org/versions/latest/ch03.pdf#G7404).)
>
> - ***字符编码模式*** (Character Encoding Form)：简称编码模式，将字符集中的定义(definition)映射到表示数据的实际编码单元。另外，Encoding Form 与 character encoding form 同义
>
> - ***转换格式*** (Transformation Format)：从已编码字符序列到唯一编码序列的映射(typically bytes)。
>
> - ***代理码点*** (Surrogate Code Point)：位于 U+D800 ~ U+DFFF 之间的 Unicode 码点属于作代理码点，保留共 UTF-16 使用。UTF-16 使用一对代理编码单元"表示"辅助码点。

