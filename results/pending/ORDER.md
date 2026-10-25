# The after-seed-73 batch - applied at seed 73's processing (Iteration 521)

Prepared while seed 73 runs; master stays what seed 73's bundle tests.

    git apply results/pending/freeze-rt-jitret-after-seed73.patch
    git apply results/pending/aos-after-seed73.patch

**freeze-rt-jitret-after-seed73.patch** (lab/evolve/evolve.py) - **the owner froze rtfuse, rtimm and jitret** (521), the
gene votes' candidates over seeds 70-72: rtfuse and rtimm 12 of 12 removal votes, jitret 11 of 12 - each under a tenth of
the front, none in its fastest, smallest or best-Q tenth. Frozen at 0: out of mutation's pool (FROZEN), so no lineage
takes them up - the founders have none (s6: rtfuse 0, rtimm and jitret unset). Reversible: out of FROZEN again. What
needs them does not: I+ (rule 7) needs rtloopall's overlay, not rtfuse; rule 9 (the rtimm=2 / rtfuse overlap) is moot
with both frozen; rule 2 watched jitret, frozen now.

**aos-after-seed73.patch** (lab/evolve/evolve.py, 526) - **adaptive operator selection** (the owner: proposal 1 of
results/drafts/ask-search-answers-525.md). Each generation, the last ten generations' children by class (crossover;
borrowed - a borrowing without crossover; mutation), each class's yield its children on the front now, smoothed;
crossover's chance and borrowing's follow the yields with a floor of 0.1 a class (from seed 72's counts: crossover
about 0.15 instead of 0.25, borrowing about 0.42 instead of 0.15). Deterministic from the records; EVOLVE_AOS=0 the
fixed chances; a line a generation says them. Tried: four generations of 32 - the chances computed from generation
3 and applied (0.28 and 0.38, then 0.37 and 0.26), the run whole.

**At seed 73's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
