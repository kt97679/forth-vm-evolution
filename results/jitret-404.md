# The gene jitret: the JIT's EXIT as a pop and an indirect jump (Iteration 404)

HANDOFF item 4's return candidate, the owner: "let's try it". The JIT's native words call each other with call and
ret (engine/jit.c). A ret is predicted by the return predictor, a stack of the last 32 or so calls; recursion deeper
than that mispredicts every return beyond it - the JIT's ackermann nests past 250 (Iteration 294's reading of jit.c).
An indirect jmp is predicted as any jump is, by the history of its targets.

**The gene** (results/pending/jitret-after-seed62.patch, patch 8 of the after-seed-62 batch): with jitret, EXIT's
stencil - mov, mov, ret: the state handed back in rax and rdx - is copied with its ret made `pop %rcx; jmp *%rcx`.
rcx is free at a return: no result is in it, and no caller keeps anything in it across a call. The same address and
the same stack pointer as ret, so correct wherever ret is; x86-64 only, as the JIT. Off by default; the search weighs it.

**Measured here** (this VM: an Intel Xeon at 2.8 GHz, enhanced IBRS; one CPU, so a rough reading - the laptop's Zen 4
predicts otherwise): engines-check's JIT design with jitret 0 and 1, each built, alive on the corpus and the kernel
workload, their engines not the same; then evolve.measure on the six selection workloads, 7 rounds, against s6 run
beside it (results/drafts/jitret-404.py):

| workload | jitret 0 | jitret 1 | change |
|---|---|---|---|
| ackermann | 0.464 | 0.343 | -26% |
| fib | 0.329 | 0.329 | 0% |
| bubble | 0.947 | 1.032 | +9% |
| loop | 1.149 | 1.213 | +6% |
| corpus | 1.272 | 1.232 | -3% |
| kernel | 1.049 | 1.077 | +3% |

Their geometric mean: about 3% faster. Ackermann, the deep recursion, gains as the reading predicted (its own median
8.2 ms to 5.3 ms); fib, whose depth stays within the predictor, is unchanged; bubble and loop lose 6-9% - noise on one
CPU, or shallow returns that ret predicted perfectly and the jump does not. A trade-off, so a gene: whether the fronts
keep it shows from seed 63, on the laptop's predictors.

batch-check, the eight: PASS - 8 patches on a fresh clone of c397f25: run-tests PASS (engines-check 84 paths), validate 7 of 7 IDENTICAL, jail PASS.
