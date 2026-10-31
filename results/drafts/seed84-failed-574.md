# Seed 84's chain failed - KeyError 'jithelp' in crossover(), 5 hours in (Iteration 574)

The archive: forth-vm-evolution-chain-d00ce78b1-fury-20261031-064058-failed_tar.gz - the chain at d00ce78b1 (Iteration
572), its line `seed 84 12h then experiment review-checks.py spread then experiment appbench.py ...` (carryall stripped
from the line; the run's WANT `seed 84 carryall at d00ce78b1, pop 256 gens 100000 rounds 3`). Status `failed`; both
experiment steps skipped after the failed run.

**Before the run - all as intended.** Tests PASS, the stages 7 of 7 IDENTICAL, the jail PASS; seeds 71-78 restored from
their packs (restore-archives.sh); carried in 14,202 designs, the strict fronts of 13 databases - the restore and the
count of databases as predicted (results/predictions.md, seed 84), the founders inside the predicted 12,000-15,000.

**Generation 0** - 01:35 to between 06:30 and 06:35, about 5 hours (predicted 3-4; carry-check's second a design would
say 3.9): 14,219 designs (7 hand-made, 10 founders, 14,202 carried), 14,163 alive, the front 297. By database:

| seed | archive | carried | died |
|---|---|---|---|
| 71 | archived-20261025-031425 | 985 | 55 (wrong output: apps) |
| 72 | archived-20261025-144518 | 821 | 0 |
| 73 | archived-20261026-025633 | 1,018 | 0 |
| 74 | archived-20261026-141341 | 1,050 | 0 |
| 75 | archived-20261027-014140 | 1,340 | 0 |
| 76 | archived-20261027-133126 | 1,295 | 0 |
| 77 | archived-20261028-023821 | 1,420 | 0 |
| 78 | archived-20261028-130255 | 953 | 0 |
| 79 | archived-20261029-040143 | 1,243 | 0 |
| 80 | archived-20261029-182437 | 1,371 | 0 |
| 81 | archived-20261030-043716 | 853 | 0 |
| 82 | archived-20261030-145521 | 1,088 | 0 |
| 83 | archived-20261031-012505 | 765 | 0 |

Seed 71's 55 deaths fit its run before Iteration 516 checked the applications' outputs (seed 71's front was selected
without that check); the 56th death is hand-made s2-cpt16 on apps (the known scale-1 reach). No other death.

**The failure.** breed()'s first crossover (evolve.py 1520): `KeyError: 'jithelp'`. Seeds 70-71 ran before Iteration 516
deleted jithelp, jitre and nocase; their genomes hold them (results/drafts/retired-genes-574.py: 161 and 210 records of
the results files, no later seed's), canon() kept dead keys, and crossover(a, b) reads b[k] for each key of a - a
seed-71 parent beside any newer genome fails (170 of 200 seeded crossovers). carryall (562) is the first run to carry
seed 71; carry-check builds and measures the pool but never breeds it, and seed 83's saw seeds 79-83 only. jithelp is a
dormant gene, so generation 0 measured those designs; only breeding read it. The fix: the after-seed-84 batch
(results/applied-after-seed84/ORDER.md, retired) - canon() keeps the current genes only, carry_pool() stops at once on a
genome off them.

**The remote checks** (seed 83's front, measured beside the run) all completed, the Spearman with the laptop's speeds
(seed 83's chain, results/xcheck-seed83.md, in brackets): dream 8-byte 0.971 (0.989), 32-bit 0.943 (0.932), 64-bit 0.985
(0.993); rage 0.953 on 16 designs (0.143 on 6) - 15 of them cross-built on fury by clang without the C library: the
after-seed-83 batch works on the laptop. Whether `tools/rage-check.sh` ran to PASS is not in the archive (HANDOFF, open
item 1). The rerun's chain runs them again.

**What it costs.** Generation 0's 5 hours: the rerun is a new commit, and next-run.sh resumes only at the same WANT (the
commit in it), so it starts fresh - generation 0 again about 5 hours, about 7 of 12 evolving. Its carry reads 14
databases: the failed run's own (archived at the rerun's start) adds no design - every one of its records is a design
of the other 13 fronts, carried once.
