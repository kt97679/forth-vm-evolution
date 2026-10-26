# The after-seed-75 batch - to apply at seed 75's processing (Iteration 550)

Prepared while seed 75 runs; master stays what seed 75's bundle tests.

    git apply results/pending/truefronts-reported-after-seed75.patch

batch-check (550): PASS - applied to a fresh clone, run-tests, validate 7 of 7 IDENTICAL, the jail.

**truefronts-reported-after-seed75.patch** (lab/evolve/truefronts.py) - its "reported" column counted a results file's
genome records; from seed 74 those list the re-measured designs off the front too (seed 74: 261 for a front of 238),
the miscount the after-seed-74 batch fixed in progress-table.py. Now the front table's designs - and a variant's
results file (seed61b.md, say) names no run, as before. Tested on seeds 73-74's packs: reported 174 and 238, the true
fronts 222 and 238 as before. Seed 75's own truefronts.md still reads 261 for seed 74:
results/drafts/truefronts-tables-550.py counts the front tables itself.
