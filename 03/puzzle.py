import math
import re
import utils


pattern = re.compile(r'#')


class Grid:
    def __init__(self, lines):
        self.trees = [[group.span()[0] for group in pattern.finditer(line)] for line in lines]
        self.width = len(lines[0]) - 1  # Remove \n
        self.height = len(lines)

    def is_tree(self, x, y):
        return (x % self.width) in self.trees[y]

    def run_slope(self, x_step, y_step):
        return sum([self.is_tree(y * x_step / y_step, y) for y in range(0, self.height, y_step)])


def read_input(filename):
    return Grid(utils.read(filename, 'array'))


class Part1(utils.Part):
    def __init__(self):
        super().__init__(7)

    def run(self, input, is_test):
        return input.run_slope(3, 1)


class Part2(utils.Part):
    def __init__(self):
        super().__init__(336)

    def run(self, input, is_test):
        steps = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        slopes = [input.run_slope(step[0], step[1]) for step in steps]
        return math.prod(slopes)
