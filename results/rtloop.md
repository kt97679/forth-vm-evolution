# Loops compiled at run time with the image's own opcodes: the gene `rtloop`

Iteration 41, the owner's call: speed up loops, and put the loop benchmark
in the selection.

## What run-time loops were

The converter turns the image's own loop words into format-10 opcodes;
the compiler the image carries did not. loop.fth's INNER (`1000 0 DO DUP
I + XOR LOOP`), compiled by seed 7's 3c2d8a577b:

```
before:  82 b6        call (DO)
         06 82 da     DUP, call I (its colon body: an entry, three, an exit)
         17 10        + XOR
         00 x 7       seven NOOPs - padding the (LOOP) operand to a cell,
                      executed on every pass (Iteration 13)
         83 14 f2 ..  far call (LOOP), then an 8-byte operand
with rtloop:
         7e           (DO) opcode
         06 82 da     DUP, call I (not an opcode in this design)
         17 10        + XOR
         7f fa ff     (LOOP) opcode, back 6
```

## How

`forth/cv8-fuse-loop.4`, loaded for designs with the gene: DO LOOP +LOOP
?DO LEAVE emit this design's opcodes with 16-bit operands - no alignment,
no padding - and COMPILE, turns I, J and UNLOOP into theirs (their image
offsets, with a two-compare range check, in a table the converter writes).
**Each word on its own**: evolution keeps only some loop opcodes (no
design on seed 7's front has all five; 39 of its 1,207 living do), so a
word without one keeps the old form - a frame one form builds the other
reads, as the image's own code mixes them. The pending ?DO / LEAVE operands
chain in 16 bits only where both are opcodes, else both keep the cell
chain, and LOOP resolves whichever it is. A word without its opcode defers
to the one it replaces.

The deferral needed the converter's lean to change: it sent every call or
(POSTPONE) of any X8 to its X - which made the new ?DO8's deferral call
itself (a return-stack overflow on the first ?DO). Now a later X8 - or its
X - reaching an earlier X8 OF ITS OWN NAME keeps it; everything else goes
to X as before. POSTPONE of an immediate word compiles (POSTPONE) and an
xt, not a call, so both count. Seed 7's whole front converts byte for byte
as recorded.

## Checks

On seed 7's 3c2d8a577b and f060a4c31f with the gene (the second without
(LEAVE): the cell chain): alive (the corpus, the kernel's rebuild); nested
DO LOOP with I and J, -2 +LOOP, a ?DO of no passes, LEAVE, UNLOOP EXIT, a
LEAVE in a nested ?DO - the recorded designs' answers. All 14 overlay dumps
load cleanly; hand-made stages IDENTICAL; tests PASS.

## Measured: image against image, one engine (development VM)

`lab/evolve/image-ab.py 49b0a93f14 f060a4c31f 3c2d8a577b 3a7c3d6e90 --db
<seed 7's> --set rtloop=1 --env SOD16_NO_RTLOOP=1 --rounds 5` (the table's
"selection" is still the four workloads of before):

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 49b0a93f14 | 8566 | 8566 | +0 | 0.999, 1.000, 1.000, 0.987, 0.204 | 0.990, 1.002, 1.003, 1.046, 0.268 | 1.010 |
| f060a4c31f | 8834 | 8834 | +0 | 0.999, 1.000, 1.000, 0.988, 0.431 | 1.153, 0.990, 0.978, 1.089, 0.490 | 1.050 |
| 3c2d8a577b | 8854 | 8854 | +0 | 0.999, 1.000, 1.000, 0.989, 0.363 | 0.945, 1.113, 1.012, 1.030, 0.404 | 1.024 |
| 3a7c3d6e90 | 12409 | 12409 | +0 | 0.999, 1.000, 1.000, 0.986, 0.221 | 0.985, 0.992, 0.977, 0.977, 0.298 | 0.983 |

**loop: 57-80% fewer dispatches, 2-4x faster** - most where I and J are
opcodes too (49b0a93f14, 3a7c3d6e90); the corpus 1.1-1.4% fewer
dispatches (its tests compile loops at run time); nothing else moves. The
bytes: 493-632 (about 6%) - the overlay, and the words it defers to.

## The selection

`lab/evolve/evolve.py`: WORK_SEL kernel, fib, parse, corpus, **loop**;
WORK_HELD **sieve** - a new held-out workload (`bench/sieve.fth`: the BYTE
sieve of 1981, 8190 flags, 1899 primes, 15 passes; memory and a BEGIN
WHILE REPEAT inner loop, which no selected workload leans on), so that
what evolution selects for is still checked on something it does not
see. Every design is timed on one workload more: a seed run about a fifth
longer. Speeds from Iteration 41 on are over five workloads; recorded
speeds of seeds 1-7, over four.
