# Seed 96-roles-c's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 716)

`python3 lab/evolve/final-pick.py results/followup-seed96-roles-c.md results/chain-followup96-roles-c/s1/loadtest.md results/chain-followup96-roles-c/s1/*.out.json --also-session results/chain-followup96-roles-c/s2 ... s11` - the laptop 6 sessions (10 rounds), dream 11 at 8-byte cells and 11 at 4-byte, the Tegra 2 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-657.md: results/followup-roles-seed96-roles-c.md.

# The final set, re-measured - 66 candidates, 66 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup96-roles-c/s2, results/chain-followup96-roles-c/s3, results/chain-followup96-roles-c/s4, results/chain-followup96-roles-c/s5, results/chain-followup96-roles-c/s6, results/chain-followup96-roles-c/s7, results/chain-followup96-roles-c/s8, results/chain-followup96-roles-c/s9, results/chain-followup96-roles-c/s10, results/chain-followup96-roles-c/s11 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 262a51bc6c | fastest | 0.1271 (0.1315) | 54,551 | 292 | 0.1638 (0.1659) | 0.934 | 0.01391 |
| 2 | 3456fc28b2 | smallest | 1.0480 (1.0562) | 21,666 | 116 | 1.1882 (1.2035) | 1.005 | 0.04663 |
| 3 | 71005d8a0d | least memory | 0.6223 (0.6108) | 25,401 | 112 | 0.6495 (0.6450) | 0.997 | 0.06447 |
| 4 | 11f956db93 | fastest at 32 bits | 0.1487 (0.1505) | 49,925 | 264 | 0.1581 (0.1612) | 0.936 | 0.01944 |
| 5 | 3eb59b271d | adds the most, the knee | 0.3293 (0.3181) | 30,244 | 132 | 0.3375 (0.3209) | 0.969 | 0.07692 |
| 6 | 15eda54ebd | adds the most | 0.1898 (0.1924) | 36,344 | 208 | 0.2113 (0.2140) | 0.951 | 0.03299 |
| 7 | ae99617f06 | adds the most | 0.4143 (0.4078) | 26,261 | 124 | 0.4125 (0.4095) | 0.974 | 0.00914 |
| 8 | 5f7e66b12d | adds the most | 0.2764 (0.2832) | 34,056 | 148 | 0.3156 (0.3276) | 0.976 | 0.00636 |
| 9 | 4acee9a48e | adds the most | 0.5229 (0.5215) | 23,742 | 128 | 0.5237 (0.5286) | 0.992 | 0.00439 |
| 10 | c7c35f9c97 | adds the most | 0.1461 (0.1464) | 47,214 | 240 | 0.1809 (0.1838) | 0.928 | 0.00383 |

Against the in-run set: in now 11f956db93, 15eda54ebd, 262a51bc6c, 3456fc28b2, 3eb59b271d, 4acee9a48e, 5f7e66b12d, 71005d8a0d, ae99617f06, c7c35f9c97; out now none - both kept as candidates.
Under load: the extremes fastest 262a51bc6c; smallest 3456fc28b2; least memory 71005d8a0d; fastest at 32 bits 69cebcaed9; in the set under load only 69cebcaed9, d727605472, alone only 11f956db93, 5f7e66b12d.

dream (4-byte cells): 66 candidates measured; its fastest 163935642a 0.204; Spearman with the laptop alone 0.943 over 66; FLAGGED, among its fastest five and not in the set: 163935642a, 69cebcaed9, ea782c6094, b525180392.

dream (8-byte cells): 66 candidates measured; its fastest 262a51bc6c 0.199; Spearman with the laptop alone 0.972 over 66; FLAGGED, among its fastest five and not in the set: 9b15ba26f7, df097ba2e2, b5c79bff7e, ea782c6094.

rage (4-byte cells): 34 candidates measured; its fastest ae99617f06 0.325; Spearman with the laptop alone 0.724 over 34; FLAGGED, among its fastest five and not in the set: d727605472, e51c01ba10.

dream (4-byte cells): 66 candidates measured; its fastest 69cebcaed9 0.202; Spearman with the laptop alone 0.946 over 66; FLAGGED, among its fastest five and not in the set: 69cebcaed9, ea782c6094, b525180392, 163935642a, 9b15ba26f7.

dream (8-byte cells): 66 candidates measured; its fastest 262a51bc6c 0.194; Spearman with the laptop alone 0.978 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, b5c79bff7e, ea782c6094.

rage (4-byte cells): 34 candidates measured; its fastest 5f7e66b12d 0.321; Spearman with the laptop alone 0.532 over 34; FLAGGED, among its fastest five and not in the set: d727605472, e51c01ba10.

dream (4-byte cells): 66 candidates measured; its fastest 69cebcaed9 0.204; Spearman with the laptop alone 0.948 over 66; FLAGGED, among its fastest five and not in the set: 69cebcaed9, ea782c6094, 163935642a, b525180392.

dream (8-byte cells): 66 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.979 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, 69cebcaed9, ea782c6094.

dream (4-byte cells): 66 candidates measured; its fastest 69cebcaed9 0.204; Spearman with the laptop alone 0.953 over 66; FLAGGED, among its fastest five and not in the set: 69cebcaed9, 163935642a, ea782c6094, b525180392.

dream (8-byte cells): 66 candidates measured; its fastest df097ba2e2 0.196; Spearman with the laptop alone 0.981 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, b525180392, b5c79bff7e.

dream (4-byte cells): 66 candidates measured; its fastest ea782c6094 0.203; Spearman with the laptop alone 0.953 over 66; FLAGGED, among its fastest five and not in the set: ea782c6094, 163935642a, 69cebcaed9, b525180392.

dream (8-byte cells): 66 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.978 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, b5c79bff7e.

dream (4-byte cells): 66 candidates measured; its fastest 163935642a 0.204; Spearman with the laptop alone 0.944 over 66; FLAGGED, among its fastest five and not in the set: 163935642a, ea782c6094, 69cebcaed9, b5c79bff7e.

dream (8-byte cells): 66 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.972 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, ea782c6094, 69cebcaed9.

dream (4-byte cells): 66 candidates measured; its fastest 69cebcaed9 0.205; Spearman with the laptop alone 0.958 over 66; FLAGGED, among its fastest five and not in the set: 69cebcaed9, 163935642a, ea782c6094, b525180392.

dream (8-byte cells): 66 candidates measured; its fastest df097ba2e2 0.195; Spearman with the laptop alone 0.978 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, ea782c6094, b525180392.

dream (4-byte cells): 66 candidates measured; its fastest 163935642a 0.204; Spearman with the laptop alone 0.957 over 66; FLAGGED, among its fastest five and not in the set: 163935642a, 69cebcaed9, ea782c6094, b525180392.

dream (8-byte cells): 66 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.979 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, b525180392, ea782c6094.

dream (4-byte cells): 66 candidates measured; its fastest ea782c6094 0.205; Spearman with the laptop alone 0.953 over 66; FLAGGED, among its fastest five and not in the set: ea782c6094, 163935642a, 69cebcaed9, b525180392.

dream (8-byte cells): 66 candidates measured; its fastest 262a51bc6c 0.198; Spearman with the laptop alone 0.977 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, b5c79bff7e, ea782c6094.

dream (4-byte cells): 66 candidates measured; its fastest 262a51bc6c 0.203; Spearman with the laptop alone 0.936 over 66; FLAGGED, among its fastest five and not in the set: 69cebcaed9, ea782c6094, df097ba2e2.

dream (8-byte cells): 66 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.985 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, ea782c6094, b525180392.

dream (4-byte cells): 66 candidates measured; its fastest ea782c6094 0.204; Spearman with the laptop alone 0.950 over 66; FLAGGED, among its fastest five and not in the set: ea782c6094, 163935642a, 69cebcaed9, b525180392, 9b15ba26f7.

dream (8-byte cells): 66 candidates measured; its fastest df097ba2e2 0.200; Spearman with the laptop alone 0.974 over 66; FLAGGED, among its fastest five and not in the set: df097ba2e2, 9b15ba26f7, b525180392, b5c79bff7e.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | d727605472 | 0.3168 | 0.3148 | 0.3280 | 0.3198 | x86-64 +100%, x86-32 +75%, ARMv7 +1% | ADDED |
| 2 | 5f7e66b12d | 0.3119 | 0.3257 | 0.3232 | 0.3202 | x86-64 +97%, x86-32 +81% | yes |
| 3 | ae99617f06 | 0.4526 | 0.4430 | 0.3243 | 0.4021 | x86-64 +185%, x86-32 +146% | yes |
| 4 | e51c01ba10 | 0.4993 | 0.4628 | 0.5512 | 0.5031 | x86-64 +215%, x86-32 +157%, ARMv7 +71% | - |
| 5 | 4acee9a48e | 0.5944 | 0.6167 | 0.4469 | 0.5472 | x86-64 +275%, x86-32 +243%, ARMv7 +38% | yes |
| 6 | 6e5c5bfe12 | 1.1031 | 0.9930 | 0.8913 | 0.9920 | x86-64 +595%, x86-32 +452%, ARMv7 +176% | - |
| 7 | b4f9afac29 | 1.1622 | 1.0499 | 1.0396 | 1.0825 | x86-64 +633%, x86-32 +484%, ARMv7 +222% | - |
| 8 | 340c985752 | 1.2888 | 1.2118 | 1.1541 | 1.2170 | x86-64 +712%, x86-32 +574%, ARMv7 +257% | - |
| 9 | 90273721a1 | 1.3161 | 1.2576 | 1.2336 | 1.2686 | x86-64 +730%, x86-32 +599%, ARMv7 +282% | - |
| 10 | 3456fc28b2 | 1.3171 | 1.3515 | 1.2814 | 1.3163 | x86-64 +730%, x86-32 +651%, ARMv7 +296% | yes |
| 11 | 3a63ab4b58 | 1.3316 | 1.3303 | 1.2970 | 1.3195 | x86-64 +739%, x86-32 +639%, ARMv7 +301% | - |
| 12 | 7086a9627c | 1.3278 | 1.3331 | 1.3041 | 1.3216 | x86-64 +737%, x86-32 +641%, ARMv7 +303% | - |
| 13 | 262a51bc6c | 0.1586 | 0.1851 | - | 0.1714 (partial) | x86-32 +3% | yes |
| 14 | 11f956db93 | 0.1755 | 0.1804 | - | 0.1779 (partial) | x86-64 +11% | yes |
| 15 | 69cebcaed9 | 0.1762 | 0.1799 | - | 0.1781 (partial) | x86-64 +11% | ADDED |
| 16 | c7c35f9c97 | 0.1800 | 0.2012 | - | 0.1903 (partial) | x86-64 +13%, x86-32 +12% | yes |
| 17 | 15eda54ebd | 0.2188 | 0.2336 | - | 0.2261 (partial) | x86-64 +38%, x86-32 +30% | yes |
| 18 | 3eb59b271d | 0.3634 | 0.4363 | - | 0.3982 (partial) | x86-64 +129%, x86-32 +142% | yes |
| 19 | 71005d8a0d | 0.6518 | 0.6762 | - | 0.6639 (partial) | x86-64 +311%, x86-32 +276% | yes |

**The generic pick**: none within the veto - the best mean d727605472 named instead.
Each class's fastest: x86-64 262a51bc6c; x86-32 69cebcaed9; ARMv7 5f7e66b12d.
**Added to the set across machines** (never taken out): d727605472 - across machines: the best mean #1; 69cebcaed9 - across machines: the fastest at x86-32.
