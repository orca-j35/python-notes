def prime_factors(natural_number):
    primes, n = [], 2
    while natural_number > 1:
        while natural_number % n == 0:
            primes.append(n)
            natural_number //= n
        n += 1
    return primes
