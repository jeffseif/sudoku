class BitBoard:

    nullSlice = slice(None, None, None)

    def __init__(self, size, bits=None, default=True):
        self.size = size
        self.root = int(self.size ** 0.5)
        self.bits = (bits is not None and bits) or [[[default for each in self] for each in self] for each in self]

    def __getitem__(self, ijk):

        index, jndex, kndex = ijk

        if self.nullSlice == index:
            return [self[index, jndex, kndex] for index in self]

        if self.nullSlice == jndex:
            return [self[index, jndex, kndex] for jndex in self]

        if self.nullSlice == kndex:
            return [self[index, jndex, kndex] for kndex in self]

        return self.bits[index][jndex][kndex]

    def __iter__(self):
        return iter(range(self.size))

    def __len__(self):
        return sum(self.bits[index][jndex][kndex] for index in self for jndex in self for kndex in self)

    def copy(self):
        return BitBoard(self.size, list(list(list(col) for col in row) for row in self.bits))

    def trues(self):
        return {
            (index, jndex, kndex)
            for index in self
            for jndex in self
            for kndex in self
            if self[index, jndex, kndex]
        }

    def zeroDirect(self, ijk):
        index, jndex, kndex = ijk

        root = self.root

        for xndex in self:
            self.bits[xndex][jndex][kndex] = False
            self.bits[index][xndex][kndex] = False
            self.bits[index][jndex][xndex] = False
            self.bits[xndex // root + root * (index // root)][xndex % root + root * (jndex // root)][kndex] = False

        self.bits[index][jndex][kndex] = True

    def zeroIndirect(self, ijk):
        index, jndex, kndex = ijk

        self.bits[index][jndex][kndex] = False
