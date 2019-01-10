# from pprint import pprint
# pprint(sys.modules)
import sys
print(f'sys.argv: {sys.argv}')
print(f'sys.path: {sys.path}')
print('=================')
print('in main, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...')
else:
    print('I am being imported from another module...')
from pkg import moduleA
if __name__ == "__main__" and __package__ is None:
    __package__ = "pkg"
from . import moduleA
print(__package__, '===')
