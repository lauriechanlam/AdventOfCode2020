import json


readers = {
    'string': lambda file: file.read(),
    'array': lambda file: file.readlines(),
    'json': lambda file: json.loads(file.read())
}


def read(filename, type):
    with open(filename, 'r') as file:
        return readers[type](file)


class Part:
    def __init__(self, test_expectation):
        self.test_expectation = test_expectation
