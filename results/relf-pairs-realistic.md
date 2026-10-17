# relf's realistic shell script, by instruction and by adjacent pair (Iteration 358)

tools/relf-pairs.py at vendor/relf's commit (8ec0e75): relf's counting engine (its profile.py's), the
realistic script (tests/bench-vm/realistic.sh), the shell image decoded by its image-audit.py. 18,401,921
dispatches (relf's own profile: 18,401,777). A pair: two adjacent instructions of one word, the first
not transferring control (branch, call, EXIT, EXECUTE, the loop operations); counted as the less run.

```
ran: ./relfsh tests/bench-vm/realistic.sh (status 0); 18,401,921 dispatches in the shell image's code

the instructions run most:
     2,801,271   15.2 %  VAR@
     1,632,971    8.9 %  ?BRANCH
     1,114,240    6.1 %  CALL
     1,057,626    5.7 %  +
     1,050,945    5.7 %  EXIT
     1,006,408    5.5 %  DUP
       624,484    3.4 %  VAR!
       588,670    3.2 %  0=
       554,668    3.0 %  push0
       494,041    2.7 %  C@
       468,562    2.5 %  @
       421,712    2.3 %  LIT8
       355,763    1.9 %  CELLS
       355,623    1.9 %  SWAP
       355,117    1.9 %  DROP

the adjacent pairs run most (the first not transferring control) - fusion candidates:
       772,771    4.2 %  VAR@ VAR@
       573,230    3.1 %  VAR@ +
       414,504    2.3 %  0= ?BRANCH
       324,461    1.8 %  + @
       231,967    1.3 %  push0 VAR!
       219,708    1.2 %  CELLS +
       217,625    1.2 %  @ EXIT
       217,498    1.2 %  VAR! VAR@
       193,834    1.1 %  VAR@ <
       190,942    1.0 %  + C@
       181,033    1.0 %  EQI ?BRANCH
       176,762    1.0 %  < ?BRANCH
       151,134    0.8 %  + VAR@
       143,515    0.8 %  DUP EQI
       140,447    0.8 %  VAR@ ?BRANCH
       123,252    0.7 %  VAR! push0
       122,481    0.7 %  VAR@ C@
       116,609    0.6 %  VAR@ 1+
       114,467    0.6 %  LIT8 CALL
       111,113    0.6 %  ?DUP ?BRANCH
       109,621    0.6 %  SWAP DROP
       108,459    0.6 %  DUP C@
       104,618    0.6 %  DUP CALL
       102,985    0.6 %  VAR@ CELLS
       102,004    0.6 %  push1 CALL
```

## The constraint: 64 one-byte opcodes (relf's QUESTIONS.md A15)

relf gave up its fused pairs at its Iteration 536 - "about 8 % of dispatches were pairs when they
went" - to bring the one-byte opcodes to 64, the prerequisite of the two-bit tag (Q2/A6, this lab's
tag2): the owner chose "the smaller opcode set, but don't implement the 1 GB call range yet"; the
coldest primitives went to the escape band. So **a new fused instruction takes a one-byte slot from
an operation that then costs an extra dispatch wherever it runs** - and a fused pair in the escape
band saves nothing (its escape and selector are two dispatches, as the pair was). Each candidate's
worth is net: its pair's dispatches, less the displaced operation's. The top ten pairs above are
about 18 % of the dispatches (overlapping chains - VAR@ VAR@ VAR@ - count less), led by VAR@'s:
VAR@ VAR@ 4.2 %, VAR@ + 3.1 %, then 0= ?BRANCH 2.3 %, + @ 1.8 %.
