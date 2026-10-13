# The cross-compiler's byte loops - a fast path, proposed (Iteration 255)

**A change to a selection workload, so the owner's to decide.** The kernel
workload compiles kernel.4 with forth/cross.4. Profiled on the fastest design
(3bb2087f9d) built without its JIT, 56% of its 1.73 million dispatches were in
words compiled at run time - cross.4's own - and most of that in @-T and !-T,
which move a target cell a byte at a time (~20 operations a byte, 8 bytes a
cell) so that any host can build any target.

`results/drafts/crossfast.patch`: when the target's cell is the host's (8 and 8)
and the host is little-endian, @-T and !-T use @ and ! - which lay the bytes
exactly as the loops do. Decided once, after TARGET-CELL-BYTES is set; a 4-byte
target keeps the loops. Checked: the reseed reaches the same fixed point (27,264
bytes) and the 4-byte kernel is identical - the seeds do not change; run-tests
PASS; 7 of 7 identical.

| | before | with the fast path |
|---|---|---|
| kernel workload, 3bb2087f9d without the JIT | 1,732,919 dispatches | 1,091,259 (-37%) |
| kernel workload, 3bb2087f9d with the JIT (VM, alternated, 15 rounds) | 2.8 ms | 2.5 ms (-9%) |

What it changes: the kernel workload becomes mostly the compiler's own work
(lookup, parsing, compiling) instead of a third byte loops. Because speed is
measured against s6, which is interpreted and gains the most, every design's
kernel ratio moves - the JIT designs' advantage there shrinks (they ran the
loops natively). Fair across runs (the comparison re-measures all on the same
code), but it reshapes one sixth of the speed objective. Also: every reseed
gets faster.
