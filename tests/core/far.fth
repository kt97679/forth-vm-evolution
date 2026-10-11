\ far.fth - code and data far from the image base (Iteration 158). Words
\ compiled past 64 KB take tag2's three-byte calls; past 8 MB more, its
\ four-byte calls, beyond the reach of cv8's far form and its links. Line k
\ prints k*100000 plus its answer. Each answer must be right; a missing one
\ must be refused out loud ("out of reach") - nothing computed otherwise.
VARIABLE V
: NEAR ( x --- x' ) V @ EXECUTE ;
: CHECK ( f k --- ) SWAP IF 100000 * 1+ . CR ELSE DROP THEN ;
\ Lines 10 and 11 say the gaps were taken: one refused leaves the rest near.
65536 ALLOT
HERE START @ - 65536 > 10 CHECK
: F1 ( n --- n' ) 1+ ;
: FIB ( n --- f ) DUP 2 < IF EXIT THEN DUP 1- RECURSE SWAP 2 - RECURSE + ;
: F2 ( n --- n' ) F1 F1 ;
12 FIB 100000 + . CR
5 F2 200000 + . CR
: CONST CREATE , DOES> @ ;
42 CONST K1
K1 300000 + . CR
' F2 V ! 10 NEAR 400000 + . CR
8388608 ALLOT
HERE START @ - 8388608 > 11 CHECK
: G1 ( n --- n' ) 2 + ;
: GFIB ( n --- f ) DUP 2 < IF EXIT THEN DUP 1- RECURSE SWAP 2 - RECURSE + ;
: G2 ( n --- n' ) G1 G1 F2 ;
CREATE BUF 4 CELLS ALLOT
: G3 ( --- n ) 7 BUF ! BUF @ 1+ ;
13 GFIB 500000 + . CR
5 G2 600000 + . CR
G3 700000 + . CR
: CONST2 CREATE , DOES> @ 1+ ;
43 CONST2 K2
K2 800000 + . CR
' G2 V ! 10 NEAR 900000 + . CR
