import re
import utils
import numpy
import itertools

pattern = re.compile(r'(mem\[(?P<address>\d+)\] = (?P<value>\d+))|(mask = (?P<mask>[01X]+))')


def read_input(filename):
    n = utils.read(filename, 'string').split(',')
    return [int(m) for m in n]


def turn(inp):
    last_turn = inp[-1]
    if inp.count(last_turn) == 1:
        return 0
    idx = [i for i, c in enumerate(inp) if c == last_turn]
    return idx[-1] - idx[-2]

class Part1(utils.Part):
    def __init__(self):
        super().__init__(0)

    def run(self, input, is_test):
        n = 10 if is_test else 2020
        while len(input) < n:
            input.append(turn(input))
        return input[-1]


def turn_with_cache(inp, cache):
    last_turn = inp[-1]
    c = cache[last_turn]
    if len(c) == 1:
        return 0
    return c[-1] - c[-2]


class Part2(utils.Part):
    def __init__(self):
        super().__init__(175594)

    def run(self, input, is_test):
        n = 30000000
        cache = {}
        for i, c in enumerate(input):
            cache[c] = [i]
        while len(input) < n:
            val = turn_with_cache(input, cache)
            input.append(val)
            if val not in cache:
                cache[val] = []
            cache[val].append(len(input) - 1)
        return input[-1]
