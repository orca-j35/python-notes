class Allergies(object):
    items = {
        'eggs': 1,
        'peanuts': 2,
        'shellfish': 4,
        'strawberries': 8,
        'tomatoes': 16,
        'chocolate': 32,
        'pollen': 64,
        'cats': 128,
    }

    def __init__(self, score):
        self._score = score

    def is_allergic_to(self, item):
        return bool(Allergies.items.get(item, 0) & self._score)

    @property
    def lst(self):
        return [k for k, v in Allergies.items.items() if v & self._score]
