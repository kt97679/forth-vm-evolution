\ evo.fth - a population of genomes evolving toward a hidden target: fitness, tournaments, crossover and mutation
\ (Iteration 470). Written for this project from scratch: an application workload of the kind Appbench's brew is
\ (an evolution simulated in Forth), not a copy of it. Core words only, upper case.

DECIMAL
64 CONSTANT NPOP   64 CONSTANT GLEN
CREATE POPA NPOP GLEN * ALLOT   CREATE POPB NPOP GLEN * ALLOT   CREATE TARGET GLEN ALLOT
CREATE FIT NPOP CELLS ALLOT     CREATE BITS 256 ALLOT
VARIABLE CUR   VARIABLE NXT   VARIABLE SEED   VARIABLE BEST   VARIABLE BESTGEN   VARIABLE CHECK
: RANDOM ( -- u ) SEED @ 1103515245 * 12345 + 2147483647 AND DUP SEED ! 8 RSHIFT ;
: CHOOSE ( n -- u ) RANDOM SWAP MOD ;
: GENOME ( i pop -- a ) SWAP GLEN * + ;
: BITS-INIT 256 0 DO 0 I BEGIN DUP WHILE DUP 1 AND ROT + SWAP 1 RSHIFT REPEAT DROP I BITS + C! LOOP ;
: FITNESS ( a -- n ) 0 SWAP GLEN 0 DO DUP I + C@ I TARGET + C@ XOR BITS + C@ 8 SWAP - ROT + SWAP LOOP DROP ;
: EVALUATE-ALL ( -- ) NPOP 0 DO I CUR @ GENOME FITNESS I CELLS FIT + ! LOOP ;
: FITTEST ( -- i ) 0 NPOP 1 DO I CELLS FIT + @ OVER CELLS FIT + @ > IF DROP I THEN LOOP ;
: TOURNAMENT ( -- i ) NPOP CHOOSE  2 0 DO NPOP CHOOSE 2DUP CELLS FIT + @ SWAP CELLS FIT + @ > IF SWAP THEN DROP LOOP ;
: BREED ( child -- )                               \ one-point crossover of two tournaments' winners, then mutation
  NXT @ GENOME  TOURNAMENT CUR @ GENOME  TOURNAMENT CUR @ GENOME  GLEN CHOOSE
  GLEN 0 DO  DUP I > IF 2 PICK ELSE OVER THEN I + C@  4 PICK I + C!  LOOP      \ no >R here: I reads the loop's own
  DROP 2DROP
  GLEN 0 DO 64 CHOOSE 0= IF DUP I + DUP C@ 1 8 CHOOSE LSHIFT XOR SWAP C! THEN LOOP DROP ;
: GENERATION ( -- )
  EVALUATE-ALL  FITTEST CUR @ GENOME  0 NXT @ GENOME  GLEN MOVE        \ the fittest kept as it is
  NPOP 1 DO I BREED LOOP
  CUR @ NXT @ CUR ! NXT ! ;
: INIT ( -- ) 777 SEED !  BITS-INIT  GLEN 0 DO 256 CHOOSE TARGET I + C! LOOP
  NPOP GLEN * 0 DO 256 CHOOSE POPA I + C! LOOP  POPA CUR !  POPB NXT !  0 BEST !  0 BESTGEN !  0 CHECK ! ;
: BENCH ( gens -- ) INIT
  0 DO GENERATION  0 CUR @ GENOME FITNESS DUP BEST @ > IF BEST ! I BESTGEN ! ELSE DROP THEN LOOP
  NPOP GLEN * 0 DO CUR @ I + C@ CHECK @ 31 * + 65521 MOD CHECK ! LOOP
  ." EVO BEST " BEST @ .  ." AT " BESTGEN @ .  ." CHECK " CHECK @ . CR ;
