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

## Iteration 470 - three more of our own: a collector, a scanner generator, an evolution

The owner: all three. Each written from scratch for this project, core words only and upper case (no prelude, no
folding), each checking its own result; appbench.py runs all four of ours by default, no zip needed:

| application | the kind (whose idea) | what it does | its check | s6 here |
|---|---|---|---|---|
| sim16.fth | a CPU simulator (cd16sim) | a 16-bit stack CPU, its assembler, a sieve and fib in its code | SIEVE 303 FIB 6765 STEPS 21,936,820 | 3.3 s |
| gc16.fth | a garbage collector (benchgc) | 20,000 cons cells, mark and sweep, a mutator building and dropping random lists and trees, a GC-visible stack for building | GCS 618 FREED 7,454,729 CHECK 2636 | 2.8 s |
| scan.fth | a scanner generator (lexex) | 14 token patterns as postfix regular expressions - Thompson's NFA, the subset construction (sets as byte arrays), a longest-match scanner over 20 KB of generated program text | NFA 44 DFA 17 IDENT 1723 NUMBER 908 SPACE 5407 ERRS 0 CHECK 20235 | 2.9 s |
| evo.fth | an evolution (brew) | 64 genomes of 64 bytes toward a hidden target: popcount fitness, tournaments, one-point crossover, mutation, the fittest kept | BEST 445 AT 200 CHECK 24466 | 2.7 s |

Checksums are kept below 65,521 so a 32-bit build computes the same; the random numbers are a 31-bit LCG, the same at
either width. On three of seed 68's front, one round:

| design | in-run speed | sim16 | gc16 | scan | evo | geometric mean |
|---|---|---|---|---|---|---|
| b9c5b4ae74 | 0.140 | 0.595 | 0.461 | 0.627 | 0.596 | 0.566 |
| 76bfbf6558 | 0.364 | 1.028 | 0.728 | 0.743 | 0.594 | 0.758 |
| 57a20bf148 | 1.605 | 1.340 | 1.869 | 1.665 | 2.074 | 1.715 |

Every output right. Our own applications keep more of the fast design's lead (1.8 times s6) than Appbench's do (1.0) -
written in the plain style of our workloads, fewer DOES>, deferred words and deep call chains - and still a quarter
of what the selection's workloads show. The held-out tier now has seven applications: four of ours, three of
Appbench's from the zip.
