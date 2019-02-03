# Globals for the bearings
# Change the values as you see fit

from collections import namedtuple
NORTH = namedtuple('NORTH', ['x', 'y'])(0, 1)  # 北
EAST = namedtuple('NORTH', ['x', 'y'])(1, 0)  # 东
SOUTH = namedtuple('NORTH', ['x', 'y'])(0, -1)  # 南
WEST = namedtuple('NORTH', ['x', 'y'])(-1, 0)  # 西


class Robot(object):
    bearings = [NORTH, EAST, SOUTH, WEST]

    def __init__(self, bearing, x, y):
        self.bearing = bearing
        self.coordinates = (x, y)

    def turn_right(self):
        self.bearing = Robot.bearings[(Robot.bearings.index(self.bearing) + 1)
                                      % 4]

    def turn_left(self):

        self.bearing = Robot.bearings[(Robot.bearings.index(self.bearing) + 3)
                                      % 4]

    def advance(self):
        self.coordinates = (
            self.bearing.x + self.coordinates[0],
            self.bearing.y + self.coordinates[1],
        )

    def simulate(self, command):
        for i in command:
            {
                'A': self.advance,
                'L': self.turn_left,
                'R': self.turn_right,
            }.get(i, lambda: None)()
