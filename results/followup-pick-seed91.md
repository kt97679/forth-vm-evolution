# Seed 91's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 640)

`python3 lab/evolve/final-pick.py results/followup-seed91.md results/chain-followup91/s1/loadtest.md results/chain-followup91/s1/*.out.json --also-session results/chain-followup91/s2 ... s40` - the laptop 35 sessions (10 rounds), dream 40 at 8-byte cells and 40 at 4-byte, the Tegra 5 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-636.md: results/followup-roles-seed91.md.

# The final set, re-measured - 38 candidates, 38 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup91/s2, results/chain-followup91/s3, results/chain-followup91/s4, results/chain-followup91/s5, results/chain-followup91/s6, results/chain-followup91/s7, results/chain-followup91/s8, results/chain-followup91/s9, results/chain-followup91/s10, results/chain-followup91/s11, results/chain-followup91/s12, results/chain-followup91/s13, results/chain-followup91/s14, results/chain-followup91/s15, results/chain-followup91/s16, results/chain-followup91/s17, results/chain-followup91/s18, results/chain-followup91/s19, results/chain-followup91/s20, results/chain-followup91/s21, results/chain-followup91/s22, results/chain-followup91/s23, results/chain-followup91/s24, results/chain-followup91/s25, results/chain-followup91/s26, results/chain-followup91/s27, results/chain-followup91/s28, results/chain-followup91/s29, results/chain-followup91/s30, results/chain-followup91/s31, results/chain-followup91/s32, results/chain-followup91/s33, results/chain-followup91/s34, results/chain-followup91/s35, results/chain-followup91/s36, results/chain-followup91/s37, results/chain-followup91/s38, results/chain-followup91/s39, results/chain-followup91/s40 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 7fb40ff7ba | fastest | 0.2878 (0.2721) | 35,126 | 140 | 0.3338 (0.3360) | 0.966 | 0.15299 |
| 2 | 01712a2639 | smallest | 1.6101 (1.6226) | 13,691 | 120 | 1.9875 (1.9975) | 1.006 | 0.00713 |
| 3 | fb0d57c8a2 | least memory | 0.8249 (0.8253) | 17,830 | 104 | 0.7688 (0.7664) | 1.004 | 0.04209 |
| 4 | 3060f04651 | fastest at 32 bits | 0.3048 (0.2840) | 33,052 | 136 | 0.3086 (0.2930) | 0.967 | 0.01512 |
| 5 | 6dbd01752e | adds the most | 0.4182 (0.3972) | 18,070 | 120 | 0.3996 (0.3762) | 0.979 | 0.04422 |
| 6 | 88cdf38fbd | adds the most | 0.3373 (0.3178) | 21,986 | 152 | 0.3244 (0.3081) | 0.977 | 0.00945 |
| 7 | 22f7ad33b4 | adds the most | 0.6853 (0.6832) | 15,516 | 108 | 0.6763 (0.6746) | 0.994 | 0.00701 |
| 8 | c6d37f5da7 | adds the most | 0.5041 (0.4889) | 16,180 | 128 | 0.4812 (0.4568) | 0.985 | 0.00221 |
| 9 | d99a498d26 | adds the most | 0.3293 (0.3111) | 22,099 | 132 | 0.3680 (0.3491) | 0.970 | 0.00183 |
| 10 | e92b45e100 | adds the most | 0.9073 (0.9064) | 14,245 | 116 | 0.9058 (0.9047) | 1.003 | 0.00175 |

Against the in-run set: in now 01712a2639, 22f7ad33b4, 3060f04651, 6dbd01752e, 7fb40ff7ba, 88cdf38fbd, c6d37f5da7, d99a498d26, e92b45e100, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest 7fb40ff7ba; smallest 01712a2639; least memory fb0d57c8a2; fastest at 32 bits 3060f04651; in the set under load only 3eb59b271d, 782f3ad7ff, 8470be6ce5, alone only 88cdf38fbd, d99a498d26, e92b45e100.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 9f68e71820.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.961 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 11a56ff9e4.

rage (4-byte cells): 38 candidates measured; its fastest 965f48c803 0.306; Spearman with the laptop alone 0.872 over 38; FLAGGED, among its fastest five and not in the set: 965f48c803, 3eb59b271d.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.353; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 9f68e71820.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

rage (4-byte cells): 38 candidates measured; its fastest 965f48c803 0.308; Spearman with the laptop alone 0.870 over 38; FLAGGED, among its fastest five and not in the set: 965f48c803, 3eb59b271d.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 9f68e71820.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.957 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 11a56ff9e4, 782f3ad7ff.

rage (4-byte cells): 38 candidates measured; its fastest 965f48c803 0.306; Spearman with the laptop alone 0.870 over 38; FLAGGED, among its fastest five and not in the set: 965f48c803, 3eb59b271d.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.856 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.963 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 11a56ff9e4.

rage (4-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.310; Spearman with the laptop alone 0.873 over 38; FLAGGED, among its fastest five and not in the set: 965f48c803, 3eb59b271d.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.961 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 11a56ff9e4.

rage (4-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.307; Spearman with the laptop alone 0.868 over 38; FLAGGED, among its fastest five and not in the set: 3eb59b271d, 965f48c803.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.857 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.962 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.854 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 11a56ff9e4, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.956 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.851 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 11a56ff9e4.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.957 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.351; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.959 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.956 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff, c2ef9488ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.956 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.854 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 11a56ff9e4.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.957 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.857 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.957 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.856 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.377; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.351; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 11a56ff9e4.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.961 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.856 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 11a56ff9e4, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.857 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 11a56ff9e4, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.348; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.352; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 8470be6ce5.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff, c2ef9488ff.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.350; Spearman with the laptop alone 0.854 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.373; Spearman with the laptop alone 0.961 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.347; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.856 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.352; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.962 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.352; Spearman with the laptop alone 0.854 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.378; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 11a56ff9e4, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.962 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.856 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.377; Spearman with the laptop alone 0.959 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 11a56ff9e4, 782f3ad7ff, c2ef9488ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.854 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 9f68e71820.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.961 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest b311f84693 0.351; Spearman with the laptop alone 0.856 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 782f3ad7ff, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.962 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 11a56ff9e4.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.957 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 11a56ff9e4.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.959 over 38; FLAGGED, among its fastest five and not in the set: b311f84693, 11a56ff9e4, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.854 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.373; Spearman with the laptop alone 0.959 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693, c2ef9488ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.857 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff, c2ef9488ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, 11a56ff9e4, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.853 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.376; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.855 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.958 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, 782f3ad7ff, b311f84693, c2ef9488ff.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.854 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.960 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, 11a56ff9e4, b311f84693.

dream (4-byte cells): 38 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.856 over 38; FLAGGED, among its fastest five and not in the set: 782f3ad7ff, b311f84693, 444a9c62f5, 5dcf9f7656.

dream (8-byte cells): 38 candidates measured; its fastest 7fb40ff7ba 0.375; Spearman with the laptop alone 0.956 over 38; FLAGGED, among its fastest five and not in the set: 11a56ff9e4, b311f84693, 782f3ad7ff, c2ef9488ff.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | 0.3428 | 0.3380 | 0.3537 | 0.3448 | x86-64 +4%, ARMv7 +15% | ADDED |
| 2 | b311f84693 | 0.3429 | 0.3388 | 0.3541 | 0.3452 | x86-64 +4%, ARMv7 +15% | ADDED |
| 3 | 7fb40ff7ba | 0.3285 | 0.4449 | 0.3102 | 0.3566 | x86-32 +32%, ARMv7 +1% | yes |
| 4 | 88cdf38fbd | 0.3659 | 0.3431 | 0.3828 | 0.3636 | x86-64 +11%, x86-32 +2%, ARMv7 +24% | yes |
| 5 | 3060f04651 | 0.3568 | 0.4128 | 0.3285 | 0.3644 | x86-64 +9%, x86-32 +22%, ARMv7 +7% | yes |
| 6 | 965f48c803 | 0.3697 | 0.4412 | 0.3083 | 0.3691 | x86-64 +13%, x86-32 +31% | ADDED |
| 7 | 3eb59b271d | 0.3776 | 0.4428 | 0.3121 | 0.3737 | x86-64 +15%, x86-32 +31%, ARMv7 +1% | - |
| 8 | d99a498d26 | 0.3568 | 0.4617 | 0.3217 | 0.3756 | x86-64 +9%, x86-32 +37%, ARMv7 +4% | yes |
| 9 | 444a9c62f5 | 0.3930 | 0.3556 | 0.3908 | 0.3794 | x86-64 +20%, x86-32 +5%, ARMv7 +27% | - |
| 10 | 5dcf9f7656 | 0.3756 | 0.3693 | 0.4443 | 0.3950 | x86-64 +14%, x86-32 +9%, ARMv7 +44% | - |
| 11 | 8470be6ce5 | 0.3800 | 0.3733 | 0.4474 | 0.3989 | x86-64 +16%, x86-32 +10%, ARMv7 +45% | - |
| 12 | 11a56ff9e4 | 0.3665 | 0.3805 | 0.4645 | 0.4016 | x86-64 +12%, x86-32 +13%, ARMv7 +51% | - |
| 13 | 6dbd01752e | 0.4704 | 0.4374 | 0.3642 | 0.4216 | x86-64 +43%, x86-32 +29%, ARMv7 +18% | yes |
| 14 | c6d37f5da7 | 0.5870 | 0.6200 | 0.4733 | 0.5564 | x86-64 +79%, x86-32 +83%, ARMv7 +54% | yes |
| 15 | 22f7ad33b4 | 0.7954 | 0.8024 | 0.5099 | 0.6878 | x86-64 +142%, x86-32 +137%, ARMv7 +65% | yes |
| 16 | fb0d57c8a2 | 0.9118 | 0.8819 | 0.5023 | 0.7392 | x86-64 +178%, x86-32 +161%, ARMv7 +63% | yes |
| 17 | e92b45e100 | 1.1468 | 1.0844 | 1.0511 | 1.0934 | x86-64 +249%, x86-32 +221%, ARMv7 +241% | yes |
| 18 | 01712a2639 | 2.0114 | 2.1997 | 1.8917 | 2.0304 | x86-64 +512%, x86-32 +551%, ARMv7 +514% | yes |

**The generic pick**: 782f3ad7ff, the mean 0.3448, within 25% of every class's best.
Each class's fastest: x86-64 7fb40ff7ba; x86-32 782f3ad7ff; ARMv7 965f48c803.
**Added to the set across machines** (never taken out): 782f3ad7ff - across machines: the best mean #1; b311f84693 - across machines: the best mean #2; 965f48c803 - across machines: the fastest at ARMv7.
