# The article's figures after seed 87, recomputed (Iteration 658; results/drafts/article-figures-658.py)

Section 17 of article/article-en-draft.md and article/article-ru-draft.md quotes these. Each line is a tool's output
on a chain's readings in results/, unless marked (record): read from the chain's document.

## Seed 88 - the second portable run

- in the run, the fastest at 32 bits: c7814def6d 0.2803 against 0.2888, -2.9% (record)
- the chain: 46 designs side by side, 8.9 hours (record)
- the laptop alone, 4-byte cells: the run's c7814def6d 0.3205, found before 9f8811f7f4 0.3141: +2.06% +/- 0.76% - no
- verdict: no extreme gained; role candidates above - another portable run, seed 89, if a role goes to one of them (the processing decides), else the portable search stops

## Seed 89 - a JIT run: its follow-up, and the quick pass over seed 88's rest

- the chain: 52 designs side by side, 9.1 hours (record)
- 3eb59b271d against 690981ca5b: -2.84% +/- 0.62%
- ee34931cd7 against 4ef851fd8e: -3.15% +/- 0.42%
- c6f1c1331b 29,306 B (-2.71%): x86-64 -2.30% +/- 0.28%, x86-32 -1.53% +/- 0.31%, ARMv7 +5.71% +/- 0.26%, memory +0 KB
- ae99617f06 against a627b954c6, 6 sessions: -1.50% -2.25% -3.48% -2.32% -0.90% -3.35%; pooled -2.30% +/- 0.42% - past 2% at 2 SE
- 8164d3858f against a627b954c6, 6 sessions: -1.18% -2.70% -3.45% -0.77% -0.86% -2.45%; pooled -1.91% +/- 0.46% - not by the rule

## Seed 90 - the other JIT run: the quick pass over seed 89's rest

- the chain: 7 designs side by side, 1.9 hours (record)
- 11a56ff9e4: x86-64 +1.54%, x86-32 -3.59%, bytes -5.45%, memory +0 KB

## Seed 91 - the third portable run

- the chain: 38 designs side by side, 14.3 hours (record)
- the laptop alone, 4-byte cells: the run's 3060f04651 0.3086, found before 782f3ad7ff 0.3262: -5.38% +/- 0.31% - GAIN
- binary + image: the run's 01712a2639 13,691 B, found before 64a7345393 13,891 B: -1.44% - GAIN
- bridged from chain-followup89: e523a45566 0.3107 (6 bridges, 0.3099-0.3119) -> -0.68% (-1.05% to -0.42%)
- binary + image (exact): the run's 01712a2639 13,691 B, the pool's smallest 4dd4e3e7e2 13,709 B: -0.13% (the rule: 1%)

## The final check

- the chain: 435 designs side by side, 25.9 hours (record)
- the laptop alone, 8-byte cells: the run's 38100f0280 0.2933, found before 7fb40ff7ba 0.2856: +2.69% +/- 0.56% - no
- the laptop alone, 4-byte cells: the run's 95077030b0 0.3078, found before e523a45566 0.3022: +1.84% +/- 0.93% - no
- x86-64: the run's 38100f0280 0.3314, found before 7fb40ff7ba 0.3273: +1.26% +/- 0.34% - no
- x86-32: the run's d710e403b0 0.3387, found before 782f3ad7ff 0.3365: +0.66% +/- 0.33% - no
- ARMv7: the run's 6f6cbe3f71 0.3177, found before 7fb40ff7ba 0.3099: +2.52% +/- 3.73% - no
- the mean of the three: the run's 208bd2d2ff 0.3540, found before 782f3ad7ff 0.3442: +2.83% +/- 0.72% - no
- so the run's fastest behind the best found before by 0.66% to 2.83%
- binary + image: the run's f75a82e4ee 13,691 B, found before 01712a2639 13,691 B: +0.00% - no
- memory: the run's e1f809095d 112 KB, found before fb0d57c8a2 104 KB: +8 KB - no
- smaller than the smallest holder (64a7345393, 13,891 B): 34 designs, 33 with a trade (slower on a class by 2 SE, or more memory); without one: d180351903
- the document: 34 smaller, 33 with a trade (record)
- the 13,691 B designs (5): x86-32 +18.23% to +18.71%
- d180351903 13,883 B (-0.06%): x86-64 -0.59% +/- 0.29%, x86-32 -3.85% +/- 0.25%, ARMv7 -3.30% +/- 0.68%, memory +0 KB

## The ten roles (results/handoff-relf-657.md, as relf takes them)

| role | design | x86-64 | x86-32 | ARMv7 | bytes, 8-byte cells | memory KB | JIT | measured |
|---|---|---|---|---|---|---|---|---|
| fastest on x86-64 (`fastest-x86-64`) | c7c35f9c97 | 0.185 | 0.207 | 0.540* | 38,898 | 244 | x86-64 and x86-32 | seed 86's chains B-D |
| fastest on x86-32 (`fastest-x86-32`) | ee34931cd7 | 0.189 | 0.193 | 0.476* | 41,990 | 224 | x86-64 and x86-32 | seed 89's follow-up |
| best all-round (the best mean of the three classes) (`best-all-round`) | 06b188f45b | 0.193 | 0.201 | 0.464* | 38,102 | 236 | x86-64 and x86-32 | seed 86's chains B-D |
| smallest of the JIT designs (`small-jit`) | c6f1c1331b | 0.225 | 0.235 | 0.577* | 29,306 | 208 | x86-64 and x86-32 | seed 89's follow-up |
| fastest portable; fastest portable on x86 (`portable-fastest`) | 782f3ad7ff | 0.343 | 0.339 | 0.372 | 26,242 | 148 | no - portable | seed 87's follow-up |
| fastest on ARMv7 (`portable-arm`) | 3eb59b271d | 0.378 | 0.443 | 0.320 | 22,522 | 132 | no - portable | seed 89's follow-up |
| the knee: fast portable on x86, small (`portable-knee`) | 11a56ff9e4 | 0.363 | 0.377 | 0.477 | 19,761 | 140 | no - portable | seed 90's follow-up |
| small, fast on ARMv7 (`portable-small`) | ae99617f06 | 0.450 | 0.444 | 0.351 | 18,599 | 124 | no - portable | seed 89's follow-up |
| least memory (`least-memory`) | fb0d57c8a2 | 0.916 | 0.884 | 0.521 | 17,830 | 104 | no - portable | seed 87's follow-up |
| smallest (`smallest`) | d180351903 | 1.926 | 1.784 | 1.717 | 13,883 | 116 | no - portable | the final check |

(*) on ARMv7 a JIT design runs without its JIT (the handoff's note).

## The check

22 figures the article quotes, recomputed; 22 of them as written in their chain's document.
