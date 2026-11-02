# The after-seed-86 batch - to apply first at seed 86's processing (Iteration 583)

**Queued for consolidation** (Iteration 583) - not results/pending/, which process-run.sh applies at the next processing: moved there at consolidation, after the final pick, with the patches drafted then (results/drafts/retire-plan-583.md), and batch-check run again on that master.

process-run.sh checks and applies it.

    git apply results/queued-consolidation/fsys45-after-seed86.patch
    git apply results/queued-consolidation/freeze-after-seed86.patch

batch-check (582, on cbf4daa - 1 patches): PASS - run-tests PASS (the generators: 107 paths), validate 7 of 7 IDENTICAL,
the jail PASS.

**fsys45-after-seed86.patch** - consolidation's first retirement (GOALS.md step 3; 578's rule): fsys levels 4 and 5 - on no design of the pooled true front of seeds 77-86 (results/drafts/retire-report-583.md) and on none of the 232 final-pick candidates (results/drafts/retire-plan-583.md). Removes the engine's three FSYS >= 4 blocks (the Forth output buffer, SYSCALL -5 and -6), forth/file-sysc4.4 and file-sysc5.4, their helpers, loads and dumps; the gene's values 0-3; canon() reads a recorded 4 or 5 as 3. Tested: the engine preprocessed (gcc -E -P) byte-identical before and after at FSYS 0, 1, 2, 3 and unset - every remaining design builds the same engine; canon(fsys 5) gives 3; then batch-check. Applied at consolidation, after the final pick (queued, not pending - chain A's processing must not apply it).

**freeze-after-seed86.patch** - the older formats' retirement, step 1 (results/drafts/retire-stages-584.md; the owner, 584: "if it will not lose good designs"): s2-s5's engines and images at 8- and 4-byte cells kept in stages/frozen/ (32 files, 1.1 MB; SHA256SUMS; README.md names the build - Iteration 587's master, ee7a0ee, by build-stages.sh - the same bytes as master's own build in any directory). tools/build-stages.sh copies them instead of building them, where they run: an x86 Linux host, at the widths it builds (the Tegra gets none - no tool there uses them), one layout variant. evolve.py --validate checks each one's engine and self image against SHA256SUMS and runs them on the corpus and the kernel workload; s0, s1 and s6 rebuilt as before - 7 of 7. The tools that read s2-s5 read them in build/ as before; the three that build them - test-ext-loops.sh (images), layout-noise.sh (s5's engine), arm-cross-check.py (the genomes) - are unchanged, the source still building them: the gene patch that retires a value one uses moves it. Tested: TESTED.
