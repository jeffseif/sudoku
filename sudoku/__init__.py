__author__ = 'Jeffrey Seifried'
__email__ = 'jeffrey.seifried@gmail.com'
__program__ = 'sudoku'
__url__ = 'http://github.com/jeffseif/{}'.format(__program__)
__version__ = '1.0.0'
__year__ = '2017'


DEFAULT_PUZZLE = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
DIGITS = list(map(chr, sum(map(list, (range(49, 58), range(48, 49), range(65, 91), range(97, 123))), [])))
PROMPT_TRANSLATOR = {
    ord(char): replacement
    for chars, replacement in (
        ('-|+, \n', None),
        ('.', u'\u241E'),
    )
    for char in chars
}


def Colorize(color, weight=1):
    """Function for bash-style color formatting."""
    def inner(value):
        return template.format(value)

    template = '\033[{:d};{:d}m{{:s}}\033[0m'.format(weight, color)
    return inner
RED = Colorize(31)
GREEN = Colorize(32)
YELLOW = Colorize(33)
BLUE = Colorize(34)
PURPLE = Colorize(35)
WHITE = Colorize(37)
GRAY = Colorize(90)
DARK_RED = Colorize(31, 0)
DARK_GREEN = Colorize(32, 0)
DARK_YELLOW = Colorize(33, 0)
DARK_BLUE = Colorize(34, 0)
DARK_PURPLE = Colorize(35, 0)
DARK_WHITE = Colorize(37, 0)
DARK_GRAY = Colorize(90, 0)
