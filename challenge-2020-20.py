import itertools
import re
import numpy
import utils
from collections import defaultdict
import math
import copy


tile_pattern = re.compile(r'Tile (?P<ID>\d+):')

def read_input(filename):
    return utils.read(filename, 'string')
    tiles = utils.read(filename, 'string').split('\n\n')
    def make_tile(lines):
        id = int(tile_pattern.fullmatch(lines[0]).group('ID'))
        lines = lines[1:]
        return id, lines
    tiles = [make_tile(tile.splitlines()) for tile in tiles]
    return {tile[0]: tile[1] for tile in tiles}
#
# def arrange(tiles, flip, rotations, combi):
#     n = int(math.sqrt(len(tiles)))
#     flip = numpy.reshape(flip, (n, n))
#     rotations = numpy.reshape(rotations, (n, n))
#     combi = numpy.reshape(combi, (n, n))
#     arranged_tiles = {}
#     for i in range(0, n):
#         for j in range(0, n):
#             if flip[i][j]:
#                 tiles[combi[i][j]] = tiles[combi[i][j]][::-1]
#             for k in range(0, rotations[i][j]):
#                 tiles[combi[i][j]] = tiles[combi[i][j]][1:] + [tiles[combi[i][j]][0]]
#     return tiles
#
# def try_combi(arranged_tiles):
#     tiles = arranged_tiles
#     n = len(arranged_tiles)
#     for i in range(0, n):
#         for j in range(0, n):
#             if i > 0:
#                 if tiles[i][j][2] != tiles[i-1][j][0]:
#                     return False
#             if i < n - 1:
#                 if tiles[i][j][0] != tiles[i+1][j][2]:
#                     return False
#             if j > 0:
#                 if tiles[i][j][3] != tiles[i][j-1][1]:
#                     return False
#             if j < n - 1:
#                 if tiles[i][j][1] != tiles[i][j+1][3]:
#                     return False
#     return True
#
#
# def corners(combi):
#     n = int(math.sqrt(len(combi)))
#     return [combi[0][0], combi[0][-1], combi[-1][0], combi[-1][-1]]

HASH = '0'


class Stack:
    def __init__(self, n):
        self.tiles = []
        self.transformed_tiles = []
        self.n = n

    def contains(self, id):
        return any([tile[0] == id for tile in self.tiles])

    def append(self, id, borders, rotation, flip):
        self.tiles.append((id, borders, rotation, flip))
        self.transformed_tiles.append(self.transform_tile(len(self.tiles)-1))

    def pop(self):
        self.tiles.pop()
        self.transformed_tiles.pop()


    def __repr__(self):
        return ' | '. join(self.lines())

    def lines(self):
        def val(i, j):
            if i*self.n + j < len(self.tiles):
                s = self.tiles[i*self.n + j]
                return str((s[0], s[2], s[3]))
            return 'XXX'
        s = []
        for i in range(0, self.n):
            s.append(' '.join([val(i, j) for j in range(0, self.n)]))
        return s

    def is_valid(self):
        """ Assuming everything but the last one is already valid"""
        idx = len(self.tiles) - 1
        i = int(idx / self.n)
        j = idx % self.n
        if i > 0:
            if self.transformed_tiles[(i-1)*self.n + j][0] != self.transformed_tiles[idx][2][::-1]:
                return False
        if j > 0:
            if self.transformed_tiles[idx - 1][1] != self.transformed_tiles[idx][3][::-1]:
                return False
        if len(self.tiles) == self.n * self.n:
            print(self)
            print(self.corner_ids())
            print(math.prod(self.corner_ids()))
            self.write_image('resources/2020-20-image.txt')
            exit(0)
        return True

    def write_image(self, filename):
        def make_image(id, borders, rotation, flip):
            pixels = Part1.tiles[id]
            pixels = [line[1:-1] for line in pixels[1:-1]]
            if flip:
                pixels = [''.join(line) for line in numpy.transpose([[c for c in line] for line in pixels])]
            for _ in range(0, rotation):
                pixels = [''.join(line) for line in numpy.rot90([[c for c in line] for line in pixels])]
            return pixels

        tile_images = []
        for i in range(0, self.n):
            tile_row = []
            for j in range(0, self.n):
                tile_row.append(make_image(*self.tiles[self.n * i + j]))
            tile_images.append(tile_row)

        s = []
        for tile_row in tile_images:
            for k in range(0, 8)[::-1]:
                line = ''.join([''.join(tile[k]) for tile in tile_row])
                s.append(line)
        t = [[c for c in line] for line in s]
        t = '\n'.join([''.join(line) for line in t])



        with open(filename, 'w') as f:
            f.write(t)


        #print(tile_images)



    def transform_tile(self, idx):
        (id, borders, rotation, flip) = self.tiles[idx]
        if flip:
            transformed_tile = [border[::-1] for border in borders][::-1]
        else:
            transformed_tile = borders[:]
        for _ in range(0, rotation):
            transformed_tile = transformed_tile[1:] + [transformed_tile[0]]
        return transformed_tile

    def corner_ids(self):
        idx = [0, self.n - 1, self.n * (self.n - 1), len(self.tiles)-1]
        return [self.tiles[i][0] for i in idx]



def try_add_tiles(stack, tiles):
    for tile in tiles:
        stack.append(*tile)
        stack_size = len(stack.tiles)
        if not stack.is_valid():
            stack.pop()
        else:
            try_add_tiles(stack, [tile for tile in tiles if not stack.contains(tile[0])])
            if stack_size == len(stack.tiles):
                stack.pop()

pattern_all = re.compile(r'\n([\.\#]*)\#[\.\#][\.\#][\.\#][\.\#]\#\#[\.\#][\.\#][\.\#][\.\#]\#\#[\.\#][\.\#][\.\#][\.\#]\#\#\#([\.\#]*)\n([\.\#]*)[\.\#]\#[\.\#][\.\#]\#[\.\#][\.\#]\#[\.\#][\.\#]\#[\.\#][\.\#]\#[\.\#][\.\#]\#[\.\#][\.\#][\.\#]([\.\#]*)')


def count_monsters(txt):
    monster_count = 0
    for maybe in pattern_all.finditer(txt):
        offset = set(len(g) for g in maybe.groups()[::2])
        if len(offset) != 1:
            continue
        offset = offset.pop()
        first_line = txt[:maybe.start()].splitlines()[-1]
        if first_line[offset + 18] == HASH:
            monster_count += 1
    return monster_count


##pattern_no_left = re.compile(r'[\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#][\.\#]#\n#[\.\#][\.\#][\.\#][\.\#]##[\.\#][\.\#][\.\#][\.\#]##[\.\#][\.\#][\.\#][\.\#]###\n[\.\#]#[\.\#][\.\#]#[\.\#][\.\#]#[\.\#][\.\#]#[\.\#][\.\#]#[\.\#][\.\#]#[\.\#][\.\#][\.\#]')
pattern_no_left = re.compile(r'[X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0][X0]0[X0]\n0[X0][X0][X0][X0]00[X0][X0][X0][X0]00[X0][X0][X0][X0]000\n[X0]0[X0][X0]0[X0][X0]0[X0][X0]0[X0][X0]0[X0][X0]0[X0][X0][X0]')


def count_monsters(txt):
    monster_count = 0
    lines = txt.splitlines()
    for i in range(0, len(lines[0]) - 20):
        r = '\n'.join([line[i:i+20] for line in lines])
        for maybe in pattern_no_left.finditer(r):
            monster_count += 1
    return monster_count

class Part2(utils.Part):
    def __init__(self):
        super().__init__(273)

    def run(self, txt, is_test):
        with open('resources/test.txt' if is_test else 'resources/-2.txt') as f:
            txt = f.read()

        total = sum(x == HASH for x in txt)

        for flip in False, True:
            v = [[c for c in line] for line in txt.splitlines()]
            if flip:
                v = numpy.transpose(v)
            for rotation in range(0, 4):
                v = numpy.rot90(v)
                t = '\n'.join([''.join(line) for line in v])
                print(flip, rotation)
                monster_count = count_monsters(t)
                if monster_count != 0:
                    r = total - monster_count * 15
                    if r in [1987, 2077, 2287]:
                        print(total)
                        print(r)
                        print('Tooh')
                        exit(1)
                    return r

class Part1(utils.Part):
    def __init__(self):
        super().__init__(None)#20899048083289)

    def run(self, tiles, is_test):
        Part1.tiles = copy.deepcopy(tiles)

        stack = Stack(int(math.sqrt(len(tiles))))

        transformed_tiles = []
        for id, lines in tiles.items():
            borders = [lines[0], ''.join([line[-1] for line in lines]), lines[-1][::-1], ''.join([line[0] for line in lines][::-1])]
            tiles[id] = borders
            for rotation in range(0, 4):
                for flip in False, True:
                    transformed_tiles.append((id, borders, rotation, flip))

        try_add_tiles(stack, transformed_tiles)

        ids = stack.corner_ids()

        return math.prod(ids)

        # combinations = itertools.permutations(tiles.keys(), len(tiles))
        # 
        # for combi in combinations:
        #     for flip in itertools.product([True, False], repeat=len(tiles)):
        #         for rotations in itertools.product(range(0, 4), repeat=len(tiles)):
        #             arranged_tiles = arrange(tiles, flip, rotations, combi)
        #             if try_combi(arranged_tiles):
        #                 return math.prod(corners(combi))
        # 
        # 
        # 
        # tile_id_per_border = defaultdict(set)
        # for id, tile in tiles.items():
        #     for border in tile:
        #         tile_id_per_border[border].add(id)
        # count_tiles_per_border = {border: len(tiles) for border, tiles in tile_id_per_border.items()}
        # borders = defaultdict(set)
        # for border, tile_count in count_tiles_per_border.items():
        #     borders[tile_count].add(border)
        # #border_count_per_tile_count = {tile_count: len(border_count) for tile_count, border_count in borders.items()}
        # n_1 = len(tiles) - 1
        # if len(borders[4]) == n_1 * n_1 \
        #     and len(borders[3]) == 3 * 4 * n_1 \
        #     and len(borders[2]) == 8 \
        #     and len(borders[1]) == 8:
        #     return borders[2].intersect(border[1])

        #values = set().union(*input['fields'].values())
        #return sum([int(value) for value in values])
