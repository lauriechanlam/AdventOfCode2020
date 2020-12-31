# Advent Of Code 2020

This year, I decided to use Python in order to solve the [Advent Of Code](https://adventofcode.com) puzzles.

## Requirements
Install [Python 3.9](https://www.python.org/downloads/) and [virtualenv](https://virtualenv.pypa.io/en/stable/)

### Session file
1. Connect to your account in [AdventOfCode.com](https://adventofcode.com)
2. Copy the session cookie you can find in the storage inspector ([Firefox](https://developer.mozilla.org/en-US/docs/Tools/Storage_Inspector), [Chrome](https://developers.google.com/web/tools/chrome-devtools/storage/cookies))
3. Paste the value in a file `resources/session.txt`

## Run the puzzles!
```console
virtualenv -p python3.9 venv
source venv/bin/activate
pip install -r requirements.txt
python main.py -d <day> -y <year> -p <part> [-s]
```