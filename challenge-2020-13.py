import itertools
import utils


def read_input(filename):
    lines = utils.read(filename, 'string').splitlines()
    return {'start': int(lines[0]), 'buses': [None if bus == 'x' else int(bus) for bus in lines[1].split(',')]}


class Part1(utils.Part):
    def __init__(self):
        super().__init__(295)

    def run(self, input, is_test):
        start_time = input['start']
        buses = [bus for bus in input['buses'] if bus is not None]
        for time in itertools.count(start_time):
            bus = next((bus for bus in buses if (time % bus) == 0), None)
            if bus is not None:
                return (time - start_time) * bus


class Part2(utils.Part):
    def __init__(self):
        super().__init__(1068781)

    def run(self, input, is_test):
        buses = input['buses']
        time = 0
        time_to_add = 1
        for i, bus in enumerate(buses):
            if bus is None:
                continue
            while (time + i) % bus != 0:
                time += time_to_add
            time_to_add *= bus
        return time

