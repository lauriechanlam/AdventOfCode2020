import utils


def read_input(filename):
    return [int(x) for x in utils.read(filename, 'array')]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(514579)

    def run(self, input, is_test):
        for x in input:
            if (2020 - x) in input:
                return x * (2020 - x)


class Part2(utils.Part):
    def __init__(self):
        super().__init__(241861950)

    def run(self, input, is_test):
        for i, x in enumerate(input):
            for j in range(i + 1, len(input)):
                if (2020 - x - input[j]) in input:
                    return x * input[j] * (2020 - x - input[j])
