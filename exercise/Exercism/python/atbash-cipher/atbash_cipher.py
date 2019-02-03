import re
from string import ascii_lowercase
CIPHER = ''.join(reversed(ascii_lowercase))


def encode(plain_text):
    s = ''.join(re.findall(r'[a-z0-9]+', plain_text.lower()))
    s = s.translate(str.maketrans(ascii_lowercase, CIPHER))
    return ' '.join([s[i:i + 5] for i in range(0, len(s), 5)])


def decode(ciphered_text):
    s = ''.join(ciphered_text.split(' '))
    return s.translate(str.maketrans(CIPHER, ascii_lowercase))