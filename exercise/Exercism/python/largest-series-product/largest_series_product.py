from operator import mul
from functools import reduce


def largest_product(series, size):
    if size == 0:
        return 1
    if any((size > len(series), not series.isdecimal(), size < 0)):
        raise ValueError('size is wrong value')

    max_v = 0
    for i in range(0, len(series) - size + 1):
        max_v = max(reduce(mul, [int(j) for j in series[i:i + size]]), max_v)
    return max_v
