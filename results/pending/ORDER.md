# The after-seed-86 batch - to apply first at seed 86's processing (Iteration 583)

process-run.sh checks and applies it.

    git apply results/pending/fsys45-after-seed86.patch

batch-check (582, on cbf4daa - 1 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**fsys45-after-seed86.patch** - consolidation's first retirement (GOALS.md step 3; 578's rule): fsys levels 4 and 5 - on no design of the pooled true front of seeds 77-86 (results/drafts/retire-report-583.md) and on none of the 232 final-pick candidates (results/drafts/retire-plan-583.md). Removes the engine's three FSYS >= 4 blocks (the Forth output buffer, SYSCALL -5 and -6), forth/file-sysc4.4 and file-sysc5.4, their helpers, loads and dumps; the gene's values 0-3; canon() reads a recorded 4 or 5 as 3. Tested: the engine preprocessed (gcc -E -P) byte-identical before and after at FSYS 0, 1, 2, 3 and unset - every remaining design builds the same engine; canon(fsys 5) gives 3; then batch-check. Applied at consolidation, after the final pick (queued, not pending - chain A's processing must not apply it).
