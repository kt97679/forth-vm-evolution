# The next genes - where the dispatches go now (Iteration 323)

Seed 54 runs the after-seed-52 genes; if it is small, the stopping rule ends them until new
genes exist. This is the search for those.

## The interpreted designs - lab/evolve/price.py on seed 53's three fastest

ccf55ad2f5, b926dd6bc8, b38afcd676 (0.343-0.355 of s6's time; the JIT designs 0.13-0.15), their
dispatch streams on the selection workloads, after their own fusions:

| workload | calls | EXIT | calls + EXIT | next 16 pairs (overstated) |
|---|---|---|---|---|
| kernel | 17-19% | 7-10% | 25-29% | 8-11% |
| fib | 11% | 11-12% | 22-24% | 12-21% |
| corpus | 12-14% | 8-9% | 21-23% | 16-19% |
| bubble | 16-19% | 10-16% | 29-32% | 7-8% |
| ackermann | 27-29% | 8% | 35-37% | 0.1% |
| loop | 0% | 0% | 0% | 60-100% |

Triples negligible (the best 0.3%). Calls and returns are the largest share - as missmap found
for mispredictions (15-25%) - but the genes for them exist: folds (prim;EXIT for 23 primitives),
tail, hotinl, factor, opinline, rtempty. Pairs: price.py's own record - nine of the next 16,
given slots, removed 0.2-2.4% in practice; the estimate's overlap overstates it. Two of the
three fastest fuse no pairs at all, the fastest 13: the evolution weighs them already. The
interpreted designs' dispatch-level levers are mostly in the genes now.

## The JIT designs - what the JIT leaves to the interpreter (next)

The speed frontier is the JIT's (0.13-0.15 of s6's time). The JIT translates a word only whole -
an operation without a stencil leaves the word interpreted - and kernel and corpus (compiling,
parsing, FIND) may run much of their time so. No tool counts it: **jitleft.py**, to build - a
JIT design with the profiler (as hotwords.py, the JIT on): the dispatches left are exactly what
the JIT did not translate; by word, and for each hot word the operation that kept it out. New
stencils for those operations are genes. And bfind's effect on the laptop's predictor (missmap,
a design with and without it) can be a chain's first measurement.
