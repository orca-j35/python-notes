from collections.abc import Iterable


def flatten(iterables):
    x = []
    for i in iterables:
        if isinstance(i, Iterable) and not isinstance(i, (str, bytes)):
            x += flatten(i)
        else:
            x += [] if i is None else [i]
    return x


'''Another good solution:
def _flatten(lst):
    for item in lst:
        if item is None:
            continue
        if isinstance(item, (str, bytes)):
            yield item
        elif isinstance(item, Iterable):
            yield from flatten(item)
        else:
            yield item

def flatten(lst):
    return list(_flatten(lst))
'''
