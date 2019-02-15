vowels = list('aeiou')


def t_(word):
    if word[0] in vowels or word[0:2] in ('xr', 'yt'):
        return word + 'ay'
    for i, j in enumerate(word):
        if j in vowels:
            if word[i - 1:i + 1] == 'qu':
                return word[i + 1:] + word[:i + 1] + 'ay'
            return word[i:] + word[:i] + 'ay'
        elif i > 0 and j == 'y':
            return word[i:] + word[:i] + 'ay'


def translate(text):
    return ' '.join([t_(w) for w in text.split(' ')])
