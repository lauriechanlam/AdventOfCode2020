import utils
import re


pattern = re.compile(r'^(?P<first>\d+)-(?P<last>\d+) (?P<value>\w): (?P<password>[A-Za-z0-9]+)$')


class Password:
    def __init__(self, line):
        match = pattern.search(line)
        self.first = int(match.group('first'))
        self.last = int(match.group('last'))
        self.value = match.group('value')
        self.password = match.group('password')

    def is_valid_1(self):
        return self.first <= self.password.count(self.value) <= self.last

    def is_valid_2(self):
        match_first = self.password[self.first - 1] == self.value
        match_last = self.password[self.last - 1] == self.value
        return match_first ^ match_last


def read_input(filename):
    return utils.read(filename, 'array')


class Part1(utils.Part):
    def __init__(self):
        super().__init__(2)

    def run(self, input):
        return sum([Password(x).is_valid_1() for x in input])


class Part2(utils.Part):
    def __init__(self):
        super().__init__(1)

    def run(self, input):
        return sum([Password(x).is_valid_2() for x in input])
