__author__ = "Jeffrey Seifried"
__version__ = "1.0.0"
__year__ = "2017"


DEFAULT_PUZZLE = (
    "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
)
DIGITS = list(
    map(
        chr,  # typing: ignore[arg-type]
        sum(
            map(
                lambda r: list(r),
                (range(49, 58), range(48, 49), range(65, 91), range(97, 123)),
            ),
            [],
        ),
    ),
)
PROMPT_TRANSLATOR = {
    ord(char): replacement
    for chars, replacement in (
        ("-|+, \n", None),
        (".", "\u241E"),
    )
    for char in chars
}
