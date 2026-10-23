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

## Iteration 469 - our own applications, written from scratch

The owner: for the programs that cannot be copied in, borrow the idea and write the code anew. Ideas and algorithms are
free to use; only a program's own text is someone's - so each is written independently, as a program of the same kind,
not a translation of theirs. **brainless needs none of this**: it is public domain and may be copied in as it is.

**The first: lab/evolve/apps/sim16.fth** - a CPU simulated in Forth, as cd16sim is, but a CPU of its own: a 16-bit
stack machine with sixteen operations and sixteen ALU functions dispatched through tables of execution tokens, a
structured assembler (IF, THEN, BEGIN, UNTIL, WHILE, REPEAT, laid into the simulated memory), and two programs in its
machine code - the sieve of Eratosthenes on 2000 flags and a recursive fib(20) by CALL and RET. Core words only, upper
case: no prelude, no folding. `60 BENCH` checks itself: SIEVE 303, FIB 6765, 21,936,820 simulated instructions - 3.3 s
on s6 here. appbench.py runs it by default and needs no zip for it. On three of seed 68's front, one round:

| design | in-run speed | sim16 | fcp |
|---|---|---|---|
| b9c5b4ae74 | 0.140 | 0.680 | 0.856 |
| 76bfbf6558 | 0.364 | 0.984 | 1.157 |
| 57a20bf148 | 1.605 | 1.346 | 1.664 |

The fast design's lead is larger on sim16 (1.5 times s6) than on the chess programs - still a fifth of what the
selection's workloads show. Next of the same kind, the owner's call: a collector over a heap of cells (benchgc's idea),
a scanner generator from regular expressions (lexex's), an evolution simulation (brew's).
