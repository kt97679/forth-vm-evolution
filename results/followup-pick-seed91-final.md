# Seed 91-final's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration 648)

`python3 lab/evolve/final-pick.py results/followup-seed91-final.md results/chain-followup91-final/s1/loadtest.md results/chain-followup91-final/s1/*.out.json --also-session results/chain-followup91-final/s2 ... s7` - the laptop 5 sessions (10 rounds), dream 7 at 8-byte cells and 7 at 4-byte, the Tegra 2 (lab/evolve/process-followup.sh). The roles against results/handoff-relf-636.md: results/followup-roles-seed91-final.md.

# The final set, re-measured - 435 candidates, 435 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup91-final/s2, results/chain-followup91-final/s3, results/chain-followup91-final/s4, results/chain-followup91-final/s5, results/chain-followup91-final/s6, results/chain-followup91-final/s7 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 7fb40ff7ba | fastest | 0.2856 (0.2721) | 35,126 | 140 | 0.3293 (0.3360) | 0.976 | 0.15443 |
| 2 | 01712a2639 | smallest | 1.6118 (1.6226) | 13,691 | 120 | 1.9792 (1.9975) | 1.003 | 0.00719 |
| 3 | fb0d57c8a2 | least memory | 0.8255 (0.8253) | 17,830 | 104 | 0.7712 (0.7664) | 1.007 | 0.04190 |
| 4 | e523a45566 | fastest at 32 bits | 0.2995 (0.2891) | 33,195 | 136 | 0.3022 (0.2910) | 0.971 | 0.01540 |
| 5 | 6dbd01752e | adds the most | 0.4152 (0.3972) | 18,070 | 120 | 0.3902 (0.3762) | 0.986 | 0.04588 |
| 6 | 88cdf38fbd | adds the most | 0.3343 (0.3178) | 21,986 | 152 | 0.3186 (0.3081) | 0.985 | 0.00955 |
| 7 | c955446411 | adds the most | 0.6133 (0.6058) | 15,684 | 116 | 0.5415 (0.5286) | 0.995 | 0.00745 |
| 8 | 51ad64b5f0 | adds the most | 0.3502 (0.3507) | 27,525 | 124 | 0.3316 (0.3330) | 0.972 | 0.00211 |
| 9 | 0250688840 | adds the most | 0.8626 (0.8722) | 14,405 | 112 | 0.8638 (0.8630) | 1.005 | 0.00206 |
| 10 | 782f3ad7ff | adds the most | 0.3040 (0.3044) | 26,242 | 148 | 0.3235 (0.3226) | 0.979 | 0.00149 |

Against the in-run set: in now 01712a2639, 0250688840, 51ad64b5f0, 6dbd01752e, 782f3ad7ff, 7fb40ff7ba, 88cdf38fbd, c955446411, e523a45566, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest 7fb40ff7ba; smallest 01712a2639; least memory fb0d57c8a2; fastest at 32 bits 95077030b0; in the set under load only 36ad2ffe02, 3eb59b271d, 95077030b0, ca31dceda6, alone only 0250688840, 51ad64b5f0, 88cdf38fbd, e523a45566.

dream (4-byte cells): 435 candidates measured; its fastest 782f3ad7ff 0.348; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: d710e403b0, 4dcea8d430, b311f84693, 350f21ecd0.

dream (8-byte cells): 435 candidates measured; its fastest 7fb40ff7ba 0.374; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: 38100f0280, 00a044c3dc, 11a56ff9e4, b311f84693.

rage (4-byte cells): 435 candidates measured; its fastest 7fb40ff7ba 0.306; Spearman with the laptop alone 0.978 over 435; FLAGGED, among its fastest five and not in the set: 3eb59b271d, 3452cb633b, c7814def6d, 9f8811f7f4.

dream (4-byte cells): 435 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: d710e403b0, b311f84693, 4dcea8d430, 208bd2d2ff.

dream (8-byte cells): 435 candidates measured; its fastest 38100f0280 0.371; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: 38100f0280, 00a044c3dc, 481bcb37ff, 11a56ff9e4.

rage (4-byte cells): 435 candidates measured; its fastest 6f6cbe3f71 0.310; Spearman with the laptop alone 0.978 over 435; FLAGGED, among its fastest five and not in the set: 6f6cbe3f71, 9ca0f67f59, 965f48c803, 768bd275d8.

dream (4-byte cells): 435 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: b311f84693, d710e403b0, 4dcea8d430, 208bd2d2ff.

dream (8-byte cells): 435 candidates measured; its fastest 38100f0280 0.374; Spearman with the laptop alone 0.986 over 435; FLAGGED, among its fastest five and not in the set: 38100f0280, 00a044c3dc, b311f84693.

dream (4-byte cells): 435 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.988 over 435; FLAGGED, among its fastest five and not in the set: b311f84693, d710e403b0, 4dcea8d430.

dream (8-byte cells): 435 candidates measured; its fastest 7fb40ff7ba 0.373; Spearman with the laptop alone 0.986 over 435; FLAGGED, among its fastest five and not in the set: 38100f0280, 00a044c3dc, b311f84693.

dream (4-byte cells): 435 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: b311f84693, d710e403b0, 4dcea8d430, 208bd2d2ff.

dream (8-byte cells): 435 candidates measured; its fastest 7fb40ff7ba 0.373; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: 00a044c3dc, 38100f0280, b311f84693.

dream (4-byte cells): 435 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.988 over 435; FLAGGED, among its fastest five and not in the set: b311f84693, d710e403b0, 4dcea8d430, 208bd2d2ff.

dream (8-byte cells): 435 candidates measured; its fastest 38100f0280 0.372; Spearman with the laptop alone 0.986 over 435; FLAGGED, among its fastest five and not in the set: 38100f0280, 00a044c3dc, b311f84693.

dream (4-byte cells): 435 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: b311f84693, d710e403b0, 4dcea8d430, 350f21ecd0.

dream (8-byte cells): 435 candidates measured; its fastest 38100f0280 0.375; Spearman with the laptop alone 0.987 over 435; FLAGGED, among its fastest five and not in the set: 38100f0280, 00a044c3dc, 11a56ff9e4, 481bcb37ff.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | 0.3412 | 0.3365 | 0.3552 | 0.3442 | x86-64 +4%, ARMv7 +15% | yes |
| 2 | b311f84693 | 0.3412 | 0.3374 | 0.3679 | 0.3486 | x86-64 +4%, ARMv7 +19% | ADDED |
| 3 | 350f21ecd0 | 0.3534 | 0.3452 | 0.3613 | 0.3532 | x86-64 +8%, x86-32 +3%, ARMv7 +17% | ADDED |
| 4 | 208bd2d2ff | 0.3475 | 0.3424 | 0.3728 | 0.3540 | x86-64 +6%, x86-32 +2%, ARMv7 +20% | - |
| 5 | 7fb40ff7ba | 0.3273 | 0.4419 | 0.3099 | 0.3552 | x86-32 +31% | yes |
| 6 | e523a45566 | 0.3541 | 0.4100 | 0.3194 | 0.3592 | x86-64 +8%, x86-32 +22%, ARMv7 +3% | yes |
| 7 | d710e403b0 | 0.3527 | 0.3387 | 0.3959 | 0.3617 | x86-64 +8%, x86-32 +1%, ARMv7 +28% | - |
| 8 | 8cc7f60d6b | 0.3469 | 0.3601 | 0.3810 | 0.3624 | x86-64 +6%, x86-32 +7%, ARMv7 +23% | - |
| 9 | 38100f0280 | 0.3314 | 0.4518 | 0.3217 | 0.3639 | x86-64 +1%, x86-32 +34%, ARMv7 +4% | - |
| 10 | 88cdf38fbd | 0.3646 | 0.3400 | 0.3919 | 0.3649 | x86-64 +11%, x86-32 +1%, ARMv7 +26% | yes |
| 11 | 3060f04651 | 0.3549 | 0.4093 | 0.3382 | 0.3662 | x86-64 +8%, x86-32 +22%, ARMv7 +9% | - |
| 12 | 4dcea8d430 | 0.3518 | 0.3489 | 0.4011 | 0.3665 | x86-64 +7%, x86-32 +4%, ARMv7 +29% | - |
| 13 | 51ad64b5f0 | 0.3884 | 0.4645 | 0.3346 | 0.3923 | x86-64 +19%, x86-32 +38%, ARMv7 +8% | yes |
| 14 | 6dbd01752e | 0.4686 | 0.4314 | 0.3765 | 0.4238 | x86-64 +43%, x86-32 +28%, ARMv7 +22% | yes |
| 15 | c955446411 | 0.6834 | 0.6891 | 0.5023 | 0.6185 | x86-64 +109%, x86-32 +105%, ARMv7 +62% | yes |
| 16 | fb0d57c8a2 | 0.9114 | 0.8870 | 0.4996 | 0.7392 | x86-64 +178%, x86-32 +164%, ARMv7 +61% | yes |
| 17 | 0250688840 | 1.0905 | 1.0325 | 0.9815 | 1.0339 | x86-64 +233%, x86-32 +207%, ARMv7 +217% | yes |
| 18 | 01712a2639 | 2.0083 | 2.2024 | 1.9421 | 2.0480 | x86-64 +514%, x86-32 +554%, ARMv7 +527% | yes |

**The generic pick**: 782f3ad7ff, the mean 0.3442, within 25% of every class's best.
Each class's fastest: x86-64 7fb40ff7ba; x86-32 782f3ad7ff; ARMv7 7fb40ff7ba.
**Added to the set across machines** (never taken out): b311f84693 - across machines: the best mean #2; 350f21ecd0 - across machines: the best mean #3.
