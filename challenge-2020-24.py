import utils
import re


pattern = re.compile(r'(e|se|sw|w|nw|ne)')


def parse_line(line):
    return pattern.finditer(line)


def read_input(filename):
    text = utils.read(filename, 'string')
    return text.splitlines()


directions = {
    'e': (2, 0),
    'w': (-2, 0),
    'ne': (1, 1),
    'nw': (-1, 1),
    'se': (1, -1),
    'sw': (-1, -1),
}


def position(line):
    moves = [directions[move.groups()[0]] for move in pattern.finditer(line)]
    return tuple(sum(x) for x in zip(*moves))


def get_black(positions):
    black = set()
    for p in positions:
        if p in black:
            black.remove(p)
        else:
            black.add(p)
    return black


class Part1(utils.Part):

    def __init__(self):
        super().__init__(10)

    def run(self, tiles, is_test):
        positions = [position(tile) for tile in tiles]
        black = get_black(positions)
        return len(black)


def make_bool():
    return False


def make_padding(tiles):
    for tile in tiles:
        [(tile[0] + m[0], tile[1] + m[1]) for m in directions.values()]


def get_neighbors(tile):
    return set([tuple(sum(x) for x in zip(tile, direction)) for direction in directions.values()])


def flip_tiles(black):

    tiles = set()
    for tile in black:
        neighbors = get_neighbors(tile)
        n = len(neighbors.intersection(black))
        if 0 < n <= 2:
            tiles.add(tile)
        for t in neighbors:
            if t in black:
                continue
            n = len(get_neighbors(t).intersection(black))
            if n == 2:
                tiles.add(t)
    return tiles


class Part2(utils.Part):

    def __init__(self):
        super().__init__(2208)

    def run(self, tiles, is_test):
        positions = [position(tile) for tile in tiles]
        black = get_black(positions)

        for i in range(0, 100):
            black = flip_tiles(black)

        return len(black)
