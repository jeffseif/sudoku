#! /usr/bin/env python3
from setuptools import setup
from sudoku import __author__
from sudoku import __email__
from sudoku import __program__
from sudoku import __url__
from sudoku import __version__


setup(
    author=__author__,
    author_email=__email__,
    install_requires=[],
    name=__program__,
    packages=[__program__],
    platforms='all',
    setup_requires=[
        'setuptools',
        'tox',
    ],
    test_suite='tests',
    url=__url__,
    version=__version__,
)
