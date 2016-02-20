# sudoku

A solution for [sudoku](https://en.wikipedia.org/wiki/Sudoku).

Casting the puzzle as a [set cover problem](https://en.wikipedia.org/wiki/Set_cover_problem), it is solved using [the DLX algorithm](http://arxiv.org/abs/cs/0011047v1).
An older [logic-based](http://www.sudokuoftheday.com/techniques/), recursive solution engine is also provided.

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
    usage: main.py [-h] [--version] [--verbose] [--use-old-solver] [prompt]

    Sudoku solver

    positional arguments:
      prompt            Puzzle prompt (e.g., 4.....8.5.3..........7......2.....6..
                        ...8.4......1.......6.3.7.5..2.....1.4......)

    optional arguments:
      -h, --help        show this help message and exit
      --version         show program's version number and exit
      --verbose, -v     Increase verbosity level.
      --use-old-solver  Use the old logic/recursion solver.

    Version 1.0.0 | Jeffrey Seifried 2016

    > ./sudoku/main.py 1....21...3....4
    1 . | . .
    . 2 | 1 .
    ----+----
    . . | 3 .
    . . | . 4
    0
    1 3 | 4 2
    4 2 | 1 3
    ----+----
    2 4 | 3 1
    3 1 | 2 4
