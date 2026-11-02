# The final pick's chain B - the shortlist across three machines (Iteration 587)

Chain aee0a409c on fury, 2026-11-02 16:06-19:02 (the owner's re-pack; the first pack, 18:34, held no remote result - 586):
tests PASS, the stages 7 of 7 IDENTICAL, the jail PASS; loadtest.py --ids results/shortlist-seed86.md --rounds 5 - 40 of
40 re-measured at both widths, alone and under load, in 14 minutes. Every remote line measured all it was given and
exited 0: rage 237 of 237 (233 asked - the 232 candidates and 1 of the 8 msc designs - and 4 sampled; 227 cross-built,
10 built there by its GCC 16, 9 of them lto=1, linked with 585's -u raise and alive) at 2 rounds a design; dream 44 of 44
at each width (the 40 and 4 sampled). Each host's readings and the laptop's are kept in results/chainB-seed86/ - chain
A's were not, so its dream session cannot be compared from the repository.

## Why 2.9 hours, not the 12 planned - nothing cut

The 12 hours were the owner's window; an experiment chain ends when its work is done, and none of it was cut: rage used
154 of its 540 minutes, dream about 3 minutes a width. 585's "about 10-11 hours" read seed 86's rage time - 15 designs in
about 28 minutes - as a per-design rate, but about 16 of those minutes are the stages built on the Tegra once (here the
load 7-8 on its 4 CPUs for the first 16 minutes, then about 1.4): measured, 35 seconds a design at 2 rounds. The lines
ran one after another inside the launch (586's fault, fixed for later chains) - rage 16:20-18:55, dream's two
18:55-19:01 - so the chain's end is rage's. The only designs not measured are 7 of retire-plan-583's 8 msc designs,
never asked for (585's lookup missed the clone's own database, fixed at 586): chain C measures all 8.

# The final set, re-measured - 40 candidates, 40 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | c7c35f9c97 | fastest | 0.1385 (0.1339) | 38,898 | 244 | 0.1885 (0.1727) | 1.002 | 0.09286 |
| 2 | cea114f47e | smallest | 1.5960 (1.5960) | 13,939 | 116 | 1.6417 (1.6331) | 0.997 | 0.01807 |
| 3 | fb0d57c8a2 | least memory | 0.8200 (0.8178) | 17,830 | 104 | 0.7589 (0.7819) | 1.007 | 0.06588 |
| 4 | df890d7385 | fastest at 32 bits | 0.1713 (0.1604) | 37,894 | 232 | 0.1678 (0.1674) | 0.968 | 0.01804 |
| 5 | c2ef9488ff | adds the most, the knee | 0.3249 (0.3125) | 20,901 | 140 | 0.3689 (0.3632) | 0.988 | 0.08981 |
| 6 | bac37f35a2 | adds the most | 0.1987 (0.1896) | 30,121 | 208 | 0.2145 (0.2009) | 0.973 | 0.02143 |
| 7 | 22420b3b61 | adds the most | 0.4098 (0.3968) | 18,928 | 120 | 0.4630 (0.4352) | 0.983 | 0.01392 |
| 8 | 9f70a06b4d | adds the most | 0.5549 (0.5361) | 16,020 | 136 | 0.5178 (0.4959) | 1.002 | 0.00629 |
| 9 | 690981ca5b | adds the most | 0.3643 (0.3590) | 23,164 | 136 | 0.3306 (0.3140) | 0.987 | 0.00557 |
| 10 | 3ee67e7d34 | adds the most | 0.1418 (0.1396) | 35,668 | 216 | 0.1976 (0.1871) | 1.008 | 0.00538 |

Against the in-run set: in now 22420b3b61, 3ee67e7d34, 690981ca5b, 9f70a06b4d, bac37f35a2, c2ef9488ff, c7c35f9c97, cea114f47e, df890d7385, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest 4df5b46d00; smallest bee0b97bb5; least memory fb0d57c8a2; fastest at 32 bits d6805a8b0a; in the set under load only 4df5b46d00, bee0b97bb5, bf25d58303, d6805a8b0a, alone only 3ee67e7d34, c7c35f9c97, cea114f47e, df890d7385.

dream (4-byte cells): 40 candidates measured; its fastest 5c1f5316db 0.217; Spearman with the laptop alone 0.924 over 40; FLAGGED, among its fastest five and not in the set: 5c1f5316db, 6064084bb3, 06b188f45b, d6b42c335a, 5050960bac.

dream (8-byte cells): 40 candidates measured; its fastest 4ef851fd8e 0.223; Spearman with the laptop alone 0.467 over 40; FLAGGED, among its fastest five and not in the set: 4ef851fd8e, 6064084bb3, 5050960bac, d6b42c335a, c13353f8cf.

rage (4-byte cells): 40 candidates measured; its fastest 690981ca5b 0.323; Spearman with the laptop alone -0.012 over 40; FLAGGED, among its fastest five and not in the set: c13353f8cf, 9a460d7122, be42bd8ea4.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 06b188f45b | 0.1898 | 0.1979 | 0.4680* | 0.2600 | x86-64 +6%, x86-32 +3%, ARMv7 +45% | ADDED |
| 2 | 6c6717b20a | 0.1935 | 0.1995 | 0.4603* | 0.2610 | x86-64 +8%, x86-32 +4%, ARMv7 +42% | ADDED |
| 3 | c13353f8cf | 0.1839 | 0.2189 | 0.4517* | 0.2629 | x86-64 +2%, x86-32 +14%, ARMv7 +40% | ADDED |
| 4 | 9a460d7122 | 0.1885 | 0.2163 | 0.4531* | 0.2643 | x86-64 +5%, x86-32 +12%, ARMv7 +40% | - |
| 5 | be42bd8ea4 | 0.1850 | 0.2187 | 0.4568* | 0.2644 | x86-64 +3%, x86-32 +14%, ARMv7 +41% | - |
| 6 | d9c6d38ce6 | 0.1826 | 0.2139 | 0.4807* | 0.2658 | x86-64 +2%, x86-32 +11%, ARMv7 +49% | - |
| 7 | 3ee67e7d34 | 0.1829 | 0.2198 | 0.4675* | 0.2658 | x86-64 +2%, x86-32 +14%, ARMv7 +45% | yes |
| 8 | 4ef851fd8e | 0.1904 | 0.1982 | 0.5079* | 0.2676 | x86-64 +6%, x86-32 +3%, ARMv7 +57% | - |
| 9 | 5050960bac | 0.1933 | 0.1946 | 0.5265* | 0.2705 | x86-64 +8%, x86-32 +1%, ARMv7 +63% | - |
| 10 | d6b42c335a | 0.1918 | 0.1925 | 0.5395* | 0.2711 | x86-64 +7%, ARMv7 +67% | ADDED |
| 11 | b0120bca4c | 0.1808 | 0.2029 | 0.5462* | 0.2716 | x86-64 +1%, x86-32 +5%, ARMv7 +69% | - |
| 12 | 8ef0975d7c | 0.1828 | 0.2042 | 0.5379* | 0.2718 | x86-64 +2%, x86-32 +6%, ARMv7 +66% | - |
| 13 | c7c35f9c97 | 0.1798 | 0.2069 | 0.5433* | 0.2723 | x86-32 +7%, ARMv7 +68% | yes |
| 14 | df890d7385 | 0.2023 | 0.1943 | 0.5396* | 0.2768 | x86-64 +13%, x86-32 +1%, ARMv7 +67% | yes |
| 15 | bac37f35a2 | 0.2273 | 0.2329 | 0.5385* | 0.3055 | x86-64 +26%, x86-32 +21%, ARMv7 +67% | yes |
| 16 | 690981ca5b | 0.4139 | 0.4483 | 0.3233 | 0.3915 | x86-64 +130%, x86-32 +133% | yes |
| 17 | c2ef9488ff | 0.3549 | 0.3917 | 0.4797 | 0.4055 | x86-64 +97%, x86-32 +103%, ARMv7 +48% | yes |
| 18 | 22420b3b61 | 0.4732 | 0.4848 | 0.3628 | 0.4366 | x86-64 +163%, x86-32 +152%, ARMv7 +12% | yes |
| 19 | 9f70a06b4d | 0.6388 | 0.6487 | 0.4919 | 0.5885 | x86-64 +255%, x86-32 +237%, ARMv7 +52% | yes |
| 20 | fb0d57c8a2 | 0.9084 | 0.8706 | 0.5134 | 0.7405 | x86-64 +405%, x86-32 +352%, ARMv7 +59% | yes |
| 21 | cea114f47e | 1.9796 | 1.9505 | 2.0055 | 1.9784 | x86-64 +1001%, x86-32 +913%, ARMv7 +520% | yes |

**The generic pick**: none within the veto - the best mean 06b188f45b named instead.
Each class's fastest: x86-64 c7c35f9c97; x86-32 d6b42c335a; ARMv7 690981ca5b.
**Added to the set across machines** (never taken out): 06b188f45b - across machines: the best mean #1; 6c6717b20a - across machines: the best mean #2; c13353f8cf - across machines: the best mean #3; d6b42c335a - across machines: the fastest at x86-32.

## The final set - 14, provisional until chain C (results/final-set-seed86.md)

The laptop's 10 - c7c35f9c97 (fastest), cea114f47e (smallest), fb0d57c8a2 (least memory), df890d7385 (fastest at 32
bits), c2ef9488ff (the knee), bac37f35a2, 22420b3b61, 9f70a06b4d, 690981ca5b (ARMv7's fastest too), 3ee67e7d34 - and the
4 added across machines: 06b188f45b, 6c6717b20a, c13353f8cf (the three best means) and d6b42c335a (x86-32's fastest).
No generic pick: no design is within 25% of every class's best - ARMv7's best is a GCC design without the JIT, 130%
behind on x86, and the JIT designs' ARMv7 builds run without it. Nothing dropped (the owner's terms, 573 and 576): chain
A's set members not in this one (2af9192e1d, bee0b97bb5, bf25d58303) and its additions not added again (4df5b46d00,
89d296ffed, 4ef851fd8e) stay candidates on the shortlist, which chain C measures again on all three machines; the set is
read from both sessions there.

## The machines' agreement (results/drafts/chainB-agreement-587.py)

The laptop's sessions hold: alone against in-run 0.950 at 64 bits, 0.897 at 32; alone against loaded 0.918, 0.845. In
the fast band - 30 of the 40 under 0.25 alone at 64 bits, all JIT designs - dream at 64 bits orders them against the
laptop (-0.263) and at 32 bits with it (0.823): chain A's finding again (585: the laptop's 64-bit fast-band order its
own). Rage against the laptop at 32 bits: -0.012 over the 40 - but 0.927 over the 10 without the JIT and -0.204 over the
30 with it, whose ARMv7 builds have the JIT off (0.452-0.580 there; the others 0.323-2.005): the x86 order says nothing
about them; against dream's 32 bits the same (0.842, -0.171). Chain A against chain B where chain A's tables keep both
readings (the set's 10; dream's from the classes' means): the laptop 1.000 and 0.988, dream 0.988 at both widths, each
design within 2.3% - over the whole speed range, no test of the fast band. The swaps against chain A's set are ties:
c7c35f9c97 0.1385 alone against 2af9192e1d's 0.1397 (0.9%; 0.1885 against 0.1811 at 32 bits); cea114f47e 1.5960
against bee0b97bb5's 1.5993 at the same 13,939 bytes. Across machines over every candidate rage measured (232; the x86
classes by the in-run speeds, no re-measure outside the 40): the best is c13353f8cf (0.2231), in the 40 and in the set;
10 within 2%, 8 of them outside the 40 - a flat top, its leader on the shortlist. Rage's fastest of all 237 is
690981ca5b (0.323), in the set.
