import re


def word_count(phrase):
    pat = re.compile(r"""[a-zA-Z0-9]+'*[a-zA-Z]*""")
    words = [i.strip("'").lower() for i in pat.findall(phrase)]
    counter = dict()
    for i in words:
        counter[i] = counter.get(i, 0) + 1
    return counter
