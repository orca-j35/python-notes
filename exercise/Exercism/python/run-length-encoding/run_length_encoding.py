import re


def decode_transform(i, j):
    return j if i == '' else int(i) * j


def decode(string):
    data = re.findall(r'(\d*)([a-zA-Z ])', string)
    return ''.join([decode_transform(*t) for t in data])


def encode_transform(i, j):
    return j if len(i) == 1 else str(len(i)) + j


def encode(string):
    data = re.findall(r'(([a-zA-Z ])\2*)', string)
    # string:'aaaAAbccc  fdsa'
    # data:[('aaa', 'a'), ('AA', 'A'), ('b', 'b'), ('ccc', 'c')]
    return ''.join([encode_transform(*t) for t in data])


''' nice solution in Community
from re import sub

def encode(s):
    return sub(r'(.)\1+', lambda x: str(len(x.group(0))) + x.group(1), s)


def decode(s):
    return sub(r'(\d+)(\D)', lambda x: x.group(2) * int(x.group(1)), s)
'''
