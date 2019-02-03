def sieve(n):
    # Note: you do not use division or remainder operations

    IsPrime = [True] * (n + 1)
    IsPrime[1] = False  # 1 is not prime
    for i in range(2, int(n**0.5) + 1):
        if IsPrime[i]:
            for j in range(i * i, n + 1, i):
                IsPrime[j] = False
    return [x for x in range(2, n + 1) if IsPrime[x]]
