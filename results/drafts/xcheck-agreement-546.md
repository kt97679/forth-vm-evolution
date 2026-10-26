# Why the cross-machine checks agreed less on seed 72's front (Iteration 546)

The checks of seed 72's front during seed 73 (results/xcheck-seed73.md) ranked it 0.870, 0.931 and 0.893 at dream's
three builds and 0.882 on the Tegra, against 0.958, 0.956, 0.955 and 0.916 for seed 71's front a run earlier
(results/xcheck-seed72.md). From the hosts' raw measurements in seed 73's chain archive (remote/*/out.json: every
design's ratio to s6 per workload) and seed 72's records - results/drafts/xcheck-agreement-546.py:

1. **Mostly the sample.** A check measures 16 to 30 designs, and the 95% bootstrap intervals are wide: dream's default
   build 0.672-0.955, its 32-bit 0.831-0.968, its 64-bit 0.739-0.959, the Tegra 0.618-0.970 - each includes or touches
   the earlier value. The two fronts are made alike: JIT designs 104 of 185, in-run 0.148-0.331, against 130 of 210,
   0.143-0.327. One check's Spearman is not a trend.
2. **What is real: the machines order the fast JIT designs differently.** Each agrees with itself - dream's two 64-bit
   sessions 0.974, 0.900 within its 15 JIT designs; the laptop's in-run speeds against its re-measured 0.958 - but the
   laptop and dream within the JIT designs only 0.44-0.54 (0.73 at 32 bits). Not the winner's curse: dream against the
   laptop's re-measured speeds agrees no better (0.846 against the in-run's 0.870). The JIT's lead over s6 shrinks on
   dream's Skylake by an amount that varies by design - here / laptop 1.38-1.73 for the JIT designs, 1.23-1.58 for the
   rest. By workload, loop (0.71-0.83) and corpus (0.80-0.83) reorder most and the applications least (0.94-0.95, the
   Tegra 0.99): the seventh workload is not the cause. On the Tegra, without JIT designs, ackermann (0.29) and bubble
   (0.34) reorder.
3. **The fast end is a band, not a winner.** The laptop's fastest lands 3.4-3.7% behind the best of dream's sample at
   64 bits and 1.0% behind the Tegra's; dream's best is the laptop's fourth, 0.7-1.4% behind the laptop's fastest
   there. Designs within about 1.5% of each other on one machine reorder on another.

For the article and GOALS.md's "generic" question: name the fastest per machine and state the cross-machine result as
a band - the laptop's fast end within a few percent of each machine's best - rather than as one design. Nothing in the
method changes.
