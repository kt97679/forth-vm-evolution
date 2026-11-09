# Seed 90's follow-up chain: 11a56ff9e4 against the knee, beside the six portable holders (Iteration 634)

The chain at 886be9a9e8 (fury, 2026-11-09 21:06 - 23:01 UTC, 1.9 hours; 13:06 - 15:01 Pacific): the 7 of
results/followup-seed90.md - 11a56ff9e4, flagged against the knee by the screen of seed 89's rest (results/xcheck-seed90.md),
and the relf handoff's six portable holders (results/relf-designs-631.md) - re-measured side by side. The laptop 20
sessions (10 rounds, alone and loaded, both widths), dream 10 a width, the Tegra 2; every session measured all 7 on every
line, no design died; the laptop's own checks PASS (run-tests, validate 7 of 7 IDENTICAL, the jail). Pooled:
results/followup-pick-seed90.md (its set as JSON, results/followup-pick-seed90.json); the readings:
results/chain-followup90/; the figures from one command, `HANDOFF=results/handoff-relf-631.md PRED=631 sh
lab/evolve/process-followup.sh 90 634 fastest=782f3ad7ff,arm=3eb59b271d,knee=c2ef9488ff,smallarm=ae99617f06,
memory=fb0d57c8a2,smallest=64a7345393`, the line-by-line check and the predictions from
results/drafts/followup-check-634.py. 782f3ad7ff 0.3383 / 0.3328 / 0.3709, the mean 0.3469 (627: 0.3429 / 0.3384 /
0.3694, 0.3500) - this chain's common shift, cancelled by pairing. Noise: a paired difference's SE 0.21-0.37% on the
laptop, 0.44-0.47% on dream (10 sessions, loaded), 0.33% on the Tegra (2).

## The roles - the rule fixed before seed 87: speed 2% (a gain at 2 SE), bytes 1%, memory 4 KB

| role | holder | by the rule | the evidence |
|---|---|---|---|
| fastest portable | 782f3ad7ff | 782f3ad7ff | the best mean of the 7 |
| fastest on ARMv7 | 3eb59b271d | 3eb59b271d | ae99617f06 +9.95% +/- 0.45%, 782f3ad7ff +15.84% |
| the knee | c2ef9488ff | **11a56ff9e4** | 5.45% smaller (19,761 B against 20,901), x86-32 -3.59% +/- 0.43%, x86-64 +1.54% +/- 0.25% (under 2%), memory the same |
| small, fast on ARMv7 | ae99617f06 | ae99617f06 | no challenger in the list |
| least memory | fb0d57c8a2 | fb0d57c8a2 | 104 KB; the next 116 KB |
| smallest | 64a7345393 | 64a7345393 | none smaller |

**The knee - the owner's decision.** 11a56ff9e4 is JIT-free (its jit gene unexpressed, as fb0d57c8a2's) and built and
ran on all three machines. Line by line, against c2ef9488ff (the mean paired log-difference, its SE, the sessions faster):

| line | sessions | 11a56ff9e4 against c2ef9488ff | range | faster |
|---|---|---|---|---|
| the laptop, 8-byte cells | 20 | +4.38% +/- 0.29% | +1.75% .. +6.35% | 0 of 20 |
| the laptop, 8-byte, loaded | 20 | +5.53% +/- 0.18% | +2.95% .. +6.74% | 0 of 20 |
| dream, 8-byte cells | 10 | -1.22% +/- 0.41% | -3.38% .. +0.32% | 6 of 10 |
| the laptop, 4-byte cells | 20 | -4.22% +/- 0.37% | -8.43% .. -0.40% | 20 of 20 |
| the laptop, 4-byte, loaded | 20 | -3.83% +/- 0.28% | -7.07% .. -1.56% | 20 of 20 |
| dream, 4-byte cells | 10 | -2.95% +/- 0.77% | -6.16% .. +1.51% | 9 of 10 |
| the Tegra | 2 | +0.35% +/- 1.08% | -0.73% .. +1.44% | 1 of 2 |

The classes as final-pick.py pools them (the laptop alone and dream, geometric mean): x86-64 +1.54% +/- 0.25%, x86-32
-3.59% +/- 0.43%, ARMv7 +0.35%. At 4-byte cells both machines agree - faster on each. At 8-byte cells they split: the
laptop 4.4% slower in every session (5.5% loaded), dream 1.2% faster; the pooled +1.54% passes the rule's 2% on the point,
its 2-SE bound (+2.04%) at the line. Dream ran under its backup copy (load over 2 in all 20 sessions; 630's finding: the
spread doubles, the paired readings unbiased) - its session differences do not follow the load: the quietest 8-byte
session (2.8) -2.37%, the busiest 4-byte one (17.2) -2.19%, near its mean. So by the rule fixed before the run 11a56ff9e4
takes the knee: smaller by an exact 5.45%, faster at 32 bits on both x86 machines, within 2% at 64 bits pooled - at the
cost, on the owner's laptop alone, of 4.4% at 8-byte cells. c2ef9488ff stays in the final set
(results/final-set-chainsBCD-seed86.md) whichever way the knee goes - nothing is lost.

**The jump-alignment test (Iteration 635)** - is dream's side of the 64-bit split the Skylake's JCC erratum (623)?
`python3 results/drafts/jcc-count-623.py results/followup-seed90.md results/chain-followup90`: the 7 built here as the
laptop builds them (the 8-byte engines the laptop's bytes, 7 of 7). At 8-byte cells 11a56ff9e4's engine has 13 of 136
dispatch jumps on a 32-byte boundary (9.6%), c2ef9488ff 11 of 170 (6.5%); branch units 11.9% and 11.5%. The erratum would
favour c2ef9488ff on dream, yet dream favours 11a56ff9e4 (dream/laptop 1.094 against 1.156): the split is not that
artefact, as far as static counts tell (not weighted by how often each jump runs) - each CPU's own, and by the rule the
pooled class is the measure.

## The rule after a follow-up (616) - not this list's

--gain: "none - the list has 0 of the run's and 7 found before": this follow-up re-measures a screened design, not a
portable run's; the portable search is reopened already (631, ae99617f06) - seed 91 set (632).

## The predictions of Iteration 631: three right, one wrong

(1) right - every line complete, done 15:01 Pacific. (2) right by the rule (the owner's decision). (3) right - x86-32
-3.59% +/- 0.43%, 8.5 SE. (4) wrong - at 8-byte cells the laptop +4.38%, dream -1.22% (results/predictions.md).
