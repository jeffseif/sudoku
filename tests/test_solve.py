import gzip

import pytest

from sudoku.logic import Logic
from sudoku.logic import State
from sudoku.matrix import Matrix


DAT_DIRECTORY = "./dat/"
FILENAMES = (
    # 6 prompts
    "4x4",
    # 50 prompts
    "easy",
    # 1 prompt
    "extreme",
    # 11 prompts
    "hard",
    # 95 prompts
    "medium",
    # 49141 prompts (http://staffhome.ecm.uwa.edu.au/~00013890/sudokumin.php)
    "minimum",
    # 19 prompts
    "various",
)
PROMPTS = (
    "1",
    "4",
    "9",
    "F",
)


def solve_and_check_logic(prompt):
    game = Logic(prompt=prompt)
    game.solve()
    assert game.state == State.SOLVED


def solve_and_check_matrix(prompt):
    game = Matrix(prompt=prompt)
    assert any(game.solve())


CHECKERS = (
    solve_and_check_logic,
    solve_and_check_matrix,
)


class TestSolve:
    @pytest.mark.parametrize("file_name", FILENAMES)
    @pytest.mark.parametrize("checker", CHECKERS)
    def test_solve_from_filename(self, file_name, checker):
        with gzip.open("{:s}{:s}.gz".format(DAT_DIRECTORY, file_name), "rb") as f:
            for prompt in f.readlines():
                prompt = prompt.decode("utf-8")
                checker(prompt)

    @pytest.mark.parametrize("prompt", PROMPTS)
    @pytest.mark.parametrize("checker", CHECKERS)
    def test_solve_from_string(self, prompt, checker):
        checker(prompt)
