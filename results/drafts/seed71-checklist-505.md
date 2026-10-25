# Seed 71's processing - the checklist, written before its results (Iteration 505)

Seed 71: `seed 71 10h widths noevolved then experiment footprint.py ... then experiment review-checks.py spread then
experiment appbench.py --zip ~/Downloads/appbench.zip --sample 16`, from the Iteration 498 bundle - **the first run with
the applications in the selection** (seven workloads), jitrp enabled, jitos frozen, nocase frozen. Read by the routine
(process-seed.sh), and these points in this order.

## What compares across the break, and what does not

The speed of seed 71 is over seven workloads; every run before it, six. Seed 72's will also join a gated design's two
readings differently (the slower, from the after-seed-71 batch). So:
- **Compares**: sizes (the smallest binary + image, the smallest engine), memory, 32-bit failures, everything measured
  within the run (held out, the fast end's optimism, the remote checks' agreement, the gene shares and votes), and
  appbench.py's ratios to s6 on fixed programs - seed 70's fastest ran the seven applications at 0.756 of s6.
- **Does not**: the in-run speed, best Q and hypervolume against seeds 70 and before. The progress table bolds the break
  (its new "speed over" column); the spread marks the runs unlike the first with \u2260 - seed 71 against seeds 66-70:
  read its sizes, not its speeds.

## The predictions it settles (results/predictions.md)

1. **The JIT genes paid for** (495): jitmul, jitdoes, jitexec and jitcfa each on at least three quarters of the front's
   JIT designs (seed 70: none).
2. **The applications** (495): appbench.py's geometric mean for the fastest JIT design below 0.30 of s6 (seed 70's
   fastest: 0.756; seed 68's fast design with the genes and the batch: 0.234). The chain's appbench.py is the bundle's -
   seven applications, without wordfreq and minif (added at 500) - so the figure compares with those.
3. **The cost** (495): the speeds on the six old workloads within 5% of seed 70's - read from the fastest design's
   per-workload times, its six old workloads' geometric mean against seed 70's fastest (0.120 in-run).
4. **32-bit failures: none** - seed 70's 906 were all CELL+/CELLS on the 32-bit JIT, fixed in the batch applied at 498
   (not a prediction made before; a check). Any other: by cause, as rule 5 says.

## Then

- **Gene votes**: appended as always; the grace period (rule 12) keeps the four JIT genes' and jitrp's out of the
  candidates until seed 72's.
- **The after-seed-71 batch** (results/applied-after-seed71/ORDER.md): `sh tools/batch-check.sh` first - it now refuses conflict
  markers - then apply the three patches in order: nocase retired, the fast gate's slower reading, jithelp and jitre
  retired; move to results/applied-after-seed71/; the routine's chain on master (build, run-tests - engines-check's
  differential JIT test at both widths in it -, validate, the jail, the gate, ans-check).
- **Seed 72's line**: the owner's hours; without the footprint experiment (504):
  `seed 72 <hours>h widths noevolved then experiment review-checks.py spread then experiment appbench.py --zip ~/Downloads/appbench.zip --sample 16 then experiment contention.py --sample 16`
  (514, the owner: the contention experiment - results/drafts/ask-noise-answers-513.md).
  appbench.py's default then includes wordfreq and minif (nine applications).
- **Records**: the results file (its first paragraph saying the speed break), xcheck, the compare-fronts session (the
  spread - sizes), the progress table (regenerated: the break bold), HANDOFF, PROGRESS, the predictions scored.
