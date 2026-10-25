# The after-seed-73 batch - applied at seed 73's processing (Iteration 521)

Prepared while seed 73 runs; master stays what seed 73's bundle tests.

    git apply results/pending/freeze-rt-after-seed73.patch
    git apply results/pending/aos-after-seed73.patch
    git apply results/pending/bughunt-evolver-after-seed73.patch
    git apply results/pending/stop1-after-seed73.patch

**freeze-rt-after-seed73.patch** (lab/evolve/evolve.py) - **the owner froze rtfuse and rtimm** (521; 528: jitret
taken out). Over seeds 70-72 by the true fronts (results/drafts/front-recheck-528.md) rtfuse and rtimm keep 11 removal
votes of 12; jitret has 8 - it is in every run's fastest tenth - so the freeze of 521, made on the reported fronts,
keeps only the two. Frozen at 0: out of mutation's pool; the founders have neither. I+ (rule 7) keeps rtloopall's
overlay; rule 9's overlap moot. Reversible.

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

**At seed 73's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
