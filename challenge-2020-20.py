import itertools
import re
import numpy
import utils
from collections import defaultdict
import math
import copy


tile_pattern = re.compile(r'Tile (?P<ID>\d+):')

def read_input(filename):
    tiles = utils.read(filename, 'string').split('\n\n')
    def make_tile(lines):
        id = int(tile_pattern.fullmatch(lines[0]).group('ID'))
        lines = lines[1:]
        borders = [lines[0], ''.join([line[-1] for line in lines]), lines[-1][::-1], ''.join([line[0] for line in lines][::-1])]
        return id, borders
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
            exit(0)
        return True

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

class Part1(utils.Part):
    def __init__(self):
        super().__init__(None)#20899048083289)

    def run(self, tiles, is_test):

        stack = Stack(int(math.sqrt(len(tiles))))

        transformed_tiles = []
        for id, borders in tiles.items():
            for rotation in range(0, 4):
                for flip in True, False:
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
