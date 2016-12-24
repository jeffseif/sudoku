#! /bin/bash

PUZZLE='12344321' ;

./sudoku.sh \
    --verbose \
    "${PUZZLE}" \
    && ./sudoku.sh \
    --verbose \
    --use-old-solver \
    "${PUZZLE}" \
    && echo 'SUCCESS' ;
