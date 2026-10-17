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

## Adopted (Iteration 189) - the owner: yes to all three, and do not filter out designs with potential - demote the worst rather than promote the best

`results/applied-after-seed41/weighing-after-seed41.patch` (the thirteenth of the batch):

- **Demote, don't delete.** Survival kept the best 256 of 512 and deleted the
  rest - a design one step from something excellent was gone for good. Now a
  demoted design carrying a gene value no survivor has goes to the attic (128,
  the rarest genes first; it leaves once the population has those values
  again). One parent in ten comes from there, and borrowed genes may: a
  stepping stone keeps its chance, at no measuring cost. Children of attic
  parents are tagged "via the attic" - the laptop's run will say whether the
  attic's children reach the front. Deterministic, so a resumed run's replay
  rebuilds it. EVOLVE_ATTIC=0 turns it off.
- **The knee survives:** the 8 best by Q always, as the extremes and each
  family's best already did.
- **Judging:** compare-fronts.py prints per run its extremes, hypervolume and
  best Q against the others, the five-part verdict for the new run, and the
  Q-best design of all runs; evolve.py's report names its own.
- **The founder from the knee:** d99e3d9ed9 (the small end's best Q) - the
  forms push out only HASH and SKIP there; on 903b231e0d they would push out
  (LOOP). Both knees are JIT designs.

Checked: a scratch run (12 x 4 generations) - the attic grew 12 -> 31
designs holding 21 -> 42 gene values no survivor had; 8 of 48 children via the
attic, all alive, four among the run's notable designs (one at speed 0.58); the
report names the knee. The judging section's own code on session 35's table:
seed 40 +49.7% fastest, hypervolume +19.3%, best Q +46.1%, not small; and it
shows seed 39's run still holding 3.6% of the joint volume. The knee founder:
alive, speed 0.980 of s6 (the knee recorded 0.986), 164 KB. run-tests PASS (as
the user; my first try ran it with sh, not bash - 27 false failures). Thirteen
patches apply in order on a fresh clone.
