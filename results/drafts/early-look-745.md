# Two looks while seed 98 runs (Iteration 745)

## The roles after seed 97 alone - a forecast, not a decision

`python3 -B results/drafts/roles-early-745.py DB REMEASURE REMEASURE32 results/relf-designs-718.md` (output
results/drafts/roles-early-745.txt): each role's rule (followup-roles.py: speed 2 %, binary + image 1 %, memory 8 KB)
read loosely on seed 97's one machine - a holder carried into seed 97 by its generation-0 reading, a challenger by
its re-measure when it has one, else in-run. The roles' screen itself (results/drafts/roles-screen-741.py on seed 97
alone, the endgame's arguments) gives 663 designs for the laptop and dream, 383 for the Tegra - chain A's lists were
944 and 437 from five runs.

| role | holder | seed 97 |
|---|---|---|
| fastest-x86-64 | 9b15ba26f7 | holds - it is the run's fastest |
| portable-fastest | d727605472 | one challenger: 39825db599 -3.2 % / -1.6 %, 2.9 % smaller (in-run; the JIT-free curse about 1.00) |
| portable-knee | 48a012411a | 178 by the rule - mostly 2-3 % smaller at the same speed (fcbee6ff6b 26,222 B, hashk and numfirst) |
| smallest | 219878ec89 | none 1 % smaller; 196 designs 37 B smaller (21,636 B, hashk) and no width 2 % slower - 649's precedent took such a one |
| small-jit | 15eda54ebd | one, marginal: c0ff16eabe 1.07 % smaller, +1.3 % / -0.4 % (jitdead) |
| least-memory | fb0d57c8a2 | not carried; 736 designs at 100 KB or less, the fastest (790f86f2ff 0.662 / 0.727) faster than the holder's 718 record (0.764 / 0.779 at 112 KB, the old layout and scale) - likely to change |
| fastest-x86-32, best-all-round | 11f956db93, df097ba2e2 | not carried; their 718 records are on the old scale - the chains decide |
| portable-arm, portable-small | a8d35bdccc, ae99617f06 | ARMv7 roles - the Tegra decides |

So the roles' chains after the series will have work: three roles likely to change (the knee, the smallest, least
memory), two possible, hashk on most of the small-end challengers.

## Seed 96's re-measure against chain A and seed 97 - a step on the laptop

**Superseded by results/drafts/scalecheck-746.md (Iteration 746)**: the kernel was the same throughout and the machine's
drift cancels; chain A's readings are the odd ones, and the boundary's step is the code's placement. Kept as written.

results/drafts/series-shift-744.txt found seed 96's end-of-run re-measure of its portable fast end ~10 % off seed 97's
generation 0, while chain A's laptop readings agree with seed 97. Checked here:

- Not a stale file: `evolve.py --remeasure` merges into an existing remeasure.json, but a fresh seed run moves all of
  build/evolve/ into its archive first (next-run.sh, "the previous runs' records, kept").
- Not the chain's measure: chain B's records' speeds are chain A's `measure-ids.py` readings on the laptop ("src":
  "measure-ids.py (the laptop, N reads)"), sequential, on seed 96's code (the batch came at 713). Seed 96's own re-measure is
  sequential too and agrees with its in-run readings (non-JIT 1.007); seed 97's parallel run agrees with chain A.
- So the step is in time: seeds 93-96's runs all read the portable designs about 8 % faster against s6 than chain A did right
  after seed 96 on the same code (seed 97 / each run's own in-run, non-JIT: 1.094, 1.088, 1.089, 1.068 -
  series-shift-744.txt, section 2), and seed 97
  reads like chain A (0.972). The JIT designs moved less (seed 97 / chain A 0.934). The laptop runs Linux
  6.17.0-1033-oem now (seed 97's machine.txt); what seed 96 ran on is in its pack on the laptop, not in the repository.

Nothing depends on it: the stopping rule compares runs of one series, and the roles' chains measure every candidate
again, paired by session. It matters only for figures that compare readings across 2026-11-19 on the laptop - the old
series' runs against chain A or later.
