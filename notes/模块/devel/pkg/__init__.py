print('in pkg.__init__, and say:')
print(__package__)
import sys
print(sys.path)
if __name__ == '__main__':
    print('This program is being run by itself...')
else:
    print('I am being imported from another module...')
