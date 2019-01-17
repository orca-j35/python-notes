def is_armstrong(number):
    return sum(pow(int(i), len(str(number))) for i in str(number)) == number
    '''
    # Complete this exercise with recursion

    def func(num: int, k):
        return pow(num % 10, k) + func(num // 10,
                                       k) if num // 10 != 0 else num**k

    return func(number, len(str(number))) == number
    '''
