# The fast end's offset, tested on seed 75's own re-measure (Iteration 554)

Seed 75's clock test left a lead: the fastest eight's user-space cycle ratio did not move between its conditions while
the time ratio did - what varies lies outside user space - and a cost there that every process pays would weigh most at
the fast end. Tested here without new timing, on the 112 designs seed 75 re-measured alone at the run's end
(remeasure.json) against their in-run numbers (db.jsonl): results/drafts/fast-end-offset-554.py.

**The models.** A cost every process pays - the same absolute time d for a design and the s6 it is paired with - moves
a ratio t to (tS + d)/(S + d), about t + (d/S)(1 - t): an absolute shift growing as t falls, the same for JIT and
non-JIT designs, negative for designs slower than s6. A cost only JIT code pays moves only the JIT designs. A uniform
slowdown moves every ratio in proportion.

**The re-measure** (re-measured / in-run speed, median, designs):

| in-run speed | JIT | non-JIT |
|---|---|---|
| under 0.2 | 1.045 (15) | - |
| 0.2-0.3 | 1.025 (31) | - |
| 0.3-0.5 | 1.025 (3) | 1.027 (13) |
| 0.5-1 | - | 1.005 (42) |
| 1 and over | - | 0.989 (8) |

The non-JIT designs at 0.33-0.5 shift as much as the JIT designs beside them (the two kinds do not overlap in speed: the
JIT ones end at 0.327, the non-JIT begin at 0.339), and the designs slower than s6 shift the other way - as a shared
cost predicts and neither other model does. Fitted to the 112 shifts: every process, c(1 - t) with c = 0.011, explains
40% of their sum of squares; JIT only, 17%; uniform, 2%; both together 46%, the JIT term then negative (-0.008).

**By workload** - the cost each implies, d = (t' - t)S/(1 - t), S s6's own in-run time (raw / t): bubble's is about
300 us in every group, JIT and non-JIT alike (296, 341, 265, 331 us), and predicts its ratios - 1.152, 1.081, 1.024
against 1.145, 1.080, 1.026 seen. Kernel's, measured as precisely (s6's run is short, 7.7 ms), is about 75 us at the
fast end: not the same number - a cost each workload's run pays, not one constant a process. Bubble carries most of the
fast end's offset (1.145; sieve, held out, 1.111); apps and fib none. The long workloads (fib, apps, parse: 57-90 ms of
s6) are too noisy at these speeds to say.

**The reading.** The offset is a cost every run of a workload pays - a design and s6 alike - outside user space (the
cycles), larger at the re-measure than in the run, and by workload. Not the JIT: the JIT designs show it most because
they are the fastest. It moves the fast designs alike, so it hardly reorders the fast end; it scales its numbers, and its
level differs from run to run and moment to moment - seed 74's fastest re-measured 7.7% slower than its report's in-run
figure, seed 75's within 1%; the clock test 40 minutes after seed 75's re-measure, 1.084. The stopping rule's 2% speed
threshold lies inside that spread.

**The measurement that would locate it** - the after-seed-76 batch's clock-split patch: the clock test records each
run's user and system time apart (tools/cputime.c prints the two parts of the CPU time it already sums), per workload,
for the design and s6 alike. A cost every process pays in system time shows as a design's system time matching s6's on
each workload; its size against bubble's 300 us and kernel's 75 us says whether it can carry the offset.
