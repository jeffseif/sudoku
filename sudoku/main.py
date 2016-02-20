#! /usr/bin/env python3
from sudoku import __author__
from sudoku import __version__
from sudoku import __year__
from sudoku import DEFAULT_PUZZLE

from sudoku.matrix import Matrix
from sudoku.solution import Solution


def main():
    import argparse

    __version__author__year__ = '{} | {} {}'.format(
        __version__,
        __author__,
        __year__,
    )

    parser = argparse.ArgumentParser(
        description='Sudoku solver',
        epilog='Version {}'.format(__version__author__year__)
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__author__year__),
    )
    parser.add_argument(
        'prompt',
        nargs='?',
        default=DEFAULT_PUZZLE,
        type=str,
        help='Puzzle prompt (e.g., %(default)s)',
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='count',
        help='Verbosity level',
    )
    args = parser.parse_args()

    game = Matrix(
        prompt=args.prompt,
        verbose=args.verbose,
    )
    print(Solution(game.solution, game.size))
    for index, solution in enumerate(game.solve()):
        print(index)
        print(Solution(solution, game.size))


if __name__ == '__main__':
    import sys
    sys.exit(main())
