# The after-seed-75 batch - to apply first at seed 75's processing (Iterations 550-551)

Prepared while seed 75 runs; master stays what seed 75's bundle tests.

    git apply results/pending/truefronts-reported-after-seed75.patch
    git apply results/pending/process-tools-after-seed75.patch

batch-check (550): PASS with the first. Again with both (551): PROGRESS.md.

**truefronts-reported-after-seed75.patch** (lab/evolve/truefronts.py) - its "reported" column counted a results file's
genome records; from seed 74 those list the re-measured designs off the front too (seed 74: 261 for a front of 238),
the miscount the after-seed-74 batch fixed in progress-table.py. Now the front table's designs - and a variant's
results file (seed61b.md, say) names no run, as before. Tested on seeds 73-74's packs: reported 174 and 238, the true
fronts 222 and 238 as before. Seed 75's own truefronts.md still reads 261 for seed 74:
results/drafts/truefronts-tables-550.py counts the front tables itself.

**process-tools-after-seed75.patch** (lab/evolve/draft-results.py and lab/evolve/process-checks.sh new,
lab/evolve/README.md) - **the processing scripted** (the owner, Iteration 551): what seeds 73 and 74's processing did by
hand. draft-results.py writes the results file from process-seed.sh's output - the run's line and records, the true front
against the report's, the fixed-box hypervolume, the extremes, one round first, the operators, the JIT designs, the fast
end re-measured, the experiments' headlines (also from failed packs), the remote checks - with TODO lines for what a chat
judges; and the xcheck file and the spread's session. process-checks.sh runs the checks on master in their order, the
jail last, one status file, FROM= to resume. Changes nothing a run uses. Tested on seed 74's archive: the draft's figures
those of its hand-written results file (238 and 238, 0.35667, 28.4% and 885 audits, crossover 27.8%, JIT 50 and 23,
1.081 / 1.070 / 1.012); process-checks.sh from the gate on it: PROGRESS.md.

