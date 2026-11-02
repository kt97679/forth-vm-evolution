# The after-seed-86 batch - to apply first at seed 86's processing (Iteration 583)

**Queued for consolidation** (Iteration 583) - not results/pending/, which process-run.sh applies at the next processing: moved there at consolidation, after the final pick, with the patches drafted then (results/drafts/retire-plan-583.md), and batch-check run again on that master.

process-run.sh checks and applies it.

    git apply results/queued-consolidation/fsys45-after-seed86.patch
    git apply results/queued-consolidation/freeze-after-seed86.patch

batch-check (582, on cbf4daa - 1 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**fsys45-after-seed86.patch** - consolidation's first retirement (GOALS.md step 3; 578's rule): fsys levels 4 and 5 - on no design of the pooled true front of seeds 77-86 (results/drafts/retire-report-583.md) and on none of the 232 final-pick candidates (results/drafts/retire-plan-583.md). Removes the engine's three FSYS >= 4 blocks (the Forth output buffer, SYSCALL -5 and -6), forth/file-sysc4.4 and file-sysc5.4, their helpers, loads and dumps; the gene's values 0-3; canon() reads a recorded 4 or 5 as 3. Tested: the engine preprocessed (gcc -E -P) byte-identical before and after at FSYS 0, 1, 2, 3 and unset - every remaining design builds the same engine; canon(fsys 5) gives 3; then batch-check. Applied at consolidation, after the final pick (queued, not pending - chain A's processing must not apply it).

**freeze-after-seed86.patch** (lab/evolve/evolve.py, stages/STAGES.md, stages/frozen/README.md, stages/frozen/SHA256SUMS, stages/frozen/s2-cpt16-32, stages/frozen/s2-cpt16-32.img, stages/frozen/s2-cpt16-64, stages/frozen/s2-cpt16-64.img, stages/frozen/s2-cpt16-k32.img, stages/frozen/s2-cpt16-k64.img, stages/frozen/s2-cpt16-s32.img, stages/frozen/s2-cpt16-s64.img, stages/frozen/s3-cpt16f-32, stages/frozen/s3-cpt16f-32.img, stages/frozen/s3-cpt16f-64, stages/frozen/s3-cpt16f-64.img, stages/frozen/s3-cpt16f-k32.img, stages/frozen/s3-cpt16f-k64.img, stages/frozen/s3-cpt16f-s32.img, stages/frozen/s3-cpt16f-s64.img, stages/frozen/s4-cv8-32, stages/frozen/s4-cv8-32.img, stages/frozen/s4-cv8-64, stages/frozen/s4-cv8-64.img, stages/frozen/s4-cv8-k32.img, stages/frozen/s4-cv8-k64.img, stages/frozen/s4-cv8-s32.img, stages/frozen/s4-cv8-s64.img, stages/frozen/s5-cv8spec-32, stages/frozen/s5-cv8spec-32.img, stages/frozen/s5-cv8spec-64, stages/frozen/s5-cv8spec-64.img, stages/frozen/s5-cv8spec-k32.img, stages/frozen/s5-cv8spec-k64.img, stages/frozen/s5-cv8spec-s32.img, stages/frozen/s5-cv8spec-s64.img, tools/build-stages.sh) - TODO: what it does, why, how it was tested.
