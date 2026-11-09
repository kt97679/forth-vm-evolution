# Seed 89's follow-up chain: the roles re-measured, and the last JIT run's gain confirmed (Iteration 627)

The chain at 6e28635dc0 (fury, 2026-11-08 03:42 - 12:48, 9.1 hours of the 10): the 52 of results/followup-seed89.md -
seed 89's 30 by select() and the seven it bred past the 32-bit bar, the relf handoff's ten holders, the screen's five -
re-measured side by side. The laptop 18 sessions (10 rounds, alone and loaded, both widths), dream 20 a width, the Tegra
3; every session measured all 52 on every line, no design died. Pooled: results/followup-pick-seed89.md (its set as JSON,
results/followup-pick-seed89.json); the readings: results/chain-followup89/; the figures from one command, `PRED=624 sh
lab/evolve/process-followup.sh 89 627 fastest=782f3ad7ff,arm=690981ca5b,knee=c2ef9488ff,smallarm=a627b954c6,
memory=fb0d57c8a2,smallest=64a7345393,fast64=c7c35f9c97,fast32=4ef851fd8e,allround=06b188f45b,smalljit=bac37f35a2`, the
session-by-session checks from results/drafts/followup-check-627.py. The incumbents agree with 621's: 782f3ad7ff 0.3429 /
0.3384 / 0.3694, the mean 0.3500 (621: 0.3429 / 0.3384 / 0.3719, 0.3507). Noise: a paired difference's SE 0.31-0.38% on
the laptop, 0.21-0.24% on dream, 0.34% on the Tegra (the median over the 52).

## The roles - the rule fixed before seed 87: speed 2% (the paired difference 2 SE or more), bytes 1%, memory 4 KB

Speeds are the classes of final-pick.py step 5 (lower is faster); errors paired by session. "By the rule" is the rule's
outcome; the owner decides each change (611's way).

| role | holder | by the rule | the evidence |
|---|---|---|---|
| fastest portable | 782f3ad7ff | 782f3ad7ff | still the best mean of the JIT-free designs |
| fastest on ARMv7 | 690981ca5b | **3eb59b271d** (seed 89 bred, gen 27, JIT-free) | -2.84% +/- 0.62%: every session faster (-2.71, -3.92, -1.86%), the holder flat; and 2.77% smaller (22,522 B against 23,164), 4 KB less memory - it dominates |
| the knee | c2ef9488ff | c2ef9488ff | none beats it by the rule (the screen's ee7258275b included) |
| small, fast on ARMv7 | a627b954c6 | **8164d3858f** (seed 88, screened) - thin | ARMv7 -2.45% +/- 0.68%, 8 B smaller, memory the same; ae99617f06 (it with varslot=1) -2.41% +/- 0.59% |
| least memory | fb0d57c8a2 | fb0d57c8a2 | 104 KB; the next 7a7edb5b0e 108 KB |
| smallest | 64a7345393 | 64a7345393 | efb0fece07 13,709 B (1.31% smaller) for x86-64 +4.6%, x86-32 +28.3%, ARMv7 +7.7% - 4dd4e3e7e2's trade again, turned down by the owner's standing decision (621) |
| fastest x86-64 | c7c35f9c97 | c7c35f9c97 | the run's best, d8471f1b16, +2.81% +/- 0.37% |
| fastest x86-32 | 4ef851fd8e | **ee34931cd7** (seed 89 bred, gen 147) | -3.15% +/- 0.42%: the laptop -4.23% +/- 0.82%, dream -2.05% +/- 0.17% (all 20 sessions faster); 5.6% larger (41,990 B against 39,778), 4 KB less memory; b969aa7bd8 -3.02%, 68f5ce466c -2.85%, d8471f1b16 -2.85% past too |
| best all-round | 06b188f45b | 06b188f45b | ee34931cd7 -1.22% +/- 0.25% (under 2%) |
| smallest JIT design | bac37f35a2 | **c6f1c1331b** (seed 89 bred, gen 93) - the pick among 8 | 2.71% smaller (29,306 B against 30,121), memory the same, no speed lost: the laptop x86-64 -5.1%, x86-32 -3.1%, dream +0.5%, +0.0% (classes -2.30% +/- 0.28%, -1.53% +/- 0.31%) |

**The smallest JIT design - the choice among the eight smaller.** The rule lists every smaller JIT design; the trade is
the owner's (611, 621: no small gain in one criterion for a large loss in the others). 93364d4fc2 is 0.53% smaller than
c6f1c1331b (under the 1% bar) and 3.4% slower at x86-64 (+1.01% and -0.51% against the holder); b9ae4e3f98 3.49% smaller
for +4.5% and +2.3%; the other five 3.6-12.2% smaller for 9-77% at one width or both. c6f1c1331b is the one that costs
nothing; its ARMv7 reading (+5.7%, the JIT-off build) is outside a role that is x86 only.

**Small and fast on ARMv7 - thin.** Three Tegra sessions: 8164d3858f -1.18%, -2.70%, -3.45%. Over each session's median
the holder read 0.741, 0.744, 0.758 - its third session its slowest, 2.3% over its first - while 8164d3858f (0.732,
0.724, 0.732) and ae99617f06 (0.730, 0.727, 0.732) stayed flat: the gain grows with the holder's drift. By the rule 3.6 SE
and 0.45% past the bar; on two degrees of freedom the 95% interval is -5.3% .. +0.5%. The screen's two sessions (seed 89's
lines, 3 rounds) had it -2.90%. Against a627b954c6 four genes: folds (XOR for R@), gotodup 1 (2), rtfuse 1 (0), t2hot 3 (0).
3eb59b271d's case is the opposite: its holder flat (0.685 in each session), every session past 1.8%, and smaller besides.

## The rule after the follow-up (618/620; results/drafts/jit-run-plan-620.md)

- **The JIT: progress confirmed** - what seed 89 bred: ee34931cd7 the fastest on x86-32 (above), and the laptop's 32-bit
  extreme, 68f5ce466c 0.1765 against 06b188f45b's 0.1819 (-3.01% +/- 0.47%). By 618/620 another JIT run follows: seed 90,
  its hours the owner's.
- **The portable roles**: 3eb59b271d, bred by the JIT run - neither a portable run's nor screened - takes the fastest on
  ARMv7: the carryall run's breeding reaches the portable roles too. 8164d3858f, screened, takes small and fast on ARMv7 by
  the rule, which by 620 reopens the portable search - on the thinnest evidence of the four changes.
- **Not a gain**: --gain's "binary + image" - efb0fece07's 13,709 B is seed 88's size (4dd4e3e7e2, not in this list: the
  tool compares with the list's designs), the pool's smallest 13,572 B (622's bar); the role turned down besides.

## Waiting on the owner

1. The changes: the fastest on x86-32 ee34931cd7, the fastest on ARMv7 3eb59b271d, the smallest JIT design c6f1c1331b,
   small and fast on ARMv7 8164d3858f. When taken: results/handoff-relf-611.md's successor, the package (pack-designs.py)
   and designs/ (export-designs.py) made again.
2. The next run: seed 90, a JIT run again (620's form, `seed 90 21h widths carryall`; its remote lines could screen seed
   89's rest - the 324 of its union front this follow-up did not re-measure - and give the Tegra more sessions of
   8164d3858f against a627b954c6); and whether 8164d3858f's thin gain opens a portable (nojit) run of its own.

## The re-measure's rule, fixed before seed 90's data (Iteration 629)

Small and fast on ARMv7 is decided on every Tegra session of the three designs: this follow-up's three (10 rounds) and
seed 90's screen's (3 rounds, up to four), each session one paired log-difference against a627b954c6, equal weights, the
SE from their spread (results/drafts/smallarm-pool-629.py; on this follow-up alone it gives the figures above).
8164d3858f or ae99617f06 - the faster, if both - takes the role at 2% faster and 2 SE, the role rule fixed before seed 87,
and by 620 the portable search reopens; otherwise a627b954c6 keeps it and the question is closed.


## The re-measure's verdict (Iteration 630)

Seed 90's Tegra line measured three sessions at 3 rounds (four planned; the fourth past the deadline), the Tegra at its
usual load (1.4). Pooled with the follow-up's three by the rule above:

```
the Tegra: 6 sessions in results/chain-followup89, results/chain-screen89
  8164d3858f against a627b954c6, 6 sessions: -1.18% -2.70% -3.45% -0.77% -0.86% -2.45%; pooled -1.91% +/- 0.46% - not by the rule
  ae99617f06 against a627b954c6, 6 sessions: -1.50% -2.25% -3.48% -2.32% -0.90% -3.35%; pooled -2.30% +/- 0.42% - past 2% at 2 SE
verdict: ae99617f06 takes small and fast on ARMv7 - by 620 the portable search reopens
```

By the rule ae99617f06 takes small and fast on ARMv7 - faster in all six sessions, 8 bytes smaller (18,599 B), memory
the same - and by 620 the portable search reopens; 8164d3858f, the challenger the card named, stops at -1.91%. Thin:
0.30% past the bar, under one SE. The owner's decision, as 628's three (results/xcheck-seed90.md).
