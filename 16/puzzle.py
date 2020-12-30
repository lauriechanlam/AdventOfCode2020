import itertools
import re
import numpy
import utils


def read_input(filename):
    text = utils.read(filename, 'string').split('\n\n')

    pattern = re.compile(r'(?P<start>\d+)-(?P<end>\d+)')

    def make_field(line):
        name = line.split(':')[0]
        ranges = [range(int(match.group('start')), int(match.group('end')) + 1) for match in pattern.finditer(line)]
        return name, set(itertools.chain(*ranges))

    def make_ticket(line):
        return [int(value) for value in line.split(',')]

    fields = dict([make_field(line) for line in text[0].splitlines()])
    my_ticket = make_ticket(text[1].splitlines()[1])
    tickets = [make_ticket(line) for line in text[2].splitlines()[1:]]

    return {'fields': fields, 'my_ticket': my_ticket, 'tickets': tickets}


class Part1(utils.Part):
    def __init__(self):
        super().__init__(71)

    def run(self, input, is_test):
        possible_values = set().union(*input['fields'].values())
        values = [value for ticket in input['tickets'] for value in ticket]
        return sum([value for value in values if value not in possible_values])


class Part2(utils.Part):
    def __init__(self):
        super().__init__(None)

    def run(self, input, is_test):
        possible_values = set().union(*input['fields'].values())
        fields = input['fields']

        valid_tickets = [ticket
                         for ticket in input['tickets'] + [input['my_ticket']]
                         if all([value in possible_values for value in ticket])]
        valid_values = numpy.transpose(valid_tickets)
        possible_fields = [
            {
                field
                for field, field_values in fields.items()
                if all([value in field_values for value in ticket_values])}
            for ticket_values in valid_values
        ]

        while any([len(field) > 1 for field in possible_fields]):
            fields_to_remove = [next(iter(fields)) for fields in possible_fields if len(fields) == 1]
            for i, fields in enumerate(possible_fields):
                if len(fields) != 1:
                    possible_fields[i] = fields.difference(fields_to_remove)

        prod = numpy.prod([value
                           for i, value in enumerate(input['my_ticket'])
                           if next(iter(possible_fields[i])).startswith('departure')])
        return prod
