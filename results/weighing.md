# Weighing the objectives - not to lock out good trade-offs (Iteration 188)

The owner: a small size increase for a big performance gain is acceptable -
that was Q's point (size x time x memory): to see a design improve even when
one parameter gets worse. What is in place: selection NSGA-II on three
objectives (rank by Pareto front, crowding within it - no weights); Q
information only (Iterations 100-103); the stopping rule on the front's three
extremes alone (fastest under 5%, smallest under 2%, memory under 8 KB).

**Selection does not lock them out.** Seed 40's joint front, its small end,
against the smallest (0ceb043115, 17,762 bytes, speed 1.389, 192 KB, Q 1.00):
903b231e0d +1.1% size, -22.8% time, 156 KB, Q 0.63; d99e3d9ed9 +1.3%, -27.9%,
164 KB, Q 0.62; cb621c5de6 +2.1%, -28.8%, Q 0.62. The trade-offs the owner
means are on the front - nothing beats them on all three.

**The judging could.** The rule looks at the extremes only: a run that moves
the middle - +1% size, -25% time - counts as small, and two such in a row
declare convergence. Measured on sessions 34-35, two front-wide measures beside
the rule (results/drafts/frontmeasures.py): seed 39 - hypervolume (log space)
+1.3%, best Q -1.1%, the rule's fastest -0.8%: small by all; seed 40 -
hypervolume +19.1%, best Q +46.1%, fastest +49.7%: big by all. No verdict would
have changed yet; nothing guarded against it.

**And my own anchoring did.** I have been reasoning from the extremes ("the
smallest lacks rtloop - the size end's choice"), and built the new founder from
the smallest - the worst Q of its neighbourhood (slower and hungrier than
designs a percent larger).

## Proposed (the owner decides)

1. Selection unchanged: NSGA-II, weight-free - the data says it keeps the
   trade-offs. Optional insurance: the best few by Q kept from crowding's
   truncation, as the extremes are.
2. A run is small only if the extremes are (as now) AND its front's
   hypervolume in log space grew under 2% AND its best Q improved under 2% -
   compare-fronts.py to print both per run.
3. Every report names the Q-best design (the knee) beside the extremes, and
   my analyses start from it - founders included: the rtimm2/keepforms founder
   rebuilt on a knee design (d99e3d9ed9 or 903b231e0d) rather than the smallest.
