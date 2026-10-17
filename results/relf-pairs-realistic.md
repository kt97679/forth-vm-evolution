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

## The budget - all five shell scripts counted together (tools/relf-pairs.py --all; Iteration 359)

```
the adjacent pairs run most (the first not transferring control) - fusion candidates:
     3,191,566    4.5 %  VAR@ VAR@
     2,041,322    2.8 %  VAR@ +
     1,660,097    2.3 %  0= ?BRANCH
     1,109,323    1.5 %  + @
       902,529    1.3 %  VAR! VAR@
       886,586    1.2 %  VAR@ <
       876,494    1.2 %  push0 VAR!
       862,135    1.2 %  CELLS +
       777,516    1.1 %  < ?BRANCH
       766,156    1.1 %  EQI ?BRANCH
       763,564    1.1 %  @ EXIT
       658,564    0.9 %  + C@
       624,631    0.9 %  VAR@ C@
       606,802    0.8 %  DUP EQI
       582,723    0.8 %  + VAR@
       543,029    0.8 %  VAR@ ?BRANCH
       491,137    0.7 %  VAR@ 1+
       451,237    0.6 %  VAR! push0
       444,259    0.6 %  LIT8 CALL
       398,861    0.6 %  VAR@ CELLS
       359,982    0.5 %  + C!
       359,192    0.5 %  > ?BRANCH
       357,717    0.5 %  push1 CALL
       354,519    0.5 %  C@ LIT8
       350,441    0.5 %  DUP VAR@

the 64 one-byte operations, the coldest first (ESC, DOVAR, DODOES and NOOP kept - see above):
  LIT64 20,127, ?BRANCH8 25,883, R@ 93,799, 0< 101,784, SP@ 112,305, LIT 116,047, LZERO 124,052, U< 130,665, (?DO) 131,062, 1- 133,354, COUNT 155,363, = 163,517, LIT32 182,760, UM* 186,054, XOR 207,378, @XT 231,823

the budget: each candidate pair displacing the next coldest one-byte operation into the escape band
   1  VAR@ VAR@               4.45 %  displaces LIT64        0.028 %  net  4.42 %  together  4.42 %
   2  VAR@ +                  2.85 %  displaces ?BRANCH8     0.036 %  net  2.81 %  together  7.23 %
   3  0= ?BRANCH              2.31 %  displaces R@           0.131 %  net  2.18 %  together  9.42 %
   4  + @                     1.55 %  displaces 0<           0.142 %  net  1.40 %  together 10.82 %
   5  VAR! VAR@               1.26 %  displaces SP@          0.157 %  net  1.10 %  together 11.92 %
   6  VAR@ <                  1.24 %  displaces LIT          0.162 %  net  1.07 %  together 13.00 %
   7  push0 VAR!              1.22 %  displaces LZERO        0.173 %  net  1.05 %  together 14.05 %
   8  CELLS +                 1.20 %  displaces U<           0.182 %  net  1.02 %  together 15.07 %
   9  < ?BRANCH               1.08 %  displaces (?DO)        0.183 %  net  0.90 %  together 15.97 %
  10  EQI ?BRANCH             1.07 %  displaces 1-           0.186 %  net  0.88 %  together 16.85 %
  11  @ EXIT                  1.06 %  displaces COUNT        0.217 %  net  0.85 %  together 17.70 %
  12  + C@                    0.92 %  displaces =            0.228 %  net  0.69 %  together 18.39 %
```

Not displaced: ESC; DOVAR and DODOES - the code fields of data words, run each time a variable or a
CREATE'd word is, but in no code body, so not counted here; NOOP, the alignment pad. **The top three
net about 9.4 % of the dispatches** (VAR@ VAR@ against LIT64, VAR@ + against ?BRANCH8, 0= ?BRANCH
against R@) - less where chains overlap (VAR@ VAR@ VAR@). In time a few per cent of the shell's work:
a fused instruction saves its pair's second dispatch, not its work, and the shell's scripts spend time
in the system too - the laptop's to measure (this VM's noise floor is about 10 %).
