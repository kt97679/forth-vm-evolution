\ audit.fth - the words the audit rewrote (Iteration 156) behave as before:
\ CMOVE and CMOVE> by D+, FILL by 1 -1 D+, 2SWAP, 2!, WORD, and INTERPRET's
\ stack check, now only where the stack can have changed.
CREATE B 16 ALLOT
: INIT  S" abcdefgh" B SWAP CMOVE  0 B 8 + C! ;
INIT B 7 + C@ . CR
INIT B B 1+ 7 CMOVE  B 7 + C@ . CR
INIT B B 1+ 7 CMOVE>  B 7 + C@ . B 1+ C@ . CR
INIT B 1+ B 7 CMOVE>  B C@ . B 6 + C@ . CR
INIT B 1+ B 7 CMOVE  B C@ . B 6 + C@ . CR
INIT B B 4 + 0 CMOVE  B B 4 + 0 CMOVE>  B 0 33 FILL  B 4 + C@ . B C@ . DEPTH . CR
INIT B B 4 + 1 CMOVE  B 4 + C@ . B 5 + C@ . CR
INIT B 4 + B 1 CMOVE>  B C@ . B 1+ C@ . CR
INIT B 8 42 FILL  B C@ . B 7 + C@ . B 8 + C@ . CR
INIT B 1 43 FILL  B C@ . B 1+ C@ . CR
INIT B B 2 + 6 MOVE  B 7 + C@ . B 2 + C@ . CR
INIT B 2 + B 6 MOVE  B C@ . B 5 + C@ . CR
1 2 3 4 2SWAP  1000 * SWAP 100 * + SWAP 10 * + + . CR
CREATE D 2 CELLS ALLOT  5 7 D 2!  D @ . D CELL+ @ . D 2@ 10 * + . CR
BL WORD hello COUNT DUP . + C@ . CR
1 2 : T12 3 4 + ; T12 . . . CR
DROP 5 . CR
6 . DEPTH . CR
