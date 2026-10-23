\ sim16.fth - a 16-bit stack-CPU simulator, its own structured assembler, and two programs run on the CPU it
\ simulates (Iteration 469). Written for this project from scratch: an application workload of the kind Appbench's
\ cd16sim is (a CPU simulated in Forth, checking its own result), not a copy of it. Core words only, upper case.
\ The CPU: 4096 16-bit words of memory; data and return stacks of 64 entries; one instruction a word - the top four
\ bits its operation, the low twelve an address, a literal or an ALU function.

DECIMAL
CREATE MEM 4096 CELLS ALLOT
: M@ ( a -- x ) 4095 AND CELLS MEM + @ ;
: M! ( x a -- ) SWAP 65535 AND SWAP 4095 AND CELLS MEM + ! ;
CREATE DSTK 64 CELLS ALLOT   VARIABLE DSP
CREATE RSTK 64 CELLS ALLOT   VARIABLE RSP
VARIABLE PC   VARIABLE STEPS   VARIABLE RUNNING
: DPUSH ( x -- ) 65535 AND DSP @ 63 AND CELLS DSTK + !  1 DSP +! ;
: DPOP ( -- x ) -1 DSP +!  DSP @ 63 AND CELLS DSTK + @ ;
: RPUSH ( x -- ) RSP @ 63 AND CELLS RSTK + !  1 RSP +! ;
: RPOP ( -- x ) -1 RSP +!  RSP @ 63 AND CELLS RSTK + @ ;
: SIGNED ( u -- n ) DUP 32767 > IF 65536 - THEN ;
: FLAG ( f -- x ) IF 65535 ELSE 0 THEN ;

\ the ALU's sixteen functions - a table of execution tokens
CREATE ALU 16 CELLS ALLOT
: ALU: ( n "name" -- ) >R ' R> CELLS ALU + ! ;
: A-ADD   DPOP DPOP + DPUSH ;            : A-SUB   DPOP DPOP SWAP - DPUSH ;
: A-AND   DPOP DPOP AND DPUSH ;          : A-OR    DPOP DPOP OR DPUSH ;
: A-XOR   DPOP DPOP XOR DPUSH ;          : A-SHL   DPOP 1 LSHIFT DPUSH ;
: A-SHR   DPOP 1 RSHIFT DPUSH ;          : A-DUP   DPOP DUP DPUSH DPUSH ;
: A-DROP  DPOP DROP ;                    : A-SWAP  DPOP DPOP SWAP DPUSH DPUSH ;
: A-OVER  DPOP DPOP DUP DPUSH SWAP DPUSH DPUSH ;
: A-LT    DPOP SIGNED DPOP SIGNED SWAP < FLAG DPUSH ;
: A-EQ    DPOP DPOP = FLAG DPUSH ;       : A-LOAD  DPOP M@ DPUSH ;
: A-STORE DPOP DPOP SWAP M! ;            : A-RET   RPOP PC ! ;
0 ALU: A-ADD   1 ALU: A-SUB   2 ALU: A-AND   3 ALU: A-OR    4 ALU: A-XOR   5 ALU: A-SHL   6 ALU: A-SHR   7 ALU: A-DUP
8 ALU: A-DROP  9 ALU: A-SWAP 10 ALU: A-OVER 11 ALU: A-LT   12 ALU: A-EQ   13 ALU: A-LOAD 14 ALU: A-STORE 15 ALU: A-RET

\ the sixteen operations - another table, the unused ones a halt that says so
CREATE OPS 16 CELLS ALLOT
: OP: ( n "name" -- ) >R ' R> CELLS OPS + ! ;
: O-LIT  ( arg -- ) DPUSH ;              : O-JMP  ( arg -- ) PC ! ;
: O-JZ   ( arg -- ) DPOP 0= IF PC ! ELSE DROP THEN ;
: O-CALL ( arg -- ) PC @ RPUSH PC ! ;
: O-ALU  ( arg -- ) 15 AND CELLS ALU + @ EXECUTE ;
: O-HALT ( arg -- ) DROP 0 RUNNING ! ;
: O-INC  ( arg -- ) DPOP + DPUSH ;
: O-BAD  ( arg -- ) DROP ." BAD INSTRUCTION AT " PC @ 1- . CR 0 RUNNING ! ;
: OPS-INIT 16 0 DO ['] O-BAD I CELLS OPS + ! LOOP ;
OPS-INIT
0 OP: O-LIT  1 OP: O-JMP  2 OP: O-JZ  3 OP: O-CALL  4 OP: O-ALU  5 OP: O-HALT  6 OP: O-INC

: STEP ( -- ) PC @ M@  1 PC +!  1 STEPS +!  DUP 4095 AND SWAP 12 RSHIFT CELLS OPS + @ EXECUTE ;
: RUN ( a -- ) PC !  0 DSP !  0 RSP !  1 RUNNING !  BEGIN STEP RUNNING @ 0= UNTIL ;

\ the assembler: words that lay instructions down at HERE16, its control structures as Forth's own
VARIABLE HERE16
: ORG ( a -- ) HERE16 ! ;
: LABEL ( -- a ) HERE16 @ ;
: INSN ( arg op -- ) 12 LSHIFT SWAP 4095 AND OR  HERE16 @ M!  1 HERE16 +! ;
: LIT, ( n -- ) 0 INSN ;       : CALL, ( a -- ) 3 INSN ;     : INC, ( n -- ) 6 INSN ;    : HALT, 0 5 INSN ;
: ALU, ( f -- ) 4 INSN ;
: ADD, 0 ALU, ;   : SUB, 1 ALU, ;   : AND, 2 ALU, ;   : OR, 3 ALU, ;    : XOR, 4 ALU, ;   : SHL, 5 ALU, ;
: SHR, 6 ALU, ;   : DUP, 7 ALU, ;   : DROP, 8 ALU, ;  : SWAP, 9 ALU, ;  : OVER, 10 ALU, ; : LT, 11 ALU, ;
: EQ, 12 ALU, ;   : LOAD, 13 ALU, ; : STORE, 14 ALU, ; : RET, 15 ALU, ;
: IF, ( -- patch ) HERE16 @  0 2 INSN ;                       \ jump if zero, its target set by THEN,
: THEN, ( patch -- ) DUP M@ HERE16 @ 4095 AND OR SWAP M! ;
: BEGIN, ( -- a ) HERE16 @ ;
: UNTIL, ( a -- ) 2 INSN ;                                    \ back while zero
: AGAIN, ( a -- ) 1 INSN ;
: WHILE, ( a -- patch a ) IF, SWAP ;
: REPEAT, ( patch a -- ) AGAIN, THEN, ;

\ program 1: the sieve of Eratosthenes on 2000 flags at 2048 - the primes below 2000, counted.
\ Its variables in memory: I at 100, J at 101, the count at 102.
2048 CONSTANT FLAGS   2000 CONSTANT LIMIT
256 ORG LABEL CONSTANT SIEVE
  0 LIT, 100 LIT, STORE,
  BEGIN,  1 LIT, 100 LIT, LOAD, FLAGS LIT, ADD, STORE,
          100 LIT, LOAD, 1 INC, DUP, 100 LIT, STORE,  LIMIT LIT, LT, 0 LIT, EQ,  UNTIL,
  0 LIT, 102 LIT, STORE,   2 LIT, 100 LIT, STORE,
  BEGIN,
    100 LIT, LOAD, FLAGS LIT, ADD, LOAD,
    IF,
      102 LIT, LOAD, 1 INC, 102 LIT, STORE,
      100 LIT, LOAD, DUP, ADD, 101 LIT, STORE,
      BEGIN,  101 LIT, LOAD, LIMIT LIT, LT,  WHILE,
        0 LIT, 101 LIT, LOAD, FLAGS LIT, ADD, STORE,
        101 LIT, LOAD, 100 LIT, LOAD, ADD, 101 LIT, STORE,
      REPEAT,
    THEN,
    100 LIT, LOAD, 1 INC, DUP, 100 LIT, STORE,  LIMIT LIT, LT, 0 LIT, EQ,
  UNTIL,
  102 LIT, LOAD,  HALT,

\ program 2: fib(n), recursive, by CALL and RET - fib(20), and a checksum of its calls' results folded by XOR
512 ORG LABEL CONSTANT FIB                                     \ ( n -- fib n )
  DUP, 2 LIT, LT, IF, RET, THEN,
  DUP, 1 LIT, SUB, FIB CALL,   SWAP, 2 LIT, SUB, FIB CALL,   ADD, RET,
600 ORG LABEL CONSTANT FIBMAIN
  20 LIT, FIB CALL,  HALT,

: SIEVE-RUN ( -- n ) SIEVE RUN DPOP ;
: FIB-RUN ( -- n ) FIBMAIN RUN DPOP ;
: BENCH ( n -- ) 0 STEPS !  0 DO SIEVE-RUN DROP FIB-RUN DROP LOOP
  ." SIM16 SIEVE " SIEVE-RUN .  ." FIB " FIB-RUN .  ." STEPS " STEPS @ . CR ;
