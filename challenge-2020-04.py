import re
import utils


pattern = re.compile(r'(\w+):(\S+)\n?')


date_pattern = re.compile(r'[0-9]{4}')
height_pattern = re.compile(r'(?P<value>\d+)(?P<unit>cm|in)')
hair_color_pattern = re.compile(r'#[0-9a-f]{6}')
eye_color_pattern = re.compile(r'(amb|blu|brn|gry|grn|hzl|oth)')
pid_pattern = re.compile(r'[0-9]{9}')


def is_valid_height(value):
    match = height_pattern.fullmatch(value)
    if match is None:
        return False
    height_range = range(150, 194) if match.group('unit') == 'cm' else range(59, 77)
    return int(match.group('value')) in height_range


fields = {
    'byr': lambda x: 1920 <= int(date_pattern.fullmatch(x).group()) <= 2002,
    'iyr': lambda x: 2010 <= int(date_pattern.fullmatch(x).group()) <= 2020,
    'eyr': lambda x: 2020 <= int(date_pattern.fullmatch(x).group()) <= 2030,
    'hgt': is_valid_height,
    'hcl': lambda x: hair_color_pattern.fullmatch(x) is not None,
    'ecl': lambda x: eye_color_pattern.fullmatch(x) is not None,
    'pid': lambda x: pid_pattern.fullmatch(x) is not None
}


class Passport:
    def __init__(self, content):
        self.dict = dict(pattern.findall(content))

    def contains_all_required_fields(self):
        return all([key in self.dict for key in fields])

    def is_valid(self):
        if not self.contains_all_required_fields():
            return False
        return all([is_field_valid(self.dict[key]) for (key, is_field_valid) in fields.items()])


def read_input(filename):
    content = utils.read(filename, 'string')
    passports = content.split('\n\n')
    return [Passport(x) for x in passports]


class Part1(utils.Part):
    def __init__(self):
        super().__init__(2)

    def run(self, input):
        return sum([passport.contains_all_required_fields() for passport in input])


class Part2(utils.Part):
    def __init__(self):
        super().__init__(None)#4)

    def run(self, input):
        return sum([passport.is_valid() for passport in input])
