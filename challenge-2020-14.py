import itertools
import re
import utils
import numpy

mem_pattern = re.compile(r'mem\[(?P<bit>\d+)] = (?P<value>\d+)')
mask_pattern = re.compile(r'mask = (?P<value>[01X]+)')
# container = container_pattern.match(line).group('container')
# content = {match.group('color'): int(match.group('count')) for match in content_pattern.finditer(line)}


def read_input(filename):
    return utils.read(filename, 'string').splitlines()
    return utils.read(filename, 'string').splitlines()


def read_input_1(lines):
    def mem_(line):
        c = mem_pattern.match(line)
        return {'bit': int(c.group('bit')), 'value': int(c.group('value'))} if c is not None else None
    def mask_(line):
        m = []
        m.append(set())
        m.append(set())
        c = mask_pattern.match(line)
        if c is None:
            return None
        d = str(c.group('value'))
        for i, r in enumerate(d):
            if r == '0' or r == '1':
                e = int(r)
                m[e].add(35 - i)
        return m

    return [ {'mem': mem_(line), 'mask': mask_(line)} for line in lines ]

def res(v, bitmask):
    value = v
    i_0 = bitmask[0]
    for i in i_0:
        #if (value / 2 ** i) % 2 == 1:
        #    value -= 2 ** i
        if value >> numpy.uint64(i) & numpy.uint64(1) == numpy.uint64(1):
            value -= numpy.uint64(1) << numpy.uint64(i)
    i_1 = bitmask[1]
    for i in i_1:
        value |= numpy.uint64(1) << numpy.uint64(i)

        #if (value / 2 ** i) % 2 == 0:
        #    value += 2 ** i
    return keep_36bits(value)

def keep_36bits(val):
    v = numpy.uint64(0)
    for i in range(0, 36):
        v |= numpy.uint64(1) << numpy.uint64(i)
    return val & v

class Part1(utils.Part):
    def __init__(self):
        super().__init__(165)

    def run(self, input, is_test):
        input = read_input_1(input)
        memory = {}
        for x in input:
            if x['mem'] is not None:
                pos = x['mem']['bit']
                val = numpy.uint64(x['mem']['value'])
                memory[pos] = res(val, bitmask)
            elif x['mask'] is not None:
                bitmask = x['mask']
            print(memory)
        return sum([keep_36bits(val) for i, val in memory.items()])







def read_input_2(lines):
    def mem_(line):
        c = mem_pattern.match(line)
        return {'bit': int(c.group('bit')), 'value': int(c.group('value'))} if c is not None else None
    def mask_(line):
        m = []
        m.append(set())
        m.append(set())
        c = mask_pattern.match(line)
        if c is None:
            return None
        return str(c.group('value'))
        for i, r in enumerate(d):
            if r == '0' or r == '1':
                e = int(r)
                m[e].add(35 - i)
        return m

    return [ {'mem': mem_(line), 'mask': mask_(line)} for line in lines ]






def res2(addr, bitmask):
    print('{} {}'.format(addr, bitmask))
    new_addr = addr
    all_addr = set()
    for i in range(35, -1, -1):
        c = bitmask[i]
        if c == '0':
            pass
        elif c == '1':
            new_addr |= numpy.uint64(1) << numpy.uint64(35-i)
        elif c == 'X':
            b0 = ''.join([b if j != i else '0' for j, b in enumerate(bitmask)])
            b1 = ''.join([b if j != i else '1' for j, b in enumerate(bitmask)])
            all_addr = all_addr.union(res2(addr, b0))
            all_addr = all_addr.union(res2(addr, b1))
    if 'X' not in bitmask:
        r = set()
        r.add(new_addr)
        return r
    return all_addr

def apply_bitmask(pos, bitmask):
    res = []
    for i in range(0, 36):
        bit = bitmask[i]
        if bitmask[i] == '0':
            bit = str(numpy.uint64(pos) >> (numpy.uint64(35-i)) & numpy.uint64(1))
        res.append(bit)
    return ''.join(res)

def get_pos(floating):
    addr = set()
    if 'X' not in floating:
        f = numpy.uint64(0)
        for i in range(0, 36):
            if floating[i] == '1':
                f |= numpy.uint64(1) << numpy.uint64(35-i)
        addr.add(f)
        return addr
    for i, c in enumerate(floating):
        if c == 'X':
            fl = floating[:]
            fl[i] = '1'
            addr = addr.union(get_pos(fl))
            fl = floating[:]
            fl[i] = '0'
            addr = addr.union(get_pos(fl))
            return addr


class Part2(utils.Part):
    def __init__(self):
        super().__init__(208)

    def run(self, inp,is_test):
        input = read_input_2(inp)
        memory = {}
        for x in input:
            if x['mem'] is not None:
                pos = x['mem']['bit']
                val = numpy.uint64(x['mem']['value'])


                result = apply_bitmask(pos, bitmask)
                positions = get_pos(list(result))
                #positions.add(pos)
                for p in positions:
                    memory[p] = val
                print(memory)

            elif x['mask'] is not None:
                bitmask = x['mask']
        ret = sum([keep_36bits(val) for i, val in memory.items()])
        if ret < 5751666782640:
            return ret
