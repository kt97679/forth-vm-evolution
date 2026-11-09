# Seed 90's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 634)

`python3 lab/evolve/final-pick.py results/followup-seed90.md results/chain-followup90/s1/loadtest.md results/chain-followup90/s1/*.out.json --also-session results/chain-followup90/s2 ... s20` - the laptop 20 sessions (10 rounds), dream 10 at 8-byte cells and 10 at 4-byte, the Tegra 2 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-631.md: results/followup-roles-seed90.md.

# The final set, re-measured - 7 candidates, 7 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup90/s2, results/chain-followup90/s3, results/chain-followup90/s4, results/chain-followup90/s5, results/chain-followup90/s6, results/chain-followup90/s7, results/chain-followup90/s8, results/chain-followup90/s9, results/chain-followup90/s10, results/chain-followup90/s11, results/chain-followup90/s12, results/chain-followup90/s13, results/chain-followup90/s14, results/chain-followup90/s15, results/chain-followup90/s16, results/chain-followup90/s17, results/chain-followup90/s18, results/chain-followup90/s19, results/chain-followup90/s20 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | fastest, fastest at 32 bits | 0.3044 (0.2921) | 26,242 | 148 | 0.3226 (0.3087) | 0.975 | 0.18951 |
| 2 | 64a7345393 | smallest | 1.5696 (1.5810) | 13,891 | 116 | 1.6034 (1.6240) | 1.005 | 0.00865 |
| 3 | fb0d57c8a2 | least memory | 0.8253 (0.8244) | 17,830 | 104 | 0.7664 (0.7667) | 1.003 | 0.02825 |
| 4 | ae99617f06 | adds the most | 0.3833 (0.3752) | 18,599 | 124 | 0.4123 (0.4045) | 0.980 | 0.03193 |
| 5 | 3eb59b271d | adds the most, the knee | 0.3349 (0.3188) | 22,522 | 132 | 0.3371 (0.3220) | 0.975 | 0.00529 |
| 6 | 11a56ff9e4 | adds the most | 0.3469 (0.3345) | 19,761 | 140 | 0.3614 (0.3464) | 0.982 | 0.00137 |
| 7 | c2ef9488ff | adds the most | 0.3323 (0.3324) | 20,901 | 140 | 0.3773 (0.3767) | 0.971 | 0.00024 |

Against the in-run set: in now 11a56ff9e4, 3eb59b271d, 64a7345393, 782f3ad7ff, ae99617f06, c2ef9488ff, fb0d57c8a2; out now none - both kept as candidates.
Under load: the same set and extremes.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.339; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 11a56ff9e4 0.378; Spearman with the laptop alone 0.786 over 7.

rage (4-byte cells): 7 candidates measured; its fastest 3eb59b271d 0.318; Spearman with the laptop alone 0.679 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.346; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.359; Spearman with the laptop alone 0.893 over 7.

rage (4-byte cells): 7 candidates measured; its fastest 3eb59b271d 0.323; Spearman with the laptop alone 0.714 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.750 over 7.

dream (8-byte cells): 7 candidates measured; its fastest c2ef9488ff 0.377; Spearman with the laptop alone 0.929 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.345; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 11a56ff9e4 0.377; Spearman with the laptop alone 0.786 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.342; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 11a56ff9e4 0.380; Spearman with the laptop alone 0.786 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.348; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.378; Spearman with the laptop alone 0.893 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.345; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest c2ef9488ff 0.382; Spearman with the laptop alone 0.821 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.330; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.378; Spearman with the laptop alone 0.893 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.339; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.380; Spearman with the laptop alone 0.964 over 7.

dream (4-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.786 over 7.

dream (8-byte cells): 7 candidates measured; its fastest 782f3ad7ff 0.358; Spearman with the laptop alone 0.964 over 7.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | 0.3383 | 0.3328 | 0.3709 | 0.3469 | ARMv7 +16% | yes |
| 2 | 3eb59b271d | 0.3746 | 0.4376 | 0.3202 | 0.3744 | x86-64 +11%, x86-32 +31% | yes |
| 3 | 11a56ff9e4 | 0.3628 | 0.3769 | 0.4773 | 0.4026 | x86-64 +7%, x86-32 +13%, ARMv7 +49% | yes |
| 4 | c2ef9488ff | 0.3573 | 0.3909 | 0.4757 | 0.4050 | x86-64 +6%, x86-32 +17%, ARMv7 +49% | yes |
| 5 | ae99617f06 | 0.4459 | 0.4390 | 0.3520 | 0.4100 | x86-64 +32%, x86-32 +32%, ARMv7 +10% | yes |
| 6 | fb0d57c8a2 | 0.9125 | 0.8780 | 0.5205 | 0.7471 | x86-64 +170%, x86-32 +164%, ARMv7 +63% | yes |
| 7 | 64a7345393 | 1.9399 | 1.8524 | 1.8385 | 1.8764 | x86-64 +473%, x86-32 +457%, ARMv7 +474% | yes |

**The generic pick**: 782f3ad7ff, the mean 0.3469, within 25% of every class's best.
Each class's fastest: x86-64 782f3ad7ff; x86-32 782f3ad7ff; ARMv7 3eb59b271d.
**Added to the set across machines** (never taken out): none - the set holds them.
