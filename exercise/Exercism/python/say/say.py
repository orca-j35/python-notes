from collections import deque
NUMERIC = {
    0: "",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen"
}
NUMERIC_TENS = {
    2: "twenty",
    3: "thirty",
    4: "forty",
    5: "fifty",
    6: "sixty",
    7: "seventy",
    8: "eighty",
    9: "ninety"
}
GROUP = {0: "", 1: " thousand", 2: " million", 3: " billion"}


def say(number):
    number = int(number)
    if number == 0:
        return 'zero'
    elif number < 0 or number >= 1e12:
        raise ValueError('Must be a positive number')
    else:
        num_groups = reversed([int(i) for i in format(number, ',').split(',')])
        words = deque()
        for j, v in enumerate(num_groups):
            sub_words = []
            if v > 99:
                sub_words.append(f"{NUMERIC.get(v // 100)} hundred"
                                 f"{' and' if v % 100 != 0 else ''}")
            if 0 < v % 100 < 20:
                sub_words.append(NUMERIC.get(v % 100))
            elif v % 100 >= 20:
                x, y = divmod(v % 100, 10)
                sub_words.append(f"{NUMERIC_TENS.get(x)}"
                                 f"{'-' + NUMERIC.get(y) if y != 0 else ''}")
            if sub_words:
                words.appendleft(' '.join(sub_words) + GROUP.get(j))
    return ' '.join(words)
