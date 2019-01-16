# # Score categories
# # Change the values as you see fit
from collections import Counter
from typing import List


def YACHT(dice: List[int]):
    return 50 if len(set(dice)) == 1 else 0


def ONES(dice: List[int]):
    return dice.count(1)


def TWOS(dice: List[int]):
    return dice.count(2) * 2


def THREES(dice: List[int]):
    return dice.count(3) * 3


def FOURS(dice: List[int]):
    return dice.count(4) * 4


def FIVES(dice: List[int]):
    return dice.count(5) * 5


def SIXES(dice: List[int]):
    return dice.count(6) * 6


def FULL_HOUSE(dice: List[int]):
    return sum(dice) if sorted(Counter(dice).values()) == [2, 3] else 0


def FOUR_OF_A_KIND(dice: List[int]):
    for i in set(dice):
        if dice.count(i) >= 4:
            return i * 4
    return 0


def LITTLE_STRAIGHT(dice: List[int]):
    return 30 if sorted(dice) == [1, 2, 3, 4, 5] else 0


def BIG_STRAIGHT(dice: List[int]):
    return 30 if sorted(dice) == [2, 3, 4, 5, 6] else 0


def CHOICE(dice: List[int]):
    return sum(dice)


def score(dice, category):
    return category(dice)
