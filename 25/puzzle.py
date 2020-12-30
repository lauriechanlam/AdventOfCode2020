import utils


def read_input(filename):
    return [int(x) for x in utils.read(filename, 'string').splitlines()]


def loop(value, subject):
    return (value * subject) % 20201227


class Part1(utils.Part):
    def __init__(self):
        super().__init__(14897079)

    def run(self, input, is_test):
        card_pub, door_pub = input
        loop_size = 0
        value, subject = 1, 7

        while value not in (card_pub, door_pub):
            loop_size += 1
            value = loop(value, subject)

        subject = card_pub if value == door_pub else door_pub
        value = 1

        for _ in range(loop_size):
            value = loop(value, subject)

        return value


class Part2(utils.Part):
    def __init__(self):
        super().__init__(None)

    def run(self, input, is_test):
        return None
