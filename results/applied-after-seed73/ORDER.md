# The after-seed-73 batch - applied at seed 73's processing (Iteration 521)

Prepared while seed 73 runs; master stays what seed 73's bundle tests.

    git apply results/applied-after-seed73/aos-after-seed73.patch
    git apply results/applied-after-seed73/bughunt-evolver-after-seed73.patch
    git apply results/applied-after-seed73/stop1-after-seed73.patch
    git apply results/applied-after-seed73/test-evolver-after-seed73.patch
    git apply results/applied-after-seed73/jit-table-bounds-after-seed73.patch
    git apply results/applied-after-seed73/unfreeze-jitos-after-seed73.patch

**freeze-rt-after-seed73.patch - withdrawn (533, the owner)**: by the vote tool's own rule - 11 of 12 votes and no
keep vote - on the true fronts neither rtfuse nor rtimm is a candidate (each has one keep vote: rtfuse in seed 72's
best-Q tenth, rtimm in seed 70's fastest); the freeze rested on the reported fronts (521) and then on a recheck that
counted the votes and missed the keep votes (528). The rule decides at seed 73's processing, its votes now from the
runs' records (532): rtimm can be a candidate then (71 and 72: 4 of 4, no keep vote), rtfuse not before seed 75's
(its keep vote is 72's). Kept as results/drafts/freeze-rt-withdrawn-533.patch. The other five apply in order without
it and the evolver self-test passes on them (533); the batch-check of 532 ran with it - run it again at processing.

**aos-after-seed73.patch** (lab/evolve/evolve.py, 526) - **adaptive operator selection** (the owner: proposal 1 of
results/drafts/ask-search-answers-525.md). Each generation, the last ten generations' children by class (crossover;
borrowed - a borrowing without crossover; mutation), each class's yield its children on the front now, smoothed;
crossover's chance and borrowing's follow the yields with a floor of 0.1 a class (from seed 72's counts: crossover
about 0.15 instead of 0.25, borrowing about 0.42 instead of 0.15). Deterministic from the records; EVOLVE_AOS=0 the
fixed chances; a line a generation says them. Tried: four generations of 32 - the chances computed from generation
3 and applied (0.28 and 0.38, then 0.37 and 0.26), the run whole.

**bughunt-evolver-after-seed73.patch** (lab/evolve/evolve.py, 527) - **from the evolver's bug hunt**
(results/drafts/ask-evolver-review-answers-527.md): first_front, which every report, the gate, the re-measure and
the appbench sample use, now follows dominates() - the old staircase ignored the 2% in speed and the 32-bit speed:
on random populations it differed from fronts()[0] 176 times in 200, now never in 400; seed 72's front is 246
designs, not the 185 reported (7 s for 21,557 designs). Selection always used fronts() and is unchanged. A gated
design whose second run fails now dies with that failure instead of keeping its first reading; a run with no
measurement is a death, not an exception that ends the run; EVOLVE_SCREEN_AUDIT=0 no longer divides by zero.

**stop1-after-seed73.patch** (lab/evolve/evolve.py, 529) - **one round first** (the owner; priced in
results/drafts/front-recheck-528.md): after the first 64-bit round, a child beaten in that round's speed by 30% by a
design measured before its generation - no larger, memory within MEM_TOL - stops: "stopped after one round", its
one-round speed, memory and total kept, no 32-bit evaluation; one in ten measured in full anyway (stopaudit). The
rest go on from the first round (measure() continues an earlier call's rounds), so a full measurement costs no more.
Seed 72: a third of the measured children so, none on the final front. Tried: four generations of 32 - 23 of 162
children stopped, one audited in full, the run whole. EVOLVE_STOP1=0: off.

**test-evolver-after-seed73.patch** (lab/evolve/test-evolver.py new, lab/evolve/evolve.py, tools/run-tests.sh; 530) -
**checks that would have caught the bug hunt's finds**: first_front against fronts()[0] (two designs 1% apart, with and
without the 32-bit speed; 300 random populations), one round first's decision, the adaptive operators' shares and
floor, a gated design's second reading (made a function, gate_again, to be checked); 14 checks, run by run-tests.sh.
Shown to fail on master's code before the batch: 6 of 6 failed - first_front differed in 255 of 300 populations, the
three new functions missing.

**jit-table-bounds-after-seed73.patch** (tools/layout.py, 531) - **two bounds a reviewer named, asserted**
(results/drafts/ask-jit-table-answers-531.md): jitexec's extra rows below T2_JIT (0xFE00), and each row's constant
within jit_op.k's signed char. Neither fires today (a jitexec table: 83 rows, the extra rows at 126-128); either
would now stop a build with a message instead of writing a wrong table.

**unfreeze-jitos-after-seed73.patch** (lab/evolve/evolve.py, lab/evolve/review-checks.py; 534) - **jitos unfrozen** (the
owner; results/drafts/frozen-recheck-534.md): its freeze (495) fails the rule on the true fronts - 11 votes over
67-69 and a keep vote (seed 69's best-Q tenth) - and in seeds 59-66 it was in the fastest and best-Q tenths in six runs
each. Out of FROZEN; its votes from seed 75 (rule 12, GRACE). Rule 11: the size objective and every workload's speed
see it - built here with and without it: 22,684 bytes against 24,892 (2,208 less), alive, outputs right;
engines-check keeps its path ('the JIT, translator -Os').

**At seed 73's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
