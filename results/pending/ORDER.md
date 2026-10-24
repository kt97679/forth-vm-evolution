# The after-seed-71 batch - applied at seed 71's processing (Iteration 501)

Prepared while seed 71 runs; master stays what seed 71's bundle tests.

    git apply results/pending/retire-nocase-after-seed71.patch

**retire-nocase-after-seed71.patch** (forth/cv8b-nocase.4 and forth/cv8bt-nocase.4 removed, lab/evolve/evolve.py,
lab/evolve/engines-check.py) - **the owner retired nocase** (501): it changes only how names are looked up, so it can
make no design faster; it costs bytes and compile time; no selection workload is in lower case - a gene the search
would never keep. Its overlays, its two extra kernel dumps per header system (built at every setup), the gene and its
engines-check variant go; coreext.4's [ELSE] matching without case stays (499: free, and right for any program). Kept
for a revival: results/drafts/nocase-496.md and results/applied-after-seed70/ (nocase-after-seed70.patch). Tested in a
clone of master (35a2a8c) with it: run-tests PASS (93 engine paths).

**At seed 71's processing**: `sh tools/batch-check.sh` first, then apply, the routine's chain after it.
