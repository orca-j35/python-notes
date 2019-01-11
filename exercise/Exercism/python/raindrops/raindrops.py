s = ((3, 'Pling'), (5, 'Plang'), (7, 'Plong'))


def raindrops(number):
    result = [j for i, j in s if number % i == 0]
    return ''.join(result) if result else str(number)
