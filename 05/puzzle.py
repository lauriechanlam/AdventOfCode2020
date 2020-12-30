from collections import defaultdict
import utils


class Position:
    def __init__(self, line):
        self.row_text = line[0:7]
        self.col_text = line[7:10]

    def row(self):
        pos = 0
        for char in self.row_text:
            pos = (pos << 1) | (char == 'B')
        return pos

    def column(self):
        pos = 0
        for char in self.col_text:
            pos = (pos << 1) | (char == 'R')
        return pos

    def id(self):
        return seat_id(self.row(), self.column())


def seat_id(row, column):
    return row * 8 + column


def read_input(filename):
    lines = utils.read(filename, 'array')
    return [Position(line) for line in lines]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(357)

    def run(self, input, is_test):
        return max([seat.id() for seat in input])


class Part2(utils.Part):
    def __init__(self):
        super().__init__(None)

    def run(self, input, is_test):
        seats = defaultdict(set)
        for seat in input:
            seats[seat.row()].add(seat.column())
        row_seats = next((row, columns) for row, columns in seats.items() if len(columns) == 7)
        missing_column = (set(range(0, 8)) - row_seats[1]).pop()
        return seat_id(row_seats[0], missing_column)
