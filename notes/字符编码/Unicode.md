# Unicode

[TOC]

### 参考

- [Glossary of Unicode Terms - Unicode 官方术语表](https://www.unicode.org/glossary/)
- [Character encoding - 字符编码](https://en.wikipedia.org/wiki/Character_encoding)
- [Self-synchronizing code - 自同步编码](https://en.wikipedia.org/wiki/Self-synchronizing_code)
- [Code point - 码点](https://en.wikipedia.org/wiki/Code_point)



## ASCII 码

一个字节是 8 位，可表示 256 个不同的符号。

ASCII 码一共规定了128个字符的编码，比如空格`SPACE`是32（二进制`00100000`），大写的字母`A`是65（二进制`01000001`）。这128个符号（包括32个不能打印出来的控制符号），只占用了一个字节的后面7位，最前面的一位统一规定为`0`。

由80H到0FFH共128个字符,一般称为"扩充字符",这128个扩充字符是由IBM制定的,并非标准的ASCII码.这些字符是用来表示框线、音标和其它欧洲非英语系的字母。



本文中提及的 `U+FFFE` 就是一个典型的非字符。



 

