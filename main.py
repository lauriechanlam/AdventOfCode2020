import aoc_to_markdown
import datetime
import getopt
from bs4 import BeautifulSoup
import importlib
import json
import logging
import os
import re
import requests
import sys


class WrongAnswerManager:
    def __init__(self, filename):
        self.filename = filename

    def is_invalid(self, answer):
        if not os.path.exists(self.filename):
            return False
        with open(self.filename, 'r') as file:
            answers = [line.split(' ') for line in file.readlines()]
        for mark, value in answers:
            if mark == '>' and int(answer) <= int(value):
                return True
            elif mark == '<' and int(answer) >= int(value):
                return True
            elif answer == value:
                return True
        return False

    def add_invalid(self, answer, response_text):
        mark = '>' if 'too low' in response_text else '<' if 'too high' in response_text else '?'
        result = '{} {}'.format(mark, answer)
        with open(self.filename, 'a') as file:
            file.writelines([result])


def run(files, options):
    puzzle = importlib.import_module(files['module'].replace('.py', '').replace(os.path.sep, '.'))
    with open(files['test'], 'r') as config_file:
        test_config = json.loads(config_file.read())

    logging.info('---------- Part {} ----------'.format(options['part']))
    part_str = 'Part{}'.format(options['part'])
    part = getattr(puzzle, part_str)()
    for config in test_config[part_str]:
        if config['expectation'] is None:
            continue
        test_result = part.run(puzzle.read_input(config['input']), is_test=True)
        if test_result != config['expectation']:
            logging.error('expected test for {} to be {}, actually was {}'.format(
                config['input'], config['expectation'], test_result
            ))
        else:
            logging.info('Test {} OK ({})'.format(config['input'], config['expectation']))
    result = part.run(puzzle.read_input(files['input']), is_test=False)
    wrong_answer_manager = WrongAnswerManager(files['wrong_answers'])
    if wrong_answer_manager.is_invalid(result):
        logging.info('Wrong puzzle result ({})'.format(result))
    elif options['send']:
        url = 'https://adventofcode.com/{}/day/{}/answer'.format(options['date'].year, options['date'].day)
        payload = {'level': options['part'], 'answer': result}
        response = requests.post(url, data=payload, cookies={'session': os.getenv('SESSION_ID')})
        text = '\n'.join([tag.get_text() for tag in BeautifulSoup(response.text, 'html.parser').find_all('article')])
        logging.info('({}) {}'.format(result, text))
        if 'That\'s not the right answer.' in text:
            wrong_answer_manager.add_invalid(result, text)
    else:
        logging.info('Puzzle result: {}'.format(result))


def make_test_files(description_filename, config_filename, folder):
    if os.path.exists(config_filename):
        with open(config_filename, 'r') as config_file:
            config = json.loads(config_file.read())
    else:
        config = {}

    with open(description_filename, 'r') as description_file:
        descriptions = description_file.read().split('## --- Part Two ---')

    inputs = [list(map(lambda text: text[1:-1], description.split('```')[1::2])) for description in descriptions]

    if 'Part1' not in config:
        input1 = inputs[0]
        filenames = ['test.txt'] + ['test-{}.txt'.format(num) for num in range(1, len(input1))]
        filenames = list(map(lambda f: os.path.join(folder, f), filenames))
        for filename, content in zip(filenames, input1):
            with open(filename, 'w') as testfile:
                testfile.write(content)
        config['Part1'] = list(map(lambda f: {'input': f, 'expectation': None}, filenames))

    if 'Part2' not in config and len(inputs) > 1:
        index = list(map(lambda test: re.match(r'test-(\d+).txt', test['input']), config['Part1']))[-1]
        index = 1 if index is None else (int(index.lastgroup) + 1)
        input2 = inputs[1]
        filenames = ['test-{}.txt'.format(num) for num in range(index, index + len(input2))]
        filenames = list(map(lambda f: os.path.join(folder, f), filenames))
        for filename, content in zip(filenames, input2):
            with open(filename, 'w') as testfile:
                testfile.write(content)
        config['Part2'] = config['Part1'] + list(map(lambda f: {'input': f, 'expectation': None}, filenames))

    with open(config_filename, 'w') as config_file:
        config_file.write(json.dumps(config, indent=2))


def setup_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s'))

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)


def get_options(arguments):
    try:
        opts, args = getopt.getopt(arguments, 'hsy:d:p:', ['help', 'send', 'year=', 'day=', 'part='])
    except getopt.GetoptError:
        print('{} -s -y <year> -d <day> -p <part>'.format(__file__))
        sys.exit(2)
    send = False
    year = 2020
    day = 25
    part = 1
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('{} -s -y <year> -d <day> -p <part>'.format(__file__))
            sys.exit()
        elif opt in ('-s', '--send'):
            send = True
        elif opt in ('-y', '--year'):
            year = int(arg)
        elif opt in ('-d', '--day'):
            day = int(arg)
        elif opt in ('-p', '--part'):
            part = int(arg)
    return {'date': datetime.date(year, 12, day), 'part': part, 'send': send}


def main(argv):
    options = get_options(argv)
    date = options['date']
    folder = '{:02d}'.format(date.day)
    files = {key: os.path.join(folder, value) for key, value in {
        'input': 'input.txt',
        'module': 'puzzle.py',
        'description': 'README.md',
        'test': 'test.json',
        'wrong_answers': 'wrong_answers.txt'
    }.items()}

    with open('resources/session.txt', 'r') as session_file:
        os.environ['SESSION_ID'] = session_file.read()

    aoc_to_markdown.write(files['description'], aoc_to_markdown.get_markdown(date.year, date.day))
    make_test_files(files['description'], files['test'], folder)

    if not os.path.exists(files['input']):
        aoc_to_markdown.write(files['input'], aoc_to_markdown.get_input(date.year, date.day))

    if not os.path.exists(files['module']):
        aoc_to_markdown.copy('resources/challenge-template.py', files['module'])

    logging.info('===== Puzzle {}-12-{:02d} ====='.format(date.year, date.day))
    for name, file in files.items():
        logging.info('{}: {}'.format(name.capitalize(), file))
    run(files, options)

    del os.environ['SESSION_ID']


if __name__ == '__main__':
    setup_logger()
    main(sys.argv[1:])
