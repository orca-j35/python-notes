def to_roman(base, base_1, base_5, base_10):
    d = {}
    for i in range(1, 10):
        if 0 <= i <= 3:
            d[i * base] = base_1 * i
        elif i == 4:
            d[i * base] = base_1 + base_5
        elif 5 <= i <= 8:
            d[i * base] = base_5 + (i - 5) * base_1
        elif i == 9:
            d[i * base] = base_1 + base_10
    return d


roman_numerals = to_roman(1, 'I', 'V', 'X')
roman_numerals.update(to_roman(10, 'X', 'L', 'C'))
roman_numerals.update(to_roman(100, 'C', 'D', 'M'))
roman_numerals.update({i: 'M' * (i // 1000) for i in range(1000, 10000, 1000)})
print(roman_numerals)


def numeral(number):
    r = []
    for n, v in enumerate(reversed(list(str(number)))):
        roman_numerals.get(int(v) * pow(10, n), '')
        r.append(roman_numerals.get(int(v) * pow(10, n), ''))
    return ''.join(reversed(r))


'''Another good solution:
roman_numbers = (
    ( 'M',  1000 ), ( 'CM',  900 ),
    ( 'D',   500 ), ( 'CD',  400 ),
    ( 'C',   100 ), ( 'XC',   90 ),
    ( 'L',    50 ), ( 'XL',   40 ),
    ( 'X',    10 ), ( 'IX',    9 ),
    ( 'V',     5 ), ( 'IV',    4 ),
    ( 'I',     1 )
)

def numeral(arabic):

    if arabic < 1:
        raise ValueError("Romans did not count below 1")
    if arabic > 3000:
        raise ValueError("Romans did not count beyond 3000")

    roman = ""

    for roman_number, value in roman_numbers:
        while arabic >= value:
            roman += roman_number
            arabic -= value

    return roman
'''
