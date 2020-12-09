import copy
import utils


def read_input(filename):
    lines = utils.read(filename, 'array')  # string, array, json
    return [int(line) for line in lines]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(127)

    def run(self, input, is_test):
        previous_count = 5 if is_test else 25
        for i in range(previous_count, len(input)):
            previous = input[i-previous_count:i]
            if not any([input[i] - previous[j] in previous[j+1:] for j in range(0, len(previous))]):
                return input[i]


class Part2(utils.Part):
    def __init__(self):
        super().__init__(62)

    def run(self, input, is_test):
        input_value = Part1().run(input, is_test)
        for start in range(0, len(input)):
            for end in range(start+1, len(input)):
                consecutives = input[start:end]
                s = sum(consecutives)
                if s > input_value:
                    break
                if s == input_value:
                    return min(consecutives) + max(consecutives)
