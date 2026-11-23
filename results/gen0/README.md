# results/gen0 - each run's generation 0, for the next run's scale check (Iteration 746)

`seedN.jsonl.gz`: run N's generation-0 alive records - id, the JIT expressed, speed and speed at 32 bits, bytes, memory,
each workload's time (raw) and its time over s6's (t), a few genes - gzipped with mtime 0, about 1 MB. Written by
lab/evolve/scalecheck.py --extract when process-seed.sh summarises run N, and committed with its processing; read by the
next run's processing, which compares its generation 0 against the newest earlier one here (summary.md's scalecheck.py
section). The designs carried into both runs are read twice, unselected: one series reads 0.99-1.01 (seeds 95 -> 96
0.998), a code change shows (seeds 96 -> 97: the rest 1.061) - results/drafts/scalecheck-746.md.

- `seed97.jsonl.gz` - seed 97's (9,102 records), written at Iteration 746 from its pack: the reference for seed 98.
