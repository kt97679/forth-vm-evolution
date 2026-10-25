\ jit-marker.fth - after extend.4 and coreext.4 (Iteration 515; lab/evolve/engines-check.py): a word without the JIT
\ header (a CONSTANT) used by native code, the dictionary rolled back by MARKER, and a different CONSTANT made at the same
\ address - its translation must be its own (jit_k was keyed by the address alone: 5 came back for 7). And a user word
\ shaped like EXECUTE (>R EXIT) is EXECUTE in the interpreter too - the JIT's helper must run it the same.
MARKER M1  5 CONSTANT KK  : USE KK ;  USE .  ' KK EXECUTE .  : USE2 ['] KK EXECUTE ;  USE2 .
M1
MARKER M1  7 CONSTANT KK  : USE KK ;  USE .  ' KK EXECUTE .  : USE2 ['] KK EXECUTE ;  USE2 .
M1
MARKER M1  -1 CONSTANT KK  : USE KK 1+ ;  USE .
: MY-TOR >R ;  : TT 5 ['] DUP MY-TOR + . ;  TT
BYE
