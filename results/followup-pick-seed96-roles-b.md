# Seed 96-roles-b's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 714)

`python3 lab/evolve/final-pick.py results/followup-seed96-roles-b.md results/chain-followup96-roles-b/s1/loadtest.md results/chain-followup96-roles-b/s1/*.out.json --also-session results/chain-followup96-roles-b/s2 ... s34` - the laptop 18 sessions (10 rounds), dream 34 at 8-byte cells and 34 at 4-byte, the Tegra 5 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-657.md: results/followup-roles-seed96-roles-b.md.

# The final set, re-measured - 99 candidates, 99 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup96-roles-b/s2, results/chain-followup96-roles-b/s3, results/chain-followup96-roles-b/s4, results/chain-followup96-roles-b/s5, results/chain-followup96-roles-b/s6, results/chain-followup96-roles-b/s7, results/chain-followup96-roles-b/s8, results/chain-followup96-roles-b/s9, results/chain-followup96-roles-b/s10, results/chain-followup96-roles-b/s11, results/chain-followup96-roles-b/s12, results/chain-followup96-roles-b/s13, results/chain-followup96-roles-b/s14, results/chain-followup96-roles-b/s15, results/chain-followup96-roles-b/s16, results/chain-followup96-roles-b/s17, results/chain-followup96-roles-b/s18, results/chain-followup96-roles-b/s19, results/chain-followup96-roles-b/s20, results/chain-followup96-roles-b/s21, results/chain-followup96-roles-b/s22, results/chain-followup96-roles-b/s23, results/chain-followup96-roles-b/s24, results/chain-followup96-roles-b/s25, results/chain-followup96-roles-b/s26, results/chain-followup96-roles-b/s27, results/chain-followup96-roles-b/s28, results/chain-followup96-roles-b/s29, results/chain-followup96-roles-b/s30, results/chain-followup96-roles-b/s31, results/chain-followup96-roles-b/s32, results/chain-followup96-roles-b/s33, results/chain-followup96-roles-b/s34 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 9b15ba26f7 | fastest | 0.1311 (0.1265) | 53,503 | 284 | 0.1662 (0.1630) | 0.918 | 0.01958 |
| 2 | 219878ec89 | smallest | 1.2857 (1.2881) | 21,673 | 116 | 1.1119 (1.1112) | 1.008 | 0.03971 |
| 3 | 71005d8a0d | least memory | 0.6223 (0.6264) | 25,401 | 112 | 0.6498 (0.6478) | 0.996 | 0.06922 |
| 4 | b5c79bff7e | fastest at 32 bits | 0.1522 (0.1481) | 51,847 | 268 | 0.1610 (0.1611) | 0.919 | 0.00938 |
| 5 | 3eb59b271d | adds the most, the knee | 0.3280 (0.3267) | 30,244 | 136 | 0.3331 (0.3236) | 0.975 | 0.07843 |
| 6 | 3dd824e8ae | adds the most | 0.1855 (0.1877) | 37,065 | 208 | 0.2020 (0.2062) | 0.935 | 0.03608 |
| 7 | ae99617f06 | adds the most | 0.4112 (0.4155) | 26,261 | 124 | 0.4116 (0.4009) | 0.979 | 0.01045 |
| 8 | ccc14cc8ff | adds the most | 0.1593 (0.1504) | 43,436 | 224 | 0.1708 (0.1684) | 0.927 | 0.00693 |
| 9 | 08e5629783 | adds the most | 0.2846 (0.2862) | 34,448 | 152 | 0.3059 (0.3126) | 0.970 | 0.00572 |
| 10 | 786caa3b98 | adds the most | 0.6443 (0.6364) | 22,801 | 140 | 0.6018 (0.6056) | 0.995 | 0.00447 |

Against the in-run set: in now 08e5629783, 219878ec89, 3dd824e8ae, 3eb59b271d, 71005d8a0d, 786caa3b98, 9b15ba26f7, ae99617f06, b5c79bff7e, ccc14cc8ff; out now none - both kept as candidates.
Under load: the extremes fastest 262a51bc6c; smallest 219878ec89; least memory 71005d8a0d; fastest at 32 bits 307718a75b; in the set under load only 262a51bc6c, 307718a75b, d727605472, alone only 08e5629783, 9b15ba26f7, b5c79bff7e.

dream (4-byte cells): 99 candidates measured; its fastest 69cebcaed9 0.203; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 69cebcaed9, ea782c6094, 2236e26656, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.950 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 923951e8ab, 107f3b104a.

rage (4-byte cells): 61 candidates measured; its fastest a8d35bdccc 0.301; Spearman with the laptop alone 0.548 over 61; FLAGGED, among its fastest five and not in the set: a8d35bdccc, a2fdd505b0, 017b9f119a, 1ce4882d06, 60d1484673.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 69cebcaed9, 163935642a, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.951 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 107f3b104a, 23541b3b75.

rage (4-byte cells): 61 candidates measured; its fastest a8d35bdccc 0.301; Spearman with the laptop alone 0.558 over 61; FLAGGED, among its fastest five and not in the set: a8d35bdccc, 017b9f119a, a2fdd505b0, 60d1484673, 89da7aaa44.

dream (4-byte cells): 99 candidates measured; its fastest 69cebcaed9 0.203; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 69cebcaed9, 2236e26656, ea782c6094, 163935642a, 107f3b104a.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.198; Spearman with the laptop alone 0.952 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 107f3b104a, 23541b3b75.

rage (4-byte cells): 61 candidates measured; its fastest a8d35bdccc 0.305; Spearman with the laptop alone 0.548 over 61; FLAGGED, among its fastest five and not in the set: a8d35bdccc, 60d1484673, a2fdd505b0, 017b9f119a, 89da7aaa44.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.933 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, ea782c6094, b525180392, 163935642a.

dream (8-byte cells): 99 candidates measured; its fastest 9b15ba26f7 0.198; Spearman with the laptop alone 0.954 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 107f3b104a.

rage (4-byte cells): 61 candidates measured; its fastest a8d35bdccc 0.301; Spearman with the laptop alone 0.547 over 61; FLAGGED, among its fastest five and not in the set: a8d35bdccc, 017b9f119a, a2fdd505b0, 60d1484673, 89da7aaa44.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, 163935642a, 51b12a7bef, ea782c6094.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.952 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 923951e8ab, 107f3b104a.

rage (4-byte cells): 61 candidates measured; its fastest a8d35bdccc 0.304; Spearman with the laptop alone 0.544 over 61; FLAGGED, among its fastest five and not in the set: a8d35bdccc, a2fdd505b0, 60d1484673, 1ce4882d06, 017b9f119a.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 51b12a7bef, 69cebcaed9, 163935642a, ea782c6094.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.954 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, 2236e26656.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.929 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 163935642a, ea782c6094, 6ab5e13894, 69cebcaed9.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.956 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.928 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 69cebcaed9, 163935642a, 307718a75b.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.956 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, 2236e26656.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 51b12a7bef, 11f956db93, ea782c6094, 69cebcaed9.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.952 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 107f3b104a, 23541b3b75.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.932 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 69cebcaed9, 163935642a, 19a46e4133.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.196; Spearman with the laptop alone 0.959 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 2236e26656.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.934 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, 163935642a, ea782c6094, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.198; Spearman with the laptop alone 0.957 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, f24c4436dd, 23541b3b75.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, ea782c6094, 163935642a, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.950 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 2236e26656, f24c4436dd.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.927 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, ea782c6094, 11f956db93, b525180392.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.956 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, f24c4436dd, 23541b3b75.

dream (4-byte cells): 99 candidates measured; its fastest 11f956db93 0.202; Spearman with the laptop alone 0.931 over 99; FLAGGED, among its fastest five and not in the set: 11f956db93, 163935642a, 2236e26656, ea782c6094, 69cebcaed9.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.955 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 923951e8ab.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.202; Spearman with the laptop alone 0.923 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, df097ba2e2, 923951e8ab, 163935642a, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.948 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, f24c4436dd.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.205; Spearman with the laptop alone 0.932 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, 51b12a7bef, 163935642a, ea782c6094.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.956 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 2236e26656, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 163935642a 0.203; Spearman with the laptop alone 0.931 over 99; FLAGGED, among its fastest five and not in the set: 163935642a, ea782c6094, 2236e26656, 51b12a7bef, 11f956db93.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.198; Spearman with the laptop alone 0.958 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 2236e26656, 23541b3b75.

dream (4-byte cells): 99 candidates measured; its fastest 69cebcaed9 0.202; Spearman with the laptop alone 0.932 over 99; FLAGGED, among its fastest five and not in the set: 69cebcaed9, ea782c6094, 2236e26656, 51b12a7bef, 163935642a.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.953 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 51b12a7bef, 69cebcaed9, 11f956db93.

dream (8-byte cells): 99 candidates measured; its fastest 9b15ba26f7 0.197; Spearman with the laptop alone 0.946 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, f24c4436dd, 2236e26656.

dream (4-byte cells): 99 candidates measured; its fastest 51b12a7bef 0.196; Spearman with the laptop alone 0.924 over 99; FLAGGED, among its fastest five and not in the set: 51b12a7bef, ea782c6094, c69c1cebf4, 163935642a, 2236e26656.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.954 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, f24c4436dd.

dream (4-byte cells): 99 candidates measured; its fastest d95cab5117 0.189; Spearman with the laptop alone 0.931 over 99; FLAGGED, among its fastest five and not in the set: d95cab5117, 51b12a7bef, ea782c6094, 2236e26656, 69cebcaed9.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.198; Spearman with the laptop alone 0.959 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, f24c4436dd.

dream (4-byte cells): 99 candidates measured; its fastest 69cebcaed9 0.204; Spearman with the laptop alone 0.929 over 99; FLAGGED, among its fastest five and not in the set: 69cebcaed9, 2236e26656, ea782c6094, 51b12a7bef, 163935642a.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.196; Spearman with the laptop alone 0.954 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.929 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 51b12a7bef, 69cebcaed9, 163935642a.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.958 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 107f3b104a, f24c4436dd.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.931 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 69cebcaed9, 163935642a, 19a46e4133.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.196; Spearman with the laptop alone 0.959 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 51b12a7bef 0.203; Spearman with the laptop alone 0.931 over 99; FLAGGED, among its fastest five and not in the set: 51b12a7bef, 69cebcaed9, 2236e26656, ea782c6094, 163935642a.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.196; Spearman with the laptop alone 0.953 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 923951e8ab, 23541b3b75.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.202; Spearman with the laptop alone 0.929 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 307718a75b, 69cebcaed9, ea782c6094, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.955 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 11f956db93 0.197; Spearman with the laptop alone 0.926 over 99; FLAGGED, among its fastest five and not in the set: 11f956db93, 51b12a7bef, ea782c6094, 2236e26656, b525180392.

dream (8-byte cells): 99 candidates measured; its fastest 9b15ba26f7 0.196; Spearman with the laptop alone 0.958 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.202; Spearman with the laptop alone 0.927 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, 163935642a, ea782c6094, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.955 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, f24c4436dd, 23541b3b75.

dream (4-byte cells): 99 candidates measured; its fastest ea782c6094 0.203; Spearman with the laptop alone 0.932 over 99; FLAGGED, among its fastest five and not in the set: ea782c6094, 51b12a7bef, 69cebcaed9, 2236e26656, 11f956db93.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.956 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, f24c4436dd.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.931 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 163935642a, 51b12a7bef, 69cebcaed9, 19a46e4133.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.953 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, f24c4436dd, 107f3b104a.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.930 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 163935642a, 51b12a7bef, 69cebcaed9.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.953 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 923951e8ab.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.927 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 51b12a7bef, 69cebcaed9, 19a46e4133, ea782c6094.

dream (8-byte cells): 99 candidates measured; its fastest 262a51bc6c 0.197; Spearman with the laptop alone 0.954 over 99; FLAGGED, among its fastest five and not in the set: 262a51bc6c, df097ba2e2, 23541b3b75, 923951e8ab.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.204; Spearman with the laptop alone 0.927 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, 69cebcaed9, ea782c6094, 163935642a, 51b12a7bef.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.198; Spearman with the laptop alone 0.950 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 107f3b104a, 2236e26656.

dream (4-byte cells): 99 candidates measured; its fastest 2236e26656 0.203; Spearman with the laptop alone 0.927 over 99; FLAGGED, among its fastest five and not in the set: 2236e26656, ea782c6094, 69cebcaed9, 51b12a7bef, 19a46e4133.

dream (8-byte cells): 99 candidates measured; its fastest df097ba2e2 0.197; Spearman with the laptop alone 0.956 over 99; FLAGGED, among its fastest five and not in the set: df097ba2e2, 262a51bc6c, 23541b3b75, 2236e26656.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | df097ba2e2 | 0.1623 | 0.1873 | 0.4321* | 0.2359 | x86-64 +1%, x86-32 +3%, ARMv7 +43% | ADDED |
| 2 | 2236e26656 | 0.1767 | 0.1844 | 0.4155* | 0.2383 | x86-64 +9%, x86-32 +1%, ARMv7 +37% | ADDED |
| 3 | 923951e8ab | 0.1654 | 0.1895 | 0.4538* | 0.2423 | x86-64 +2%, x86-32 +4%, ARMv7 +50% | ADDED |
| 4 | 0fed6b2276 | 0.1777 | 0.1848 | 0.4453* | 0.2446 | x86-64 +10%, x86-32 +1%, ARMv7 +47% | - |
| 5 | 90f578b487 | 0.1808 | 0.1879 | 0.4354* | 0.2454 | x86-64 +12%, x86-32 +3%, ARMv7 +44% | - |
| 6 | 873d4502fa | 0.1841 | 0.1906 | 0.4371* | 0.2485 | x86-64 +14%, x86-32 +4%, ARMv7 +45% | - |
| 7 | 06b188f45b | 0.1903 | 0.2000 | 0.4364* | 0.2551 | x86-64 +18%, x86-32 +10%, ARMv7 +44% | - |
| 8 | d727605472 | 0.3181 | 0.3174 | 0.3243 | 0.3199 | x86-64 +97%, x86-32 +74%, ARMv7 +7% | - |
| 9 | 5f7e66b12d | 0.3139 | 0.3258 | 0.3226 | 0.3207 | x86-64 +95%, x86-32 +79%, ARMv7 +7% | - |
| 10 | 428be2869c | 0.3130 | 0.3258 | 0.3259 | 0.3215 | x86-64 +94%, x86-32 +79%, ARMv7 +8% | - |
| 11 | a4e502f224 | 0.3131 | 0.3278 | 0.3243 | 0.3217 | x86-64 +94%, x86-32 +80%, ARMv7 +7% | - |
| 12 | eab0b42b6a | 0.3215 | 0.3280 | 0.3166 | 0.3220 | x86-64 +99%, x86-32 +80%, ARMv7 +5% | - |
| 13 | 08e5629783 | 0.3182 | 0.3235 | 0.3318 | 0.3245 | x86-64 +97%, x86-32 +77%, ARMv7 +10% | yes |
| 14 | a8d35bdccc | 0.3386 | 0.4314 | 0.3023 | 0.3534 | x86-64 +110%, x86-32 +136% | ADDED |
| 15 | 3eb59b271d | 0.3620 | 0.4334 | 0.3104 | 0.3652 | x86-64 +124%, x86-32 +138%, ARMv7 +3% | yes |
| 16 | ae99617f06 | 0.4506 | 0.4427 | 0.3239 | 0.4013 | x86-64 +179%, x86-32 +143%, ARMv7 +7% | yes |
| 17 | 71005d8a0d | 0.6518 | 0.6789 | 0.5097 | 0.6087 | x86-64 +304%, x86-32 +272%, ARMv7 +69% | yes |
| 18 | 786caa3b98 | 0.7790 | 0.7238 | 0.7306 | 0.7440 | x86-64 +383%, x86-32 +297%, ARMv7 +142% | yes |
| 19 | 219878ec89 | 1.4832 | 1.2845 | 1.2336 | 1.3296 | x86-64 +819%, x86-32 +604%, ARMv7 +308% | yes |
| 20 | 9b15ba26f7 | 0.1614 | 0.1860 | - | 0.1733 (partial) | x86-32 +2% | yes |
| 21 | b5c79bff7e | 0.1767 | 0.1827 | - | 0.1797 (partial) | x86-64 +10% | yes |
| 22 | ea782c6094 | 0.1775 | 0.1824 | - | 0.1799 (partial) | x86-64 +10% | ADDED |
| 23 | ccc14cc8ff | 0.1847 | 0.1906 | - | 0.1876 (partial) | x86-64 +14%, x86-32 +4% | yes |
| 24 | 3dd824e8ae | 0.2116 | 0.2249 | - | 0.2181 (partial) | x86-64 +31%, x86-32 +23% | yes |

**The generic pick**: none within the veto - the best mean df097ba2e2 named instead.
Each class's fastest: x86-64 9b15ba26f7; x86-32 ea782c6094; ARMv7 a8d35bdccc.
**Added to the set across machines** (never taken out): df097ba2e2 - across machines: the best mean #1; 2236e26656 - across machines: the best mean #2; 923951e8ab - across machines: the best mean #3; ea782c6094 - across machines: the fastest at x86-32; a8d35bdccc - across machines: the fastest at ARMv7.
