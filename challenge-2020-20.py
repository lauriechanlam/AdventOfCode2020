import re
import numpy
import utils
import math
import copy
import functools


def read_input(filename):
    pattern = re.compile(r'Tile (?P<ID>\d+):')
    tiles = utils.read(filename, 'string').split('\n\n')

    def parse_tile(tile_info):
        lines = tile_info.splitlines()
        tile_id = int(pattern.fullmatch(lines[0]).group('ID'))
        pixels = lines[1:]
        return tile_id, pixels

    tile_list = [parse_tile(tile) for tile in tiles]
    return {tile_id: pixels for (tile_id, pixels) in tile_list}
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

class Part3(utils.Part):
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


class Stack:
    def __init__(self, tiles_count):
        self.n = int(math.sqrt(tiles_count))
        self.stack = numpy.empty((self.n, self.n), dtype=dict)
        self.next_int = 0

    @property
    def next(self):
        return divmod(self.next_int, self.n)

    def contains(self, tile_id):
        return any(grid['id'] == tile_id for grid in self.stack.flatten() if isinstance(grid, dict))

    def can_add(self, grid):
        if self.contains(grid['id']):
            return False
        i, j = self.next
        if i > 0 and self.stack[i-1][j]['bottom_border'] != grid['top_border']:
            return False
        if j > 0 and self.stack[i][j-1]['right_border'] != grid['left_border']:
            return False
        return True

    def push(self, grid):
        self.stack[self.next] = grid
        self.next_int += 1

    def pop(self):
        self.next_int -= 1
        self.stack[self.next] = None

    def is_full(self):
        return self.next_int == self.n * self.n

    def fill(self, grids_per_id):
        for tile_id, grids in grids_per_id.items():
            if self.contains(tile_id):
                continue
            for grid in grids:
                if not self.can_add(grid):
                    continue
                self.push(grid)
                self.fill(grids_per_id)
                if self.is_full():
                    return self
                self.pop()

    def corners(self):
        corners_locations = ((0, 0), (0, -1), (-1, 0), (-1, -1))
        return [self.stack[location]['id'] for location in corners_locations]

    def __repr__(self):
        return '\n'.join(['Stack ({})'.format(self.next)] + [
            ' '.join(['({} {} {})'.format(tile['id'], tile['rotation'], tile['flip'])
                      if isinstance(tile, dict) else '(XXXX X XXXX)' for tile in row])
            for row in self.stack])


class Part1(utils.Part):
    def __init__(self):
        super().__init__(20899048083289)

    def run(self, tiles, is_test):

        def get_grid(pixels, tile_id, rotation, flip):
            return {
                'id': tile_id,
                'rotation': rotation,
                'flip': flip,
                'top_border': ''.join(pixels[0]),
                'bottom_border': ''.join(pixels[-1]),
                'right_border': ''.join(line[-1] for line in pixels),
                'left_border': ''.join([line[0] for line in pixels])
            }

        def make_grids(tile_id, pixels):
            pixels = list(map(list, pixels))
            return [get_grid(numpy.rot90(pixels, rot), tile_id, rot, False) for rot in range(0, 4)] \
                   + [get_grid(numpy.rot90(numpy.transpose(pixels), rot), tile_id, rot, True) for rot in range(0, 4)]

        grids_per_id = {tile_id: make_grids(tile_id, pixels) for tile_id, pixels in tiles.items()}

        tiles_count = len(tiles)
        stack = Stack(tiles_count)
        stack.fill(grids_per_id)

        return math.prod(stack.corners())
