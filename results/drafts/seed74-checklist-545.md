# Seed 74's processing - the checklist (Iteration 545)

`seed 74 10h widths noevolved then experiment review-checks.py spread then experiment appbench.py --zip
~/Downloads/appbench.zip --sample 16 then experiment clockcheck.py --sample 8` at 8eda91e (Iteration 544) - the first
run of the after-seed-73 batch: adaptive operators, the true front in every report, one round first, the evolver
self-test, the JIT table's bounds, jitos unfrozen. The method changed: GOALS.md's stopping count starts here, at 10
hours. Then "Processing a returned seed" (HANDOFF.md), with these:

1. **The archive** about 13 MB - without the bundle and the binaries (541). clean-runs.sh tidied the laptop's runs/ at
   the chain's start: if the owner sends its output, only copies gone (repo.bundle, bins.tar.gz, chain tarballs past
   the newest two).
2. **The front** the reports show is the true one now (first_front by dominates()): `review-checks.py votes --db`
   gives the same size - every share and vote from either.
3. **Predictions** (results/predictions.md):
   - 526, adaptive operators: crossover under 20% of the children (seed 72: 36.6%); front entries per child at least
     0.85% (a fifth above seed 72's 185 of 26,100).
   - 527, the fronts reported: at least a quarter larger than the old staircase's on the same records - the old
     first_front is 7da6566's (`git show 7da6566:lab/evolve/evolve.py`).
   - 529, one round first: a quarter to two fifths of the children past the screen stop after one round; at least
     3,353 designs an hour (seed 72's 2,916 and 15%); no stopped child's audited full measurement on the final front.
   - 534, jitos: on the true front, and one of its designs at least in the fastest or the best-Q tenth.
4. **The hypervolume** - `python3 lab/evolve/hv.py <db>`: the stopping series' first run on the method (seed 73's
   0.34915 was on the old one - scale, not the count).
5. **The clock test** (open item 3), `clockcheck.md` in its pack: per block - alone, beside benchmarks, beside
   compiles - the time ratio and the core's clock; cycles only if the owner set kernel.perf_event_paranoid to 2 by
   hand. The offset is the clock if the cycle ratio holds where the time ratio moves; without cycles, does the time
   ratio follow the clock? Seed 75 repeats it with the chain's hold (the after-seed-74 batch).
6. **The votes**: jitrp 8 of 8 over 72-73 - a freeze candidate if seed 74 gives it three or four (11 of 12) with no
   keep vote; rtfuse not before seed 75's processing.
7. **Rule 5**: cpt16 designs failing the applications at 32 bits are expected (the reach, 517) - fail32 learns it with
   the after-seed-74 batch; before that, its ATTENTION for them is in name only.
8. **The after-seed-74 batch** (results/applied-after-seed74/ORDER.md): batch-check, then apply - no patch touches forth/kernel.4,
   no reseed.
9. **Seed 75's line**: `seed 75 10h widths noevolved then experiment review-checks.py spread then experiment
   appbench.py --zip ~/Downloads/appbench.zip --sample 16 then experiment clockcheck.py --sample 8 then experiment
   truefronts.py` - 10 hours, the method's; with the batch, next-run.sh asks for sudo once at the start, for the clock
   test's hold - tell the owner. truefronts.py last (547): every archived run's true front, read at seed 75's processing
   - the seed names checked by their share, then the progress table and the charts rebuilt on the true fronts.
