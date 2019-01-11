class Matrix(object):
    def __init__(self, matrix_string):
        self.matrix_int = []
        for row in [i.split(' ') for i in matrix_string.splitlines()]:
            self.matrix_int.append([int(i) for i in row])

    def row(self, index):
        return self.matrix_int[index]

    def column(self, index):
        return [i[index] for i in self.matrix_int]
