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
