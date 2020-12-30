import utils
import copy
import numpy
import itertools


def read_input(filename):
    lines = utils.read(filename, 'string').splitlines()
    return numpy.array([[char == '#' for char in line] for line in lines])


def pad(grid):
    return numpy.pad(grid, (1, 1), 'constant', constant_values=(False, False))


class Part1(utils.Part):
    def __init__(self):
        super().__init__(112)

    @staticmethod
    def get_state(cells):
        count = numpy.sum(cells)
        if cells[1][1][1]:
            return 2 < count < 5
        return count == 3

    @staticmethod
    def cycle(grid):
        grid = pad(grid)
        new_grid = copy.deepcopy(grid)

        for x in range(1, len(new_grid) - 1):
            for y in range(1, len(new_grid[x]) - 1):
                for z in range(1, len(new_grid[x][y]) - 1):
                    cells = grid[x - 1:x + 2, y - 1:y + 2, z - 1:z + 2]
                    new_grid[x][y][z] = Part1.get_state(cells)

        return new_grid

    def run(self, input, is_test):
        grid = pad(numpy.array([input]))

        for round in range(0, 6):
            grid = Part1.cycle(grid)

        return numpy.sum(grid)


class Part2(utils.Part):
    def __init__(self):
        super().__init__(848)

    @staticmethod
    def get_state(cells):
        count = numpy.sum(cells)
        if cells[1][1][1][1]:
            return 2 < count < 5
        return count == 3

    @staticmethod
    def cycle(grid):
        grid = pad(grid)
        new_grid = copy.deepcopy(grid)

        for x in range(1, len(new_grid) - 1):
            for y in range(1, len(new_grid[x]) - 1):
                for z in range(1, len(new_grid[x][y]) - 1):
                    for w in range(1, len(new_grid[x][y][z]) - 1):
                        cells = grid[x - 1:x + 2, y - 1:y + 2, z - 1:z + 2, w - 1:w + 2]
                        new_grid[x][y][z][w] = Part2.get_state(cells)
        return new_grid

    def run(self, input, is_test):
        grid = pad(numpy.array([numpy.array([input])]))

        for round in range(0, 6):
            grid = Part2.cycle(grid)

        return numpy.sum(grid)
