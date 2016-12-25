from sudoku import __author__
from sudoku import __version__
from sudoku import __year__
from sudoku import DEFAULT_PUZZLE
from sudoku.logic import Logic
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
        '--verbose',
        '-v',
        action='count',
        default=1,
        help='Increase verbosity level.',
    )
    parser.add_argument(
        '--use-old-solver',
        action='store_true',
        default=False,
        help='Use the old logic/recursion solver.',
    )
    parser.add_argument(
        'prompt',
        nargs='?',
        default=DEFAULT_PUZZLE,
        type=str,
        help='Puzzle prompt (e.g., %(default)s)',
    )
    args = parser.parse_args()

    if args.use_old_solver:
        game = Logic(prompt=args.prompt, verbose=args.verbose)
        game.solve()
    else:
        game = Matrix(prompt=args.prompt, verbose=args.verbose)
        print(Solution(game.solution, game.size))
        for index, solution in enumerate(game.solve()):
            print(index)
            print(Solution(solution, game.size))


if __name__ == '__main__':
    import sys
    sys.exit(main())
