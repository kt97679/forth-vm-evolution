# The method section's figures, recomputed (Iteration 600; results/drafts/article-figures-600.py)

## The genome (lab/evolve/evolve.py, after consolidation - 599)

84 genes; 9 frozen at one value (bytehdr, doesfar, kstack, lean, scale, sharedcall, tail, tailpn, varcall); 75 free.

## The runs from seed 77 (the ledger's true fronts; each results file's counts)

Speeds are against the hand-made s6 of the same commit (lower is faster); hv the hypervolume in the fixed box.

| seed | kind | hours | generations | designs | an hour | ok | stopped after one round | screened | true front | hv | fastest | fastest 32-bit | smallest bytes | memory KB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 77 | series | 12 | 161 | 41,308 | 3,442 | 26,519 | 9,925 | 4,836 | 370 | 0.3501 | 0.1406 | 0.1702 | 14,015 | 108 |
| 78 | series | 9 | 126 | 32,394 | 3,599 | 19,303 | 7,488 | 5,209 | 182 | 0.3395 | 0.1477 | 0.1818 | 14,189 | 108 |
| 79 | series | 12 | 177 | 45,419 | 3,784 | 26,537 | 12,059 | 6,456 | 257 | 0.3517 | 0.1378 | 0.1643 | 14,055 | 112 |
| 80 | series | 12 | 178 | 45,696 | 3,808 | 26,610 | 11,794 | 6,934 | 258 | 0.3364 | 0.1439 | 0.1758 | 13,989 | 112 |
| 81 | series | 9 | 128 | 32,906 | 3,656 | 19,153 | 7,858 | 5,524 | 215 | 0.3475 | 0.1377 | 0.1691 | 14,210 | 112 |
| 82 | series | 9 | 126 | 32,396 | 3,599 | 19,721 | 7,496 | 4,836 | 246 | 0.3315 | 0.1378 | 0.1683 | 14,043 | 108 |
| 83 | series | 9 | 126 | 32,400 | 3,600 | 19,011 | 8,578 | 4,430 | 180 | 0.3358 | 0.1459 | 0.1782 | 14,187 | 108 |
| 84 | confirmation | 12 | 94 | 38,270 | 3,189 | 27,873 | 7,025 | 3,196 | 389 | 0.3656 | 0.1325 | 0.1648 | 13,973 | 108 |
| 85 | random | 10 | 140 | 35,760 | 3,576 | - | - | - | 30 | 0.1878 | 0.3200 | 0.3806 | 16,446 | 116 |
| 86 | confirmation | 12 | 91 | 38,853 | 3,237 | 28,006 | 6,958 | 3,749 | 320 | 0.3693 | 0.1330 | 0.1645 | 13,939 | 104 |

**The series** (seeds 77-83, 7 runs, the rule's): median (range) - hours 9 (9-12); generations 128 (126-178); designs 32906 (32394-45696); true front 246 (180-370); hv 0.3395 (0.3315-0.3517); fastest 0.1406 (0.1377-0.1477); fastest 32-bit 0.1702 (0.1643-0.1818); smallest 14055 (13989-14210) bytes; memory 108 (108-112) KB.

## The shortcuts' audits, and the checks (each results file)

| seed | stopped after one round | of them audited in full | on the front | screened | of them audited | on the front | the fast ten re-measured / in-run | JIT | the rest | held out: Spearman |
|---|---|---|---|---|---|---|---|---|---|---|
| 77 | 9,925 | 1061 | 0 | 4,836 | 28 | 0 | 1.061 | 1.047 | 0.992 | 0.955 |
| 78 | 7,488 | 779 | 0 | 5,209 | 80 | 0 | 1.063 | 1.053 | 1.009 | 0.94 |
| 79 | 12,059 | 1315 | 0 | 6,456 | 75 | 1 | 1.063 | 1.044 | 1.016 | 0.954 |
| 80 | 11,794 | 1224 | 0 | 6,934 | 59 | 0 | 1.068 | 1.039 | 1.002 | 0.952 |
| 81 | 7,858 | 829 | 0 | 5,524 | 77 | 1 | 1.064 | 1.034 | 0.999 | 0.979 |
| 82 | 7,496 | 780 | 0 | 4,836 | 57 | 0 | 1.051 | 1.035 | 0.991 | 0.969 |
| 83 | 8,578 | 946 | 0 | 4,430 | 45 | 0 | 1.073 | 1.057 | 0.998 | 0.959 |
| 84 | 7,025 | 743 | 0 | 3,196 | 9 | 0 | 1.052 | 1.043 | 0.995 | 0.94 |
| 85 | - | 0 | 0 | - | None | None | 1.022 | 1.02 | 0.998 | 0.859 |
| 86 | 6,958 | 773 | 0 | 3,749 | 29 | 2 | 1.062 | 1.038 | 0.996 | 0.951 |

Seeds 77-86 but the random one: stopped after one round 79,181 of 339,642 designs; audited in full 8,450, on the front 0; screened 45,170, audited 459, on the front 4.

The series alone: stopped after one round 65,198 of 262,519 designs (7,488-12,059 a run); audited in full 6,934, on the front 0; screened 38,225 (4,430-6,934 a run), audited and run in full 421, on the front 2; the fast ten re-measured / in-run 1.051-1.073, the JIT designs 1.034-1.057, the rest 0.991-1.016; held out (sieve) Spearman 0.940-0.979.

**The random baseline** (seed 85, 10 hours, 140 generations): hv 0.1878 - 0.55 of the series' median at their ends (0.3395); fastest 0.3200 (the series' median 0.1406), fastest 32-bit 0.3806 (0.1702), smallest 16,446 bytes (14,055), memory 116 KB (108); true front 30 designs (246).

## The final set (results/final-set-chainsBCD-seed86.md - the laptop alone, every session's geometric mean)

21 designs. Fastest 4df5b46d00 0.1473 (6.79 times s6's speed); fastest at 32 bits 5050960bac 0.1811; smallest cea114f47e 13,939 bytes; least memory fb0d57c8a2 104 KB.

## Across machines (the shortlist's 40; every session pooled - chains B, C, D)

The laptop's fastest alone at 64 bits: 4df5b46d00.

| host | sessions | Spearman with the laptop alone, pooled | its fastest | the laptop's fastest there, behind it |
|---|---|---|---|---|
| dream.lan-prebuilt32 | 42 | 0.917 | 4ef851fd8e 0.2161 | +6.9% |
| dream.lan-prebuilt64 | 42 | 0.472 | 4ef851fd8e 0.2236 | +6.2% |
| rage.lan-prebuiltarm | 6 | 0.082 | 690981ca5b 0.3270 | +59.2% |
