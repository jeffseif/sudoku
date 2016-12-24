#! /bin/bash

# Setup

make ;
source venv/bin/activate ;

# Run

python -m sudoku.main "$@" ;
