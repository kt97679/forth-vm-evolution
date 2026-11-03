# The final pick from chains B, C and D - the final set 21, msc kept (Iteration 598)

**Chain C** (ee7a0ee97, fury 2026-11-02 20:01-22:55, 2.9 hours): the shortlist's 40 at 10 rounds - the laptop alone and
loaded at both widths, dream at both widths, the Tegra the 8 msc designs and the 40; every line all it was given.
**Chain D** (cdb8375c4, 2026-11-03 02:14-13:55, 11.7 hours of the owner's 12): the same, repeated while another session
fit - the laptop 29 sessions (about 23 minutes each), dream 40 a width (its cap; about 7 minutes), rage 4 (9590-9614 s
each; a 5th refused by its deadline); every session complete (the 40 at four readings; dream 44, rage 52 with the
samples). next-run.sh ended it unpacked after session 29 (fixed at 597); nothing lost. No design died on any line.

Readings kept: results/chainC-seed86/ (one session, as chain B's), results/chainD-seed86/sK (lab/evolve/chain-sessions.py).

## The final set - 21 (results/final-set-chainsBCD-seed86.md; results/drafts/final-set-598.py)

The pooled pick (every session: chain D's 40, chains B and C - the laptop's 31 sessions merged) gives 15: the laptop's
10 and 5 added across machines. With chain B's 14 and chain C's own 15 - a design in any session's set kept (the
owner's terms, 576) - 21; chain D alone (its 40 sessions without B and C) adds none beyond the pooled. Chain B's 14:
11 in the pooled set, 10 in chain C's; all 14 kept. cea114f47e and bee0b97bb5 are the smallest by the same 13,939
bytes and 116 KB (1.590 against 1.594 alone - noise): each session's tie went its own way; both kept. Speeds below: the
laptop alone, every session's geometric mean.

| design | B | C | pooled | why | speed alone | 32-bit alone | bytes | memory KB |
|---|---|---|---|---|---|---|---|---|
| 4df5b46d00 |  |  | x | fastest | 0.1473 | 0.1867 | 38,386 | 232 |
| c7c35f9c97 | x | x | x | across machines: the fastest at x86-64 | 0.1476 | 0.1881 | 38,898 | 244 |
| 45efec9d25 |  | x |  | kept - chain C's set | 0.1493 | 0.1889 | 38,282 | 244 |
| c13353f8cf | x |  | x | across machines: the best mean #3 | 0.1511 | 0.2002 | 41,040 | 216 |
| be42bd8ea4 |  | x |  | kept - chain C's set | 0.1513 | 0.2007 | 41,460 | 220 |
| 3ee67e7d34 | x |  |  | kept - chain B's set | 0.1543 | 0.2029 | 35,668 | 216 |
| 06b188f45b | x | x | x | across machines: the best mean #1 | 0.1662 | 0.1811 | 38,102 | 236 |
| 6c6717b20a | x | x | x | across machines: the best mean #2 | 0.1694 | 0.1836 | 33,918 | 236 |
| d6b42c335a | x | x |  | kept - chains B and C's sets | 0.1698 | 0.1826 | 34,958 | 232 |
| 5050960bac |  | x | x | fastest at 32 bits | 0.1700 | 0.1811 | 35,350 | 228 |
| 4ef851fd8e |  |  | x | across machines: the fastest at x86-32 | 0.1706 | 0.1830 | 39,778 | 228 |
| df890d7385 | x |  |  | kept - chain B's set | 0.1758 | 0.1829 | 37,894 | 232 |
| bf25d58303 |  | x | x | adds the most | 0.1794 | 0.1903 | 31,962 | 216 |
| bac37f35a2 | x | x | x | adds the most | 0.2044 | 0.2202 | 30,121 | 208 |
| c2ef9488ff | x | x | x | adds the most | 0.3324 | 0.3767 | 20,901 | 140 |
| 690981ca5b | x | x | x | adds the most | 0.3669 | 0.3371 | 23,164 | 136 |
| 22420b3b61 | x | x | x | adds the most | 0.4115 | 0.4617 | 18,928 | 120 |
| 9f70a06b4d | x | x | x | adds the most | 0.5572 | 0.5306 | 16,020 | 136 |
| fb0d57c8a2 | x | x | x | least memory | 0.8244 | 0.7667 | 17,830 | 104 |
| cea114f47e | x |  | x | smallest | 1.5900 | 1.6372 | 13,939 | 116 |
| bee0b97bb5 |  | x |  | kept - chain C's set | 1.5937 | 1.6310 | 13,939 | 116 |

**No generic pick** within the 25% veto, as in chain B: the best mean 06b188f45b, 42% behind ARMv7's best there
(690981ca5b, a design without the JIT, 124% behind on x86-64). Each class's fastest: x86-64 c7c35f9c97, x86-32
4ef851fd8e, ARMv7 690981ca5b.

## The sessions' agreement (results/drafts/chainCD-agreement-598.py) - Spearman on the 40

| line | B against C | D: sessions | D: median pairwise (range) | D against B | D against C | D's fastest (sessions it leads) | median CV a design |
|---|---|---|---|---|---|---|---|
| dream.lan-prebuilt64 | 0.943 | 40 | 0.977 (0.933-0.995) | 0.970 | 0.981 | 4ef851fd8e (22 of 40) | 0.50% |
| dream.lan-prebuilt32 | 0.978 | 40 | 0.990 (0.966-0.999) | 0.971 | 0.993 | 4ef851fd8e (31 of 40) | 0.41% |
| rage.lan-prebuiltarm | 0.954 | 4 | 0.962 (0.947-0.974) | 0.959 | 0.987 | 690981ca5b (4 of 4) | 0.49% |
| the laptop alone, 64 bits | 0.943 | 29 | 0.957 (0.887-0.990) | 0.953 | 0.953 | 4df5b46d00 (10 of 29) | 2.08% |
| the laptop alone, 32 bits | 0.897 | 29 | 0.900 (0.751-0.974) | 0.880 | 0.897 | 06b188f45b (8 of 29) | 2.22% |

Within a night the sessions agree better than chain B's against chain C's on every line; the laptop is the noisy one (a
design's spread over its sessions about 2.1% against dream's and rage's 0.5%), and its 64-bit order against dream's
stays low (0.44-0.50 by session) - the fast end a band across machines, as at 582. Rage's order against the laptop's is
near 0 (the JIT designs measured JIT-off there).

## msc - kept (retire-plan-583.md's rule; lab/evolve/chain-sessions.py)

Each of the Tegra's 4 pairs' msc=0 design slower than its msc=1 one, the geometric mean of chain C's session and chain
D's 4: 6d321be1cc / 9920e9af07 0.3937 / 0.4640 (+17.9%), 01efebca24 / 97a4e37ab4 0.3949 / 0.4677 (+18.4%), c67e6b5336 /
8bddf3a5e4 0.4025 / 0.4742 (+17.8%), 629b7e96ec / 75acca89a6 0.4415 / 0.5192 (+17.6%) - chain C alone 16.4-19.2%,
chain D alone 17.6-18.2%. So msc earns its place on ARMv7 and stays a gene; its queued patch is deleted (the 8 before
it unchanged). The pairs are 20-35% behind ARMv7's fastest (690981ca5b, msc=0): whether msc helps the designs ARMv7
ranks first was not measured. The 8 records: results/msc-pairs-seed86.md.

## The pooled pick - final-pick.py's output

    python3 lab/evolve/chain-sessions.py /tmp/UNPACKED-D results/chainD-seed86 results/shortlist-seed86.md   # prints:
    python3 lab/evolve/final-pick.py results/shortlist-seed86.md results/chainD-seed86/s1/loadtest.md \
        results/chainD-seed86/s1/*.out.json --also-session results/chainD-seed86/s2 ... s40 \
        --also-session results/chainB-seed86 --also-session results/chainC-seed86

# The final set, re-measured - 40 candidates, 40 re-measured at both widths (final-pick.py; GOALS.md step 3, the owner's decisions of Iteration 573)

Two or more sessions (Iteration 588): results/chainD-seed86/s1 and s2-s40, results/chainB-seed86, results/chainC-seed86 - the laptop's re-measures each the geometric mean of the sessions that have it (31); each host's lines its mean in step 5.

Chosen from the laptop's re-measures alone (loadtest.py --ids, idle), re-measured against re-measured: the four extremes, then by hypervolume to 10. Size and memory exact.

| # | design | why | speed alone (in-run) | binary + image | memory KB | 32-bit alone (in-run) | under load / alone | adds |
|---|---|---|---|---|---|---|---|---|
| 1 | 4df5b46d00 | fastest | 0.1473 (0.1345) | 38,386 | 232 | 0.1867 (0.1739) | 0.932 | 0.10788 |
| 2 | cea114f47e | smallest | 1.5900 (1.5960) | 13,939 | 116 | 1.6372 (1.6331) | 1.007 | 0.01750 |
| 3 | fb0d57c8a2 | least memory | 0.8244 (0.8178) | 17,830 | 104 | 0.7667 (0.7819) | 1.002 | 0.06203 |
| 4 | 5050960bac | fastest at 32 bits | 0.1700 (0.1550) | 35,350 | 228 | 0.1811 (0.1670) | 0.940 | 0.01488 |
| 5 | c2ef9488ff | adds the most, the knee | 0.3324 (0.3125) | 20,901 | 140 | 0.3767 (0.3632) | 0.973 | 0.08210 |
| 6 | bac37f35a2 | adds the most | 0.2044 (0.1896) | 30,121 | 208 | 0.2202 (0.2009) | 0.951 | 0.01624 |
| 7 | 22420b3b61 | adds the most | 0.4115 (0.3968) | 18,928 | 120 | 0.4617 (0.4352) | 0.984 | 0.01405 |
| 8 | 9f70a06b4d | adds the most | 0.5572 (0.5361) | 16,020 | 136 | 0.5306 (0.4959) | 0.993 | 0.00616 |
| 9 | 690981ca5b | adds the most | 0.3669 (0.3590) | 23,164 | 136 | 0.3371 (0.3140) | 0.980 | 0.00556 |
| 10 | bf25d58303 | adds the most | 0.1794 (0.1662) | 31,962 | 216 | 0.1903 (0.1723) | 0.948 | 0.00299 |

Against the in-run set: in now 22420b3b61, 4df5b46d00, 5050960bac, 690981ca5b, 9f70a06b4d, bac37f35a2, bf25d58303, c2ef9488ff, cea114f47e, fb0d57c8a2; out now none - both kept as candidates.
Under load: the extremes fastest c7c35f9c97; smallest bee0b97bb5; least memory fb0d57c8a2; fastest at 32 bits 06b188f45b; in the set under load only 06b188f45b, bee0b97bb5, c7c35f9c97, alone only 4df5b46d00, 5050960bac, cea114f47e.

Step 4, each host line by session (90 lines, folded here; the command above prints them):

| line | sessions | Spearman with the laptop alone (range) | its fastest, by sessions |
|---|---|---|---|
| dream, 4-byte cells | 42 | 0.900-0.931 | 4ef851fd8e 32, d6b42c335a 8, 5c1f5316db 2 |
| dream, 8-byte cells | 42 | 0.441-0.501 | 4ef851fd8e 24, 6064084bb3 8, 5050960bac 7, d6b42c335a 2, 06b188f45b 1 |
| rage, 4-byte cells | 6 | 0.047-0.102 | 690981ca5b 6 |

## Across machines (GOALS.md, Iteration 377; the owner's terms at 576)

Each class once - x86-64 (the laptop, dream), x86-32 (the laptop, dream), ARMv7 (rage); the mean their geometric mean (lower is faster). A JIT design's ARMv7 reading is its JIT-off build (*). The veto (25%) removes nothing: it names the generic pick only.

| # | design | x86-64 | x86-32 | ARMv7 | mean | behind its class's best | in the set |
|---|---|---|---|---|---|---|---|
| 1 | 06b188f45b | 0.1935 | 0.2013 | 0.4636* | 0.2623 | x86-64 +5%, x86-32 +1%, ARMv7 +42% | ADDED |
| 2 | 6c6717b20a | 0.1965 | 0.2021 | 0.4560* | 0.2626 | x86-64 +6%, x86-32 +2%, ARMv7 +39% | ADDED |
| 3 | c13353f8cf | 0.1864 | 0.2206 | 0.4567* | 0.2658 | x86-64 +1%, x86-32 +11%, ARMv7 +40% | ADDED |
| 4 | be42bd8ea4 | 0.1870 | 0.2213 | 0.4570* | 0.2664 | x86-64 +1%, x86-32 +11%, ARMv7 +40% | - |
| 5 | 3ee67e7d34 | 0.1912 | 0.2231 | 0.4588* | 0.2695 | x86-64 +3%, x86-32 +12%, ARMv7 +40% | - |
| 6 | 9a460d7122 | 0.1913 | 0.2241 | 0.4572* | 0.2696 | x86-64 +4%, x86-32 +13%, ARMv7 +40% | - |
| 7 | 4ef851fd8e | 0.1953 | 0.1989 | 0.5095* | 0.2705 | x86-64 +6%, ARMv7 +56% | ADDED |
| 8 | d9c6d38ce6 | 0.1875 | 0.2209 | 0.4837* | 0.2716 | x86-64 +1%, x86-32 +11%, ARMv7 +48% | - |
| 9 | 4df5b46d00 | 0.1870 | 0.2076 | 0.5208* | 0.2725 | x86-64 +1%, x86-32 +4%, ARMv7 +59% | yes |
| 10 | 5050960bac | 0.1953 | 0.1989 | 0.5290* | 0.2739 | x86-64 +6%, ARMv7 +62% | yes |
| 11 | c7c35f9c97 | 0.1848 | 0.2071 | 0.5400* | 0.2744 | x86-32 +4%, ARMv7 +65% | ADDED |
| 12 | d6b42c335a | 0.1959 | 0.1990 | 0.5383* | 0.2759 | x86-64 +6%, ARMv7 +65% | - |
| 13 | bf25d58303 | 0.2039 | 0.2087 | 0.5523* | 0.2864 | x86-64 +10%, x86-32 +5%, ARMv7 +69% | yes |
| 14 | bac37f35a2 | 0.2303 | 0.2383 | 0.5433* | 0.3101 | x86-64 +25%, x86-32 +20%, ARMv7 +66% | yes |
| 15 | 690981ca5b | 0.4143 | 0.4546 | 0.3270 | 0.3949 | x86-64 +124%, x86-32 +129% | yes |
| 16 | c2ef9488ff | 0.3588 | 0.3943 | 0.4759 | 0.4068 | x86-64 +94%, x86-32 +98%, ARMv7 +46% | yes |
| 17 | 22420b3b61 | 0.4693 | 0.4837 | 0.3637 | 0.4354 | x86-64 +154%, x86-32 +143%, ARMv7 +11% | yes |
| 18 | 9f70a06b4d | 0.6430 | 0.6523 | 0.4937 | 0.5917 | x86-64 +248%, x86-32 +228%, ARMv7 +51% | yes |
| 19 | fb0d57c8a2 | 0.9160 | 0.8813 | 0.5203 | 0.7489 | x86-64 +396%, x86-32 +343%, ARMv7 +59% | yes |
| 20 | cea114f47e | 1.9940 | 1.9341 | 1.9823 | 1.9699 | x86-64 +979%, x86-32 +872%, ARMv7 +506% | yes |

**The generic pick**: none within the veto - the best mean 06b188f45b named instead.
Each class's fastest: x86-64 c7c35f9c97; x86-32 4ef851fd8e; ARMv7 690981ca5b.
**Added to the set across machines** (never taken out): 06b188f45b - across machines: the best mean #1; 6c6717b20a - across machines: the best mean #2; c13353f8cf - across machines: the best mean #3; c7c35f9c97 - across machines: the fastest at x86-64; 4ef851fd8e - across machines: the fastest at x86-32.
