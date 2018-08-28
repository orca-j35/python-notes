# bytearray

*class* bytearray([*source*[, *encoding*[, *errors*]]])

## 支持的编码

pass

## 



## bom





在 bytes 字面值中，十六进制和八进制转义符表示具有给定值的字节。

鲸 码点:9CB8

```
# 获取Unicode编码，此时看到的是大端模式
>>> bytes("鲸hellp","unicode_internal")
b'\xb8\x9ch\x00e\x00l\x00l\x00p\x00'
```

`fe ff` 表示 Big endian 大端模式；`ff fe` 表示 little endian 小端模式