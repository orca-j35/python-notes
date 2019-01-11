import re


def is_isogram(string):
    pat = re.compile(r'[a-zA-z]+')
    letters = ''.join(pat.findall(string)).lower()
    return True if len(set(letters)) == len(letters) else False


#     print(letters)

# is_isogram('sada d=a-sd')