# How the designs were evolved - a draft of the method section (Iteration 548; figures recomputed at 600)

*For the article after consolidation (GOALS.md, "The article"), written while seed 74 ran; its figures recomputed at
Iteration 600 from the runs' records on the true fronts - results/article-figures-600.md (results/drafts/article-figures-600.py):
the series from seed 77 that the stopping rule ended, its confirmation runs, the random baseline, the final set. In the
author's register (article/AUTHOR-STYLE.md): first person, commands as typed, numbers flat, what was not isolated said
plainly. [check] marks a sentence the owner should confirm - none left (659).*

## The design space

Every design is a genome - 84 genes, nine of them frozen at one value - and a genome is all it takes to build one:
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
afterwards, to see whether the speed carries over (sieve against the selection speed over each run's true front,
seeds 77-83: Spearman 0.94-0.98).

## The search

A population of 32. Parents are picked by binary tournament - lower Pareto rank wins, then the larger crowding distance
(NSGA-II's scheme); the second parent comes from the first one's encoding family four times in five. A child comes from
crossover, from genes borrowed from a third design, and from mutation - nine children in ten get one - and from seed
74 on, the chances of crossover and borrowing follow how many of their children reached the front in the last ten
generations. The survivors: the best of each family (crowding cannot kill a family), the eight best by a quality score
(the knee of the front), then the rest by rank. A design already in the database is never measured again. A run is
bounded by hours, not generations: the seven runs from seed 77 made 126-178 generations and 32,394-45,696 designs in 9
or 12 hours, 3,400-3,800 an hour.

## Three shortcuts, each audited

Most children are worse than what the run already has, and each costs a build and seven workloads at two widths.
Three shortcuts spend less on them, each with a check that it is not losing front designs:

1. **The screen** - from generation 5, an additive model fitted on the run's own measured designs (refitted every ten
   generations, once there are 1,000) predicts a child's speed and size; a child predicted far behind the run's
   staircase is not measured. One in ten of those is measured anyway. In the seven runs, 4,430-6,934 of a run's designs were screened;
   of the audited ones that ran in full, 2 of 421 reached the true front - the screen loses a few front designs (on that
   rate, about twenty across the seven runs, against 180-370 on each run's front).
2. **One round first** - from seed 74, a child 30% behind after its first round stops there; one in ten is measured in
   full anyway. In the seven runs, 7,488-12,059 children a run stopped there; of the 6,934 audited in full, none reached the true front.
3. **The fast gate** - a child whose first reading would put it on the front is measured again in the next batch,
   beside other work, and its speed is the geometric mean of the two readings: one lucky reading cannot carry a design
   onto the front.

## The front

From seed 74 the front a report shows is the true one: every design that no other dominates, tolerances included. Before
it, the reports used a staircase that ignored the 2% band and the 32-bit speed, and kept about a third of each true front
(seed 73: 61 of 222). Every figure here is recomputed from the runs' records on the true fronts.

## One command a run

A run is one command on one laptop, an AMD Ryzen 7 PRO 8840HS:

    sh lab/evolve/next-run.sh

It reads its line from lab/evolve/NEXT-RUN - seed 77's:

    seed 77 12h widths noevolved then experiment review-checks.py spread then experiment appbench.py --zip ~/Downloads/appbench.zip --sample 16 then experiment clockcheck.py --sample 8

and runs a chain: the tests and the byte-identical rebuild, the evolution, the front measured again in six rounds, the
experiments, and one archive to send back. `widths` is the 32-bit objective; `noevolved` means nothing is carried from
an earlier run - every run starts from the hand-made designs and the founders built from them, so the runs are
replicates, not one long run - every run of the series, seeds 77 to 83, was `widths noevolved`. Each archive came back
to the same scripts: the pack's own checks again, the results file drafted from the database, the remote machines'
readings set beside it, the stopping rule's numbers, and the next run's line written from that.

## Checks against fooling myself

- The fastest ten of a front, measured again after the run, come out 5-7% slower than in it (seeds 77-83: 1.051-1.073;
  the JIT designs 1.034-1.057, the rest 0.991-1.016). Not the clock: seed 77's clock test, with the cycle counters, found
  the cores no slower beside the run's compiles than alone (time 0.990, cycles 1.002). The rest left
  unread - the winner's curse, or a cost outside user space (results/drafts/fast-end-offset-554.md, HANDOFF open item 4);
  the article names no cause (606; the [check] closed, 659).
- On other machines - an Intel i7-6700 at both widths and an ARMv7 board, a Tegra - a sample of each run's front ranks
  close to the laptop's order (seed 83 on the i7: Spearman 0.932-0.993). The final pick's 40 candidates, mostly from the fast
  end, measured in 42 sessions on the i7 and 6 on the Tegra: Spearman 0.92 against the laptop at 32 bits, 0.47 at 64,
  0.08 on the Tegra (where the JIT designs run without the JIT). Each machine agrees with itself better than with the
  others (0.96-0.99 between its own sessions). The laptop's fastest is 6-7% behind the i7's own best at either width: the
  fast end is a band, not one design.
- Designs from the front are rebuilt and run on the Forth core tests by a second tool, with a negative control - a test
  with one wrong expected value, which must fail.
- An engine the evolver runs cannot fork or outlive its time limit: every one runs jailed - no new processes, bounded
  memory, CPU time and files. lab/evolve/test-jail.py checks it in an order that is safe if the jail fails: one fork,
  jailed, must fail; one fork, not jailed, must succeed, so the first tested something; only then a fork bomb through
  the evolver's own runner, at most one engine alive. (Iteration 10: a broken design reached FORK in a loop and froze the
  laptop.)

## When to stop

Each run's true front gets one number: its hypervolume in a box fixed before seed 74 (lab/evolve/hv.py; speed on a
log scale). A run gains when that number beats the best earlier run's by 1%, or an extreme improves by its threshold
(speed 2%, size 1%, memory 4 KB, the 32-bit speed 2%). The runs stop when, after at least three on an unchanged method
- the same workloads, selection, operators, gates and box - the last two gain nothing. A change to the method
restarts the count: the last one at seed 77 (12 hours, every freeze that still had code lifted), and since the hours
vary with my days, a run is judged at its last generation against each earlier run at that same generation. The rule
stopped after seed 83 - seven runs, the last two gaining nothing. Two confirmation runs from the pooled front (seeds 84
and 86) confirmed nothing new: seed 84's gain at the fast end was the laptop's (on the i7 -0.6% and +0.2%), seed 86's
came from designs carried in, not bred. With three runs no significance test can decide anything, so the rule uses
effect sizes fixed in advance, and the article reports values and spreads, not p-values.

## What the search itself adds

One more run of the same hours, in which every child is a fresh random genome - drawn uniformly, as the random
founders are - and measured exactly as the method's children are, with nothing learned in the loop: no breeding, no
operators' adaptation, no screen, no one round first. (The fast gate stays: it is a measurement, not a search.) Its
true front's hypervolume and extremes, beside the method's runs, are what the evolutionary search contributed over the
design space alone:

    seed 85 10h widths noevolved random

Its 35,760 random genomes left a true front of 30 designs, against 180-370 in the series' runs; its hypervolume 0.188
is 0.55 of the series' median (0.340); its fastest 0.320 against the series' 0.138-0.148, its smallest 16,446 bytes
against 13,989-14,210, its least memory 116 KB against 108-112.

## What was not isolated

- Selection ran on one machine. The fast end's order is that machine's; on the i7 its fastest is 6-7% behind the best.
- CPU time is not cycles - but seed 77's clock test found the cores no slower under the run's load (cycles 1.002 of
  alone), so the fast end's 5-7% offset is not the clock.
- The screen and one round first skip children by prediction. The audits measure how often that misses - not that it
  never does.
- The final method ran seven times (seeds 77-83), a single seed each; the spread between runs is reported, not tested.
