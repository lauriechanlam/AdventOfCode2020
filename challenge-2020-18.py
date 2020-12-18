import re
import utils

int_pattern = re.compile(r'^(\d+)$')

pattern = re.compile(r'^(?P<left>\d+) (?P<op>\+|\*) (?P<right>\d+)')
pattern_add = re.compile(r'(?P<left>\d+) \+ (?P<right>\d+)')
pattern_mul = re.compile(r'(?P<left>\d+) \* (?P<right>\d+)')
parenthesis_pattern = re.compile(r'\((?P<val>[0-9 \+\*]+)\)')


def read_input(filename):
    return utils.read(filename, 'string').splitlines()  # string, array, json


def count_val(line):
    def replace(match):
        if match.group('op') == '+':
            val = str(int(match.group('left')) + int(match.group('right')))
        else:
            val = str(int(match.group('left')) * int(match.group('right')))
        return val
    def parenthesis_replace(match):
        return str(count_val(match.group('val')))
    new_line = parenthesis_pattern.sub(parenthesis_replace, line)
    print(new_line)
    while new_line != line:
        line = new_line
        new_line = parenthesis_pattern.sub(parenthesis_replace, line)
        print(new_line)
    while int_pattern.fullmatch(new_line) is None:
        new_line = pattern.sub(replace, new_line)
        print(new_line)
    return int(new_line)


class Part1(utils.Part):
    def __init__(self):
        super().__init__(13632)

    def run(self, input, is_test):
        return sum([count_val(x) for x in input])


def count_val2(line):
    def replace(match, op):
        if op == '+':
            val = str(int(match.group('left')) + int(match.group('right')))
        else:
            val = str(int(match.group('left')) * int(match.group('right')))
        return val
    def parenthesis_replace(match):
        return str(count_val2(match.group('val')))
    new_line = parenthesis_pattern.sub(parenthesis_replace, line)
    print(new_line)
    while new_line != line:
        line = new_line
        new_line = parenthesis_pattern.sub(parenthesis_replace, line)
    line = new_line
    new_line = pattern_add.sub(lambda x: replace(x, '+'), line)
    print(new_line)
    while new_line != line:
        line = new_line
        new_line = pattern_add.sub(lambda x: replace(x, '+'), line)
        print(new_line)
    while int_pattern.fullmatch(new_line) is None:
        line = new_line
        new_line = pattern_mul.sub(lambda x: replace(x, '*'), line)
        print(new_line)
    return int(new_line)

class Part2(utils.Part):
    def __init__(self):
        super().__init__(23340)

    def run(self, input, is_test):
        return sum([count_val2(x) for x in input])