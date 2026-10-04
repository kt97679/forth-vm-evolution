\ lab/evolve/pgo-train.fth - what profile-guided optimisation trains an
\ engine on (the pgo gene, Iteration 7). NEVER one of the measured
\ workloads - kernel, fib, parse, corpus, loop: a profile taken from them
\ tunes the engine to the benchmark. The same ingredients, other text:
\ compiling through the outer interpreter (the 120 T-words, generated once
\ with a seeded script), calls and returns, DO loops, bytes and cells,
\ strings, CREATE/DOES>, pictured number output. Prints one checksum.
DECIMAL
VARIABLE SUM  0 SUM !
: ACC ( n -- ) SUM @ + 65535 AND SUM ! ;
: T0 ( n -- n ) 5 0 DO 1 + LOOP 549 + 2* 3 0 DO 1 + LOOP 65535 AND ;
: T1 ( n -- n ) 2* 565 AND 65535 AND ;
: T2 ( n -- n ) DUP 64 < IF 15 + ELSE 41 - THEN T0 65535 AND ;
: T3 ( n -- n ) 227 + T0 148 OR 316 OR DUP 93 < IF 7 + ELSE 38 - THEN 65535 AND ;
: T4 ( n -- n ) 1+ T0 T3 65535 AND ;
: T5 ( n -- n ) DUP 239 < IF 38 + ELSE 30 - THEN 2/ DUP 358 < IF 50 + ELSE 16 - THEN 308 OR ABS 65535 AND ;
: T6 ( n -- n ) 75 + 2/ DUP 78 < IF 32 + ELSE 27 - THEN 685 + DUP 294 < IF 21 + ELSE 22 - THEN 65535 AND ;
: T7 ( n -- n ) T4 DUP 36 < IF 6 + ELSE 18 - THEN 1- 749 MAX 65535 AND ;
: T8 ( n -- n ) T7 396 MAX 964 AND 1+ 65535 AND ;
: T9 ( n -- n ) 2/ DUP 67 < IF 48 + ELSE 16 - THEN 65535 AND ;
: T10 ( n -- n ) INVERT 1 AND + 2/ 1+ 141 MIN 1+ 65535 AND ;
: T11 ( n -- n ) T8 T9 3 0 DO 2 + LOOP 238 MAX 65535 AND ;
: T12 ( n -- n ) 852 OR 289 + 548 XOR 65535 AND ;
: T13 ( n -- n ) 6 0 DO 1 + LOOP INVERT 1 AND + DUP 448 < IF 44 + ELSE 36 - THEN NEGATE 65535 AND ;
: T14 ( n -- n ) 650 AND 69 - 2* 54 + 155 OR 65535 AND ;
: T15 ( n -- n ) 6 0 DO 1 + LOOP 213 OR 65535 AND ;
: T16 ( n -- n ) 259 XOR T15 870 AND 5 0 DO 8 + LOOP 2* 65535 AND ;
: T17 ( n -- n ) 351 MAX 849 MAX 24 - 65535 AND ;
: T18 ( n -- n ) 557 + DUP 153 < IF 42 + ELSE 6 - THEN T14 2/ 65535 AND ;
: T19 ( n -- n ) DUP 273 < IF 35 + ELSE 50 - THEN 1- 831 MIN 3 0 DO 4 + LOOP 65535 AND ;
: T20 ( n -- n ) T15 505 XOR T12 DUP 242 < IF 17 + ELSE 13 - THEN T17 65535 AND ;
: T21 ( n -- n ) DUP 371 < IF 23 + ELSE 24 - THEN 105 - ABS 640 OR DUP 246 < IF 42 + ELSE 23 - THEN 65535 AND ;
: T22 ( n -- n ) DUP 62 < IF 25 + ELSE 46 - THEN DUP 245 < IF 12 + ELSE 28 - THEN 65535 AND ;
: T23 ( n -- n ) 969 MAX NEGATE T16 T17 65535 AND ;
: T24 ( n -- n ) 605 AND DUP 75 < IF 40 + ELSE 39 - THEN 4 0 DO 3 + LOOP 65535 AND ;
: T25 ( n -- n ) 819 MAX T19 INVERT 1 AND + 65535 AND ;
: T26 ( n -- n ) DUP 109 < IF 2 + ELSE 17 - THEN 514 - DUP 167 < IF 17 + ELSE 35 - THEN 65535 AND ;
: T27 ( n -- n ) DUP 32 < IF 48 + ELSE 23 - THEN 6 0 DO 9 + LOOP 1+ 156 OR INVERT 1 AND + 65535 AND ;
: T28 ( n -- n ) DUP 312 < IF 1 + ELSE 50 - THEN DUP 89 < IF 10 + ELSE 31 - THEN T21 T25 T27 65535 AND ;
: T29 ( n -- n ) 2 0 DO 4 + LOOP 44 MIN 65535 AND ;
: T30 ( n -- n ) 1+ 916 + 65535 AND ;
: T31 ( n -- n ) 997 OR T26 T30 INVERT 1 AND + 2/ 65535 AND ;
: T32 ( n -- n ) 3 0 DO 8 + LOOP 125 AND 2* T30 65535 AND ;
: T33 ( n -- n ) 311 MIN 796 - 65535 AND ;
: T34 ( n -- n ) 905 - 3 0 DO 2 + LOOP NEGATE 684 MIN 65535 AND ;
: T35 ( n -- n ) 442 OR NEGATE 327 + 65535 AND ;
: T36 ( n -- n ) 568 AND 2* 1+ T29 65535 AND ;
: T37 ( n -- n ) 3 0 DO 2 + LOOP 279 + 65535 AND ;
: T38 ( n -- n ) 133 MIN 1- DUP 133 < IF 26 + ELSE 10 - THEN 65535 AND ;
: T39 ( n -- n ) T32 819 MAX 917 + 18 MAX 267 + 65535 AND ;
: T40 ( n -- n ) 884 + ABS 5 0 DO 5 + LOOP 65535 AND ;
: T41 ( n -- n ) 727 - 3 0 DO 5 + LOOP 207 XOR 65535 AND ;
: T42 ( n -- n ) 2/ 513 MAX 356 MIN 257 + 65535 AND ;
: T43 ( n -- n ) 518 OR 6 0 DO 8 + LOOP 65535 AND ;
: T44 ( n -- n ) 2 0 DO 7 + LOOP T42 4 0 DO 4 + LOOP 65535 AND ;
: T45 ( n -- n ) 853 MAX T39 ABS 65535 AND ;
: T46 ( n -- n ) DUP 8 < IF 5 + ELSE 41 - THEN T42 65535 AND ;
: T47 ( n -- n ) 87 MAX DUP 446 < IF 33 + ELSE 43 - THEN 6 0 DO 4 + LOOP T39 2/ 65535 AND ;
: T48 ( n -- n ) ABS ABS 6 0 DO 6 + LOOP 989 XOR 65535 AND ;
: T49 ( n -- n ) 2* 86 AND 672 - 65535 AND ;
: T50 ( n -- n ) 2* 837 + 601 + 65535 AND ;
: T51 ( n -- n ) 312 MAX 600 OR DUP 80 < IF 43 + ELSE 46 - THEN DUP 306 < IF 25 + ELSE 49 - THEN 507 - 65535 AND ;
: T52 ( n -- n ) T46 856 MAX 5 0 DO 9 + LOOP 537 MIN 65535 AND ;
: T53 ( n -- n ) DUP 300 < IF 46 + ELSE 44 - THEN 3 0 DO 2 + LOOP 65535 AND ;
: T54 ( n -- n ) 653 XOR 5 0 DO 8 + LOOP 65535 AND ;
: T55 ( n -- n ) T50 2* 65535 AND ;
: T56 ( n -- n ) DUP 384 < IF 33 + ELSE 35 - THEN 539 + T55 77 MIN 747 MIN 65535 AND ;
: T57 ( n -- n ) 666 AND NEGATE 933 MAX 65535 AND ;
: T58 ( n -- n ) DUP 316 < IF 41 + ELSE 42 - THEN 615 - 668 MAX T52 65535 AND ;
: T59 ( n -- n ) NEGATE 689 + 65535 AND ;
: T60 ( n -- n ) T56 T56 NEGATE 65535 AND ;
: T61 ( n -- n ) 6 0 DO 4 + LOOP 88 AND 65535 AND ;
: T62 ( n -- n ) 79 MIN NEGATE 65535 AND ;
: T63 ( n -- n ) 2/ 93 - T59 3 0 DO 9 + LOOP 65535 AND ;
: T64 ( n -- n ) 4 0 DO 4 + LOOP NEGATE 2/ 504 MAX 65535 AND ;
: T65 ( n -- n ) 1- 353 AND 861 XOR 769 XOR DUP 62 < IF 13 + ELSE 46 - THEN 65535 AND ;
: T66 ( n -- n ) 4 0 DO 5 + LOOP NEGATE 65535 AND ;
: T67 ( n -- n ) 6 0 DO 2 + LOOP NEGATE DUP 438 < IF 4 + ELSE 18 - THEN 855 MAX 959 - 65535 AND ;
: T68 ( n -- n ) 5 0 DO 9 + LOOP 792 XOR DUP 220 < IF 2 + ELSE 49 - THEN 65535 AND ;
: T69 ( n -- n ) 6 0 DO 9 + LOOP 83 + 5 0 DO 8 + LOOP T63 T65 65535 AND ;
: T70 ( n -- n ) 950 OR 484 AND 305 XOR T66 2/ 65535 AND ;
: T71 ( n -- n ) 1- 2/ T64 928 MIN 65535 AND ;
: T72 ( n -- n ) T71 5 0 DO 7 + LOOP 198 - 351 OR 245 XOR 65535 AND ;
: T73 ( n -- n ) DUP 104 < IF 2 + ELSE 48 - THEN DUP 197 < IF 27 + ELSE 48 - THEN NEGATE 771 + 65535 AND ;
: T74 ( n -- n ) 991 XOR 516 OR T69 919 - 1- 65535 AND ;
: T75 ( n -- n ) ABS DUP 447 < IF 2 + ELSE 9 - THEN 727 MIN 5 0 DO 8 + LOOP 401 MIN 65535 AND ;
: T76 ( n -- n ) 3 0 DO 2 + LOOP 156 OR 2 0 DO 8 + LOOP 796 + 129 - 65535 AND ;
: T77 ( n -- n ) T73 4 0 DO 9 + LOOP 65535 AND ;
: T78 ( n -- n ) T71 308 OR 3 0 DO 7 + LOOP 810 OR 551 XOR 65535 AND ;
: T79 ( n -- n ) 324 MAX DUP 125 < IF 31 + ELSE 34 - THEN 253 + 4 0 DO 1 + LOOP 511 MAX 65535 AND ;
: T80 ( n -- n ) 234 MAX ABS 35 MAX 431 XOR T75 65535 AND ;
: T81 ( n -- n ) DUP 379 < IF 33 + ELSE 5 - THEN 994 - 65535 AND ;
: T82 ( n -- n ) DUP 100 < IF 15 + ELSE 30 - THEN 779 XOR 639 AND T77 65535 AND ;
: T83 ( n -- n ) 1- 610 - 2 0 DO 4 + LOOP 611 - 1- 65535 AND ;
: T84 ( n -- n ) 461 MAX 2 0 DO 2 + LOOP 65535 AND ;
: T85 ( n -- n ) 190 MAX 5 0 DO 1 + LOOP 743 AND 65535 AND ;
: T86 ( n -- n ) 5 0 DO 3 + LOOP 81 XOR 431 + T81 65535 AND ;
: T87 ( n -- n ) INVERT 1 AND + 824 AND 723 AND 555 AND 373 MAX 65535 AND ;
: T88 ( n -- n ) 421 - DUP 393 < IF 26 + ELSE 3 - THEN NEGATE 943 + 766 + 65535 AND ;
: T89 ( n -- n ) ABS 6 0 DO 1 + LOOP 734 MAX 283 XOR 65535 AND ;
: T90 ( n -- n ) T83 240 + 65535 AND ;
: T91 ( n -- n ) T90 5 0 DO 5 + LOOP 5 0 DO 3 + LOOP 3 0 DO 1 + LOOP DUP 379 < IF 20 + ELSE 45 - THEN 65535 AND ;
: T92 ( n -- n ) T89 DUP 236 < IF 24 + ELSE 39 - THEN 203 AND 65535 AND ;
: T93 ( n -- n ) 67 MAX 566 OR 437 + 65535 AND ;
: T94 ( n -- n ) 87 - 511 MAX 65535 AND ;
: T95 ( n -- n ) 137 AND 1- 552 MIN DUP 389 < IF 8 + ELSE 50 - THEN DUP 151 < IF 18 + ELSE 37 - THEN 65535 AND ;
: T96 ( n -- n ) 1- 450 - 242 - 930 OR 65535 AND ;
: T97 ( n -- n ) 406 XOR 6 0 DO 9 + LOOP 828 + 65535 AND ;
: T98 ( n -- n ) 2 0 DO 1 + LOOP INVERT 1 AND + 460 XOR 301 - 195 OR 65535 AND ;
: T99 ( n -- n ) 4 0 DO 9 + LOOP DUP 230 < IF 39 + ELSE 17 - THEN DUP 341 < IF 1 + ELSE 7 - THEN 65535 AND ;
: T100 ( n -- n ) 378 XOR 209 XOR 750 MAX 2 0 DO 6 + LOOP 65535 AND ;
: T101 ( n -- n ) T95 T94 815 AND 2* INVERT 1 AND + 65535 AND ;
: T102 ( n -- n ) T96 T95 T100 T100 4 0 DO 7 + LOOP 65535 AND ;
: T103 ( n -- n ) 581 XOR 2* 65535 AND ;
: T104 ( n -- n ) T102 T99 5 0 DO 3 + LOOP INVERT 1 AND + 65535 AND ;
: T105 ( n -- n ) ABS 2/ 65535 AND ;
: T106 ( n -- n ) 565 - T104 638 XOR 65535 AND ;
: T107 ( n -- n ) 291 - 2* 503 MIN 65535 AND ;
: T108 ( n -- n ) 858 + 5 0 DO 6 + LOOP 949 MAX 65535 AND ;
: T109 ( n -- n ) 730 OR T103 T104 T104 DUP 94 < IF 37 + ELSE 14 - THEN 65535 AND ;
: T110 ( n -- n ) 1+ 368 + 65535 AND ;
: T111 ( n -- n ) 743 MIN 2 0 DO 9 + LOOP DUP 345 < IF 3 + ELSE 43 - THEN 65535 AND ;
: T112 ( n -- n ) 614 AND T108 T108 T110 65535 AND ;
: T113 ( n -- n ) T112 2/ 634 AND NEGATE DUP 400 < IF 30 + ELSE 12 - THEN 65535 AND ;
: T114 ( n -- n ) 2* 441 XOR 453 OR 2* 134 + 65535 AND ;
: T115 ( n -- n ) DUP 262 < IF 6 + ELSE 4 - THEN DUP 459 < IF 25 + ELSE 42 - THEN 3 0 DO 1 + LOOP DUP 315 < IF 47 + ELSE 45 - THEN 65535 AND ;
: T116 ( n -- n ) 907 AND 831 MIN 65535 AND ;
: T117 ( n -- n ) T112 360 OR DUP 82 < IF 21 + ELSE 40 - THEN 65535 AND ;
: T118 ( n -- n ) 5 0 DO 3 + LOOP 988 AND 270 OR ABS 65535 AND ;
: T119 ( n -- n ) 187 AND 959 XOR T117 804 XOR 65535 AND ;
: RUN-T ( -- ) 40 0 DO I T119 ACC I T60 ACC I T7 ACC LOOP ;
: BINOM ( n k -- c )
  DUP 0= IF 2DROP 1 EXIT THEN
  2DUP = IF 2DROP 1 EXIT THEN
  2DUP 1- SWAP 1- SWAP RECURSE >R
  SWAP 1- SWAP RECURSE R> + ;
8190 CONSTANT SZ
CREATE FLAGS SZ ALLOT
: SIEVE ( -- count )
  FLAGS SZ 1 FILL  0
  SZ 0 DO
    FLAGS I + C@ IF
      I 2* 3 + DUP I +
      BEGIN DUP SZ < WHILE 0 OVER FLAGS + C! OVER + REPEAT
      2DROP 1+
    THEN
  LOOP ;
: DIGITSUM ( addr u -- n ) 0 SWAP 0 ?DO OVER I + C@ [CHAR] 0 - + LOOP SWAP DROP ;
: NUMBERS ( -- ) 3000 0 DO I 7919 * S>D <# #S #> DIGITSUM ACC LOOP ;
: ARRAY ( n -- ) CREATE CELLS ALLOT DOES> ( i -- addr ) SWAP CELLS + ;
200 ARRAY TBL
: TABLE ( -- ) 200 0 DO I I * 7 + I TBL ! LOOP  0 200 0 DO I TBL @ + LOOP ACC ;
CREATE SRC 64 ALLOT  CREATE DST 64 ALLOT
: STRINGS ( -- ) SRC 64 [CHAR] a FILL
  2000 0 DO SRC DST I 63 AND 1+ MOVE DST I 63 AND + C@ ACC LOOP ;
16 9 BINOM ACC  3 0 DO SIEVE ACC LOOP  NUMBERS TABLE STRINGS RUN-T
SUM @ . CR
BYE
