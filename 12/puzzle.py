import re
import utils
import math


def read_input(filename):
    lines = utils.read(filename, 'string').splitlines()
    return [(instruction[0], int(instruction[1:])) for instruction in lines]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(25)

    def run(self, input, is_test):
        x = 0
        y = 0
        facing = 'E'

        instructions = {
            'E': lambda n: (x + n, y, facing),
            'W': lambda n: (x - n, y, facing),
            'N': lambda n: (x, y + n, facing),
            'S': lambda n: (x, y - n, facing),
            'F': lambda n: (instructions[facing](n)[0], instructions[facing](n)[1], facing),
            'L': lambda n: (x, y, 'NWSE'[('NWSE'.find(facing) + int(n / 90)) % 4]),
            'R': lambda n: (x, y, 'NESW'[('NESW'.find(facing) + int(n / 90)) % 4])
        }
        for direction, value in input:
            x, y, facing = instructions[direction](value)
        return int(math.fabs(x) + math.fabs(y))


class Part2(utils.Part):
    def __init__(self):
        super().__init__(286)

    def run(self, input, is_test):
        ship = {'x': 0, 'y': 0}
        waypoint = {'x': 10, 'y': 1}

        def rotate(point, times, left_right):
            sign = 1 if left_right == 'L' else -1
            for _ in range(0, times):
                tmp = point['y']
                point['y'] = point['x'] * sign
                point['x'] = -tmp * sign
            return point

        instructions = {
            'E': lambda n: (ship, {'x': waypoint['x'] + n, 'y': waypoint['y']}),
            'W': lambda n: (ship, {'x': waypoint['x'] - n, 'y': waypoint['y']}),
            'N': lambda n: (ship, {'x': waypoint['x'], 'y': waypoint['y'] + n}),
            'S': lambda n: (ship, {'x': waypoint['x'], 'y': waypoint['y'] - n}),
            'F': lambda n: ({'x': ship['x'] + n * waypoint['x'], 'y': ship['y'] + n * waypoint['y']}, waypoint),
            'L': lambda n: (ship, rotate(waypoint, int(n / 90), 'L')),
            'R': lambda n: (ship, rotate(waypoint, int(n / 90), 'R')),
        }
        for direction, value in input:
            ship, waypoint = instructions[direction](value)
        return int(math.fabs(ship['x']) + math.fabs(ship['y']))
