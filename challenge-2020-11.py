import utils
import copy


class Grid:
    def __init__(self, lines):
        self.grid = [['.'] + list(line) + ['.'] for line in lines]
        self.grid.insert(0, ['.' for i in range(0, len(self.grid[0]))])
        self.grid.append(['.' for i in range(0, len(self.grid[0]))])
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def round(self, move):
        grid = copy.deepcopy(self.grid)
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.grid[i][j] == '.':
                    continue
                move(i, j, grid)
        has_moved = grid != self.grid
        self.grid = grid
        return has_moved

    def move(self, i, j, grid):
        neighbors = [row[j - 1:j + 2] for row in self.grid[i - 1:i + 2]]
        occupied_count = sum([seat == '#' for row in neighbors for seat in row])
        if self.grid[i][j] == 'L' and occupied_count == 0:
            grid[i][j] = '#'
        elif self.grid[i][j] == '#' and occupied_count >= 5:  # counting current seat
            grid[i][j] = 'L'

    def move2(self, i, j, grid):
        directions = [
            [row[j] for row in self.grid[0:i][::-1]],  # top
            [row[j] for row in self.grid[i+1:]],  # bottom
            self.grid[i][0:j][::-1],  # left
            self.grid[i][j + 1:],  # right
            [self.grid[i + k][j + k]
             for k in range(1, min(self.height - i, self.width - j))],  # bottom right
            [self.grid[i + k][j - k]
             for k in range(1, min(self.height - i, j + 1))],  # bottom left
            [self.grid[i - k][j + k]
             for k in range(1, min(i + 1, self.width - j))],  # top right
            [self.grid[i - k][j - k]
             for k in range(1, min(i + 1, j + 1))]  # top left
        ]
        first_visible_seat_in_directions = [next((seat for seat in seats if seat != '.'), None) for seats in directions]
        count = sum([seat == '#' for seat in first_visible_seat_in_directions])
        if self.grid[i][j] == 'L' and count == 0:
            grid[i][j] = '#'
        elif self.grid[i][j] == '#' and count >= 5:
            grid[i][j] = 'L'

    def count(self):
        return sum([seat == '#' for row in self.grid for seat in row])


def read_input(filename):
    return Grid(utils.read(filename, 'string').splitlines())


class Part1(utils.Part):
    def __init__(self):
        super().__init__(37)

    def run(self, input, is_test):
        while input.round(input.move):
            pass
        return input.count()


class Part2(utils.Part):
    def __init__(self):
        super().__init__(26)

    def run(self, input, is_test):
        while input.round(input.move2):
            pass
        return input.count()
