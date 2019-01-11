from string import ascii_lowercase


def is_pangram(sentence):
    # issubset可接受序列类型的参数
    return set(ascii_lowercase).issubset(sentence.lower())