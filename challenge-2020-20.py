import re
import numpy
import utils
import math


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

    def __repr__(self):
        return '\n'.join(['Stack ({})'.format(self.next)] + [
            ' '.join(['({} {} {})'.format(tile['id'], tile['rotation'], tile['flip'])
                      if isinstance(tile, dict) else '(XXXX X XXXX)' for tile in row])
            for row in self.stack])


def get_grid(pixels, tile_id, rotation, flip):
    return {
        'id': tile_id,
        'rotation': rotation,
        'pixels': pixels,
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


def order_tiles(tiles):
    grids_per_id = {tile_id: make_grids(tile_id, pixels) for tile_id, pixels in tiles.items()}

    tiles_count = len(tiles)
    stack = Stack(tiles_count)
    stack.fill(grids_per_id)
    return stack.stack


class Part1(utils.Part):
    def __init__(self):
        super().__init__(20899048083289)

    def run(self, tiles, is_test):
        ordered_tiles = order_tiles(tiles)
        corners_locations = ((0, 0), (0, -1), (-1, 0), (-1, -1))
        return math.prod([ordered_tiles[location]['id'] for location in corners_locations])


def make_image(ordered_tiles):
    def crop(pixels):
        return [line[1:-1] for line in pixels[1:-1]]

    tiled_pixels = [[tile['pixels'] for tile in tile_row] for tile_row in ordered_tiles]
    cropped_tiled_tiles = [[crop(pixels) for pixels in tile_row] for tile_row in tiled_pixels]

    tile_size = len(cropped_tiled_tiles[0][0])

    image_rows = []
    for tile_row in cropped_tiled_tiles:
        rows = [
            ''.join([''.join(tile[pixel_line_index]) for tile in tile_row])
            for pixel_line_index in range(0, tile_size)]
        image_rows.extend(rows)

    return '\n'.join(image_rows)


def count_monsters(pixels):

    monster_pattern = re.compile(r"""
..................#.
#....##....##....###
.#..#..#..#..#..#...""")

    monster_count = 0
    lines = pixels.splitlines()
    for column in range(0, len(lines[0]) - 20):
        thumbnail = '\n'.join([line[column:column+20] for line in lines])
        for i in monster_pattern.finditer(thumbnail):
            monster_count += 1
    return monster_count


class Part2(utils.Part):
    def __init__(self):
        super().__init__(273)

    def run(self, tiles, is_test):
        ordered_tiles = order_tiles(tiles)
        image = make_image(ordered_tiles)

        for grid in make_grids(tile_id=None, pixels=image):
            pixels = '\n'.join([''.join(row[:]) for row in grid['pixels']])
            monsters = count_monsters(pixels)
            if monsters != 0:
                return sum(pix == '#' for pix in pixels) - 15 * monsters
