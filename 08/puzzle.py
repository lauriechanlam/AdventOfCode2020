import re
import utils
import copy

pattern = re.compile(r'^(?P<operator>nop|acc|jmp) (?P<sign>-|\+)(?P<value>\d+)$')


class Operation:
    def __init__(self, line):
        match = pattern.search(line)
        self.operator = match.group('operator')
        sign = 1 if match.group('sign') == '+' else -1
        self.value = int(match.group('value')) * sign


class State:
    def __init__(self):
        self.line = 0
        self.accumulator = 0
        self.executed_instructions = set()

    def execute(self, operations):
        self.executed_instructions.add(self.line)
        operation = operations[self.line]
        if operation.operator == 'nop':
            self.line += 1
        elif operation.operator == 'jmp':
            self.line += operation.value
        elif operation.operator == 'acc':
            self.accumulator += operation.value
            self.line += 1


def read_input(filename):
    lines = utils.read(filename, 'array')
    return [Operation(line) for line in lines]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(5)

    def run(self, input, is_test):
        state = State()
        while state.line not in state.executed_instructions:
            state.execute(input)
        return state.accumulator


class Part2(utils.Part):
    def __init__(self):
        super().__init__(8)

    def run(self, input, is_test):
        indices = [index for index, x in enumerate(input) if x.operator == 'jmp']
        for index in indices:
            lines = copy.deepcopy(input)
            lines[index].operator = 'nop'
            accumulator = Part2.compute(lines)
            if accumulator is not None:
                return accumulator

        indices = [index for index, x in enumerate(input) if x.operator == 'nop']
        for index in indices:
            lines = copy.deepcopy(input)
            lines[index].operator = 'jmp'
            accumulator = Part2.compute(lines)
            if accumulator is not None:
                return accumulator

    @staticmethod
    def compute(input):
        state = State()
        while state.line not in state.executed_instructions and state.line < len(input):
            state.execute(input)
        return state.accumulator if state.line >= len(input) else None
