import utils
import itertools
import math


def read_input(filename):
    lines = utils.read(filename, 'array')  # string, array, json
    outlets = [int(x) for x in lines]
    return [0] + sorted(outlets) + [max(outlets) + 3]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(220)

    def run(self, input, is_test):
        diff = [current - previous for previous, current in zip(input, input[1:])]
        return diff.count(3) * diff.count(1)


class Part2(utils.Part):
    def __init__(self):
        super().__init__(19208)

    def run(self, input, is_test):
        count = list(itertools.repeat(0, input[-1] + 1))
        count[0] = 1
        for joltage in input[1:]:
            count[joltage] = count[joltage - 1] + count[joltage - 2] + count[joltage - 3]
        return count[-1]
