import aoc_to_markdown
import datetime
import importlib
import json
import logging
import os
import sys


def run(module_filename, input_filename, test_filename):
    challenge = importlib.import_module(module_filename.replace('.py', '').replace(os.path.sep, '.'))
    with open(test_filename, 'r') as config_file:
        test_config = json.loads(config_file.read())

    for part_num in range(1, 3):
        logging.info('---------- Part {} ----------'.format(part_num))
        part_str = 'Part{}'.format(part_num)
        part = getattr(challenge, part_str)()
        for config in test_config[part_str]:
            if config['expectation'] is None:
                continue
            test_result = part.run(challenge.read_input(config['input']), is_test=True)
            if test_result != config['expectation']:
                logging.error('expected test for {} to be {}, actually was {}'.format(
                    config['input'], config['expectation'], test_result
                ))
            else:
                logging.info('Test {} OK ({})'.format(config['input'], config['expectation']))
        logging.info('Puzzle result: {}'.format(part.run(challenge.read_input(input_filename), is_test=False)))


def make_test_files(description_filename, config_filename, folder):
    if os.path.exists(config_filename):
        return
    with open(description_filename, 'r') as description_file:
        inputs = list(map(lambda text: text[1:-1], description_file.read().split('```')[1::2]))
    filenames = ['test.txt'] + ['test-{}.txt'.format(num) for num in range(1, len(inputs))]
    filenames = list(map(lambda basename: os.path.join(folder, basename), filenames))
    for filename, content in zip(filenames, inputs):
        with open(filename, 'w') as testfile:
            testfile.write(content)
    config = list(map(lambda filename: {'input': filename, 'expectation': None}, filenames))
    with open(config_filename, 'w') as config_file:
        config_file.write(json.dumps({'Part1': config, 'Part2': config}, indent=2))


def setup_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s'))

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)


def main(argv):
    if len(argv) > 1:
        date = datetime.date(2020, 12, int(argv[1]))
    else:
        date = datetime.datetime.today()

    with open('resources/session.txt', 'r') as session_file:
        os.environ['SESSION_ID'] = session_file.read()

    folder = '{:02d}'.format(date.day)
    files = {
        'input': os.path.join(folder, 'input.txt'),
        'module': os.path.join(folder, 'puzzle.py'),
        'description': os.path.join(folder, 'README.md'),
        'test': os.path.join(folder, 'test.json')
    }

    if not os.path.exists(files['description']):
        aoc_to_markdown.write(files['description'], aoc_to_markdown.get_markdown(date.year, date.day))
        make_test_files(files['description'], files['test'], folder)

    if not os.path.exists(files['input']):
        aoc_to_markdown.write(files['input'], aoc_to_markdown.get_input(date.year, date.day))

    if not os.path.exists(files['module']):
        aoc_to_markdown.copy('resources/challenge-template.py', files['module'])

    del os.environ['SESSION_ID']

    logging.info('===== Puzzle {}-12-{:02d} ====='.format(date.year, date.day))
    for name, file in files.items():
        logging.info('{}: {}'.format(name.capitalize(), file))
    run(files['module'], files['input'], files['test'])


if __name__ == '__main__':
    setup_logger()
    main(sys.argv)
