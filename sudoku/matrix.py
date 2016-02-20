from sudoku import DIGITS
from sudoku import PROMPT_TRANSLATOR

from sudoku.link import Link


PREFIXES = ('C', 'R', 'F', 'B')


class Matrix:
    """A data structure for DLX (dancing links algorithm X).  (Doubly-linked)
    head Links link to a list of column Links -- corresponding to constraints
    for the set cover problem.  Column Links additionally link to rows which
    link to their own list of contraints they cover -- corresponding to choices
    or possible configurations which assemble to a solution.
    """

    def __init__(self, prompt, verbose=0):
        self.set_prompt(prompt)
        self.set_dimensions()

        self.make_primary_columns()
        self.make_secondary_columns()
        self.make_and_attach_rows()

        self.apply_prompt()

    def set_prompt(self, prompt):
        self.prompt = prompt.translate(PROMPT_TRANSLATOR)

    def set_dimensions(self):
        maximum = max(each for each in self.prompt if each in DIGITS)
        index = DIGITS.index(maximum)

        root = (index + 1) ** 0.5
        root = int(root) + bool(root % 1)

        self.root = root
        self.size = root ** 2
        self.square = root ** 4

    def make_primary_columns(self):
        self.primary = Link(name='primary')
        self.primary.attach(self.primary, 'right')
        previous = self.primary
        prefix = PREFIXES[0]
        for index in range(self.size):
            for jndex in range(self.size):
                name = (prefix, index, jndex)
                column = Link(name=name)
                column.attach(column, 'up')

                previous.attach(column, 'right')
                previous = column

    def make_secondary_columns(self):
        self.secondary = Link(name='secondary')
        self.secondary.attach(self.secondary, 'right')
        previous = self.secondary
        for prefix in PREFIXES[1:]:
            for index in range(self.size):
                for jndex in range(self.size):
                    name = (prefix, index, jndex + 1)
                    column = Link(name=name)
                    column.attach(column, 'up')

                    previous.attach(column, 'right')
                    previous = column

    def make_and_attach_rows(self):
        for index in range(self.size):
            for jndex in range(self.size):
                for kndex in range(self.size):
                    names = self.get_names_from_ijk(self.root, index, jndex, kndex)

                    previous = None
                    for column in self.column_link_iter():
                        if column.name in names:
                            row = Link(column=column, name=DIGITS[kndex])
                            column.attach(row, 'up')
                            column.size += 1

                            if previous is None:
                                row.attach(row, 'right')
                            else:
                                previous.attach(row, 'right')
                            previous = row

    @staticmethod
    def get_names_from_ijk(root, index, jndex, kndex):
        boxex = root * (index // root) + (jndex // root)
        return (
            # Cell
            (PREFIXES[0], index, jndex),
            # Rank
            (PREFIXES[1], index, kndex + 1),
            # File
            (PREFIXES[2], jndex, kndex + 1),
            # Box
            (PREFIXES[3], boxex, kndex + 1),
        )

    def column_link_iter(self):
        for head in (self.primary, self.secondary):
            yield from head.loop('right')

    def print_columns(self):
        print(','.join(map(str, self.column_link_iter())))

    def print_column_rows(self):
        for column in self.column_link_iter():
            print('{}:'.format(column), ','.join(map(str, column.loop('down'))))

    def solve(self):
        yield from self.search(self.primary, self.solution)

    def search(self, head, solution):
        """The heart of the DLX algorithm."""
        column = head.right
        if column == head:
            yield solution
            return
        else:
            column = self.find_column_of_smallest_size(head)

        column.cover()

        for row in column.loop('down'):

            solution.append(row)
            for link in row.loop('right'):
                link.column.cover()

            yield from self.search(head, solution)

            for link in solution.pop().loop('left'):
                link.column.uncover()

        column.uncover()

    @staticmethod
    def find_column_of_smallest_size(head):
        size = int(1e9)
        smallest = None
        for column in head.loop('right'):
            if column.size < size:
                size = column.size
                smallest = column
        return smallest

    def apply_prompt(self):
        self.solution = []
        for position, token in enumerate(self.prompt):
            if token not in DIGITS:
                continue

            index = position // self.size
            jndex = position % self.size
            kndex = DIGITS.index(token)

            names = self.get_names_from_ijk(self.root, index, jndex, kndex)
            for column in self.column_link_iter():
                if column.name in names:
                    column.cover()

                    if column.name[0] == PREFIXES[0]:
                        for row in column.loop('down'):
                            if row.name == token:
                                self.solution.append(row)
