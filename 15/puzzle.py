import utils
from collections import defaultdict


def read_input(filename):
    text = utils.read(filename, 'string').split(',')
    return [int(n) for n in text]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(0)

    def run(self, input, is_test):
        n = 2020
        while len(input) < n:
            input.append(Part1.turn(input))
        return input[-1]

    @staticmethod
    def turn(input):
        num = input[-1]
        if input.count(num) == 1:
            return 0
        turns = [i for i, n in enumerate(input) if n == num]
        return turns[-1] - turns[-2]


class Part2(utils.Part):
    def __init__(self):
        super().__init__(175594)

    def run(self, input, is_test):
        turns_per_num = defaultdict(list)
        for turn_count, num in enumerate(input):
            turns_per_num[num].append(turn_count)
        num = input[-1]
        for turn_count in range(len(input), 30000000):
            turns = turns_per_num[num]
            num = turns[-1] - turns[-2] if len(turns) > 1 else 0
            turns_per_num[num].append(turn_count)
        return num
