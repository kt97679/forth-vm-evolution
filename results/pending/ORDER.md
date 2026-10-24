# The after-seed-71 batch - applied at seed 71's processing (Iteration 501)

Prepared while seed 71 runs; master stays what seed 71's bundle tests.

    git apply results/pending/retire-nocase-after-seed71.patch
    git apply results/pending/fastgate-slower-after-seed71.patch

**retire-nocase-after-seed71.patch** (forth/cv8b-nocase.4 and forth/cv8bt-nocase.4 removed, lab/evolve/evolve.py,
lab/evolve/engines-check.py) - **the owner retired nocase** (501): it changes only how names are looked up, so it can
make no design faster; it costs bytes and compile time; no selection workload is in lower case - a gene the search
would never keep. Its overlays, its two extra kernel dumps per header system (built at every setup), the gene and its
engines-check variant go; coreext.4's [ELSE] matching without case stays (499: free, and right for any program). Kept
for a revival: results/drafts/nocase-496.md and results/applied-after-seed70/ (nocase-after-seed70.patch). Tested in a
clone of master (35a2a8c) with it: run-tests PASS (93 engine paths).

**fastgate-slower-after-seed71.patch** (lab/evolve/evolve.py, 503; the owner agreed to proposal 6 of
results/drafts/process-review-501.md): a gated design - faster than the fast gate, measured a second time in the next
generation's batch - takes the slower of its two readings, each workload's, not their geometric mean. Free: no reading
more - the whole slower reading: a first version took each workload's slower time, which compounded (0.70 and 0.70
made 0.74, slower than either). Tested: applies after the retirement; three generations of the evolver with both and
the gate at the third fastest - gated designs measured again, the slower reading kept (0.9512 then 0.9771: 0.9771).

**At seed 71's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
