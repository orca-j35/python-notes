import re


# Complete this exercise with regular expression
def rotate(text, key):
    text = re.sub(
        r'[a-z]',
        lambda x: chr((ord(x.group(0)) - ord('a') + key) % 26 + ord('a')),
        text)
    return re.sub(
        r'[A-Z]',
        lambda x: chr((ord(x.group(0)) - ord('A') + key) % 26 + ord('A')),
        text)


from string import ascii_lowercase as al


# Complete this exercise with str.translate
def rotate1(text, key):
    key %= 26
    newchars = al[key:] + al[:key]
    trans = str.maketrans(al + al.upper(), newchars + newchars.upper())
    return text.translate(trans)
