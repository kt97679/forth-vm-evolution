# Evolution on the Ryzen 7 PRO 8840HS - the first run

`python3 lab/evolve/evolve.py --pop 32 --gens 40 --rounds 3 --seed 1` on
the laptop ("fury"), then `--remeasure 6`. Measured: the engine process's
own CPU time over hand-made s6's, each timed run paired with one of s6,
best of three rounds, geometric mean over kernel, fib, parse and corpus;
`loop` is held out. Evolver at 9dbfd86 - before 679e6f3, so with the bug
that recorded 34 designs dead that would have converted (below).

1,306 designs, 1,135 alive.

## The front, measured again

| design | in the run | re-measured (6 rounds) | size | loop (held out) |
|---|---|---|---|---|
| 38d187239c | 0.630 | **0.609** | 13,480 | 0.795 |
| 5b70f3dd64 | 0.671 | **0.649** | 9,801 | 0.739 |
| 83cb81c383 | 0.694 | **0.705** | 9,761 | 0.843 |
| 448ef1ef43 | 0.590 | 0.620 | 13,488 | 0.762 |
| a4e82e02e5 | 0.668 | 0.654 | 9,809 | 0.736 |
| 53ec9bedde | 0.662 | 0.670 | 13,464 | 0.755 |

Measured again, the first three are the front; the run's own leader,
448ef1ef43, went from 0.590 to 0.620 (the winner's curse) and is
dominated. Hand-made s6 is 10,065 bytes: 5b70f3dd64 takes 35% less CPU
time at 3% less size; 38d187239c 39% less at a third more.

All six have the escape (rare primitives behind one byte), multi-state
stack caching, 11-13 of relf's format-10 opcodes, 21-23 superinstructions,
-fcf-protection=none (nocet), and almost all guard pages for the stack
checks. 38d187239c calls in 8-byte units (scale 3) without byte headers,
like s5; the small ones keep s6's byte headers and byte-granular calls.

## The hand-made stages, here

| s0-cell | s1-sod16 | s2-cpt16 | s3-cpt16f | s4-cv8 | s5-cv8spec | s6-cv8b |
|---|---|---|---|---|---|---|
| 1.247 | 1.569 | 1.228 | 1.181 | 1.166 | 0.942 | 1.000 |

## Two searches, one answer

The VM rehearsal (lab/evolve/REHEARSAL.md) selected on another machine.
Its front, re-measured here: best 57a9dcc7cb at 0.605 and 13,480 bytes;
this run's best, 38d187239c, 0.609 at 13,480 bytes. Both found the same
kind of design - escape, multi-state caching, format-10 opcodes, about 22
pairs - at the same level: about 39-40% less CPU time than s6 on the
Ryzen. That is the gene pool's reach, as far as these two runs can tell.

## Deaths

99 kernel workload, 30 timed out, 6 corpus - the reach limit, as in the
rehearsal (byte-granular calls without the three-byte form, or near DOES>
calls). 1 cpt16 alignment refusal. And two bugs, fixed in 679e6f3: 34
"--bytehdr requires --v8 --cpt 0" - the evolver built the raw genome but
recorded the death under the canonical identity, a design that converts
(it also poisoned that identity for later children, so the small end of
this front explored less than it could); 1 "superinstruction table
overflows" - more than 24 pairs with run-time fusion.
