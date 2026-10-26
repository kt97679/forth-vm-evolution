# Where the fast end's offset comes from (Iteration 550)

The front measured again after a run comes out slower than in it - the fastest tenth by 6.6% in seed 74 (rule 3:
1.066; seed 73: 1.070). Seed 74's clock test ruled out the clock: the offset held in every condition while the core's
clock moved between about 2,000 and 4,600 MHz. From seed 74's records and its re-measurement (remeasure.json: the front's
88 fastest, 6 rounds, one design at a time) - results/drafts/fast-end-offset-550.py:

1. **Not luck.** The run's two readings of a gated design agree: the second against the first 1.001 (quartiles
   0.993-1.009, 1,226 designs), a reading's noise about 0.9% - too little for a 7% winner's curse. And the offset is
   tight where it is large: the fastest ten 1.081 (quartiles 1.065-1.085).
2. **The JIT designs.** Re-measured against in-run: 1.070 for the 22 JIT designs, 1.012 for the 66 without; by in-run
   rank 1.081, 1.055, 1.022 and 0.992, from the fastest ten down - the JIT designs are the fast end.
3. **Some workloads more than others.** For the JIT designs: bubble 1.170, sieve 1.115, ackermann 1.065, kernel 1.063,
   loop 1.062, fib 1.036, corpus 1.026, parse 1.021, apps 1.018. Every ratio is design against s6 from runs seconds
   apart, so what differs between the run and after it is the two designs' speed relative to each other.
4. **The run's load, most likely.** In the run four workers measure at once beside their builds; after it, one design
   at a time. The clock test's co-runners took the ratio part of the way: its fastest eight against the run 1.079
   alone, 1.056 beside three compiles, 1.039 beside three benchmarks. The hand-made s6 interprets its code and may lose
   more to shared caches under load than a JIT design's machine code does - which makes the JIT designs look faster in
   the run.

The test that would decide: the front measured again with four designs at once, as the run measures, against one at a
time - if the ratio comes back to about 1.00, the load is the cause (evolve.py's --remeasure measures one at a time; a
--jobs for it is a small change). Meanwhile: the in-run speed flatters the JIT designs by about 6%. Within a run every
design is measured so, and the fronts stand; across machines the JIT designs' lead shrinks too
(results/drafts/xcheck-agreement-546.md: here / laptop 1.63 for them, 1.45 for the rest). For the article, the fast
end's speeds are the re-measured ones; and rule 3's ATTENTION reads this - not a failing gate - its "0.98-1.05 works"
written before the JIT designs led the front.
