print('in moduleC, and say:')
import sys
print(sys.path)
if __name__ == '__main__':
    print('This program is being run by itself...')
else:
    print('I am being imported from another module...')
from pkg1 import moduleB

print(__package__)