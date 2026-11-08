# Seed 89's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 627)

`python3 lab/evolve/final-pick.py results/followup-seed89.md results/chain-followup89/s1/loadtest.md results/chain-followup89/s1/*.out.json --also-session results/chain-followup89/s2 ... s20` - the laptop 18 sessions (10 rounds), dream 20 at 8-byte cells and 20 at 4-byte, the Tegra 3 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-611.md: results/followup-roles-seed89.md.

# The final set, re-measured - 52 candidates, 52 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup89/s2, results/chain-followup89/s3, results/chain-followup89/s4, results/chain-followup89/s5, results/chain-followup89/s6, results/chain-followup89/s7, results/chain-followup89/s8, results/chain-followup89/s9, results/chain-followup89/s10, results/chain-followup89/s11, results/chain-followup89/s12, results/chain-followup89/s13, results/chain-followup89/s14, results/chain-followup89/s15, results/chain-followup89/s16, results/chain-followup89/s17, results/chain-followup89/s18, results/chain-followup89/s19, results/chain-followup89/s20 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | c7c35f9c97 | fastest | 0.1480 (0.1476) | 38,898 | 244 | 0.1897 (0.1881) | 0.925 | 0.09063 |
| 2 | efb0fece07 | smallest | 1.6765 (1.7113) | 13,709 | 116 | 2.1873 (2.1871) | 1.009 | 0.00878 |
| 3 | fb0d57c8a2 | least memory | 0.8256 (0.8244) | 17,830 | 104 | 0.7720 (0.7667) | 1.003 | 0.07288 |
| 4 | 68f5ce466c | fastest at 32 bits | 0.1673 (0.1520) | 42,686 | 236 | 0.1765 (0.1599) | 0.925 | 0.00821 |
| 5 | 3eb59b271d | adds the most, the knee | 0.3391 (0.3188) | 22,522 | 132 | 0.3439 (0.3220) | 0.971 | 0.09716 |
| 6 | b9ae4e3f98 | adds the most | 0.2158 (0.2034) | 29,070 | 196 | 0.2257 (0.2075) | 0.955 | 0.02688 |
| 7 | 27b45a79ca | adds the most | 0.4573 (0.4406) | 17,156 | 116 | 0.5005 (0.4794) | 0.982 | 0.01749 |
| 8 | 88233c0551 | adds the most | 0.1755 (0.1587) | 31,550 | 220 | 0.1912 (0.1715) | 0.941 | 0.00672 |
| 9 | e523a45566 | adds the most | 0.3045 (0.2891) | 33,195 | 136 | 0.3121 (0.2910) | 0.965 | 0.00481 |
| 10 | 7a7edb5b0e | adds the most | 0.7824 (0.7877) | 15,173 | 108 | 0.7100 (0.7062) | 1.000 | 0.00468 |

Against the in-run set: in now 27b45a79ca, 3eb59b271d, 68f5ce466c, 7a7edb5b0e, 88233c0551, b9ae4e3f98, c7c35f9c97, e523a45566, efb0fece07, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest c7c35f9c97; smallest efb0fece07; least memory fb0d57c8a2; fastest at 32 bits 68f5ce466c; in the set under load only c6f1c1331b, alone only 88233c0551.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.208; Spearman with the laptop alone 0.882 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, ee34931cd7, 1d8000a2c1, d8471f1b16, a1a38c35bd.

dream (8-byte cells): 52 candidates measured; its fastest ee34931cd7 0.218; Spearman with the laptop alone 0.973 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, ec54004b67, d8471f1b16.

rage (4-byte cells): 52 candidates measured; its fastest 3eb59b271d 0.321; Spearman with the laptop alone -0.031 over 52; FLAGGED, among its fastest five and not in the set: 768bd275d8, ff56712222, 690981ca5b.

dream (4-byte cells): 52 candidates measured; its fastest ee34931cd7 0.202; Spearman with the laptop alone 0.881 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, ec54004b67, a1a38c35bd, 4ef851fd8e, b969aa7bd8.

dream (8-byte cells): 52 candidates measured; its fastest ee34931cd7 0.218; Spearman with the laptop alone 0.973 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, 1d8000a2c1, b969aa7bd8, ec54004b67, d8471f1b16.

rage (4-byte cells): 52 candidates measured; its fastest 3eb59b271d 0.316; Spearman with the laptop alone -0.018 over 52; FLAGGED, among its fastest five and not in the set: 768bd275d8, 690981ca5b, ff56712222.

dream (4-byte cells): 52 candidates measured; its fastest ec54004b67 0.211; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: ec54004b67, ee34931cd7, a1a38c35bd, b969aa7bd8.

dream (8-byte cells): 52 candidates measured; its fastest 68f5ce466c 0.217; Spearman with the laptop alone 0.972 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, d8471f1b16, 1d8000a2c1.

rage (4-byte cells): 52 candidates measured; its fastest 3eb59b271d 0.322; Spearman with the laptop alone -0.039 over 52; FLAGGED, among its fastest five and not in the set: 768bd275d8, 690981ca5b, ff56712222.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.211; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, d8471f1b16, ec54004b67, ee34931cd7.

dream (8-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.217; Spearman with the laptop alone 0.974 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, d8471f1b16, 1d8000a2c1, ec54004b67.

dream (4-byte cells): 52 candidates measured; its fastest d8471f1b16 0.208; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, ee34931cd7, b969aa7bd8, a1a38c35bd.

dream (8-byte cells): 52 candidates measured; its fastest ee34931cd7 0.218; Spearman with the laptop alone 0.974 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, d8471f1b16, 1d8000a2c1.

dream (4-byte cells): 52 candidates measured; its fastest d8471f1b16 0.210; Spearman with the laptop alone 0.883 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, b969aa7bd8, a1a38c35bd, ee34931cd7, ec54004b67.

dream (8-byte cells): 52 candidates measured; its fastest ee34931cd7 0.208; Spearman with the laptop alone 0.974 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, 1d8000a2c1, d8471f1b16, b969aa7bd8, ec54004b67.

dream (4-byte cells): 52 candidates measured; its fastest ee34931cd7 0.211; Spearman with the laptop alone 0.885 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, d8471f1b16, 1d8000a2c1.

dream (8-byte cells): 52 candidates measured; its fastest d8471f1b16 0.216; Spearman with the laptop alone 0.974 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, ec54004b67, b969aa7bd8, 1d8000a2c1.

dream (4-byte cells): 52 candidates measured; its fastest d8471f1b16 0.209; Spearman with the laptop alone 0.883 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, b969aa7bd8, ee34931cd7, ec54004b67.

dream (8-byte cells): 52 candidates measured; its fastest 1d8000a2c1 0.216; Spearman with the laptop alone 0.973 over 52; FLAGGED, among its fastest five and not in the set: 1d8000a2c1, ec54004b67, b969aa7bd8, ee34931cd7, d8471f1b16.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.211; Spearman with the laptop alone 0.885 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, ec54004b67, d8471f1b16, ee34931cd7.

dream (8-byte cells): 52 candidates measured; its fastest ec54004b67 0.210; Spearman with the laptop alone 0.974 over 52; FLAGGED, among its fastest five and not in the set: ec54004b67, d8471f1b16, ee34931cd7, 1d8000a2c1.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.210; Spearman with the laptop alone 0.886 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, ee34931cd7, ec54004b67, d8471f1b16.

dream (8-byte cells): 52 candidates measured; its fastest ec54004b67 0.213; Spearman with the laptop alone 0.974 over 52; FLAGGED, among its fastest five and not in the set: ec54004b67, d8471f1b16, ee34931cd7, 1d8000a2c1, b969aa7bd8.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.212; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, ec54004b67, d8471f1b16, ee34931cd7.

dream (8-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.213; Spearman with the laptop alone 0.975 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, d8471f1b16, ee34931cd7, ec54004b67.

dream (4-byte cells): 52 candidates measured; its fastest ee34931cd7 0.212; Spearman with the laptop alone 0.883 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, 1d8000a2c1, d8471f1b16, a1a38c35bd.

dream (8-byte cells): 52 candidates measured; its fastest 1d8000a2c1 0.212; Spearman with the laptop alone 0.973 over 52; FLAGGED, among its fastest five and not in the set: 1d8000a2c1, ee34931cd7, d8471f1b16, b969aa7bd8.

dream (4-byte cells): 52 candidates measured; its fastest ee34931cd7 0.212; Spearman with the laptop alone 0.885 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, d8471f1b16, ec54004b67, 1d8000a2c1.

dream (8-byte cells): 52 candidates measured; its fastest ec54004b67 0.213; Spearman with the laptop alone 0.970 over 52; FLAGGED, among its fastest five and not in the set: ec54004b67, 1d8000a2c1, d8471f1b16, ee34931cd7.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.212; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, ec54004b67, a1a38c35bd, ee34931cd7.

dream (8-byte cells): 52 candidates measured; its fastest 68f5ce466c 0.215; Spearman with the laptop alone 0.975 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, ec54004b67, d8471f1b16, ee34931cd7.

dream (4-byte cells): 52 candidates measured; its fastest d8471f1b16 0.213; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, ec54004b67, ee34931cd7, a1a38c35bd.

dream (8-byte cells): 52 candidates measured; its fastest d8471f1b16 0.213; Spearman with the laptop alone 0.977 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, b969aa7bd8, ee34931cd7, ec54004b67, 1d8000a2c1.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.210; Spearman with the laptop alone 0.886 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, d8471f1b16, ee34931cd7, ec54004b67.

dream (8-byte cells): 52 candidates measured; its fastest 1d8000a2c1 0.212; Spearman with the laptop alone 0.971 over 52; FLAGGED, among its fastest five and not in the set: 1d8000a2c1, ec54004b67, ee34931cd7, b969aa7bd8.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.210; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, ec54004b67, d8471f1b16, a1a38c35bd, ee34931cd7.

dream (8-byte cells): 52 candidates measured; its fastest ee34931cd7 0.216; Spearman with the laptop alone 0.973 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, d8471f1b16, b969aa7bd8, ec54004b67, 1d8000a2c1.

dream (4-byte cells): 52 candidates measured; its fastest d8471f1b16 0.211; Spearman with the laptop alone 0.885 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, ec54004b67, b969aa7bd8, ee34931cd7.

dream (8-byte cells): 52 candidates measured; its fastest ee34931cd7 0.214; Spearman with the laptop alone 0.973 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, d8471f1b16, 1d8000a2c1.

dream (4-byte cells): 52 candidates measured; its fastest ee34931cd7 0.211; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, a1a38c35bd, d8471f1b16, ec54004b67.

dream (8-byte cells): 52 candidates measured; its fastest ee34931cd7 0.212; Spearman with the laptop alone 0.973 over 52; FLAGGED, among its fastest five and not in the set: ee34931cd7, b969aa7bd8, ec54004b67, 1d8000a2c1, d8471f1b16.

dream (4-byte cells): 52 candidates measured; its fastest b969aa7bd8 0.210; Spearman with the laptop alone 0.884 over 52; FLAGGED, among its fastest five and not in the set: b969aa7bd8, d8471f1b16, ee34931cd7, 1d8000a2c1, ec54004b67.

dream (8-byte cells): 52 candidates measured; its fastest d8471f1b16 0.216; Spearman with the laptop alone 0.975 over 52; FLAGGED, among its fastest five and not in the set: d8471f1b16, ee34931cd7, b969aa7bd8, ec54004b67.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | ee34931cd7 | 0.1894 | 0.1933 | 0.4763* | 0.2593 | x86-64 +3%, ARMv7 +49% | ADDED |
| 2 | d8471f1b16 | 0.1894 | 0.1939 | 0.4776* | 0.2598 | x86-64 +3%, ARMv7 +49% | ADDED |
| 3 | b969aa7bd8 | 0.1896 | 0.1936 | 0.4794* | 0.2601 | x86-64 +3%, ARMv7 +50% | ADDED |
| 4 | 68f5ce466c | 0.1908 | 0.1939 | 0.4802* | 0.2609 | x86-64 +4%, ARMv7 +50% | yes |
| 5 | ec54004b67 | 0.1902 | 0.1947 | 0.4838* | 0.2617 | x86-64 +3%, x86-32 +1%, ARMv7 +51% | - |
| 6 | 06b188f45b | 0.1932 | 0.2014 | 0.4652* | 0.2625 | x86-64 +5%, x86-32 +4%, ARMv7 +45% | - |
| 7 | 1d8000a2c1 | 0.1905 | 0.1964 | 0.4852* | 0.2628 | x86-64 +3%, x86-32 +2%, ARMv7 +52% | - |
| 8 | a1a38c35bd | 0.1963 | 0.1958 | 0.4821* | 0.2646 | x86-64 +7%, x86-32 +1%, ARMv7 +51% | - |
| 9 | 4ef851fd8e | 0.1957 | 0.1996 | 0.5094* | 0.2710 | x86-64 +6%, x86-32 +3%, ARMv7 +59% | - |
| 10 | 88233c0551 | 0.1997 | 0.2090 | 0.4939* | 0.2742 | x86-64 +8%, x86-32 +8%, ARMv7 +54% | yes |
| 11 | c7c35f9c97 | 0.1842 | 0.2079 | 0.5407* | 0.2746 | x86-32 +8%, ARMv7 +69% | yes |
| 12 | 717756aa37 | 0.2094 | 0.2106 | 0.5566* | 0.2906 | x86-64 +14%, x86-32 +9%, ARMv7 +74% | - |
| 13 | b9ae4e3f98 | 0.2403 | 0.2438 | 0.6339* | 0.3336 | x86-64 +30%, x86-32 +26%, ARMv7 +98% | yes |
| 14 | e523a45566 | 0.3570 | 0.4166 | 0.3253 | 0.3644 | x86-64 +94%, x86-32 +116%, ARMv7 +2% | yes |
| 15 | 3eb59b271d | 0.3779 | 0.4435 | 0.3198 | 0.3770 | x86-64 +105%, x86-32 +129% | yes |
| 16 | 27b45a79ca | 0.5283 | 0.5852 | 0.4154 | 0.5045 | x86-64 +187%, x86-32 +203%, ARMv7 +30% | yes |
| 17 | 7a7edb5b0e | 0.8878 | 0.7809 | 0.5595 | 0.7293 | x86-64 +382%, x86-32 +304%, ARMv7 +75% | yes |
| 18 | fb0d57c8a2 | 0.9144 | 0.8870 | 0.5235 | 0.7516 | x86-64 +396%, x86-32 +359%, ARMv7 +64% | yes |
| 19 | efb0fece07 | 2.0170 | 2.3859 | 1.9776 | 2.1192 | x86-64 +995%, x86-32 +1134%, ARMv7 +518% | yes |

**The generic pick**: none within the veto - the best mean ee34931cd7 named instead.
Each class's fastest: x86-64 c7c35f9c97; x86-32 ee34931cd7; ARMv7 3eb59b271d.
**Added to the set across machines** (never taken out): ee34931cd7 - across machines: the best mean #1; d8471f1b16 - across machines: the best mean #2; b969aa7bd8 - across machines: the best mean #3.
