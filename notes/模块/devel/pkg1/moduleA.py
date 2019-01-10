import sys
print(sys.argv)
print(sys.path)
# print(sys.modules)

print('in pkg.moduleA, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...')
else:
    print('I am being imported from another module...')
from . import moduleC
