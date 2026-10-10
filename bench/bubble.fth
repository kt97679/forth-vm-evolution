\ bubble.fth - a bubble sort of pseudo-random cells: loops, memory, compares.
\
\ The owner's RelF bench (relf's bench/langs/bench.4 - his own, the same
\ program in C, Go, Python and Ruby beside it), the array 300 cells, not 3000,
\ so a timed run stays near the others. DO LOOP two deep, @ and ! through
\ computed addresses, a compare and a swap: execution, where parse - which it
\ replaced in the selection, with ackermann.fth (Iteration 127) - is the
\ interpreter. CORE words only, as the others; the checksum is printed, so a
\ design that sorts wrongly shows.

300 CONSTANT NB
CREATE ARR NB CELLS ALLOT
VARIABLE SEED
: RND ( --- n )  SEED @ 1103515245 * 12345 + 2147483647 AND DUP SEED ! ;
: BUBBLE ( --- checksum )
  74755 SEED !  NB 0 DO RND 1000000 MOD ARR I CELLS + ! LOOP
  NB 1 DO  NB I - 0 DO
    ARR I CELLS + DUP @ OVER CELL+ @ 2DUP > IF ROT DUP >R ! R> CELL+ ! ELSE 2DROP DROP THEN
  LOOP LOOP
  0 NB 0 DO ARR I CELLS + @ I 1+ * + LOOP ;

: BENCH ( --- )  BUBBLE . CR ;

BENCH
S" BENCH-DONE" TYPE CR
