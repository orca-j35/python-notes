import re


def verify(isbn):
    _isbn = isbn.replace('-', '')
    if re.compile(r'^\d{9}[X\d]$').match(_isbn):
        nums = list(_isbn)
        if nums[-1] == 'X':
            nums[-1] = '10'
        return sum(int(i) * j
                   for i, j in zip(nums, range(10, 0, -1))) % 11 == 0
    return False
