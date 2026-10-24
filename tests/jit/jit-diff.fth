\ jit-diff.fth - what the JIT translates, run against the interpreter (Iteration 501; lab/evolve/engines-check.py).
\ Every word here is meant to be translated: arithmetic and its throw, EXECUTE and its cache, DOES> children, inline
\ strings, cold calls, (ABORT"), PICK, SP@, ALIGNED, CELL+ and CELLS (the 32-bit bug of 493), loops with LEAVE and ?DO,
\ the return stack balanced along branches (jitcfa), recursion. The output is compared with s6's at the same width.
DECIMAL
: SQ DUP * ;  : KONST CREATE , DOES> @ ;  5 KONST FIVE  : APPLY EXECUTE ;
CREATE TAB ' SQ , ' FIVE , ' DUP , 7 , 9 ,
: T1 3 TAB @ EXECUTE . TAB CELL+ @ EXECUTE . 6 TAB 2 CELLS + @ EXECUTE + . TAB 3 CELLS + @ TAB 4 CELLS + @ + . ;
: T2 0 100 0 DO I ['] SQ APPLY + LOOP . 0 50 0 DO I I 1 AND IF ['] SQ ELSE ['] 1+ THEN APPLY + LOOP . ;
: T3 47 5 / . -47 5 / . 47 -5 MOD . -47 -5 MOD . 1000 3 7 */ . 100 0 7 UM/MOD . . 5 6 UM* . . -7 2 /MOD . . ;
: DZ 1 0 / ;  : T4 ['] DZ CATCH . DEPTH . ;
: CHK DUP 0< ABORT" negative" 1+ ;  : T5 0 100 0 DO CHK LOOP . ;  : BAD -1 CHK ;  : T6 ['] BAD CATCH . ;
: GREET ." Hi" ;  : T7 3 0 DO GREET LOOP S" abc" TYPE SPACE S" " . DROP ;
: T8 1 2 3 4 2 PICK . 0 PICK . 3 PICK . 2DROP 2DROP 10 ALIGNED . 1 ALIGNED . SP@ SP@ - . ;
: T9 0 20 0 DO I 7 MOD 0= I 0> AND IF LEAVE THEN I + LOOP . 0 5 0 ?DO I + LOOP . 0 0 0 ?DO 1+ LOOP . ;
: EV ( n -- n ) DUP 3 * >R DUP 5 > IF R> 7 + >R THEN DUP 8 MOD 0= IF DROP R> EXIT THEN 2 * R> + ;
: T10 0 40 0 DO I EV + LOOP . 1 2 >R >R R@ R> R> + + . ;
: FIB DUP 2 < IF EXIT THEN DUP 1- FIB SWAP 2 - FIB + ;  : T11 20 FIB . ;
: T12 0 10 0 DO I 3 0 DO J I * + LOOP LOOP . 100 0 DO I CELLS DROP LOOP 6 CELLS 3 CELL+ + . ;
T1 CR T2 CR T3 CR T4 CR T5 CR T6 CR T7 CR T8 CR T9 CR T10 CR T11 CR T12 CR T1 CR T3 CR T10 CR
BYE
