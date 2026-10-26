# How the designs were evolved - a draft of the method section (Iteration 548)

*For the article after consolidation (GOALS.md, "The article"), written while seed 74 ran. In the author's register
(article/AUTHOR-STYLE.md): first person, commands as typed, numbers flat, what was not isolated said plainly. [74+]
marks a figure that waits - for the true fronts (lab/evolve/truefronts.py, seed 75's chain) or the random-search
baseline; [check] a sentence the owner should confirm. Everything else is the method as it stands at Iteration 548.*

## The design space

Every design is a genome - 84 genes, a few of them frozen at one value - and a genome is all it takes to build one:
lab/evolve/evolve.py turns it into a C engine and a self-hosting Forth image. The genes are the kind of decision the
first article took by hand, one at a time: how operations are encoded (four families, called cell, sod16, cpt16 and
cv8 in the code), whether the top of the stack lives in a register, how far a call reaches, which pairs of operations
are fused into one, whether a small JIT turns hot words into machine code and which stencils it has, how the
dictionary is laid out, which compiler builds the engine - and a few dozen smaller ones. The hand-made designs are
points in the same space, and that is checked rather than assumed:

    python3 lab/evolve/evolve.py --validate

rebuilds each of them from its genome and requires the images byte for byte identical to the ones the build makes.

## What a design is judged on

Three objectives, all to be minimised:

- **speed** - CPU time against the hand-made s6 built from the same commit, on seven workloads (kernel, fib, corpus,
  loop, bubble, ackermann, and since seed 71 a set of small applications): on each, the median of three rounds, the
  design and s6 measured in turn; the geometric mean over the seven. CPU time, not wall time, each run pinned to a core,
  four workers on four cores;
- **size** - the stripped engine binary plus the image, in bytes;
- **memory** - peak resident memory, in KB.

Since mid-October (Iteration 336) every design is also built and measured at 32 bits, and that speed is a fourth
objective. A design
dominates another when it is no worse in all of them and better in one - with speeds within 2% counted equal and
memory within 8 KB. A design that computes anything wrong dies: every workload's output is compared with the expected
one, at both widths. Two more workloads, sieve and parse, are never used for selection; they are measured on the front
afterwards, to see whether the speed carries over (seed 73: Spearman 0.961 between the two).

## The search

A population of 32. Parents are picked by binary tournament - lower Pareto rank wins, then the larger crowding distance
(NSGA-II's scheme); the second parent comes from the first one's encoding family four times in five. A child comes from
crossover, from genes borrowed from a third design, and from mutation - nine children in ten get one - and from seed
74 on, the chances of crossover and borrowing follow how many of their children reached the front in the last ten
generations. The survivors: the best of each family (crowding cannot kill a family), the eight best by a quality score
(the knee of the front), then the rest by rank. A design already in the database is never measured again. A run is
bounded by hours, not generations: seed 73 made 128 generations and 32,876 designs in its 11 hours, about 3,000 an
hour.

## Three shortcuts, each audited

Most children are worse than what the run already has, and each costs a build and seven workloads at two widths.
Three shortcuts spend less on them, each with a check that it is not losing front designs:

1. **The screen** - from generation 5, an additive model fitted on the run's own measured designs (refitted every ten
   generations, once there are 1,000) predicts a child's speed and size; a child predicted far behind the run's
   staircase is not measured. One in ten of those is measured anyway. Seed 73: 5,981 of its 32,876 designs screened.
2. **One round first** - from seed 74, a child 30% behind after its first round stops there; one in ten is measured in
   full anyway. [74+: how many stopped, and whether an audited one reached the front.]
3. **The fast gate** - a child whose first reading would put it on the front is measured again in the next batch,
   beside other work, and its speed is the geometric mean of the two readings: one lucky reading cannot carry a design
   onto the front.

## The front

From seed 74 the front a report shows is the true one: every design that no other dominates, tolerances included. Before
it, the reports used a staircase that ignored the 2% band and the 32-bit speed, and kept about a third of each true front
(seed 73: 61 of 222). Every figure here is recomputed from the runs' records on the true fronts. [74+]

## One command a run

A run is one command on one laptop, an AMD Ryzen 7 PRO 8840HS:

    sh lab/evolve/next-run.sh

It reads its line from lab/evolve/NEXT-RUN - seed 74's:

    seed 74 10h widths noevolved then experiment review-checks.py spread then experiment appbench.py --zip ~/Downloads/appbench.zip --sample 16 then experiment clockcheck.py --sample 8

and runs a chain: the tests and the byte-identical rebuild, the evolution, the front measured again in six rounds, the
experiments, and one archive to send back. `widths` is the 32-bit objective; `noevolved` means nothing is carried from
an earlier run - every run starts from the hand-made designs and the founders built from them, so the runs are
replicates, not one long run. [check: say how the archives were analysed between runs, or leave it out.]

## Checks against fooling myself

- The fastest tenth of a front, measured again after the run, comes out about 7% slower than in it (seed 73: 1.070) -
  partly the winner's curse, perhaps the clock: the cores run slower under the run's compiles than alone. A clock test
  with the cycle counters decides. [74+]
- On other machines - an Intel i7-6700 at three builds and an ARMv7 board - a sample of the front ranks at Spearman
  0.87-0.96 against the laptop. Each machine agrees with itself better than with the others; where they differ is the
  order of the fastest JIT designs, which lie within about 1.5% of each other here. The laptop's fastest lands 1-4%
  behind each machine's own best: the fast end is a band, not one design.
- Designs from the front are rebuilt and run on the Forth core tests by a second tool, with a negative control - a test
  with one wrong expected value, which must fail.
- An engine the evolver runs cannot fork or outlive its time limit (lab/evolve/test-jail.py). [check: the jail's full
  list]

## When to stop

Each run's true front gets one number: its hypervolume in a box fixed before seed 74 (lab/evolve/hv.py; speed on a
log scale). A run gains when that number beats the best earlier run's by 1%, or an extreme improves by its threshold
(speed 2%, size 1%, memory 4 KB, the 32-bit speed 2%). The runs stop when, after at least three on an unchanged method
- the same workloads, selection, operators, gates, hours and box - the last two gain nothing. A change to the method
restarts the count; seed 74 started it. With three runs no significance test can decide anything, so the rule uses
effect sizes fixed in advance, and the article reports values and spreads, not p-values.

## What the search itself adds

One more run of the same hours, in which every child is a fresh random genome - drawn uniformly, as the random
founders are - and measured exactly as the method's children are, with nothing learned in the loop: no breeding, no
operators' adaptation, no screen, no one round first. (The fast gate stays: it is a measurement, not a search.) Its
true front's hypervolume and extremes, beside the method's runs, are what the evolutionary search contributed over the
design space alone:

    seed N 10h widths noevolved random

[74+: the baseline's figures.]

## What was not isolated

- Selection ran on one machine. The fast end's order is that machine's; on others it holds to within a few percent.
- CPU time is not cycles: a busy laptop runs its cores slower, and the 7% offset may be that. [74+]
- The screen and one round first skip children by prediction. The audits measure how often that misses - not that it
  never does.
- Each method was run three times at most, single seeds each; the spread between runs is reported, not tested.
