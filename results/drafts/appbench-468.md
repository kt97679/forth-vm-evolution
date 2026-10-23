# Applications held out - the tool, and a first reading: the speed does not travel (Iteration 468)

The owner (467-468): run more applications. lab/evolve/appbench.py makes it a step a chain can take after its run
(`then experiment appbench.py --zip PATH --sample 16`, with appbench.zip at PATH on the laptop): N designs across the
newest front built and run on fcp, brainless and cd16sim against s6, each design's output checked as the
application's own result, the CPU time of the whole run, Spearman between the in-run speed and the applications'
geometric mean. Its folding and prelude live in lab/evolve/appbench/ (results/drafts/appbench-467.md has the study).

## First reading - three of seed 68's front, here (one round, CPU time)

| design | in-run speed | fcp | brainless | cd16sim | geometric mean |
|---|---|---|---|---|---|
| b9c5b4ae74 (near its fastest) | 0.140 | 0.887 | 1.041 | 1.176 | 1.028 |
| 76bfbf6558 | 0.364 | 1.094 | 1.087 | 1.263 | 1.145 |
| 57a20bf148 (its smallest) | 1.605 | 1.700 | 1.696 | 1.837 | 1.743 |

All outputs right. The order holds (Spearman 1.000 over three) - **the size of the lead does not**: the design that
runs the selection's workloads in 0.140 of s6's time runs the applications in 1.03 of it. Not the loading: split for
two applications, the prelude and the program's compilation took 0.01-0.06 s of runs lasting 4-7 s -

| application | s6 | b9c5b4ae74 |
|---|---|---|
| fcp, its benchmark alone | 6.71 s | 5.87 s (13% faster) |
| brainless, its benchmark alone | 3.84 s | 4.45 s (16% slower) |

Three designs and one round on a one-core machine: a first look, not a verdict. It says what the held-out tier is for:
our six workloads are kernels - a few hot loops the JIT and the fusions take whole - and the applications are many
words, deep stacks, frequent calls, DOES>, deferred words, CATCH. What the evolved designs gain does not reach them.

## What it opens (the owner's calls)

1. **appbench.py in the chain** - the zip on the laptop at a fixed path; its reading at every processing beside sieve's.
2. **Why the lead vanishes**: the JIT's coverage on the applications (JITLOG names each word it refuses) - which words
   stay interpreted, and why.
3. **Applications in the selection itself** - the search would then be paid for general speed, not for six kernels; a
   change to what it optimises, so a decision, not a patch.
