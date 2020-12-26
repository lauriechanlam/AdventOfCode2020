import utils
import itertools
from collections import deque


class Ruleset:

    def __init__(self, text):
        lines = text.splitlines()

        def parse(line):
            left, right = line.split(': ')
            rule_id = int(left)
            if '"' in right:
                rule = right[1]
            else:
                rules = right.split(' | ')
                rule = [[int(x) for x in rule_list.split(' ')] for rule_list in rules]
            return rule_id, rule

        self.rules = dict(parse(line) for line in lines)

    def all_matching_strings(self, rule_id):
        if rule_id not in self.rules:
            return set()

        rule = self.rules[rule_id]
        if isinstance(rule, str):
            return {rule}

        def combine(sets):
            if len(sets) == 1:
                return sets[0]
            return set([left + right for left in sets[0] for right in combine(sets[1:])])

        result = map(lambda x: combine([self.all_matching_strings(rid) for rid in x]), rule)

        return set(itertools.chain(*result))

    def matches(self, message, stack):
        if len(stack) == 0:
            return len(message) == 0

        rule = self.rules[stack.popleft()]
        if isinstance(rule, str):
            if len(message) == 0:
                return False
            if message[0] == rule:
                return self.matches(message[1:], stack.copy())
        else:
            for r in rule:
                if self.matches(message, deque(r) + stack):
                    return True
        return False


def read_input(filename):
    text = utils.read(filename, 'string')
    rules, messages = text.split('\n\n')
    return Ruleset(rules), messages.splitlines()


class Part1(utils.Part):
    def __init__(self):
        super().__init__(2)

    def run(self, input, is_test):
        ruleset, messages = input
        all_matching_strings = ruleset.all_matching_strings(rule_id=0)
        return sum(message in all_matching_strings for message in messages)


class Part2(utils.Part):
    def __init__(self):
        super().__init__(12)

    def run(self, input, is_test):
        ruleset, messages = input
        ruleset.rules.update({8: [[42], [42, 8]], 11: [[42, 31], [42, 11, 31]]})
        return sum(ruleset.matches(message, deque([0])) for message in messages)
