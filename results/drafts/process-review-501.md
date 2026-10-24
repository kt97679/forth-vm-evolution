# What the recent runs say about the workflow, the processes and the rules (Iteration 501)

The owner asked, after seeds 64-70 and the JIT work of 471-500. Changed now, as tools: (1)-(3). The owner's to decide:
(4)-(7).

1. **The 32-bit JIT was never tested by engines-check** - its 32-bit variants were built with jit=0, so CELL+ and CELLS
   with eight-byte cells reached seed 70 (906 failures). Now the JIT is kept at 32 bits there, and every JIT variant
   runs tests/jit/jit-diff.fth - this session's hand-made JIT tests made permanent: arithmetic and its throw, EXECUTE,
   DOES>, inline strings, cold calls, (ABORT"), PICK, SP@, ALIGNED, CELL+ and CELLS, LEAVE and ?DO, the return stack
   along branches, recursion - its output s6's at the same width. engines-check PASS with it (95 paths).
2. **A patch can carry conflict markers and still apply** - the after-seed-68 engine patch did, from its 475 rebase to
   486, through four "applies in order" checks. tools/batch-check.sh now refuses a patch that adds them.
3. **Rebasing a batch**: in a clone; `git diff HEAD` (a three-way apply stages what it applies); markers looked for in
   every file; engines-check after - the ways 475-494 went wrong, each once.
4. **A gene must be paid for by a workload before it is enabled** - jitmul, jitdoes, jitexec and jitcfa were enabled on
   application measurements while the selection measured none: tried on thousands of designs, on none of the front.
   Proposed rule: a gene whose benefit no selection workload (nor size or memory) can see is not enabled until one can;
   a prediction for a gene names the workload that pays for it.
5. **Gene votes need a grace period** - seed 70 cast four removal votes against each of those genes, which had no
   workload to win on; three such runs would make them freeze candidates. Proposed: a gene's votes count from its second
   run with a workload that measures it (for the four, from seed 72).
6. **Rule 3, the fast gate, has been ATTENTION every run** (the fastest tenth re-measured 1.07-1.10 of in-run, against a
   0.98-1.05 band) - load is about half of it (458), selection's luck the rest. Either re-measure the front's fastest
   few each generation with more rounds before they enter it, or move the band to what is known (up to 1.10).
7. **The footprint experiment has answered its question** - over seeds 64-70 its Spearman ran 0.89, 0.55, 0.21, -0.03,
   0.12, -0.17, 0.68: the fast end's order at program sizes is too close to call. Proposed: drop it from the chain
   (about 10 minutes a run), run it when a change is meant to move it.

And for the processing of seed 71, the first with the applications in the selection: its speeds compare with no run
before it; the spread compares sizes, not speeds; seed 72 onward compare with 71.

**The owner (502)**: 4, 5 and 6 agreed - rule 11 (a gene paid for before it is enabled) and rule 12 (a grace period for
the votes, review-checks.py's GRACE: the four JIT genes and jitrp from seed 72) in results/seed63-rules.md; 6 as the
re-measure, the slower of the two readings (the after-seed-71 batch, 503). 7 explained further - the owner's to decide.
