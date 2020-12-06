import datetime
import importlib
import sys
import utils


def run(module_filename, input_filename):
    challenge = importlib.import_module(module_filename.replace('.py', ''))
    part = getattr(challenge, 'Part2', challenge.Part1)()

    if part.test_expectation is not None:
        test_result = part.run(challenge.read_input('resources/test.txt'))
        assert(test_result == part.test_expectation), \
            'expected test result to be {}, actually was {}'.format(part.test_expectation, test_result)
        print('Test succeeded')
    print('Challenge result: {}'.format(part.run(challenge.read_input(input_filename))))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        date = datetime.date(2020, 12, int(sys.argv[1]))
    else:
        date = datetime.datetime.today()
    print('===== Challenge {}-12-{:02d} ====='.format(date.year, date.day))
    input_filename = utils.download_input_if_necessary(date)
    print('Input file: {}'.format(input_filename))
    module_filename = utils.copy_template_if_necessary(date)
    print('Module file: {}'.format(module_filename))
    run(module_filename, input_filename)
