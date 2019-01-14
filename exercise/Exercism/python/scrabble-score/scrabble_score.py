points = dict()
points.update(dict.fromkeys(('AEIOULNRST'), 1))
points.update(dict.fromkeys(('DG'), 2))
points.update(dict.fromkeys(('BCMP'), 3))
points.update(dict.fromkeys(('FHVWY'), 4))
points.update(dict.fromkeys(('K'), 5))
points.update(dict.fromkeys(('JX'), 8))
points.update(dict.fromkeys(('QZ'), 10))


def score(word):
    return sum([points[i.upper()] for i in list(word) if i.isalpha()])
