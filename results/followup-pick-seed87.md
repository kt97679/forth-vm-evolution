# Seed 87's best beside the 282's, re-measured on three machines, every session pooled (Iteration 611)

`python3 lab/evolve/final-pick.py results/followup-seed87.md results/chain-followup87/s1/loadtest.md results/chain-followup87/s1/*.out.json --also-session results/chain-followup87/s2 ... s45` - the laptop 28 sessions (10 rounds), dream 45 at 8-byte cells and 41 at 4-byte, the Tegra 5. The roles against results/handoff-relf-601.md: results/followup-roles-seed87.md.

# The final set, re-measured - 45 candidates, 45 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): this one and results/chain-followup87/s2, results/chain-followup87/s3, results/chain-followup87/s4, results/chain-followup87/s5, results/chain-followup87/s6, results/chain-followup87/s7, results/chain-followup87/s8, results/chain-followup87/s9, results/chain-followup87/s10, results/chain-followup87/s11, results/chain-followup87/s12, results/chain-followup87/s13, results/chain-followup87/s14, results/chain-followup87/s15, results/chain-followup87/s16, results/chain-followup87/s17, results/chain-followup87/s18, results/chain-followup87/s19, results/chain-followup87/s20, results/chain-followup87/s21, results/chain-followup87/s22, results/chain-followup87/s23, results/chain-followup87/s24, results/chain-followup87/s25, results/chain-followup87/s26, results/chain-followup87/s27, results/chain-followup87/s28, results/chain-followup87/s29, results/chain-followup87/s30, results/chain-followup87/s31, results/chain-followup87/s32, results/chain-followup87/s33, results/chain-followup87/s34, results/chain-followup87/s35, results/chain-followup87/s36, results/chain-followup87/s37, results/chain-followup87/s38, results/chain-followup87/s39, results/chain-followup87/s40, results/chain-followup87/s41, results/chain-followup87/s42, results/chain-followup87/s43, results/chain-followup87/s44, results/chain-followup87/s45 - the laptop's re-measures each the geometric mean of the sessions that have it; each host's lines its mean in step 5, each named in step 4.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | fastest | 0.3069 (0.2921) | 26,242 | 148 | 0.3271 (0.3087) | 0.976 | 0.18764 |
| 2 | 62abdb2c64 | smallest | 1.8559 (1.8620) | 13,803 | 120 | 2.1399 (2.1971) | 1.010 | 0.00329 |
| 3 | fb0d57c8a2 | least memory | 0.8272 (0.8310) | 17,830 | 104 | 0.7699 (0.7698) | 1.002 | 0.03231 |
| 4 | 9f8811f7f4 | fastest at 32 bits | 0.3074 (0.2967) | 33,747 | 132 | 0.3128 (0.2947) | 0.972 | 0.01243 |
| 5 | a627b954c6 | adds the most | 0.3853 (0.3712) | 18,607 | 124 | 0.4138 (0.4013) | 0.984 | 0.02538 |
| 6 | 58479dda0a | adds the most | 0.5890 (0.5760) | 15,836 | 120 | 0.5288 (0.5189) | 0.992 | 0.00814 |
| 7 | 12c66adc50 | adds the most | 0.3535 (0.3378) | 19,985 | 140 | 0.3590 (0.3303) | 0.977 | 0.00322 |
| 8 | ce5bbc5dc2 | adds the most | 0.8658 (0.8717) | 14,541 | 116 | 0.8206 (0.8247) | 1.001 | 0.00227 |
| 9 | bdfd4fb056 | adds the most | 0.6530 (0.6546) | 15,765 | 112 | 0.6688 (0.6636) | 1.003 | 0.00133 |
| 10 | 51ad64b5f0 | adds the most | 0.3507 (0.3301) | 27,525 | 124 | 0.3330 (0.3098) | 0.977 | 0.00133 |

Against the in-run set: in now 12c66adc50, 51ad64b5f0, 58479dda0a, 62abdb2c64, 782f3ad7ff, 9f8811f7f4, a627b954c6, bdfd4fb056, ce5bbc5dc2, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest 9f8811f7f4; smallest 62abdb2c64; least memory fb0d57c8a2; fastest at 32 bits a2df4ef183; in the set under load only 1f2e71902c, a2df4ef183, alone only 12c66adc50, bdfd4fb056.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.765 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

rage (4-byte cells): 45 candidates measured; its fastest 3452cb633b 0.328; Spearman with the laptop alone 0.841 over 45; FLAGGED, among its fastest five and not in the set: 3452cb633b, 690981ca5b, a2df4ef183, b35ae710e6.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.353; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.366; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

rage (4-byte cells): 45 candidates measured; its fastest 3452cb633b 0.329; Spearman with the laptop alone 0.837 over 45; FLAGGED, among its fastest five and not in the set: 3452cb633b, 690981ca5b, a2df4ef183, b35ae710e6.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.354; Spearman with the laptop alone 0.770 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.936 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, c2ef9488ff.

rage (4-byte cells): 45 candidates measured; its fastest 690981ca5b 0.329; Spearman with the laptop alone 0.835 over 45; FLAGGED, among its fastest five and not in the set: 690981ca5b, 3452cb633b, a2df4ef183, b35ae710e6.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.936 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

rage (4-byte cells): 45 candidates measured; its fastest 3452cb633b 0.329; Spearman with the laptop alone 0.837 over 45; FLAGGED, among its fastest five and not in the set: 3452cb633b, 690981ca5b, a2df4ef183, b35ae710e6.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.769 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.366; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

rage (4-byte cells): 45 candidates measured; its fastest 3452cb633b 0.329; Spearman with the laptop alone 0.853 over 45; FLAGGED, among its fastest five and not in the set: 3452cb633b, 690981ca5b, a2df4ef183, b35ae710e6.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.936 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.348; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.369; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.765 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.935 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, c2ef9488ff.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.765 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.366; Spearman with the laptop alone 0.942 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.364; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.765 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.369; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.940 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.940 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.770 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.369; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.355; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.370; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.369; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.352; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 72dd720079.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.354; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.934 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.353; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.347; Spearman with the laptop alone 0.765 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.765 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.935 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 213415ff71, 05dfa902ed, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.348; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.369; Spearman with the laptop alone 0.940 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.369; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.768 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.366; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.765 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.366; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.351; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.936 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.349; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.933 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.352; Spearman with the laptop alone 0.767 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.371; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.355; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, f55cec5849, 1f2e71902c.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (4-byte cells): 45 candidates measured; its fastest 782f3ad7ff 0.350; Spearman with the laptop alone 0.766 over 45; FLAGGED, among its fastest five and not in the set: 350f21ecd0, 5c0e405cec, 1f2e71902c, f55cec5849.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.370; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.374; Spearman with the laptop alone 0.938 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.368; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.365; Spearman with the laptop alone 0.939 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

dream (8-byte cells): 45 candidates measured; its fastest 1f2e71902c 0.367; Spearman with the laptop alone 0.937 over 45; FLAGGED, among its fastest five and not in the set: 1f2e71902c, 05dfa902ed, 213415ff71, 8cc7f60d6b.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 782f3ad7ff | 0.3428 | 0.3387 | 0.3715 | 0.3507 | ARMv7 +13% | yes |
| 2 | 350f21ecd0 | 0.3545 | 0.3486 | 0.3779 | 0.3601 | x86-64 +3%, x86-32 +3%, ARMv7 +15% | ADDED |
| 3 | 8cc7f60d6b | 0.3475 | 0.3606 | 0.3915 | 0.3661 | x86-64 +1%, x86-32 +6%, ARMv7 +19% | ADDED |
| 4 | f55cec5849 | 0.3620 | 0.3581 | 0.3898 | 0.3697 | x86-64 +6%, x86-32 +6%, ARMv7 +18% | - |
| 5 | 5c0e405cec | 0.3606 | 0.3571 | 0.3996 | 0.3719 | x86-64 +5%, x86-32 +5%, ARMv7 +21% | - |
| 6 | 9f8811f7f4 | 0.3610 | 0.4527 | 0.3353 | 0.3798 | x86-64 +5%, x86-32 +34%, ARMv7 +2% | yes |
| 7 | a2df4ef183 | 0.3613 | 0.4542 | 0.3351 | 0.3803 | x86-64 +5%, x86-32 +34%, ARMv7 +2% | - |
| 8 | 72dd720079 | 0.3766 | 0.3605 | 0.4153 | 0.3834 | x86-64 +10%, x86-32 +6%, ARMv7 +26% | - |
| 9 | b35ae710e6 | 0.3680 | 0.4594 | 0.3405 | 0.3861 | x86-64 +7%, x86-32 +36%, ARMv7 +3% | - |
| 10 | 1f2e71902c | 0.3543 | 0.3582 | 0.4571 | 0.3871 | x86-64 +3%, x86-32 +6%, ARMv7 +39% | - |
| 11 | 05dfa902ed | 0.3625 | 0.3594 | 0.4673 | 0.3934 | x86-64 +6%, x86-32 +6%, ARMv7 +42% | - |
| 12 | 3452cb633b | 0.4155 | 0.4555 | 0.3295 | 0.3966 | x86-64 +21%, x86-32 +34% | ADDED |
| 13 | 51ad64b5f0 | 0.3885 | 0.4649 | 0.3508 | 0.3986 | x86-64 +13%, x86-32 +37%, ARMv7 +6% | yes |
| 14 | a627b954c6 | 0.4521 | 0.4429 | 0.3593 | 0.4159 | x86-64 +32%, x86-32 +31%, ARMv7 +9% | yes |
| 15 | 12c66adc50 | 0.3814 | 0.3886 | 0.5224 | 0.4262 | x86-64 +11%, x86-32 +15%, ARMv7 +59% | yes |
| 16 | 58479dda0a | 0.6714 | 0.6572 | 0.4955 | 0.6024 | x86-64 +96%, x86-32 +94%, ARMv7 +50% | yes |
| 17 | bdfd4fb056 | 0.7741 | 0.7383 | 0.5305 | 0.6718 | x86-64 +126%, x86-32 +118%, ARMv7 +61% | yes |
| 18 | fb0d57c8a2 | 0.9164 | 0.8836 | 0.5215 | 0.7502 | x86-64 +167%, x86-32 +161%, ARMv7 +58% | yes |
| 19 | ce5bbc5dc2 | 1.0792 | 0.9940 | 0.9115 | 0.9925 | x86-64 +215%, x86-32 +193%, ARMv7 +177% | yes |
| 20 | 62abdb2c64 | 2.2398 | 2.3867 | 2.0103 | 2.2068 | x86-64 +553%, x86-32 +605%, ARMv7 +510% | yes |

**The generic pick**: 782f3ad7ff, the mean 0.3507, within 25% of every class's best.
Each class's fastest: x86-64 782f3ad7ff; x86-32 782f3ad7ff; ARMv7 3452cb633b.
**Added to the set across machines** (never taken out): 350f21ecd0 - across machines: the best mean #2; 8cc7f60d6b - across machines: the best mean #3; 3452cb633b - across machines: the fastest at ARMv7.
