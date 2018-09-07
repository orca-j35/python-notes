# 字符编码方案(CES)

Character Encoding Scheme (CES)

[TOC]

Tips：由于部分"编码模式"与"编码方案"拥有相同的名称，本文为了避免出现混淆，会使用完整术语，比如用 UTF-16 CEF 表示"UTF-16 编码模式"，使 UTF-16 CES 表示"UTF-16 编码方案"。

在基于字节(8-bits)的文件系统或网络系统中，所有的数据都以字节为单位。而在 Unicode 标准中，不同 CEF 的编码单元的位数并不相同：UTF-8 CEF 中使用 8-bit 编码单元；UTF-16 CEF中使用 16-bit 编码单元；UTF-32 CEF 中使用 32-bit 编码单元。如果编码单元不是 8-bit 的话，便无法在基于字节的系统中直接使用，因此需要先将 16-bit 或 32-bit 编码单元转换为字节序列，所以便出现了"字符编码方案"的概念。

**字符编码方案**的作用就是将"编码单元序列"转换为"字节序列"，并且是可逆转换。

Unicode 中的 CES 可分为两类，共 7 种：

- 简单 CES：UTF-8 CES 、UTF-16BE CES 、 UTF-16LE CES 、 UTF-32BE CES 、UTF-32LE CES ，简单 CES 均不带 BOM(字节顺序标记)
  - **UTF-8 CES**：UTF-8 CEF 中使用 8-bit 编码单元，转换时直接导出编码单元即可；
  - **UTF-16BE CES**：会将每个 16-bit 编码单元转换为 2 个字节，第 1 个字节表示高 8 位，第 2 个字节表示低 8 位，不带 BOM；
  - **UTF-16LE CES**：会将每个 16-bit 编码单元转换为 2 个字节，第 1 个字节表示低 8 位，第 2 个字节表示高 8 位，不带 BOM；
  - **UTF-32BE CES**：会将每个 32-bit 编码单元转换为 4 个字节，第 1 个字节表示 32 ~  25 比特位，第 2 个字节表示 24 ~  17 比特位，依次类推，不带 BOM；
  - **UTF-32LE CES**：会将每个 32-bit 编码单元转换为 4 个字节，第 1 个字节表示 1 ~  8 比特位，第 2 个字节表示 9 ~  16 比特位，依次类推，不带 BOM；
- 复合 CES：UTF-16 CES 和 UTF-32 CES
  - **UTF-16 CES**：由 UTF-16BE CES 或  UTF-16LE CES 加 BOM 构成
  - **UTF-32 CES**：由 UTF-32BE CES 或  UTF-32LE CES 加 BOM 构成

## 1. 字节序列

字节顺序标记(*byte order mark* - BOM)是 Unicode 中的一个特殊字符，其码点是 U+FEFF。该特殊字符被用于文件或字节流的开头，用于说明每个字节序列的长度和顺序。不同 CES 的字节标记标记顺序如下：

| Bytes       | Encoding Scheme       |
| ----------- | --------------------- |
| 00 00 FE FF | UTF-32, big-endian    |
| FF FE 00 00 | UTF-32, little-endian |
| FE FF       | UTF-16, big-endian    |
| FF FE       | UTF-16, little-endian |
| EF BB BF    | UTF-8                 |

big-endian 高字节优先；little-endian 低字节优先。

这两个古怪的名称来自英国作家斯威夫特的《格列佛游记》，在该书中，小人国里爆发了内战，战争起因是人们争论，吃鸡蛋时究竟是从大头(Big-Endian)敲开还是从小头(Little-Endian)敲开。为了这件事情，前后爆发了六次战争，一个皇帝送了命，另一个皇帝丢了王位。

## 2. 相关术语补充

以下内容直接翻译自 Unicode 术语表：

> - ***Unicode 编码方案*** (Encoding Scheme)：是指拥有特定字节序列的 Unicode 编码模式。如果允许的话，会包含字节顺序标记(byte order mark - BOM)。(See definition D94 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)
>
> - ***字符编码方案*** (Character Encoding Scheme)：字符编码模式加上字节序列。Unicode 中有 7 中编码方案：UTF-8, UTF-16, UTF-16BE, UTF-16LE, UTF-32, UTF-32BE, UTF-32LE。另外，Encoding Scheme 与 character encoding scheme 同义
>
>
>
> - ***UTF-8 编码方案*** (*Encoding Scheme*)：该 Unicode 编码方案会使用与 UTF-8 "编码单元序列"自身完全相同的顺序来序列化"编码单元序列"。(See definition D95 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)The Unicode encoding scheme that serializes a UTF-8 code unit sequence in exactly the same order as the code unit sequence itself. 
>
>
>
> - ***UTF-16 编码方案*** (Encoding Scheme)：该编码方案会将 UTF-16 "编码单元序列"序列化为 big-endian 或 little-endian 格式的字节序列。(See definition D98 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)
> - ***UTF-16BE*** ：一种 Unicode 编码方案，会将 UTF-16 "编码单元序列"序列化为 big-endian 格式的字节序列。(See definition D96 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)
> - ***UTF-16LE*** ：一种 Unicode 编码方案，会将 UTF-16 "编码单元序列"序列化为 little-endian 格式的字节序列。(See definition D96 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)
>
>
>
> - ***UTF-32 编码方案*** (Encoding Scheme)：该 Unicode 编码方案会将 UTF-32 "编码单元序列" 序列化为 big-endian 或 little-endian 格式的字节序列。(See definition D101 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)
>
> - ***UTF-32BE*** ：一种 Unicode 编码方案，会将 UTF-32 "编码单元序列"序列化为 big-endian 格式的字节序列。(See definition D99 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)
>
> - ***UTF-32LE*** ：一种 Unicode 编码方案，会将 UTF-32 "编码单元序列"序列化为 little-endian 格式的字节序列。 (See definition D100 in [Section 3.10, Unicode Encoding Schemes](http://www.unicode.org/versions/latest/ch03.pdf#G28070).)
>
>
>
> - ***字节序列*** (Byte Serialization)：The order of a series of bytes determined by a computer architecture.由计算机体系结构确定的一系列字节的顺序。
>
>   不同的处理器架构会将多字节机器整数映射到存储器中的不同位置，*Little Endian* 构架会将位于末尾的有效字节放置在低地址上，*Big Endian* 构架会将位于头部有效字节放置在低地址上。在计算机内存中存储存储的数据类型的长度大于一字节时，如果最高有效字节被优先存储，便是被称为 big-endian，若果最高有效字节被最后存储，便是 latter little-endian。https://www.unicode.org/reports/tr17/#ByteOrder  https://www.unicode.org/faq/utf_bom.html#bom3
>
> - ***字节序列标记*** (byte order mark - BOM)：Unicode 字符 U+FEFF 用于表示文本的字节顺序(See [Section 2.13, Special Characters and Noncharacters](http://www.unicode.org/versions/latest/ch02.pdf#G27981), and [Section 23.8, Specials](http://www.unicode.org/versions/latest/ch23.pdf#G19635).)
>
> - ***Little-endian*** ：A computer architecture that stores multiple-byte numerical values with the least significant byte (LSB) values first. 低字节优先，小端模式
>
> - ***Big-endian***. A computer architecture that stores multiple-byte numerical values with the most significant byte (MSB) values first. 高字节优先，大端模式



