import itertools
import re
import numpy
import utils
import copy


def read_input(filename):
    text = utils.read(filename, 'string').splitlines()

    #pattern = re.compile(r'(?P<start>\d+)-(?P<end>\d+)')

    arr = [[False, False, False, False, False, False, False] +  [c == '#' for c in line] + [False, False, False, False, False, False, False]  for line in text]

    for i in range(0, 7):
        arr.insert(0, [False for i in range(0, len(arr[0]))])
        arr.append([False for i in range(0, len(arr[0]))])
    return arr

class Part1(utils.Part):
    def __init__(self):
        super().__init__(None)

    def run(self, input, is_test):
        act = {
            True: lambda x: True if 2 <= sum(x) <= 3 else False,
            False: lambda x: True if sum(x) == 3 else False
        }

        d = [[[False for i in inp] for inp in input],
            [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input],
            [[False for i in inp] for inp in input],
            [[False for i in inp] for inp in input],
            [[False for i in inp] for inp in input],
            input,
             [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input],
             [[False for i in inp] for inp in input]]
        #print_arr(d)
        for round in range(0, 6):
            d2= copy.deepcopy(d)
            for i, x in enumerate(d):
                if i == 0 or i == len(d)-1:
                    continue

                for j, y in enumerate(x):
                    if j == 0 or j == len(x) - 1:
                        continue
                    for k, z in enumerate(y):
                        if k == 0 or k == len(y) - 1:
                            continue
                        se = d[i][j][k]
                        ne = []
                        for i2 in range(i-1, i+2):
                            for j2 in range(j-1, j+2):
                                for k2 in range(k-1, k+2):
                                    if i2 == i and j2 == j and k2 == k:
                                         continue
                                    ne.append(d[i2][j2][k2])
                        d2[i][j][k] = act[se](ne)
            #print('============Round {}'.format(round))
            #print_arr(d2)
            d = d2

        v = 0
        for i2 in d:
            for j2 in i2:
                for k2 in j2:
                    v += k2
        return v

def make_3(d):

    r = []
    for i in range(0, 7):
        add = [[False for i in range(0, len(d[j]))] for j in range(0, len(d))]
        r.append(add)
    r.append(d)
    for i in range(0, 7):
        add = [[False for i in range(0, len(d[j]))] for j in range(0, len(d))]
        r.append(add)
    return r

def make_4(d):
    r = []
    for i in range(0, 7):
        add = [[[False for k in j] for j in i] for i in d]
        r.append(add)
    r.append(d)
    for i in range(0, 7):
        add = [[[False for k in j] for j in i] for i in d]
        r.append(add)
    return r

class Part1(utils.Part):
    def __init__(self):
        super().__init__(848)

    def run(self, input, is_test):
        d = make_4(make_3(input))
        act = {
            True: lambda x: True if 2 <= sum(x) <= 3 else False,
            False: lambda x: True if sum(x) == 3 else False
        }

        for round in range(0, 6):
            print('============Round {}'.format(round))
            d2= copy.deepcopy(d)
            for i, x in enumerate(d):
                print(i)
                if i == 0 or i == len(d)-1:
                    continue

                for j, y in enumerate(x):
                    if j == 0 or j == len(x) - 1:
                        continue
                    for k, z in enumerate(y):
                        if k == 0 or k == len(y) - 1:
                            continue
                        for l, w in enumerate(z):
                            if l == 0 or l == len(z) - 1:
                                continue
                            se = d[i][j][k][l]
                            ne = []
                            for i2 in range(i-1, i+2):
                                for j2 in range(j-1, j+2):
                                    for k2 in range(k-1, k+2):
                                        for l2 in range(l - 1, l + 2):
                                            if i2 == i and j2 == j and k2 == k and l == l2:
                                                continue
                                            ne.append(d[i2][j2][k2][l2])
                            d2[i][j][k][l] = act[se](ne)
            #
            #print_arr4(d2)
            d = d2

        v = 0
        for i2 in d:
            for j2 in i2:
                for k2 in j2:
                    for l2 in k2:
                        v += l2
        #if v > 976:
        return v



def print_arr(r):
    s = [[''.join(['#' if w else '.' for w in y]) for y in x] for x in r]
    s =['\n'.join(x) for x in s]
    for x in s:
        print(x)
        print('')

def print_arr4(r):
    s = [[[''.join(['#' if w else '.' for w in y]) for y in x] for x in w] for w in r]
    s = [['\n'.join(x) for x in d] for d in s]
    for i, d in enumerate(s):
        for j, k in enumerate(d):
            print('w={} z={}'.format(i, j))
            print(k)
            print('')
    print('')
