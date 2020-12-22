import utils


def read_input(filename):
    text = utils.read(filename, 'string')
    return [[int(card) for card in deck.splitlines()[1:]] for deck in text.split('\n\n')]


def score(deck):
    return sum((len(deck) - index) * card for index, card in enumerate(deck))


class Part1(utils.Part):
    def __init__(self):
        super().__init__(306)

    def run(self, input, is_test):
        deck1, deck2 = input

        while len(deck1) != 0 and len(deck2) != 0:
            card1 = deck1.pop(0)
            card2 = deck2.pop(0)
            if card1 > card2:
                deck1.extend((card1, card2))
            else:
                deck2.extend((card2, card1))

        return score(deck1 + deck2)


def play(deck1, deck2):
    states = set()
    while len(deck1) != 0 and len(deck2) != 0:
        state = (tuple(deck1), tuple(deck2))
        if state in states:
            return 1
        states.add(state)

        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

        if card1 <= len(deck1) and card2 <= len(deck2):
            winner = play(deck1[:card1], deck2[:card2])
        elif card1 > card2:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            deck1.extend((card1, card2))
        else:
            deck2.extend((card2, card1))
    return 1 if len(deck1) != 0 else 2



class Part2(utils.Part):

    def __init__(self):
        super().__init__(291)

    def run(self, input, is_test):
        deck1, deck2 = input
        play(deck1, deck2)
        return score(deck1 + deck2)
