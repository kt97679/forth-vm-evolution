# The 282 portable designs found before seed 87, re-measured on three machines, every complete session pooled (Iteration 610)

`python3 lab/evolve/final-pick.py results/portable-front-seed86.md results/chain-seed87/s1/loadtest.md results/chain-seed87/s1/*.out.json --also-session results/chain-seed87/s2 ... s10 --also-session results/chain-seed87-interrupted/s1 ... s9` - the laptop 1 session (5 rounds), dream 18 sessions at 4-byte cells and 10 at 8-byte, the Tegra 4. process-seed.sh's own pick read each line's first session only; pooled, the ARMv7 fastest is 3452cb633b (0.3280) by 0.3% over 690981ca5b (0.3291) - each the fastest in two of the Tegra's four sessions: a tie. Each host's per-session lines below, then the set and the classes.

# The final set, re-measured - 282 candidates, 282 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and /tmp/sessions87/chain/s2, /tmp/sessions87/chain/s3, /tmp/sessions87/chain/s4, /tmp/sessions87/chain/s5, /tmp/sessions87/chain/s6, /tmp/sessions87/chain/s7, /tmp/sessions87/chain/s8, /tmp/sessions87/chain/s9, /tmp/sessions87/chain/s10, /tmp/sessions87/interrupted/s1, /tmp/sessions87/interrupted/s2, /tmp/sessions87/interrupted/s3, /tmp/sessions87/interrupted/s4, /tmp/sessions87/interrupted/s5, /tmp/sessions87/interrupted/s6, /tmp/sessions87/interrupted/s7, /tmp/sessions87/interrupted/s8, /tmp/sessions87/interrupted/s9 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 8cc7f60d6b | fastest | 0.3109 (0.2978) | 26,130 | 148 | 0.3357 (0.3205) | 0.984 | 0.18494 |
| 2 | cea114f47e | smallest | 1.5995 (1.5960) | 13,939 | 116 | 1.6307 (1.6331) | 1.013 | 0.00811 |
| 3 | fb0d57c8a2 | least memory | 0.8310 (0.8178) | 17,830 | 104 | 0.7698 (0.7819) | 1.002 | 0.02818 |
| 4 | 1f2e71902c | fastest at 32 bits, the knee | 0.3408 (0.3362) | 21,701 | 148 | 0.3243 (0.3206) | 0.991 | 0.01627 |
| 5 | 22420b3b61 | adds the most | 0.4164 (0.3968) | 18,928 | 120 | 0.4643 (0.4352) | 0.968 | 0.01927 |
| 6 | e6ca8a928f | adds the most | 0.5987 (0.5740) | 15,924 | 136 | 0.5076 (0.5051) | 0.980 | 0.00626 |
| 7 | dea923f5a8 | adds the most | 0.3594 (0.3379) | 23,495 | 124 | 0.3727 (0.3479) | 0.959 | 0.00412 |
| 8 | 2a8401f193 | adds the most | 0.8864 (0.9274) | 14,741 | 112 | 0.8332 (0.8405) | 1.001 | 0.00199 |
| 9 | 7aa49309c5 | adds the most | 0.4038 (0.3927) | 18,381 | 136 | 0.3901 (0.3606) | 0.988 | 0.00195 |
| 10 | 491139cdbc | adds the most | 0.6926 (0.6686) | 15,957 | 112 | 0.6611 (0.6694) | 0.972 | 0.00121 |

Against the in-run set: in now 1f2e71902c, 22420b3b61, 2a8401f193, 491139cdbc, 7aa49309c5, 8cc7f60d6b, cea114f47e, dea923f5a8, e6ca8a928f, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest 8cc7f60d6b; smallest bee0b97bb5; least memory fb0d57c8a2; fastest at 32 bits 296ce280ac; in the set under load only 296ce280ac, 9e66aa9ce6, bee0b97bb5, alone only 1f2e71902c, 7aa49309c5, cea114f47e.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.368; Spearman with the laptop alone 0.981 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, f55cec5849, 14c3222ba1, 88c83a0def.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.370; Spearman with the laptop alone 0.980 over 282; FLAGGED, among its fastest five and not in the set: 8d227f588f, 4b4afda2e8, fc5a62af47, b1022c7066.

rage (4-byte cells): 282 candidates measured; its fastest 690981ca5b 0.325; Spearman with the laptop alone 0.935 over 282; FLAGGED, among its fastest five and not in the set: 690981ca5b, 3452cb633b, 44f2b94ce9, ce4baefaf5.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.364; Spearman with the laptop alone 0.983 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 4b4afda2e8, 88c83a0def, 14c3222ba1.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.979 over 282; FLAGGED, among its fastest five and not in the set: 4b4afda2e8, 88c83a0def, b1022c7066, 14c3222ba1.

rage (4-byte cells): 282 candidates measured; its fastest 690981ca5b 0.326; Spearman with the laptop alone 0.935 over 282; FLAGGED, among its fastest five and not in the set: 690981ca5b, 3452cb633b, ce4baefaf5, 44f2b94ce9.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.367; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, f55cec5849, 4b4afda2e8, b1022c7066, 88c83a0def.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.978 over 282; FLAGGED, among its fastest five and not in the set: 88c83a0def, 4b4afda2e8, b1022c7066, 14c3222ba1.

rage (4-byte cells): 282 candidates measured; its fastest 3452cb633b 0.328; Spearman with the laptop alone 0.935 over 282; FLAGGED, among its fastest five and not in the set: 3452cb633b, 690981ca5b, 44f2b94ce9, ce4baefaf5, 3e2b120cba.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.372; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 4b4afda2e8, 88c83a0def, 14c3222ba1.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.979 over 282; FLAGGED, among its fastest five and not in the set: 88c83a0def, fc5a62af47, b1022c7066, 8d227f588f.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.368; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, f55cec5849, 4b4afda2e8, 14c3222ba1.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.369; Spearman with the laptop alone 0.979 over 282; FLAGGED, among its fastest five and not in the set: 88c83a0def, 14c3222ba1, 4b4afda2e8, fc5a62af47.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.367; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 4b4afda2e8, 88c83a0def, 14c3222ba1, fc5a62af47.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.366; Spearman with the laptop alone 0.978 over 282; FLAGGED, among its fastest five and not in the set: 88c83a0def, 14c3222ba1, 4b4afda2e8, 8d227f588f.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.368; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 88c83a0def, f55cec5849, 14c3222ba1, 4b4afda2e8.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.370; Spearman with the laptop alone 0.980 over 282; FLAGGED, among its fastest five and not in the set: 88c83a0def, 4b4afda2e8, 14c3222ba1, b1022c7066.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.367; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 14c3222ba1, f55cec5849, 4b4afda2e8, 88c83a0def.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.978 over 282; FLAGGED, among its fastest five and not in the set: 14c3222ba1, 88c83a0def, 4b4afda2e8, 8d227f588f.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.370; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 88c83a0def, f55cec5849, 14c3222ba1.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.979 over 282; FLAGGED, among its fastest five and not in the set: 88c83a0def, 14c3222ba1, fc5a62af47, b1022c7066.

dream (8-byte cells): 282 candidates measured; its fastest 1f2e71902c 0.370; Spearman with the laptop alone 0.979 over 282; FLAGGED, among its fastest five and not in the set: 14c3222ba1, 4b4afda2e8, fc5a62af47, b1022c7066.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.367; Spearman with the laptop alone 0.983 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, b1022c7066, 88c83a0def, 4b4afda2e8.

rage (4-byte cells): 282 candidates measured; its fastest 3452cb633b 0.327; Spearman with the laptop alone 0.935 over 282; FLAGGED, among its fastest five and not in the set: 3452cb633b, 690981ca5b, 44f2b94ce9, ce4baefaf5, 3e2b120cba.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.368; Spearman with the laptop alone 0.983 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 4b4afda2e8, 88c83a0def, f55cec5849.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.368; Spearman with the laptop alone 0.983 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 14c3222ba1, f55cec5849, 4b4afda2e8.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.366; Spearman with the laptop alone 0.983 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, f55cec5849, 88c83a0def, 14c3222ba1.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.364; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 4b4afda2e8, 88c83a0def, f55cec5849, 8d227f588f.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.366; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 88c83a0def, 4b4afda2e8, f55cec5849.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.367; Spearman with the laptop alone 0.982 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, f55cec5849, 4b4afda2e8, 88c83a0def.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.369; Spearman with the laptop alone 0.983 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, 14c3222ba1, f55cec5849, 88c83a0def, 4b4afda2e8.

dream (4-byte cells): 282 candidates measured; its fastest 5c0e405cec 0.368; Spearman with the laptop alone 0.983 over 282; FLAGGED, among its fastest five and not in the set: 5c0e405cec, f55cec5849, 4b4afda2e8, 88c83a0def, fc5a62af47.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | f55cec5849 | 0.3634 | 0.3535 | 0.3858 | 0.3673 | x86-64 +5%, x86-32 +1%, ARMv7 +18% | ADDED |
| 2 | 8cc7f60d6b | 0.3460 | 0.3615 | 0.3966 | 0.3675 | x86-32 +4%, ARMv7 +21% | yes |
| 3 | 5c0e405cec | 0.3604 | 0.3575 | 0.3975 | 0.3714 | x86-64 +4%, x86-32 +2%, ARMv7 +21% | ADDED |
| 4 | 1f2e71902c | 0.3541 | 0.3489 | 0.4578 | 0.3839 | x86-64 +2%, ARMv7 +40% | yes |
| 5 | 0d2912ef80 | 0.3570 | 0.3813 | 0.4247 | 0.3867 | x86-64 +3%, x86-32 +9%, ARMv7 +29% | - |
| 6 | 88c83a0def | 0.3585 | 0.3632 | 0.4544 | 0.3897 | x86-64 +4%, x86-32 +4%, ARMv7 +39% | - |
| 7 | 14c3222ba1 | 0.3590 | 0.3642 | 0.4556 | 0.3905 | x86-64 +4%, x86-32 +4%, ARMv7 +39% | - |
| 8 | 8d227f588f | 0.3650 | 0.3567 | 0.4579 | 0.3906 | x86-64 +5%, x86-32 +2%, ARMv7 +40% | - |
| 9 | b1022c7066 | 0.3651 | 0.3595 | 0.4569 | 0.3914 | x86-64 +6%, x86-32 +3%, ARMv7 +39% | - |
| 10 | 4b4afda2e8 | 0.3601 | 0.3654 | 0.4562 | 0.3916 | x86-64 +4%, x86-32 +5%, ARMv7 +39% | - |
| 11 | fc5a62af47 | 0.3674 | 0.3582 | 0.4576 | 0.3920 | x86-64 +6%, x86-32 +3%, ARMv7 +39% | - |
| 12 | 690981ca5b | 0.4178 | 0.4512 | 0.3291 | 0.3959 | x86-64 +21%, x86-32 +29% | - |
| 13 | 3452cb633b | 0.4168 | 0.4591 | 0.3280 | 0.3974 | x86-64 +20%, x86-32 +32% | ADDED |
| 14 | dea923f5a8 | 0.4047 | 0.4724 | 0.3474 | 0.4050 | x86-64 +17%, x86-32 +35%, ARMv7 +6% | yes |
| 15 | 22420b3b61 | 0.4723 | 0.4852 | 0.3654 | 0.4375 | x86-64 +36%, x86-32 +39%, ARMv7 +11% | yes |
| 16 | 7aa49309c5 | 0.4349 | 0.4072 | 0.5089 | 0.4483 | x86-64 +26%, x86-32 +17%, ARMv7 +55% | yes |
| 17 | e6ca8a928f | 0.6712 | 0.6468 | 0.5022 | 0.6019 | x86-64 +94%, x86-32 +85%, ARMv7 +53% | yes |
| 18 | 491139cdbc | 0.7871 | 0.7556 | 0.5276 | 0.6795 | x86-64 +127%, x86-32 +117%, ARMv7 +61% | yes |
| 19 | fb0d57c8a2 | 0.9201 | 0.8835 | 0.5250 | 0.7529 | x86-64 +166%, x86-32 +153%, ARMv7 +60% | yes |
| 20 | 2a8401f193 | 1.0707 | 0.9726 | 1.0111 | 1.0174 | x86-64 +209%, x86-32 +179%, ARMv7 +208% | yes |
| 21 | cea114f47e | 1.9958 | 1.9306 | 1.9700 | 1.9652 | x86-64 +477%, x86-32 +453%, ARMv7 +501% | yes |

**The generic pick**: f55cec5849, the mean 0.3673, within 25% of every class's best.
Each class's fastest: x86-64 8cc7f60d6b; x86-32 1f2e71902c; ARMv7 3452cb633b.
**Added to the set across machines** (never taken out): f55cec5849 - across machines: the best mean #1; 5c0e405cec - across machines: the best mean #3; 3452cb633b - across machines: the fastest at ARMv7.
