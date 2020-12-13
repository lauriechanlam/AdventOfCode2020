import re
import utils
import math


# content_pattern = re.compile(r'(?P<count>\d+) (?P<color>[a-z ]+) bags?')
# container = container_pattern.match(line).group('container')
#  content = {match.group('color'): int(match.group('count')) for match in content_pattern.finditer(line)}

def read_input(filename):
    lines = utils.read(filename, 'string').splitlines()

    return (int(lines[0]), lines[1])


class Part1(utils.Part):
    def __init__(self):
        super().__init__(295)

    def run(self, input, is_test):
        time = input[0]
        pattern = re.compile(r'(?P<bus>\d+)')
        buses = {int(match.group('bus')) for match in pattern.finditer(input[1])}
        t = time
        while True:
            if any([(t % bus) == 0 for bus in buses]):
                b = [bus for bus in buses if (t % bus) == 0][0]
                return (t - time)*b
            t += 1

def primes():
    p = []
    for possiblePrime in range(2, 60):

        # Assume number is prime until shown it is not.
        isPrime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                isPrime = False
                break

        if isPrime:
            p.append(possiblePrime)
    return p

class Part2(utils.Part):
    def __init__(self):
        super().__init__(1068781)

    def run(self, input, is_test):

        buses = [None if v == 'x' else int(v) for v in input[1].split(',')]

        b = [(i, bus) for i, bus in enumerate(buses) if bus is not None]

        prod = 1
        for f in b:
            prod *= f[1]
        t = 0

        next = 1

        for e in b:
            i = e[0]
            bus = e[1]
            while (t + i)% bus != 0:
                t += next
            next *= bus
        return t

        while True:
            if all([(t + i) % bus == 0 for i, bus in b]):
                return t
            t += next

