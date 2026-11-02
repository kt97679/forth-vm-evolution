# The final pick's chain A - the 232 candidates re-measured (Iteration 585)

Chain d804d66d9 on fury, 2026-11-02 05:36-06:43: tests PASS, the stages 7 of 7 IDENTICAL, the jail PASS; loadtest.py --ids
results/candidates-final-seed86.md - 232 of 232 re-measured at both widths, alone and under load, in 50 minutes. Dream
measured all 232 at both widths beside its 24-design sample line. Rage's line (queued, 120 minutes) was still starting -
its stages being built there - when the chain packed, and remote-checks.sh's gather skipped it without a word (it gathers
only lines that wrote `until`; fixed at 585). Below, final-pick.py as 585 corrected it: each host against the laptop at its
own width (the 64-bit before: dream-32 read -0.183), the sample line with no candidate left out. The set and the shortlist
are the same either way.

# The final set, re-measured - 232 candidates, 232 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 2af9192e1d | fastest | 0.1376 (0.1365) | 38,050 | 240 | 0.1957 (0.1738) | 1.007 | 0.09989 |
| 2 | bee0b97bb5 | smallest | 1.5933 (1.6295) | 13,939 | 116 | 1.6288 (1.6767) | 1.009 | 0.01798 |
| 3 | fb0d57c8a2 | least memory | 0.8268 (0.8178) | 17,830 | 104 | 0.7550 (0.7819) | 0.992 | 0.06407 |
| 4 | df890d7385 | fastest at 32 bits | 0.1752 (0.1604) | 37,894 | 232 | 0.1734 (0.1674) | 0.923 | 0.01209 |
| 5 | c2ef9488ff | adds the most, the knee | 0.3368 (0.3125) | 20,901 | 140 | 0.3654 (0.3632) | 0.958 | 0.08824 |
| 6 | bac37f35a2 | adds the most | 0.1980 (0.1896) | 30,121 | 208 | 0.2051 (0.2009) | 0.952 | 0.02302 |
| 7 | 22420b3b61 | adds the most | 0.4030 (0.3968) | 18,928 | 120 | 0.4558 (0.4352) | 0.987 | 0.01441 |
| 8 | 9f70a06b4d | adds the most | 0.5591 (0.5361) | 16,020 | 136 | 0.5350 (0.4959) | 0.993 | 0.00607 |
| 9 | bf25d58303 | adds the most | 0.1714 (0.1662) | 31,962 | 216 | 0.1840 (0.1723) | 0.987 | 0.00422 |
| 10 | 690981ca5b | adds the most | 0.3623 (0.3590) | 23,164 | 136 | 0.3489 (0.3140) | 0.983 | 0.00270 |

Against the in-run set: in now 2af9192e1d, bee0b97bb5, df890d7385; out now 15ecc6a232, 9e22f1625c, cea114f47e - both kept as candidates.
Under load: the extremes fastest 8ef0975d7c; smallest cea114f47e; least memory fb0d57c8a2; fastest at 32 bits 5050960bac; in the set under load only 5050960bac, 8ef0975d7c, cea114f47e, alone only 2af9192e1d, bee0b97bb5, df890d7385.

dream (4-byte cells): 232 candidates measured; its fastest 287cb20138 0.215; Spearman with the laptop alone 0.585 over 232; FLAGGED, among its fastest five and not in the set: 287cb20138, 4ef851fd8e, 65bdd99f9e, 5c1f5316db, 874c21f3a3.

dream (8-byte cells): 232 candidates measured; its fastest 373f401344 0.220; Spearman with the laptop alone -0.124 over 232; FLAGGED, among its fastest five and not in the set: 373f401344, a11cfaee62, 1e8ca13412, 2f446215b3, 490a87d0e6.

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream); the mean their geometric mean (lower is faster). No ARMv7 reading - two classes. The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|
| 1 | 4df5b46d00 | 0.1811 | 0.2029 | 0.1917 | x86-64 +1%, x86-32 +3% | ADDED |
| 2 | c7c35f9c97 | 0.1813 | 0.2047 | 0.1926 | x86-64 +1%, x86-32 +4% | ADDED |
| 3 | 89d296ffed | 0.1809 | 0.2062 | 0.1931 | x86-64 +1%, x86-32 +5% | ADDED |
| 4 | 15ecc6a232 | 0.1855 | 0.2016 | 0.1934 | x86-64 +4%, x86-32 +3% | - |
| 5 | f7a6d16a66 | 0.1850 | 0.2027 | 0.1936 | x86-64 +3%, x86-32 +3% | - |
| 6 | b0120bca4c | 0.1842 | 0.2036 | 0.1936 | x86-64 +3%, x86-32 +4% | - |
| 7 | 2af9192e1d | 0.1792 | 0.2097 | 0.1939 | x86-32 +7% | yes |
| 8 | 8ef0975d7c | 0.1835 | 0.2050 | 0.1940 | x86-64 +2%, x86-32 +5% | - |
| 9 | 9880e6f1ee | 0.1821 | 0.2068 | 0.1941 | x86-64 +2%, x86-32 +5% | - |
| 10 | d701cad70b | 0.1857 | 0.2036 | 0.1945 | x86-64 +4%, x86-32 +4% | - |
| 11 | 4ef851fd8e | 0.1944 | 0.1961 | 0.1952 | x86-64 +8% | ADDED |
| 12 | 23b6a752aa | 0.1826 | 0.2090 | 0.1954 | x86-64 +2%, x86-32 +7% | - |
| 13 | df890d7385 | 0.2048 | 0.1985 | 0.2016 | x86-64 +14%, x86-32 +1% | yes |
| 14 | bf25d58303 | 0.2003 | 0.2045 | 0.2024 | x86-64 +12%, x86-32 +4% | yes |
| 15 | bac37f35a2 | 0.2279 | 0.2303 | 0.2291 | x86-64 +27%, x86-32 +17% | yes |
| 16 | c2ef9488ff | 0.3648 | 0.3873 | 0.3759 | x86-64 +104%, x86-32 +98% | yes |
| 17 | 690981ca5b | 0.4128 | 0.4604 | 0.4359 | x86-64 +130%, x86-32 +135% | yes |
| 18 | 22420b3b61 | 0.4639 | 0.4804 | 0.4721 | x86-64 +159%, x86-32 +145% | yes |
| 19 | 9f70a06b4d | 0.6431 | 0.6534 | 0.6482 | x86-64 +259%, x86-32 +233% | yes |
| 20 | fb0d57c8a2 | 0.9143 | 0.8717 | 0.8928 | x86-64 +410%, x86-32 +345% | yes |
| 21 | bee0b97bb5 | 1.9985 | 1.9333 | 1.9656 | x86-64 +1015%, x86-32 +886% | yes |

**The generic pick**: 4df5b46d00, the mean 0.1917, within 25% of every class's best.
Each class's fastest: x86-64 2af9192e1d; x86-32 4ef851fd8e.
**Added to the set across machines** (never taken out): 4df5b46d00 - across machines: the best mean #1; c7c35f9c97 - across machines: the best mean #2; 89d296ffed - across machines: the best mean #3; 4ef851fd8e - across machines: the fastest at x86-32.

**The shortlist for chain B**: 40 designs in results/shortlist-seed86.md.

## The machines' agreement (results/drafts/chainA-agreement-585.py)

Over all 232: dream against the laptop alone -0.125 at 64 bits, +0.588 at 32; the 14 slower candidates 0.978 and 0.956.
Within the fast band - the 218 under 0.25 on the laptop at 64 bits, every one a JIT design - the laptop's 64-bit order is
reproducible there (in-run against re-measure 0.889, alone against loaded 0.844) and opposed to the three other readings:
its own 32-bit -0.270, dream 64 -0.357, dream 32 -0.430; those three agree with one another (0.430-0.536; the laptop's
32-bit against itself 0.640). Not the JIT - all 218 have it. Part is the selection: the candidates are each width's
fastest on the laptop together, so within them a design weak at one width was taken for the other (Berkson). Seed 84's
bred lead, the laptop's and not the designs' (582), is the same finding at the fast end. Across machines the classes'
geometric mean (the owner's terms, 576) weighs it: the fast end is a band, its fastest named per machine.
