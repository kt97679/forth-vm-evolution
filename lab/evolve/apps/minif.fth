\ minif.fth - a small Forth interpreted in Forth: source text parsed word by word, a dictionary of counted names
\ searched by string compare, numbers converted by hand, colon definitions compiled to token lists run by an inner
\ interpreter through EXECUTE, IF and THEN compiled to branch tokens, unknown words thrown and caught (Iteration
\ 500). Written for this project from scratch, a held-out application (appbench.py) - core words only, upper case.

DECIMAL
CREATE MSTK 64 CELLS ALLOT   VARIABLE MSP                     \ the mini system's data stack
: MPUSH ( n -- ) MSP @ 63 AND CELLS MSTK + !  1 MSP +! ;
: MPOP ( -- n ) -1 MSP +!  MSP @ 63 AND CELLS MSTK + @ ;
VARIABLE CHECK   : OUT ( n -- ) CHECK @ 31 * + 65535 AND 65521 MOD CHECK ! ;
CREATE NAMES 4096 ALLOT   VARIABLE NHERE                       \ the mini dictionary: name, kind, value
CREATE DNAME 64 CELLS ALLOT   CREATE DKIND 64 CELLS ALLOT   CREATE DVAL 64 CELLS ALLOT   VARIABLE NDEF
CREATE CODE 8192 CELLS ALLOT   VARIABLE CHERE                    \ compiled token lists
0 CONSTANT K-PRIM   1 CONSTANT K-COLON   2 CONSTANT K-IMM
-1 CONSTANT T-LIT   -2 CONSTANT T-BRZ   -3 CONSTANT T-EXIT       \ tokens below 0 are the inner interpreter's own
: ADD-NAME ( c-addr u kind val -- ) NDEF @ >R  R@ CELLS DVAL + !  R@ CELLS DKIND + !
  NHERE @ NAMES + R@ CELLS DNAME + !  DUP NHERE @ NAMES + C!  NHERE @ NAMES + 1+ SWAP CMOVE
  NHERE @ NAMES + C@ 1+ NHERE +!  R> 1+ NDEF ! ;
: SAME? ( c-addr u key -- f ) 2DUP C@ = 0= IF DROP 2DROP 0 EXIT THEN
  1+ SWAP 0 ?DO OVER I + C@ OVER I + C@ <> IF 2DROP 0 UNLOOP EXIT THEN LOOP 2DROP -1 ;
: LOOKUP ( c-addr u -- i | -1 )   \ the newest first
  NDEF @ BEGIN DUP WHILE 1- >R 2DUP R@ CELLS DNAME + @ SAME? IF 2DROP R> EXIT THEN R> REPEAT DROP 2DROP -1 ;
: NUMBER? ( c-addr u -- n f ) DUP 0= IF 2DROP 0 0 EXIT THEN
  OVER C@ 45 = DUP >R IF 1- SWAP 1+ SWAP THEN   0 SWAP 0 ?DO
    OVER I + C@ 48 - DUP 0< OVER 9 > OR IF 2DROP R> DROP 0 0 UNLOOP EXIT THEN SWAP 10 * + LOOP
  SWAP DROP R> IF NEGATE THEN -1 ;
CREATE SRC 256 ALLOT   VARIABLE SLEN   VARIABLE SPOS   VARIABLE STATE?   VARIABLE CUR
: NEXT-WORD ( -- c-addr u ) BEGIN SPOS @ SLEN @ < IF SPOS @ SRC + C@ 32 = ELSE 0 THEN WHILE 1 SPOS +! REPEAT
  SPOS @ SRC + SPOS @ BEGIN SPOS @ SLEN @ < IF SPOS @ SRC + C@ 32 <> ELSE 0 THEN WHILE 1 SPOS +! REPEAT SPOS @ SWAP - ;
: ,T ( x -- ) CHERE @ CELLS CODE + !  1 CHERE +! ;
: RUN-LIST ( a -- )               \ the inner interpreter: a token list from cell a
  BEGIN
    DUP CELLS CODE + @ SWAP 1+ SWAP
    DUP T-EXIT = IF 2DROP EXIT THEN
    DUP T-LIT = IF DROP DUP CELLS CODE + @ MPUSH 1+ ELSE
    DUP T-BRZ = IF DROP MPOP IF 1+ ELSE CELLS CODE + @ THEN ELSE
      DUP CELLS DKIND + @ K-COLON = IF CELLS DVAL + @ RECURSE ELSE CELLS DVAL + @ EXECUTE THEN
    THEN THEN
  0 UNTIL ;
\ the mini system's words: primitives on its own stack, and the compiler's immediates
: P+ MPOP MPOP + MPUSH ;   : P- MPOP MPOP SWAP - MPUSH ;   : P* MPOP MPOP * MPUSH ;
: PDUP MPOP DUP MPUSH MPUSH ;   : PDROP MPOP DROP ;   : PSWAP MPOP MPOP SWAP MPUSH MPUSH ;
: PROT MPOP MPOP MPOP SWAP MPUSH SWAP MPUSH MPUSH ;   : P. MPOP OUT ;
: P; T-EXIT ,T 0 STATE? ! ;   : PIF T-BRZ ,T CHERE @ 0 ,T ;   : PTHEN CHERE @ SWAP CELLS CODE + ! ;
: DEFINE ( -- ) NEXT-WORD K-COLON CHERE @ ADD-NAME  -1 STATE? ! ;
: DO-WORD ( c-addr u -- )
  DUP 1 = IF OVER C@ 58 = IF 2DROP DEFINE EXIT THEN THEN
  2DUP LOOKUP DUP 0< 0= IF >R 2DROP R>
    DUP CELLS DKIND + @ K-IMM = IF CELLS DVAL + @ EXECUTE EXIT THEN
    STATE? @ IF ,T EXIT THEN
    DUP CELLS DKIND + @ K-COLON = IF CELLS DVAL + @ RUN-LIST ELSE CELLS DVAL + @ EXECUTE THEN EXIT
  THEN DROP
  NUMBER? IF STATE? @ IF T-LIT ,T ,T ELSE MPUSH THEN EXIT THEN
  DROP -13 THROW ;
: INTERPRET-LINE ( c-addr u -- ) DUP SLEN ! SRC SWAP CMOVE 0 SPOS !
  BEGIN NEXT-WORD DUP WHILE DO-WORD REPEAT 2DROP ;
VARIABLE ERRS
: LINE ( c-addr u -- ) ['] INTERPRET-LINE CATCH IF 2DROP 1 ERRS +! 0 STATE? ! THEN ;
: SETUP ( -- ) 0 NDEF ! 0 NHERE ! 0 CHERE ! 0 MSP ! 0 STATE? !
  S" +" K-PRIM ['] P+ ADD-NAME   S" -" K-PRIM ['] P- ADD-NAME   S" *" K-PRIM ['] P* ADD-NAME
  S" DUP" K-PRIM ['] PDUP ADD-NAME   S" DROP" K-PRIM ['] PDROP ADD-NAME   S" SWAP" K-PRIM ['] PSWAP ADD-NAME
  S" ROT" K-PRIM ['] PROT ADD-NAME   S" ." K-PRIM ['] P. ADD-NAME
  S" ;" K-IMM ['] P; ADD-NAME   S" IF" K-IMM ['] PIF ADD-NAME   S" THEN" K-IMM ['] PTHEN ADD-NAME ;
: PROGRAM ( -- )
  S" : SQ DUP * ;" LINE
  S" : DOWN DUP IF DUP SQ ROT + SWAP 1 - DOWN THEN ;" LINE
  S" 0 40 DOWN DROP ." LINE
  S" : TRI DUP IF DUP 1 - TRI + THEN ;" LINE
  S" 100 TRI . 7 TRI 3 * ." LINE
  S" 1 2 FROB ." LINE
  S" -12 5 * 3 - ." LINE ;
: BENCH ( n -- ) 0 CHECK ! 0 ERRS !  0 DO SETUP PROGRAM LOOP
  ." MINIF CHECK " CHECK @ .  ." ERRS " ERRS @ .  ." DEFS " NDEF @ . CR ;
