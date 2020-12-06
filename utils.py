import json
import numpy
import os
import requests
import shutil


readers = {
    'string': lambda file: file.read(),
    'array': lambda file: file.readlines(),
    'json': lambda file: json.loads(file.read())
}


def read(filename, type):
    with open(filename, 'r') as file:
        return readers[type](file)


def download_input_if_necessary(date):
    path = 'resources/{}-{:02d}.txt'.format(date.year, date.day)
    if os.path.isfile(path):
        return path
    session = read('resources/session.txt', 'string')
    response = requests.get('https://adventofcode.com/{}/day/{}/input'.format(date.year, date.day),
                            cookies={'session': session})
    with open(path, 'w') as file:
        file.write(response.text)
    return path


def copy_template_if_necessary(date):
    filename = 'challenge-{}-{:02d}.py'.format(date.year, date.day)
    if not os.path.isfile(filename):
        shutil.copyfile('resources/challenge-template.py', filename)
        print('File {} created from template'.format(filename))
        print('Exiting')
        exit(1)
    return filename


class Part:
    def __init__(self, test_expectation):
        self.test_expectation = test_expectation

