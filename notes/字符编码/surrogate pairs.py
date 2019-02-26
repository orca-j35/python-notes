
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
get_surrogate_pairs("𤭢")
get_surrogate_pairs(0x10FFFF)
