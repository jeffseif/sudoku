# Sudoku

TODO

## Installation

    > pip install -e git+https://github.com/jeffseif/sudoku.git#egg=sudoku

## Development

    > git clone git@github.com:jeffseif/sudoku.git
    > cd sudoku
    > virtualenv venv --python=$(which python3)
    > source venv/bin/activate
    > make
    > make test

## Example invocation

    > ./sudoku/main.py --help
    usage: main.py [-h] [--version] [--verbose] [prompt]

    Sudoku solver

    positional arguments:
      prompt         Puzzle prompt (e.g., 4.....8.5.3..........7......2.....6.....
                     8.4......1.......6.3.7.5..2.....1.4......)

    optional arguments:
      -h, --help     show this help message and exit
      --version      show program's version number and exit
      --verbose, -v  Verbosity level

    Version 1.0.0 | Jeffrey Seifried 2016

    > ./sudoku/main.py 123434122143
    1 2 | 3 4
    3 4 | 1 2
    ----+----
    2 1 | 4 3
    . . | . .
    0
    1 2 | 3 4
    3 4 | 1 2
    ----+----
    2 1 | 4 3
    4 3 | 2 1
