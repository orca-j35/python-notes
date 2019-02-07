def sum_of_multiples(limit, multiples):
    return sum({x for m in multiples if m != 0 for x in range(m, limit, m)})
