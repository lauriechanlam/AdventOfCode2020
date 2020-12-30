import re
import utils


class Group:
    def __init__(self, lines):
        self.persons = lines

    def count_any(self):
        return len(set(self.persons.replace('\n', '')))

    def count_all(self):
        persons = [set(person) for person in self.persons.splitlines()]
        return len(persons[0].intersection(*persons[1:]))


def read_input(filename):
    text = utils.read(filename, 'string')
    return [Group(x) for x in text.split('\n\n')]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(11)

    def run(self, input, is_test):
        return sum([x.count_any() for x in input])


class Part2(utils.Part):
    def __init__(self):
        super().__init__(6)

    def run(self, input, is_test):
        return sum([x.count_all() for x in input])