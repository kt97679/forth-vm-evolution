# Seed 88's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 621)

`python3 lab/evolve/final-pick.py results/followup-seed88.md results/chain-followup88/s1/loadtest.md results/chain-followup88/s1/*.out.json --also-session results/chain-followup88/s2 ... s28` - the laptop 18 sessions (10 rounds), dream 28 at 8-byte cells and 25 at 4-byte, the Tegra 3 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-611.md: results/followup-roles-seed88.md.

# The final set, re-measured - 46 candidates, 46 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup88/s2, results/chain-followup88/s3, results/chain-followup88/s4, results/chain-followup88/s5, results/chain-followup88/s6, results/chain-followup88/s7, results/chain-followup88/s8, results/chain-followup88/s9, results/chain-followup88/s10, results/chain-followup88/s11, results/chain-followup88/s12, results/chain-followup88/s13, results/chain-followup88/s14, results/chain-followup88/s15, results/chain-followup88/s16, results/chain-followup88/s17, results/chain-followup88/s18, results/chain-followup88/s19, results/chain-followup88/s20, results/chain-followup88/s21, results/chain-followup88/s22, results/chain-followup88/s23, results/chain-followup88/s24, results/chain-followup88/s25, results/chain-followup88/s26, results/chain-followup88/s27, results/chain-followup88/s28 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | fastest | 0.3069 (0.3069) | 26,242 | 148 | 0.3264 (0.3271) | 0.970 | 0.18781 |
| 2 | 4dd4e3e7e2 | smallest | 1.6798 (1.6820) | 13,709 | 116 | 2.1882 (2.1492) | 1.008 | 0.00394 |
| 3 | fb0d57c8a2 | least memory | 0.8268 (0.8272) | 17,830 | 104 | 0.7705 (0.7699) | 1.002 | 0.03179 |
| 4 | 9f8811f7f4 | fastest at 32 bits | 0.3100 (0.3074) | 33,747 | 132 | 0.3141 (0.3128) | 0.963 | 0.01193 |
| 5 | f3e832ef82 | adds the most | 0.3848 (0.3680) | 18,599 | 124 | 0.4148 (0.4029) | 0.977 | 0.02538 |
| 6 | 0e192e15fc | adds the most | 0.5578 (0.5305) | 15,932 | 120 | 0.5167 (0.4975) | 0.990 | 0.00834 |
| 7 | d47ab67a90 | adds the most | 0.3419 (0.3240) | 21,674 | 148 | 0.3307 (0.3154) | 0.975 | 0.00326 |
| 8 | 7a248231e7 | adds the most | 0.8176 (0.8277) | 14,509 | 116 | 0.8104 (0.8171) | 0.999 | 0.00260 |
| 9 | 51ad64b5f0 | adds the most | 0.3507 (0.3507) | 27,525 | 124 | 0.3316 (0.3330) | 0.971 | 0.00149 |
| 10 | 8642898a7d | adds the most | 0.4182 (0.3958) | 17,513 | 132 | 0.4034 (0.3815) | 0.979 | 0.00137 |

Against the in-run set: in now 0e192e15fc, 4dd4e3e7e2, 51ad64b5f0, 782f3ad7ff, 7a248231e7, 8642898a7d, 9f8811f7f4, d47ab67a90, f3e832ef82, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest 782f3ad7ff; smallest 4dd4e3e7e2; least memory fb0d57c8a2; fastest at 32 bits 9f8811f7f4; in the set under load only 12c66adc50, bdfd4fb056, alone only 8642898a7d, d47ab67a90.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.962 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 291b405067.

rage (4-byte cells): 46 candidates measured; its fastest 690981ca5b 0.327; Spearman with the laptop alone 0.862 over 46; FLAGGED, among its fastest five and not in the set: 690981ca5b, 3452cb633b, c7814def6d.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.378; Spearman with the laptop alone 0.958 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 291b405067.

rage (4-byte cells): 46 candidates measured; its fastest c7814def6d 0.326; Spearman with the laptop alone 0.865 over 46; FLAGGED, among its fastest five and not in the set: c7814def6d, 690981ca5b, 3452cb633b.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.868 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.958 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

rage (4-byte cells): 46 candidates measured; its fastest c7814def6d 0.327; Spearman with the laptop alone 0.855 over 46; FLAGGED, among its fastest five and not in the set: c7814def6d, 3452cb633b, 690981ca5b.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.866 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.956 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, a96deba5f8.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.352; Spearman with the laptop alone 0.865 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.379; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.352; Spearman with the laptop alone 0.868 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 291b405067.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.870 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.961 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, c2ef9488ff, 8cc7f60d6b, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.868 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 291b405067.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.352; Spearman with the laptop alone 0.870 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.378; Spearman with the laptop alone 0.962 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.381; Spearman with the laptop alone 0.962 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.353; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, c2ef9488ff, 8cc7f60d6b, 291b405067.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.868 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.375; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.961 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.868 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.354; Spearman with the laptop alone 0.870 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.354; Spearman with the laptop alone 0.868 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.962 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.352; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.378; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.870 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.377; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, c2ef9488ff, 8cc7f60d6b, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.961 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.868 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.378; Spearman with the laptop alone 0.959 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, c2ef9488ff, 8cc7f60d6b, 350f21ecd0.

dream (4-byte cells): 46 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.867 over 46; FLAGGED, among its fastest five and not in the set: 7055894eea, 350f21ecd0, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.955 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 328cec9957.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 7055894eea.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.963 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 350f21ecd0.

dream (8-byte cells): 46 candidates measured; its fastest a8ea0ad5b7 0.376; Spearman with the laptop alone 0.960 over 46; FLAGGED, among its fastest five and not in the set: a8ea0ad5b7, 8cc7f60d6b, c2ef9488ff, 291b405067.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | 0.3429 | 0.3384 | 0.3719 | 0.3507 | ARMv7 +14% | yes |
| 2 | 350f21ecd0 | 0.3550 | 0.3478 | 0.3788 | 0.3603 | x86-64 +4%, x86-32 +3%, ARMv7 +16% | ADDED |
| 3 | 8cc7f60d6b | 0.3475 | 0.3600 | 0.3908 | 0.3656 | x86-64 +1%, x86-32 +6%, ARMv7 +20% | ADDED |
| 4 | 7055894eea | 0.3572 | 0.3443 | 0.4117 | 0.3699 | x86-64 +4%, x86-32 +2%, ARMv7 +26% | - |
| 5 | d47ab67a90 | 0.3721 | 0.3505 | 0.4065 | 0.3757 | x86-64 +9%, x86-32 +4%, ARMv7 +24% | yes |
| 6 | 328cec9957 | 0.3854 | 0.3478 | 0.4006 | 0.3773 | x86-64 +12%, x86-32 +3%, ARMv7 +23% | - |
| 7 | c7814def6d | 0.3640 | 0.4589 | 0.3267 | 0.3793 | x86-64 +6%, x86-32 +36% | ADDED |
| 8 | 9f8811f7f4 | 0.3627 | 0.4538 | 0.3324 | 0.3796 | x86-64 +6%, x86-32 +34%, ARMv7 +2% | yes |
| 9 | 690981ca5b | 0.4152 | 0.4537 | 0.3290 | 0.3957 | x86-64 +21%, x86-32 +34%, ARMv7 +1% | - |
| 10 | 3452cb633b | 0.4156 | 0.4556 | 0.3292 | 0.3965 | x86-64 +21%, x86-32 +35%, ARMv7 +1% | - |
| 11 | 51ad64b5f0 | 0.3886 | 0.4645 | 0.3482 | 0.3976 | x86-64 +13%, x86-32 +37%, ARMv7 +7% | yes |
| 12 | a8ea0ad5b7 | 0.3499 | 0.3963 | 0.4668 | 0.4015 | x86-64 +2%, x86-32 +17%, ARMv7 +43% | - |
| 13 | f3e832ef82 | 0.4495 | 0.4420 | 0.3640 | 0.4166 | x86-64 +31%, x86-32 +31%, ARMv7 +11% | yes |
| 14 | 8642898a7d | 0.4470 | 0.4192 | 0.5107 | 0.4574 | x86-64 +30%, x86-32 +24%, ARMv7 +56% | yes |
| 15 | 0e192e15fc | 0.6357 | 0.6400 | 0.5117 | 0.5927 | x86-64 +85%, x86-32 +89%, ARMv7 +57% | yes |
| 16 | fb0d57c8a2 | 0.9156 | 0.8809 | 0.5214 | 0.7492 | x86-64 +167%, x86-32 +160%, ARMv7 +60% | yes |
| 17 | 7a248231e7 | 1.0383 | 0.9749 | 0.8980 | 0.9687 | x86-64 +203%, x86-32 +188%, ARMv7 +175% | yes |
| 18 | 4dd4e3e7e2 | 2.0209 | 2.3826 | 1.9896 | 2.1238 | x86-64 +489%, x86-32 +604%, ARMv7 +509% | yes |

**The generic pick**: 782f3ad7ff, the mean 0.3507, within 25% of every class's best.
Each class's fastest: x86-64 782f3ad7ff; x86-32 782f3ad7ff; ARMv7 c7814def6d.
**Added to the set across machines** (never taken out): 350f21ecd0 - across machines: the best mean #2; 8cc7f60d6b - across machines: the best mean #3; c7814def6d - across machines: the fastest at ARMv7.
