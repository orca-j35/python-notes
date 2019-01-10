print('in other, and say:')
if __name__ == '__main__':
    print('This program is being run by itself...')
else:
    print('I am being imported from another module...')
# from . import pkg
print(__package__)
