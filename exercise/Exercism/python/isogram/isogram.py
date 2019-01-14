import re


def is_isogram(string):
    pat = re.compile(r'[a-zA-z]+')
    letters = ''.join(pat.findall(string)).lower()
    return len(set(letters)) == len(letters)
