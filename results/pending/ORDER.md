# The after-seed-76 batch - to apply first at seed 76's processing (Iteration 554)

Prepared while seed 76 runs (the owner, 554: "all three"); master stays what seed 76's bundle tests.

    git apply results/pending/stopping-rule-after-seed76.patch
    git apply results/pending/clock-cost-after-seed76.patch

batch-check (554): pending.

**stopping-rule-after-seed76.patch** (lab/evolve/stopping.py and results/stopping-series.md new; lab/evolve/hv.py,
process-seed.sh, draft-results.py, README.md; tools/run-tests.sh) - **GOALS.md's stopping rule, mechanical** (prompts/21,
item 9): a run's fixed-box hypervolume and four extremes against the best of the method's earlier runs in a ledger,
criterion by criterion; the count, the earliest stop, the next run's bar. process-seed.sh puts it in summary.md beside the
votes; draft-results.py writes it into the results file's hypervolume line, where a TODO was; step 6 appends the run
(--append). Seed 75 was judged at first by its hypervolume alone; the tool reproduces the corrected judgment - a gain, by
the fastest; the earliest stop after seed 77; the bar 0.36024, 0.1336, 13,938, 108 KB, 0.1688. hv.py's printed line is
byte-identical (its new measure() shared). The ledger seeded: seed 74 from its processing and records, seed 75 from its
pack's database. Tested: the self-test (17 checks, now in run-tests); process-seed.sh and draft-results.py on seed 75's
archive. Changes nothing a run uses.

**clock-cost-after-seed76.patch** (tools/cputime.c, lab/evolve/clockcheck.py, README.md) - **the cost a design and s6
both pay** (results/drafts/fast-end-offset-554.md): the clock test's second table, per workload - the time a run spends
outside its user-space work that a design and s6 pay alike, s6's time x (t - c)/(1 - c) from the time ratio and the
user-space cycle ratio at one clock (it needs the counters: the perf hold), beside getrusage's system time. cputime
prints the two parts of the CPU time it sums ("USERNS", "SYSNS") after the child is gone; the run's number is the sum,
computed and printed as before, and every reader of its output anchors on its own key - in this reading not a method
change (GOALS.md: workloads, selection, operators, gates, hours, box), the owner's to say. The split is sampled at the
kernel's tick (here single runs read 0 or a tick): means over every run, a coarse check. Tested: the self-test (the parse
and the formula: 350.68 us on a made-up pair); one-design clock tests on seed 75's database here - no counters on this
machine, so the cost reads '-', the system time's means printed. Seed 77's line, if the owner wants the measurement: `...
then experiment clockcheck.py --sample 8` (sudo asked once, at the start, for the perf hold).
