import re
import utils
from collections import defaultdict


container_pattern = re.compile(r'^(?P<container>[a-z ]+) bags contain ')
content_pattern = re.compile(r'(?P<count>\d+) (?P<color>[a-z ]+) bags?')


def read_input(filename):
    rules = {}
    lines = utils.read(filename, 'array')  # string, array, json
    for line in lines:
        container = container_pattern.match(line).group('container')
        content = {match.group('color'): int(match.group('count')) for match in content_pattern.finditer(line)}
        rules[container] = content
    return rules


class Part1(utils.Part):
    def __init__(self):
        super().__init__(4)

    def run(self, content_per_container):
        container_per_content = defaultdict(set)
        for container, content in content_per_container.items():
            for color in content.keys():
                container_per_content[color].add(container)

        colors = set()
        def add(color):
            for c in container_per_content[color]:
                add(c)
            colors.add(color)

        add('shiny gold')
        return len(colors) - 1


class Part2(utils.Part):
    def __init__(self):
        super().__init__(126)

    def run(self, content_per_container):
        def add_bags(color):
            return sum([
                content_per_container[color][content] * add_bags(content)
                for content in content_per_container
                if content in content_per_container[color]
            ]) + 1
        return add_bags('shiny gold') - 1
