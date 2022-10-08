from enum import Enum

from colors import BLUE
from colors import GREEN
from colors import RED
from colors import YELLOW

from sudoku import DIGITS
from sudoku.bitBoard import BitBoard


class NoSolutionError(Exception):
    def __str__(self):
        return "No solution exists"


class State(Enum):
    PROMPT = 0
    ZERO = 1
    FIND = 2
    STOP = 3
    SOLVED = 4


class Logic:
    def __getitem__(self, ijk):
        return self.board.__getitem__(ijk)

    def __init__(
        self,
        prompt,
        size=None,
        state=None,
        board=None,
        iteration=None,
        verbose=1,
    ):

        self.root, self.size, self.square = self.__size__helper(prompt)

        self.state = State.PROMPT if state is None else state

        self.board = BitBoard(self.size) if board is None else board

        self.iteration = 0 if iteration is None else iteration

        self.verbose = verbose

        self.found = set(self.__prompt__helper(prompt, self.size, iteration))

    def __iter__(self):
        return iter(range(self.size))

    def __prompt__helper(self, prompt, size, iteration):

        offset = not (bool(iteration))

        for position, ijk in enumerate(prompt):

            if isinstance(ijk, tuple):
                yield ijk[0] - offset, ijk[1] - offset, ijk[2] - offset

            elif ijk in DIGITS:

                index = position // size
                jndex = position % size
                kndex = DIGITS.index(ijk)

                yield index, jndex, kndex

    def __size__helper(self, prompt):
        if isinstance(prompt, str):
            maximum = max(prompt)
            index = DIGITS.index(maximum)
        else:
            index = max(each[2] for each in prompt)

        root = (index + 1) ** 0.5
        root = int(root) + bool(root % 1)

        return root, root**2, root**4

    def __str__(self):
        return "\n".join(self.__str__helper__())

    def __str__helper__(self):
        root = self.root
        line = GREEN(
            "+".join(
                "-" * (root * 2 + (box not in (0, root - 1))) for box in range(root)
            ),
        )

        if self.state in (State.ZERO, State.FIND):
            status = "LOGIC"
        elif self.state == State.STOP:
            status = "FAIL"
        else:
            status = self.state.name

        remaining = self.square - len(self.found)

        width = max(0, (self.size + self.root - 1) * 2 - 1 - 4)
        header = "".join(
            (
                BLUE("{:>2d}".format(self.iteration)),
                YELLOW(("{:^" + str(width) + "s}").format(status)),
                RED("{:>2d}".format(remaining)),
            ),
        )
        yield header

        for index in self:

            if index and not (index % self.root):
                yield line

            row = []
            for jndex in self:
                if not (jndex % self.root) and jndex:
                    row.append(GREEN("|"))

                kndex = self.getFound((index, jndex))

                row.append(str(kndex is not None and DIGITS[kndex] or "."))

            yield " ".join(row)

    def __repr__(self):
        return str(self)

    def copy(self, seed):

        prompt = self.found.copy()
        board = self.board.copy()

        prompt.add(seed)
        board.zeroDirect(seed)

        verbose = self.verbose - (self.verbose > 3)

        return Logic(
            prompt=prompt,
            size=self.size,
            state=State.FIND,
            board=board,
            iteration=self.iteration,
            verbose=verbose,
        )

    def devour(self, other):
        for attr in ("board", "found", "iteration", "state"):
            setattr(self, attr, getattr(other, attr))
        return self

    def find(self):

        yield from self.findRows()

        yield from self.findColumns()

        yield from self.findBoxes()

        yield from self.findSquares()

    def findColumns(self):
        root = self.root

        for kndex in self:
            for jndex in self:

                numbers = self[:, jndex, kndex]
                count = sum(numbers)

                if count == 0:
                    raise NoSolutionError

                if count == 1:

                    # unique candidate

                    index = numbers.index(True)
                    yield (index, jndex, kndex)

                elif count < root:

                    for indexs in (
                        range((boxdex) * root, (boxdex + 1) * root)
                        for boxdex in range(root)
                    ):
                        if count == sum(numbers[index] for index in indexs):

                            # locked candidate

                            jndexs = filter(
                                lambda each: each != jndex,
                                (
                                    boxdex + (jndex // root) * root
                                    for boxdex in range(root)
                                ),
                            )
                            any(
                                map(
                                    self.board.zeroIndirect,
                                    (
                                        (index, jndex, kndex)
                                        for jndex in jndexs
                                        for index in indexs
                                    ),
                                ),
                            )

    def findBoxes(self):
        root = self.root
        for kndex in self:
            for boxdex in self:

                indexs = [index + root * (boxdex // root) for index in range(root)]
                jndexs = [jndex + root * (boxdex % root) for jndex in range(root)]

                numbers = [
                    self[index, jndex, kndex] for index in indexs for jndex in jndexs
                ]
                count = sum(numbers)

                if count == 0:
                    raise NoSolutionError

                if count == 1:

                    # unique candidate

                    lndex = numbers.index(True)
                    index, jndex = (
                        boxdex // root * root + lndex // root,
                        boxdex % root * root + lndex % root,
                    )
                    yield (index, jndex, kndex)

                elif count < root:

                    # rows

                    for index in indexs:
                        if count == sum(self[index, jndex, kndex] for jndex in jndexs):

                            # locked candidate

                            any(
                                map(
                                    self.board.zeroIndirect,
                                    (
                                        (index, jndex, kndex)
                                        for jndex in self
                                        if jndex not in jndexs
                                    ),
                                ),
                            )

                    for jndex in jndexs:
                        if count == sum(self[index, jndex, kndex] for index in indexs):

                            # locked candidate

                            any(
                                map(
                                    self.board.zeroIndirect,
                                    (
                                        (index, jndex, kndex)
                                        for index in self
                                        if index not in indexs
                                    ),
                                ),
                            )

    def findRows(self):
        root = self.root

        for kndex in self:
            for index in self:

                numbers = self[index, :, kndex]
                count = sum(numbers)

                if count == 0:
                    raise NoSolutionError

                if count == 1:

                    # unique candidate

                    jndex = numbers.index(True)
                    yield (index, jndex, kndex)

                elif count < root:

                    for jndexs in (
                        range((boxdex) * root, (boxdex + 1) * root)
                        for boxdex in range(root)
                    ):
                        if count == sum(numbers[jndex] for jndex in jndexs):

                            # locked candidate

                            indexs = filter(
                                lambda each: each != index,
                                (
                                    boxdex + (index // root) * root
                                    for boxdex in range(root)
                                ),
                            )
                            any(
                                map(
                                    self.board.zeroIndirect,
                                    (
                                        (index, jndex, kndex)
                                        for index in indexs
                                        for jndex in jndexs
                                    ),
                                ),
                            )

    def findSquares(self):
        for index in self:
            for jndex in self:

                numbers = self[index, jndex, :]
                count = sum(numbers)

                if count == 0:
                    raise NoSolutionError

                if count == 1:

                    # unique candidate

                    kndex = numbers.index(True)
                    yield (index, jndex, kndex)

    def getFound(self, ij):
        for found in self.found:
            if found[:2] == ij:
                return found[2]

    def increment(self):
        self.iteration += 1

    def kSlice(self, kndex):
        return "\n".join(self.__kSlice__helper(kndex))

    def __kSlice__helper(self, kndex):

        yield "k = {}".format(kndex + 1)

        for index in self:
            yield "".join(str(int(self.board[index, jndex, kndex])) for jndex in self)

    def seeds(self):
        seeds = self.board.trues() - self.found

        return sorted(
            seeds,
            key=lambda seed: (sum(self.board[seed[0], seed[1], :]), seed[2], seed[:2]),
            reverse=True,
        )

    @staticmethod
    def __seed__helper(seed):
        return "> Seeded {0[2]} @ {0[0]},{0[1]}".format([each + 1 for each in seed])

    def solve(self):

        # Logic

        while self.state != State.STOP:

            statusQuo = len(self.board), len(self.found)

            if statusQuo[1] > self.square or self.square > statusQuo[0]:
                raise NoSolutionError

            # start

            if self.state == State.PROMPT:

                if self.verbose > 0:
                    print(self)

                self.state = State.ZERO

            # find

            if self.state == State.FIND:

                self.found.update(self.find())

                if (len(self.board), len(self.found)) == statusQuo:
                    self.state = State.STOP
                else:
                    self.state = State.ZERO

                self.increment()

                if self.verbose > 1:
                    print(self)

            # zero

            if self.state == State.ZERO:

                any(map(self.board.zeroDirect, self.found))

                if (len(self.board), len(self.found)) == statusQuo:
                    self.state = State.STOP
                else:
                    self.state = State.FIND

            # solved?

            if len(self.board) == len(self.found) == self.square:
                self.state = State.SOLVED

                if self.verbose > 0:
                    print(self)

                return self

        # Recursive

        if self.state == State.STOP:

            seeds = self.seeds()

            while seeds:

                seed = seeds.pop()

                if self.verbose > 2:
                    print(self.__seed__helper(seed))

                try:
                    child = self.copy(seed)
                    child.solve()
                except NoSolutionError:

                    # The seed was no good

                    self.board.zeroIndirect(seed)
                    continue

                if child.state == State.SOLVED:

                    # A solution was found!

                    self.devour(child)
                    return self

        raise NoSolutionError
