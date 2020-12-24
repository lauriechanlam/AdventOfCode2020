import utils
from collections import defaultdict
import re


pattern = re.compile(r'(e|se|sw|w|nw|ne)')

def parse_line(line):
    return pattern.finditer(line)


def read_input(filename):
    text = utils.read(filename, 'string')
    return text.splitlines()

mp = {
        'e': (2, 0),
        'w': (-2, 0),
        'ne': (1, 2),
        'nw': (-1, 2),
        'se': (1, -2),
        'sw': (-1, -2),
    }

def position(line):
    pos = (0, 0)
    for move in pattern.finditer(line):
        #print(move.groups()[0])
        m = mp[move.groups()[0]]
        pos = (pos[0] + m[0], pos[1] + m[1])
        #print(pos)
    return pos


class Part1(utils.Part):

    def __init__(self):
        super().__init__(10)

    def run(self, tiles, is_test):
        pos = [position(tile) for tile in tiles]
        d = defaultdict(int)
        for p in pos:
            d[p] += 1

        s = 0
        for p in d.values():
            if p%2 == 1:
                s += 1
        return s

def make_bool():
    return False

def make_padding(tiles):
    for tile in tiles:
        [(tile[0] + m[0], tile[1] + m[1]) for m in mp.values()]

def flip_tiles(inp):
    tiles = set()
    for tile in inp:
        neighbors = [(tile[0]+m[0], tile[1]+m[1]) for m in mp.values()]
        n = len(inp.intersection(neighbors))
        if 0 < n <= 2:
            tiles.add(tile)
        for t in neighbors:
            nbg = [(t[0] + m[0], t[1] + m[1]) for m in mp.values()]
            n = len(inp.intersection(nbg))
            if t not in inp:  # white
                if n == 2:
                    tiles.add(t)
            else:
                if 0 < n <= 2:
                    tiles.add(t)

    return tiles



class Part2(utils.Part):

    def __init__(self):
        super().__init__(2208)

    def run(self, tiles, is_test):
        pos = [position(tile) for tile in tiles]
        d = defaultdict(int)
        for p in pos:
            d[p] += 1

        is_black = set()
        for tile, p in d.items():
            if p%2 == 1:
                is_black.add(tile)

        print('day {}: {}'.format(0, len(is_black)))

        for i in range(0, 100):
            is_black = flip_tiles(is_black)
            print('day {}: {}'.format(i+1, len(is_black)))


        return len(is_black)