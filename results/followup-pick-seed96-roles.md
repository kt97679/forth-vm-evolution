# Seed 96-roles's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 713)

`python3 lab/evolve/final-pick.py results/followup-seed96-roles.md results/chain-followup96-roles/s1/loadtest.md results/chain-followup96-roles/s1/*.out.json --also-session results/chain-followup96-roles/s2 ... s8` - the laptop 5 sessions (10 rounds), dream 8 at 8-byte cells and 8 at 4-byte, the Tegra 3 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-657.md: results/followup-roles-seed96-roles.md.

# The final set, re-measured - 944 candidates, 944 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup96-roles/s2, results/chain-followup96-roles/s3, results/chain-followup96-roles/s4, results/chain-followup96-roles/s5, results/chain-followup96-roles/s6, results/chain-followup96-roles/s7, results/chain-followup96-roles/s8 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 9b15ba26f7 | fastest | 0.1301 (0.1194) | 55,663 | 284 | 0.1681 (0.1560) | 0.963 | 0.01552 |
| 2 | 21768033b7 | smallest | 1.2054 (1.2231) | 22,409 | 116 | 1.1190 (1.1290) | 1.007 | 0.04209 |
| 3 | d3496fcc6c | least memory | 0.6076 (0.6133) | 25,819 | 108 | 0.6721 (0.6786) | 0.990 | 0.06797 |
| 4 | d95cab5117 | fastest at 32 bits | 0.1567 (0.1422) | 46,364 | 264 | 0.1593 (0.1522) | 0.930 | 0.02495 |
| 5 | bee5d0daa2 | adds the most, the knee | 0.3090 (0.2960) | 30,151 | 140 | 0.3149 (0.3002) | 0.984 | 0.07984 |
| 6 | 3dd824e8ae | adds the most | 0.1861 (0.1709) | 38,929 | 208 | 0.2029 (0.1876) | 0.940 | 0.02462 |
| 7 | 91e0b5942e | adds the most | 0.4410 (0.4228) | 25,269 | 120 | 0.4056 (0.3902) | 0.990 | 0.01463 |
| 8 | 4b6ca4aaf8 | adds the most | 0.2633 (0.2527) | 36,136 | 172 | 0.2846 (0.2740) | 0.991 | 0.00457 |
| 9 | d6e149f5bc | adds the most | 0.1399 (0.1241) | 48,443 | 236 | 0.1795 (0.1629) | 0.947 | 0.00390 |
| 10 | 786caa3b98 | adds the most | 0.5972 (0.5930) | 23,545 | 136 | 0.6125 (0.5969) | 1.010 | 0.00302 |

Against the in-run set: in now 21768033b7, 3dd824e8ae, 4b6ca4aaf8, 786caa3b98, 91e0b5942e, 9b15ba26f7, bee5d0daa2, d3496fcc6c, d6e149f5bc, d95cab5117; out now none - both kept as candidates.
Under load: the extremes fastest b4a004d9ab; smallest 21768033b7; least memory d3496fcc6c; fastest at 32 bits 307718a75b; in the set under load only 00995a7f26, 307718a75b, b4a004d9ab, ccc14cc8ff, ec331aea6e, alone only 4b6ca4aaf8, 9b15ba26f7, bee5d0daa2, d6e149f5bc, d95cab5117.

dream (4-byte cells): 944 candidates measured; its fastest 23541b3b75 0.184; Spearman with the laptop alone 0.922 over 944; FLAGGED, among its fastest five and not in the set: 23541b3b75, 07f234ce51, ea782c6094, 2236e26656, 163935642a.

dream (8-byte cells): 944 candidates measured; its fastest a75bb42a90 0.190; Spearman with the laptop alone 0.847 over 944; FLAGGED, among its fastest five and not in the set: a75bb42a90, 2ba6bf917e, 107f3b104a, a2235db290.

rage (4-byte cells): 437 candidates measured; its fastest 1ce4882d06 0.303; Spearman with the laptop alone 0.612 over 437; FLAGGED, among its fastest five and not in the set: 1ce4882d06, a8d35bdccc, 82242fd1e1, 136bb9e65e, 852d8459ec.

dream (4-byte cells): 944 candidates measured; its fastest e7227cefdf 0.180; Spearman with the laptop alone 0.915 over 944; FLAGGED, among its fastest five and not in the set: e7227cefdf, 77597e23e4, f0c0fb2c0a, 79e5a089b2, 8035ad0930.

dream (8-byte cells): 944 candidates measured; its fastest 5618a2b6e6 0.181; Spearman with the laptop alone 0.855 over 944; FLAGGED, among its fastest five and not in the set: 5618a2b6e6, 879cab7556, e8557e7523, 1f8b80d3c7, 8ef3d880b8.

rage (4-byte cells): 437 candidates measured; its fastest a8d35bdccc 0.302; Spearman with the laptop alone 0.602 over 437; FLAGGED, among its fastest five and not in the set: a8d35bdccc, 017b9f119a, 60d1484673, a2fdd505b0, 136bb9e65e.

dream (4-byte cells): 944 candidates measured; its fastest d595e43a48 0.195; Spearman with the laptop alone 0.919 over 944; FLAGGED, among its fastest five and not in the set: d595e43a48, e384512e21, 2cc03aa974, 03e797f52a, 371bcdcbbc.

dream (8-byte cells): 944 candidates measured; its fastest dd708a94a5 0.196; Spearman with the laptop alone 0.859 over 944; FLAGGED, among its fastest five and not in the set: dd708a94a5, 2ad0154893, f991568387, fa6248dbb4, a8b7b690a5.

rage (4-byte cells): 437 candidates measured; its fastest a8d35bdccc 0.308; Spearman with the laptop alone 0.581 over 437; FLAGGED, among its fastest five and not in the set: a8d35bdccc, 94a4605110, 60d1484673, a2fdd505b0, b4c80cafb1.

dream (4-byte cells): 944 candidates measured; its fastest e384512e21 0.189; Spearman with the laptop alone 0.924 over 944; FLAGGED, among its fastest five and not in the set: e384512e21, 265fb83579, f3961c3e23, 628ab7a720, a600492996.

dream (8-byte cells): 944 candidates measured; its fastest 0398326f75 0.194; Spearman with the laptop alone 0.845 over 944; FLAGGED, among its fastest five and not in the set: 0398326f75, 67cd07c5e9, d96855b35c, 86c4230d64, df097ba2e2.

dream (4-byte cells): 944 candidates measured; its fastest ebd3ad7619 0.190; Spearman with the laptop alone 0.917 over 944; FLAGGED, among its fastest five and not in the set: ebd3ad7619, 8086028f0b, 7f87f387aa, 0335e71438, fb87013a24.

dream (8-byte cells): 944 candidates measured; its fastest ef77ad048a 0.190; Spearman with the laptop alone 0.850 over 944; FLAGGED, among its fastest five and not in the set: ef77ad048a, 1f0d70d8ce, 672c19e6ff, 262a51bc6c, d58b1827a8.

dream (4-byte cells): 944 candidates measured; its fastest 49a4262a19 0.197; Spearman with the laptop alone 0.921 over 944; FLAGGED, among its fastest five and not in the set: 49a4262a19, 2da719475e, 4a01c70a50, 404e80c5a8, ebd3ad7619.

dream (8-byte cells): 944 candidates measured; its fastest 3ba6ef6048 0.168; Spearman with the laptop alone 0.850 over 944; FLAGGED, among its fastest five and not in the set: 3ba6ef6048, 4e28a43a01, 8086028f0b, 72060411c1, ae05d3f23d.

dream (4-byte cells): 944 candidates measured; its fastest 2236e26656 0.183; Spearman with the laptop alone 0.917 over 944; FLAGGED, among its fastest five and not in the set: 2236e26656, 87fc9d7b95, 07433d96e5, 262a51bc6c.

dream (8-byte cells): 944 candidates measured; its fastest 1a31bd7056 0.200; Spearman with the laptop alone 0.855 over 944; FLAGGED, among its fastest five and not in the set: 1a31bd7056, d595e43a48, d7167a8003, 5618a2b6e6, 879cab7556.

dream (4-byte cells): 944 candidates measured; its fastest bd8dc4a4f5 0.193; Spearman with the laptop alone 0.914 over 944; FLAGGED, among its fastest five and not in the set: bd8dc4a4f5, 6d7559ee00, 0b7d1535dd, 163935642a, 549a33d755.

dream (8-byte cells): 944 candidates measured; its fastest 5618a2b6e6 0.202; Spearman with the laptop alone 0.858 over 944; FLAGGED, among its fastest five and not in the set: 5618a2b6e6, 1a31bd7056, d7167a8003, 65afc5c00a.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 923951e8ab | 0.1709 | 0.1917 | 0.4467* | 0.2446 | x86-64 +4%, x86-32 +6%, ARMv7 +46% | ADDED |
| 2 | 90f578b487 | 0.1852 | 0.1850 | 0.4347* | 0.2460 | x86-64 +13%, x86-32 +3%, ARMv7 +42% | ADDED |
| 3 | 0fed6b2276 | 0.1830 | 0.1838 | 0.4489* | 0.2472 | x86-64 +12%, x86-32 +2%, ARMv7 +47% | ADDED |
| 4 | 873d4502fa | 0.1874 | 0.1896 | 0.4382* | 0.2497 | x86-64 +14%, x86-32 +5%, ARMv7 +43% | - |
| 5 | ccc14cc8ff | 0.1914 | 0.1933 | 0.4418* | 0.2538 | x86-64 +17%, x86-32 +7%, ARMv7 +45% | - |
| 6 | 06b188f45b | 0.1969 | 0.2016 | 0.4420* | 0.2598 | x86-64 +20%, x86-32 +12%, ARMv7 +45% | - |
| 7 | ee34931cd7 | 0.1931 | 0.1956 | 0.4686* | 0.2606 | x86-64 +18%, x86-32 +9%, ARMv7 +53% | - |
| 8 | c7c35f9c97 | 0.1839 | 0.2013 | 0.5249* | 0.2688 | x86-64 +12%, x86-32 +12%, ARMv7 +72% | - |
| 9 | 5d8279397f | 0.2021 | 0.2047 | 0.5198* | 0.2781 | x86-64 +23%, x86-32 +14%, ARMv7 +70% | - |
| 10 | 24360c16f0 | 0.1951 | 0.2279 | 0.5212* | 0.2851 | x86-64 +19%, x86-32 +26%, ARMv7 +71% | - |
| 11 | 3dd824e8ae | 0.2160 | 0.2264 | 0.5192* | 0.2939 | x86-64 +32%, x86-32 +26%, ARMv7 +70% | yes |
| 12 | f4d3f7ccc9 | 0.2116 | 0.2415 | 0.5643* | 0.3066 | x86-64 +29%, x86-32 +34%, ARMv7 +85% | - |
| 13 | bee5d0daa2 | 0.3308 | 0.3281 | 0.3741 | 0.3437 | x86-64 +102%, x86-32 +82%, ARMv7 +22% | yes |
| 14 | a8d35bdccc | 0.3489 | 0.4324 | 0.3055 | 0.3585 | x86-64 +113%, x86-32 +140% | ADDED |
| 15 | 91e0b5942e | 0.5145 | 0.5064 | 0.3670 | 0.4573 | x86-64 +214%, x86-32 +181%, ARMv7 +20% | yes |
| 16 | d3496fcc6c | 0.6447 | 0.7042 | 0.4914 | 0.6065 | x86-64 +293%, x86-32 +291%, ARMv7 +61% | yes |
| 17 | 786caa3b98 | 0.7545 | 0.7209 | 0.7258 | 0.7336 | x86-64 +360%, x86-32 +300%, ARMv7 +138% | yes |
| 18 | 21768033b7 | 1.4582 | 1.2958 | 1.2109 | 1.3177 | x86-64 +790%, x86-32 +619%, ARMv7 +296% | yes |
| 19 | df097ba2e2 | 0.1639 | 0.1884 | - | 0.1757 (partial) | x86-32 +5% | ADDED |
| 20 | 9b15ba26f7 | 0.1644 | 0.1878 | - | 0.1757 (partial) | x86-32 +4% | yes |
| 21 | 2236e26656 | 0.1819 | 0.1802 | - | 0.1811 (partial) | x86-64 +11% | ADDED |
| 22 | d95cab5117 | 0.1824 | 0.1828 | - | 0.1826 (partial) | x86-64 +11%, x86-32 +1% | yes |
| 23 | d6e149f5bc | 0.1784 | 0.1983 | - | 0.1881 (partial) | x86-64 +9%, x86-32 +10% | yes |
| 24 | 4b6ca4aaf8 | 0.2835 | 0.3025 | - | 0.2929 (partial) | x86-64 +73%, x86-32 +68% | yes |

**The generic pick**: none within the veto - the best mean 923951e8ab named instead.
Each class's fastest: x86-64 df097ba2e2; x86-32 2236e26656; ARMv7 a8d35bdccc.
**Added to the set across machines** (never taken out): 923951e8ab - across machines: the best mean #1; 90f578b487 - across machines: the best mean #2; 0fed6b2276 - across machines: the best mean #3; df097ba2e2 - across machines: the fastest at x86-64; 2236e26656 - across machines: the fastest at x86-32; a8d35bdccc - across machines: the fastest at ARMv7.
