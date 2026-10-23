\ gc16.fth - a heap of cons cells and a mark-and-sweep collector, under a mutator that builds and drops random
\ lists and trees (Iteration 470). Written for this project from scratch: an application workload of the kind
\ Appbench's benchgc is (a garbage collector at work), not a copy of it. Core words only, upper case.

DECIMAL
20000 CONSTANT NCELLS   64 CONSTANT NROOTS   0 CONSTANT NIL       \ cell 0 is nil, never allocated
CREATE CARS NCELLS CELLS ALLOT   CREATE CDRS NCELLS CELLS ALLOT   CREATE MARKS NCELLS ALLOT
CREATE ROOTS NROOTS 4 + CELLS ALLOT          \ each holds a tagged value; the last four are the system's
: ROOT ( i -- a ) CELLS ROOTS + ;
NROOTS ROOT CONSTANT ARG0   NROOTS 1+ ROOT CONSTANT ARG1   NROOTS 2 + ROOT CONSTANT TEMP   NROOTS 3 + ROOT CONSTANT STK
VARIABLE FREELIST   VARIABLE NFREE   VARIABLE GCS   VARIABLE FREED   VARIABLE SEED   VARIABLE CHECK
: CAR ( c -- x ) CELLS CARS + @ ;      : CDR ( c -- c' ) CELLS CDRS + @ ;
: CAR! ( x c -- ) CELLS CARS + ! ;     : CDR! ( c' c -- ) CELLS CDRS + ! ;
: RANDOM ( -- u ) SEED @ 1103515245 * 12345 + 2147483647 AND DUP SEED ! 8 RSHIFT ;
: CHOOSE ( n -- u ) RANDOM SWAP MOD ;

\ a tagged value: a number odd (n*2+1), a cell even (c*2; nil is 0, no reference)
: >NUM ( n -- x ) 2* 1+ ;   : NUM> ( x -- n ) 2/ ;   : >REF ( c -- x ) 2* ;   : REF> ( x -- c ) 2/ ;
: REF? ( x -- f ) DUP 1 AND 0= SWAP 0= 0= AND ;

: MARK ( c -- )                                    \ the car by recursion, the cdr chain by a loop
  BEGIN DUP NIL = 0= WHILE
    DUP MARKS + C@ IF DROP EXIT THEN
    1 OVER MARKS + C!
    DUP CAR DUP REF? IF REF> RECURSE ELSE DROP THEN
    CDR
  REPEAT DROP ;
: SWEEP ( -- )
  NIL FREELIST !  0 NFREE !
  NCELLS 1 DO
    I MARKS + C@ IF 0 I MARKS + C!
    ELSE FREELIST @ I CDR!  I FREELIST !  1 NFREE +!  1 FREED +! THEN
  LOOP ;
: GC ( -- ) 1 GCS +!
  NROOTS 4 + 0 DO I ROOT @ DUP REF? IF REF> MARK ELSE DROP THEN LOOP
  SWEEP  NFREE @ 0= IF ." HEAP FULL" CR ABORT THEN ;
: CONS ( x c -- c' )                               \ x tagged, c a cell or nil - both in roots while a collection runs
  NFREE @ 0= IF >REF ARG1 !  ARG0 !  GC  ARG0 @  ARG1 @ REF>  0 ARG0 !  0 ARG1 ! THEN
  FREELIST @ DUP CDR FREELIST !  -1 NFREE +!
  >R R@ CDR! R@ CAR! R> ;

\ the mutator: lists and trees of random numbers, each built under a root
: PUSH ( c -- ) >REF STK @ REF> CONS >REF STK ! ;                 \ a stack the collector sees
: POP ( -- c ) STK @ REF> DUP CAR REF> SWAP CDR >REF STK ! ;
: LIST ( n -- c ) NIL >REF TEMP !  0 DO 1000 CHOOSE >NUM TEMP @ REF> CONS >REF TEMP ! LOOP  TEMP @ REF>  0 TEMP ! ;
: TREE ( depth -- c )
  DUP 0= IF DROP 1000 CHOOSE >NUM NIL CONS EXIT THEN
  1- DUP RECURSE PUSH  RECURSE  POP >REF SWAP CONS ;              \ ( left saved ) right, then cons(left, right)
: SUM ( c -- n ) 0 SWAP
  BEGIN DUP NIL = 0= WHILE
    DUP CAR DUP REF? IF REF> RECURSE ELSE NUM> THEN ROT + SWAP
    CDR
  REPEAT DROP ;
: INIT ( -- )
  NCELLS 0 DO 0 I CAR! NIL I CDR! 0 I MARKS + C! LOOP
  NROOTS 4 + 0 DO 0 I ROOT ! LOOP  0 GCS !  0 FREED !  0 CHECK !  12345 SEED !  SWEEP  0 FREED ! ;
: STEP ( -- )                                      \ one root replaced: its old structure becomes garbage
  NROOTS CHOOSE
  3 CHOOSE IF 200 CHOOSE 1+ LIST ELSE 6 CHOOSE 3 + TREE THEN
  >REF SWAP ROOT ! ;
: CHECKSUM ( -- ) 0 NROOTS 0 DO I ROOT @ DUP REF? IF REF> SUM ELSE DROP 0 THEN + LOOP
  CHECK @ 31 * + 65521 MOD CHECK ! ;                \ small enough for 32-bit cells
: BENCH ( n -- ) INIT  0 DO STEP  I 100 MOD 99 = IF CHECKSUM THEN LOOP
  ." GC16 GCS " GCS @ .  ." FREED " FREED @ .  ." CHECK " CHECK @ . CR ;
