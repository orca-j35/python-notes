print(f'in {__name__}')
# from . import a_2
# a_2 = __import__('a_2', globals(), locals(), (), 1)
# __import__('b_1', globals={'__package__': 'top_pkg.pkg_b'}, level=1)
__import__(
    'b_1',
    globals={
        '__package__': 'top_pkg.pkg_b',
        '__name__': 'top_pkg.pkg_b.b_2',
    },
    level=1)
# print(__package__)