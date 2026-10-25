# Seed 73's processing - a checklist written before its results (Iteration 532)

Seed 73: `seed 73 11h widths noevolved then experiment review-checks.py spread then experiment appbench.py --zip
~/Downloads/appbench.zip --sample 16`, at the bundle of 520 - jitexec's table fixed (its first fair run), the memory
objective without the applications' data. Its own code still has the old front shortcut (fixed in the after-seed-73
batch), so its results file's front is not the true one.

## What compares

- Speed with seeds 71 and 72 (seven workloads each); sizes with every run.
- **Memory with no run since 70**: seeds 71-72's memory was the applications' data (460-500 KB for every design);
  seed 73's is the six old workloads' again - expect the front's least memory near 100-140 KB.
- **The front**: the results file's (the shortcut's) and the true one (review-checks.py votes --db, or the batch's
  first_front) - record both sizes, use the true one for every share and vote.

## What it settles

- **jitexec, fairly weighed (prediction 518)**: on at least a quarter of the true front's JIT designs, most of its
  fastest tenth.
- **jitfuse's votes count from 73** (rule 12); jitexec's from 74.
- The votes (process-seed.sh passes --db now): the ledger's 70-72 rows were rewritten from the runs' records (532), so
  the window 71-73 is the true fronts' throughout.

## The batch

results/pending/ORDER.md - six patches: adaptive operators, the bug-hunt fixes, one round first, the evolver
self-test, the JIT table's bounds, jitos unfrozen (534; the freeze withdrawn at 533). batch-check ran at 532 with the freeze among them -
**run it again**, then the routine's chain. **The freeze question**: the votes over 71-73 decide - rtimm is a candidate
if seed 73 gives it 4 of 4 with no keep vote; rtfuse cannot be before seed 75's processing.

## Seed 74's line

`seed 74 <hours>h widths noevolved then experiment review-checks.py spread then experiment appbench.py --zip
~/Downloads/appbench.zip --sample 16 then experiment clockcheck.py --sample 8` - cycles need perf-hold-start.sh run
first, as for the counters step. Seed 74 will show: stopped children (one round first), the operators' line each
generation, the reported fronts by the true rule (predictions 526, 527, 529).
