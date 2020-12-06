import re
import utils


pattern = re.compile(r'^(?P<key>\S+):(?P<value>\d+)$')


class Object:
    def __init__(self, line):
        match = pattern.search(line)
        self.key = match.group('key')
        self.value = int(match.group('value'))

    def count(self):
        return self.value


def read_input(filename):
    text = utils.read(filename, 'array')  # string, array, json
    return [Object(x) for x in text.splitlines()]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(0)

    def run(self, input):
        return sum([x.count() for x in input])


# class Part2(utils.Part):
#     def __init__(self):
#         super().__init__(0)
#
#     def run(self, input):
#         return sum(input)
