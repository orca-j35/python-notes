import re
import string


def abbreviate(words):
    return ''.join([i[0].upper() for i in re.split(r'\s*[-,\s]\s*', words)])
