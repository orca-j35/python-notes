# Globals for the bearings
# Change the values as you see fit

# WEST = None  # 西
# NORTH = None  # 北
# EAST = None  # 东
# SOUTH = None  # 南


# def NORTH(t):
#     return WEST if t == 'L' else EAST
def NORTH(turn='L', advance=False):  # 北
    if advance:
        return (0, 1)
    return WEST if turn is 'L' else EAST


def EAST(turn='L', advance=False):  # 东
    if advance:
        return (1, 0)
    return NORTH if turn == 'L' else SOUTH


def SOUTH(turn='L', advance=False):  # 南
    if advance:
        return (0, -1)
    return EAST if turn == 'L' else WEST


def WEST(turn='L', advance=False):  # 西
    if advance:
        return (-1, 0)
    return SOUTH if turn == 'L' else NORTH


class Robot(object):
    def __init__(self, bearing=NORTH, x=0, y=0):
        self.bearing = bearing
        self.coordinates = (x, y)

    def turn_right(self):
        self.bearing = self.bearing('R')

    def turn_left(self):
        self.bearing = self.bearing('L')

    def advance(self):
        self.coordinates = tuple(
            i + j
            for i, j in zip(self.bearing(advance=True), self.coordinates))

    def simulate(self, command):
        for i in command:
            if i == 'A':
                self.advance()
            elif i == 'L':
                self.turn_left()
            elif i == 'R':
                self.turn_right()
            else:
                raise ValueError()


print(tuple(i + j for i, j in zip((0, 1), (0, 0))))
