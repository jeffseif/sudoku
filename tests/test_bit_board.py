import random
import pytest

from sudoku.bitBoard import BitBoard


class TestBitBoard:

    @pytest.fixture
    def size(self):
        return 9

    @pytest.fixture
    def iterator(self, size):
        return range(size)

    @pytest.fixture
    def bit_false(self, iterator):
        return [[[False for each in iterator] for each in iterator] for each in iterator]

    @pytest.fixture
    def bit_true(self, iterator):
        return [[[True for each in iterator] for each in iterator] for each in iterator]

    @pytest.fixture
    def bit_random(self, iterator):
        return [[[random.choice((True, False)) for each in iterator] for each in iterator] for each in iterator]

    def test_bit_board_init(self, size, bit_true):
        bitBoard = BitBoard(size)
        assert bitBoard.bits == bit_true

    def test_bit_board_init_false(self, size, bit_false):
        bitBoard = BitBoard(size, bit_false)
        assert bitBoard.bits is bit_false

    def test_bit_board_len(self, size, bit_false):
        bitBoard = BitBoard(size, bit_false)
        assert len(bitBoard) == 0

    def test_bit_board_zero_direct(self, size, bit_random):
        bitBoard = BitBoard(size, bit_random)
        ijk = next(iter(bitBoard.trues()))
        assert bitBoard[ijk] is True
        bitBoard.zeroDirect(ijk)
        assert bitBoard[ijk] is True
        index, jndex, kndex = ijk
        assert sum(bitBoard[:, jndex, kndex]) == 1
        assert sum(bitBoard[index, :, kndex]) == 1
        assert sum(bitBoard[index, jndex, :]) == 1

    def test_bit_board_zero_indirect(self, size, bit_random):
        bitBoard = BitBoard(size, bit_random)
        ijk = next(iter(bitBoard.trues()))
        assert bitBoard[ijk] is True
        bitBoard.zeroIndirect(ijk)
        assert bitBoard[ijk] is False
