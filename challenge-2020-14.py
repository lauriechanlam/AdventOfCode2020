import re
import utils
import numpy

pattern = re.compile(r'(mem\[(?P<address>\d+)\] = (?P<value>\d+))|(mask = (?P<mask>[01X]+))')
ZERO = numpy.uint64(0)
ONE = numpy.uint64(1)
RANGE = [numpy.uint64(i) for i in range(0, 36)]
MASK = numpy.sum([ONE << i for i in RANGE])

def read_input(filename):
    lines = utils.read(filename, 'string').splitlines()

    def make_instruction(line):
        match = pattern.match(line)
        if match.group('mask') is not None:
            return list(str(match.group('mask')))  #[uint64(char) if char in '01' else 'X' for char in list(str(match.group('mask')))]
        return {'address': numpy.uint64(match.group('address')), 'value': numpy.uint64(match.group('value'))}

    return [make_instruction(line) for line in lines]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(165)

    def run(self, input, is_test):
        memory = {}
        for instruction in input:
            if isinstance(instruction, list):  # mask
                bitmask = instruction
            else:
                address = instruction['address']
                value = instruction['value']
                memory[address] = Part1.apply(bitmask, value)
        return sum([val for val in memory.values()])

    @staticmethod
    def apply(bitmask, value):

        change_bit = {
            '0': lambda val, i: value - ONE << i if value >> i & ONE == ONE else value,
            '1': lambda val, i: value | ONE << i,
            'X': lambda val, i: value
        }

        for pos in RANGE:
            bit = bitmask[int(RANGE[-1] - pos)]
            value = change_bit[bit](value, pos) & MASK

        return value


class Part2(utils.Part):
    def __init__(self):
        super().__init__(208)

    def run(self, input, is_test):
        memory = {}
        for instruction in input:
            if isinstance(instruction, list):  # mask
                bitmask = instruction
            else:
                address = instruction['address']
                value = instruction['value']
                address_bitmask = Part2.get_address_bitmask(bitmask, address)
                memory.update({addr: value for addr in Part2.get_addresses(address_bitmask)})
        return sum([val for val in memory.values()])

    @staticmethod
    def get_address_bitmask(bitmask, address):
        address_bitmask = bitmask[:]
        for i in RANGE:
            if bitmask[i] == '0':
                address_bitmask[i] = '1' if address >> (RANGE[-1] - i) & ONE else '0'
        return address_bitmask

    @staticmethod
    def get_addresses(address_bitmask):
        addresses = set()

        try:
            index = address_bitmask.index('X')
        except ValueError:
            address = numpy.sum([ONE << numpy.uint64(RANGE[-1] - i) for i in RANGE if address_bitmask[i] == '1'])
            addresses.add(address)
            return addresses

        return set().union(
            Part2.get_addresses(address_bitmask[:index] + ['1'] + address_bitmask[index + 1:]),
            Part2.get_addresses(address_bitmask[:index] + ['0'] + address_bitmask[index + 1:])
        )
