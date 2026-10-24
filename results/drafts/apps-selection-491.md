# The applications in the selection - priced, a draft for the owner (Iteration 491)

The question open since 468: the selection's six workloads are kernels, and what the JIT work of 472-490 bought on real
programs the search could not see - jitexec and jitcfa were enabled knowing the selection pays neither for nor against
them. Priced here: one short pass of each of our own four applications (lab/evolve/apps/ - sim16 once, gc16 1000 steps,
scan 12 builds, evo 60 generations), each checking itself, as one workload. CPU time, median of five, master as seed 70
runs it (the after-seed-70 batch not applied):

| design | time | over s6 |
|---|---|---|
| s6 | 0.299 s | 1 |
| seed 68's fast design (0.140 on the six) | 0.171 s | 0.573 |
| the same with jitmul, jitdoes, jitexec, jitcfa | 0.058 s | **0.193** |

The four genes make a threefold difference on it - a difference the six workloads do not register. Every output the
same on all three. Sized for the selection (the six are ~11 ms on the fastest designs) the pass shrinks to sim16 once,
gc16 300 steps, scan 4, evo 20 (about 0.06 s on s6).

**The draft** (apps-selection-491.patch, against 0b52e1b's evolve.py): `apps` the seventh selection workload - APPS_IN
the four files INCLUDED with their counts; the speed objective's geometric mean then over seven. Not applied, not
batch-checked: it changes what the search optimises, so the speed column breaks at it; tools that print one column per
workload (the report, remeasure, the gate's tables) will need a look before it runs. **The owner's decision**: whether,
and whether with weight one of seven or more.
