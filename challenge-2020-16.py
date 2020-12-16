import itertools
import re
import numpy
import utils
import collections
from collections import defaultdict

constrainsts_pattern = re.compile(r'(?P<cla>[a-z ]+): (?P<first>\d+)-(?P<sec>\d+) or (?P<thi>\d+)-(?P<four>\d+)')


def constr(line):
    match = constrainsts_pattern.fullmatch(line)
    if match is None:
        print(line)
    r = range(int(match.group('first')), int(match.group('sec'))+1)
    s = range(int(match.group('thi')), int(match.group('four'))+1)
    return itertools.chain(r, s)

def read_input(filename):
    text = utils.read(filename, 'string').split('\n\n')
    constrainsts = [constr(line) for line in text[0].splitlines()]
    t = set()
    for c in constrainsts:
        t = t.union(c)

    tickets = [[int(r) for r in line.split(',')] for line in text[2].splitlines()[1:]]
    return {'constraints': t, 'tickets': tickets}


class Part1(utils.Part):
    def __init__(self):
        super().__init__(71)

    def run(self, input, is_test):
        tickets = [r for t in input['tickets'] for r in t]
        return sum([t for t in tickets if t not in input['constraints']])


def read_line(line):
    match = constrainsts_pattern.fullmatch(line)
    if match is None:
        print(line)
    r = range(int(match.group('first')), int(match.group('sec'))+1)
    s = range(int(match.group('thi')), int(match.group('four'))+1)
    name = match.group('cla')
    return [name, itertools.chain(r, s)]

def read_input(filename):
    text = utils.read(filename, 'string').split('\n\n')
    constrainsts = [read_line(line) for line in text[0].splitlines()]
    t = {c[0]: set(c[1]) for c in constrainsts}

    my = [int(r) for r in text[1].splitlines()[1].split(',')]

    tickets = [[int(r) for r in line.split(',')] for line in text[2].splitlines()[1:]]
    return {'constraints': t, 'my': my, 'tickets': tickets}


class Part1(utils.Part):
    def __init__(self):
        super().__init__(None)

    def run(self, input, is_test):
        const = set(itertools.chain(*input['constraints'].values()))
        fields = input['constraints']

        valids = [t for t in input['tickets'] + [input['my']] if all([r in const for r in t])]
        t = numpy.transpose(valids)
        tk = []
        for x in t:
            tk.append({key for key, val in fields.items() if all([s in val for s in x])})

        st = {}
        while any([len(c) > 1 for c in tk]):
            for i, c in enumerate(tk):
                if len(c) == 1:
                    for j, d in enumerate(tk):
                        if i != j and c.issubset(d):
                            d.remove(*c)


        m = input['my']
        w = 1
        for i, p in enumerate(m):
            for c in tk[i]:
                if c.startswith('departure'):
                    w *= p
        return w

