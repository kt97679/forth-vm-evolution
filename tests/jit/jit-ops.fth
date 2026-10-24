\ jit-ops.fth - every word the JIT maps to stencils (tools/layout.py's S1, K and the genes' maps), each in a word of its
\ own so it is translated, on edge values, its output compared with s6's at the same width (Iteration 509; run with
\ jit-diff.fth by lab/evolve/engines-check.py). The map's constants once assumed eight-byte cells at either width -
\ CELL+ and CELLS (493), 2@ and 2! (507): every entry run at both widths is what finds the next one.
DECIMAL
CREATE B1 16 CELLS ALLOT   CREATE CS 5 C, CHAR h C, CHAR e C, CHAR l C, CHAR l C, CHAR o C,
: .S3 ( a b c -- ) ROT . SWAP . . ;
: O1 7 DUP . . -3 4 DROP . 1 2 SWAP . . 1 2 OVER . . . 1 2 3 ROT .S3 ;
: O2 5 7 + . -5 7 + . 5 7 - . 7 -5 - . 12 10 AND . 12 10 OR . 12 10 XOR . 5 NEGATE . -1 NEGATE . 0 NEGATE . ;
: O3 3 3 = . 3 4 = . -1 1 < . 1 -1 < . -1 1 > . 2 1 > . -1 1 U< . 1 -1 U< . 0 0 U< . ;
: O4 1 1 LSHIFT . 1 4 LSHIFT . 3 0 LSHIFT . 256 3 RSHIFT . -1 1 RSHIFT 0> . 1 0 RSHIFT . ;
: O5 99 B1 ! B1 @ . 7 B1 CELL+ ! B1 CELL+ @ . 65 B1 C! B1 C@ . 300 B1 C! B1 C@ . B1 4 CELLS 2 FILL B1 C@ . B1 3 CELLS + C@ . ;
: O6 0 0= . 5 0= . -2 0< . 2 0< . 0 INVERT . 5 INVERT . 3 3 <> . 3 4 <> . 9 1+ . 9 1- . B1 CELL+ B1 - . B1 CHAR+ B1 - . 3 CELLS . 0 CELLS . ;
: O7 11 22 B1 2! B1 2@ . . B1 @ . B1 CELL+ @ . 1 2 2DUP . . . . 1 2 3 2DROP . CS COUNT . C@ . ;
: O8 5 >R R@ . R> . 1 2 >R >R R> R> . . 0 10 0 DO I + LOOP . 0 3 0 DO 2 0 DO J 10 * I + + LOOP LOOP . ;
: O9 0 5 0 DO I 3 = IF UNLOOP EXIT THEN I + LOOP ;  : O10 O9 . 7 8 9 2 PICK . 0 PICK . 1 PICK . DROP DROP DROP ;
: O11 3 4 UM* . . -1 2 UM* . . 100 0 7 UM/MOD . . 10 ALIGNED . 9 ALIGNED . 0 ALIGNED . SP@ SP@ - . ;
: O12 1 0 2 0 D+ . . -1 0 1 0 D+ . . -1 -1 1 0 D+ . . ;
: O13 0 20 0 DO I + LOOP . 0 4 0 DO I 1 AND IF I + THEN LOOP . 0 3 0 DO I 2 + + LOOP . ;   \ I + (the I+ operation where a design has it)
O1 CR O2 CR O3 CR O4 CR O5 CR O6 CR O7 CR O8 CR O10 CR O11 CR O12 CR O13 CR
BYE
