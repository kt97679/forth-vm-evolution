\ wordfreq.fth - words counted in generated text: string hashing, an open-addressing hash table of counted strings
\ kept in a pool, comparison byte by byte, and the most frequent found (Iteration 500). Written for this project from
\ scratch, a held-out application (appbench.py) - core words only, upper case, checking itself.

DECIMAL
4096 CONSTANT TSIZE   65536 CONSTANT PSIZE
CREATE TKEY TSIZE CELLS ALLOT   CREATE TCNT TSIZE CELLS ALLOT   CREATE POOL PSIZE ALLOT
VARIABLE PHERE   VARIABLE SEED   VARIABLE NWORDS   VARIABLE NDIST   VARIABLE CHECK
CREATE WBUF 32 ALLOT   VARIABLE WLEN
: RANDOM ( -- u ) SEED @ 1103515245 * 12345 + 2147483647 AND DUP SEED ! 8 RSHIFT ;
: CHOOSE ( n -- u ) RANDOM SWAP MOD ;
: SYL ( n -- c-addr u ) 3 * S" taxbelmorinusepakodivunasoltermigafe" DROP + 3 ;   \ twelve syllables of three letters
: GENWORD ( -- )                  \ one to three syllables, the first more likely short - words repeat
  0 WLEN !  3 CHOOSE 1+ 2 CHOOSE IF 1 MIN THEN 0 DO 12 CHOOSE SYL WBUF WLEN @ + SWAP CMOVE 3 WLEN +! LOOP ;
: HASH ( c-addr u -- h ) 5381 SWAP 0 ?DO OVER I + C@ SWAP 33 * + 65535 AND LOOP SWAP DROP ;
: SAME? ( c-addr u key -- f )     \ key: a counted string in the pool
  2DUP C@ = 0= IF DROP 2DROP 0 EXIT THEN
  1+ SWAP 0 ?DO OVER I + C@ OVER I + C@ <> IF 2DROP 0 UNLOOP EXIT THEN LOOP 2DROP -1 ;
: KEEP ( c-addr u -- key ) PHERE @ POOL + >R  DUP R@ C!  R@ 1+ SWAP CMOVE  R@ C@ 1+ PHERE +!  R> ;
: SLOT ( c-addr u -- i )          \ the word's slot - its own, or the empty one it takes
  2DUP HASH TSIZE 1- AND
  BEGIN DUP CELLS TKEY + @ DUP WHILE
    >R 2 PICK 2 PICK R> SAME? IF SWAP DROP SWAP DROP EXIT THEN
    1+ TSIZE 1- AND
  REPEAT DROP  >R KEEP R@ CELLS TKEY + !  1 NDIST +!  R> ;
: COUNT-WORD ( -- ) WBUF WLEN @ SLOT CELLS TCNT + 1 SWAP +!  1 NWORDS +! ;
: CLEAR ( -- ) TKEY TSIZE CELLS 0 FILL  TCNT TSIZE CELLS 0 FILL  0 PHERE !  0 NWORDS !  0 NDIST ! ;
: TOP ( -- i n )                  \ the most frequent word's slot and its count
  0 0 TSIZE 0 DO I CELLS TCNT + @ OVER > IF 2DROP I I CELLS TCNT + @ THEN LOOP ;
: FOLD ( n -- ) CHECK @ 31 * + 65521 MOD CHECK ! ;
: PASS ( n -- ) CLEAR  0 DO GENWORD COUNT-WORD LOOP
  NDIST @ FOLD  TOP FOLD CELLS TKEY + @ COUNT 0 ?DO DUP I + C@ FOLD LOOP DROP ;
: BENCH ( passes -- ) 0 CHECK !  777 SEED !  0 DO 20000 PASS LOOP
  ." WORDFREQ WORDS " NWORDS @ .  ." DISTINCT " NDIST @ .  ." TOP " TOP SWAP DROP .  ." CHECK " CHECK @ . CR ;
