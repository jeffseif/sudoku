from colors import GRAY
from colors import WHITE


class Solution:

    BAR = GRAY("|")
    EMPTY = WHITE(".")

    def __init__(self, solution, size):
        self.process(solution)
        self.size = size

    def process(self, solution):
        self.positions = {link.column.name[1:]: link.name for link in solution}

    def __str__(self):
        return "\n".join(
            self.row_iter(),
        )

    def row_iter(self):
        root = int(self.size**0.5)
        line = GRAY(
            "+".join(
                "-" * (root * 2 + (box not in (0, root - 1))) for box in range(root)
            ),
        )

        for index in range(self.size):
            if index and not (index % root):
                yield line

            row = []
            for jndex in range(self.size):
                if jndex and not (jndex % root):
                    row.append(self.BAR)

                if (index, jndex) in self.positions:
                    token = self.positions[(index, jndex)]
                    row.append(WHITE(token))
                else:
                    row.append(self.EMPTY)
            yield " ".join(row)
