import utils
from functools import reduce


class Cups:
    def __init__(self, cups):
        self.next = {cup: cups[(i+1) % len(cups)] for i, cup in enumerate(cups)}

    def pickup(self, source):
        return [
                self.next[source],
                self.next[self.next[source]],
                self.next[self.next[self.next[source]]]]

    def destination(self, source, pickup):
        dest = source
        while dest == source or dest in pickup:
            dest = dest - 1 if dest > 1 else len(self.next)
        return dest

    def insert(self, pickup, source, destination):
        self.next[source] = self.next[pickup[-1]]
        self.next[pickup[-1]] = self.next[destination]
        self.next[destination] = pickup[0]

    def move(self, source, times):
        for _ in range(0, times):
            pickup = self.pickup(source)
            destination = self.destination(source, pickup)
            self.insert(pickup, source, destination)
            source = self.next[source]


def read_input(filename):
    text = utils.read(filename, 'string')
    return [int(x) for x in text.strip()]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(92658374)

    def run(self, input, is_test):
        move_count = 10 if is_test else 100
        cups = Cups(input)
        cups.move(input[0], move_count)

        val = 0
        source = 1
        while cups.next[source] != 1:
            source = cups.next[source]
            val = 10 * val + source
        return val


class Part2(utils.Part):
    def __init__(self):
        super().__init__(149245887792)

    def run(self, input, is_test):
        move_count = 10000000
        cup_count = 1000000
        source = input[0]
        cups = Cups(input + list(range(len(input) + 1, cup_count + 1)))

        for move in range(0, move_count):
            pickup = cups.pickup(source)
            destination = cups.destination(source, pickup)
            cups.insert(pickup, source, destination)
            source = cups.next[source]

        return cups.next[1] * cups.next[cups.next[1]]
