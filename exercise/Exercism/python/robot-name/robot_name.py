from random import choice
from string import ascii_uppercase, digits


class Robot(object):
    names = set()

    def __init__(self):
        self.reset()

    def reset(self):
        while True:
            self.name = ''.join((
                choice(ascii_uppercase),
                choice(ascii_uppercase),
                choice(digits),
                choice(digits),
                choice(digits),
            ))
            if self.name not in Robot.names:
                Robot.names.add(self.name)
                return
