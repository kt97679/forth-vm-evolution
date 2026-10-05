# Tests that keep their value: DUP ?BRANCH and OVER ?BRANCH

Iteration 33 - the first opcodes from the register machine's first-stage
price (results/price-register-stage1.md). `DUP ?BRANCH` and `OVER ?BRANCH`
as format-10 opcodes, long and short, jumping where the pair would and
popping nothing: tools/sod16.py's TESTBR, engine/vm-lab.c (only under
X_DUPBR / X_OVERBR), tools/gen-tos.py and gen-msc.py, and the gene
(lab/evolve/evolve.py, OPS10_POOL) - so the evolver weighs them against
the pairs whose slots they take. Designs without them are unchanged: the
hand-made stages IDENTICAL, and seed 5's 8dc0f97f2c converts to the same
image with the old converter and the new.

## Measured: image against image, one engine (development VM)

`lab/evolve/image-ab.py 8dc0f97f2c --set ops10=<its 29 + the 4 new>
--env SOD16_TESTBR_SKIP=DUP,OVER --rounds 10`: both images on the engine
that has the opcodes - A with the fusion declined, B as the converter
stands; dispatches counted on a profiling engine (exact), time the median
of 10 rounds, back to back.

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 8dc0f97f2c | 9466 | 9458 | -8 | 0.982, 1.000, 0.968, 0.972, 1.000 | 0.988, 0.996, 0.974, 0.963, 0.997 | 0.980 |

**2-3% fewer dispatches, 8 bytes, about 2% faster on selection** - all of
what the two opcodes can reach: run with the branch kinds kept apart,
regprice.py splits its "DUP | ?BRANCH" (5.8-6.2%) into `DUP 0= ?BRANCH`
3.4-4.3% and plain `DUP ?BRANCH` 1.5-2.8%. The larger part, and `SWAP
addi` (3.7-5.0%), are next.

## Iteration 34: DUP 0= ?BRANCH kept, and SWAP n +

`DUP?NBRANCH` (long and short: DUP before the fused 0= ?BRANCH - jumps
when the top is NOT zero, keeping it) and `SWAP+I` (( a b -- b a+n ), ADDI's
immediate byte) - converter (keepbranch, after the pairs, as the price
was taken), engine (only under X_DUPNBR / X_SWAPADDI), both generators,
the gene. Designs without them unchanged: stages IDENTICAL; 8dc0f97f2c,
as recorded and with Iteration 33's four, the same images from the old
converter and the new.

On 8dc0f97f2c with all 36 opcode words in its slots, image against image:

All seven new opcodes, fused or declined (SOD16_TESTBR_SKIP=DUP,OVER,DUPN,SADDI):

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 8dc0f97f2c | 9490 | 9450 | -40 | 0.905, 1.000, 0.902, 0.900, 1.000 | 0.942, 1.018, 0.907, 0.942, 0.997 | 0.951 |

Iteration 34's two alone (Iteration 33's on both sides; SKIP=DUPN,SADDI):

pinned to cpu 0 (it and its sibling 0% busy; BENCH_CPU=N to choose)
| design | size A | size B | B - A | dispatches B / A: kernel, fib, parse, corpus, loop | time B / A: kernel, fib, parse, corpus, loop | selection |
|---|---|---|---|---|---|---|
| 8dc0f97f2c | 9458 | 9450 | -8 | 0.922, 1.000, 0.931, 0.925, 1.000 | 0.959, 1.040, 0.969, 0.964, 1.010 | 0.982 |

**About 10% fewer dispatches on kernel, parse and corpus - the 10-12% the
price promised - 40 bytes, and selection 0.951 on the VM.** fib's and
loop's dispatches do not move (their hot code is compiled at run time), so
their time ratios are this machine's noise.

**Against the pairs they displace**: the seven take seven of the 14 slots
the design's pairs had (OVER C@, C@ =, C@ DUP, SWAP R>, LSHIFT OVER, OVER R>,
ROT ROT). Dispatches counted on profiling engines, the design as recorded
against it with the seven: kernel 0.932, parse 0.937, corpus 0.934; fib
and loop 1.000; 8 bytes smaller. The opcodes beat the pairs they take the
slots of - which is for a seed run to weigh, design by design.
