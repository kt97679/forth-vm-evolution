# Seed 75's processing - the checklist (Iteration 550)

`seed 75 10h widths noevolved then experiment review-checks.py spread then experiment appbench.py --zip
~/Downloads/appbench.zip --sample 16 then experiment clockcheck.py --sample 8 then experiment truefronts.py` at 8f2c3af
(Iteration 549) - the second run on the method seed 74 began, the after-seed-74 batch's first. Then "Processing a
returned seed" (HANDOFF.md), with these:

1. **The chain's status**: done, every experiment's pack whole (the chain-logs patch: the first step's logs kept in the
   chain's checked/). A "failed" again - its packs' logs first.
2. **The prediction (549)**: no gain over seed 74 - the hypervolume (`python3 lab/evolve/hv.py DB`) within 1% of
   0.35667 or below, and no extreme past its threshold: fastest 0.1402 by 2%, smallest 14,079 bytes by 1%, least memory
   112 KB by 4 KB, fastest at 32 bits 0.1740 by 2%. No gain: seed 76, the third run, decides whether the count ends.
3. **The clock test with cycles**: sudo asked once at the start, the setting held only while it measured (the chain's
   log; runs/perf-hold.log on the laptop); clockcheck.md's cycle columns filled. Read against
   results/drafts/fast-end-offset-550.md: not the clock - does the cycle ratio agree?
4. **truefronts.md**, the last step: every seed pack's true front. The seed names first - every row "(pack)", any "?"
   explained; then `python3 results/drafts/truefronts-tables-550.py truefronts.md chart.json`: the progress table on
   the true fronts (stdout - results/progress-true-fronts.md, beside progress-by-run.md) and the charts' data (the
   fastest by seed, every run's size-speed staircase by era) for the chat's chart tool. The tool's own "reported" column
   reads 261 for seed 74 (it counts genomes - the after-seed-75 batch fixes it); the tables script counts the front
   tables.
5. **jitrp**: a freeze candidate since seed 74 (12 of 12, no keep vote) - the owner's; a freeze restarts the count.
6. **Rule 3**: ATTENTION expected - the JIT designs read faster under the run's load (fast-end-offset-550.md). Rule 5:
   cpt16's reach now named expected (the fail32 patch).
7. **The after-seed-75 batch** (results/pending/ORDER.md): one patch, truefronts.py's reported column - batch-check,
   then apply.
8. **Seed 76's line**, 10 hours, the method's: `seed 76 10h widths noevolved then experiment review-checks.py spread
   then experiment appbench.py --zip ~/Downloads/appbench.zip --sample 16` - the clock test and truefronts done; the
   test that would decide the offset (the front re-measured four at a time against one) needs --remeasure with workers,
   a small patch - the owner's call.
