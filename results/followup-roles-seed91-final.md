# The final check before the freeze: 435 designs on three machines - no extreme gained, one trade-free smallest (Iteration 648)

The chain at 16681a02bf (fury, 2026-11-11 14:48 - 2026-11-12 16:39 UTC, 25.9 hours; 06:48 - 08:39 Pacific): the 435 of
results/followup-seed91-final.md - the 72 pooled-front designs no chain had measured across machines ("the check"), seed
91's rest (320), the six holders, c2ef9488ff and the 36 best re-measured before - side by side. The laptop 5 sessions (the
sixth step skipped by repeat-fits: it would end 279 minutes past the remote lines' deadline), dream 7 a width, **the Tegra 2
of 3** (the third not started: it would end past the 1555 minutes; a session took about 9.3 hours). Every session measured
all 435 on every line, none died; the laptop's own checks PASS (run-tests, validate, the jail). Load: the Tegra's first
session 3.0 on average (peak 8), the rest under 2.0. A paired difference's SE: the laptop 0.29% / 0.44% (8 / 4-byte),
dream 0.32% / 0.36%, the Tegra 0.85%. Pooled: results/followup-pick-seed91-final.md (its set as JSON,
results/followup-pick-seed91-final.json); the readings results/chain-followup91-final/; the figures from
`HANDOFF=results/handoff-relf-636.md PRED=641 sh lab/evolve/process-followup.sh 91-final 648 fastest=782f3ad7ff,
arm=3eb59b271d,knee=11a56ff9e4,smallarm=ae99617f06,memory=fb0d57c8a2,smallest=64a7345393`, the rest from
results/drafts/finalcheck-648.py.

## The roles (results/handoff-relf-636.md; speed 2% at 2 SE, binary + image 1%, memory 4 KB)

- Fastest portable: 782f3ad7ff kept - the mean 0.3442 (x86-64 0.3412, x86-32 0.3365, ARMv7 0.3552); next b311f84693
  0.3486 (+1.3%); the run's best mean, 208bd2d2ff, +2.83% +/- 0.72%.
- Fastest on ARMv7: 3eb59b271d kept (0.3128) - 7fb40ff7ba -0.94% +/- 0.14% (-1.08% and -0.81%; seed 91's follow-up
  -0.62%), short of 2%.
- The knee (11a56ff9e4), least memory (fb0d57c8a2, 104 KB; the next 108 KB): no candidate.
- Small and fast on ARMv7: ae99617f06 kept by 629's rule (every Tegra session pooled). followup-roles.py lists
  a627b954c6, the holder before 631: -3.21% +/- 0.07% in this chain (-3.28%, -3.14%); but every session of every chain
  that measured both, 10: +1.21% +/- 0.84% (the 8 before this chain +2.34% +/- 0.51%) - not by the rule. See "The Tegra
  between chains".
- Smallest: 64a7345393 (13,891 B). 30 smaller designs, 29 with a trade - the 13,691 B five (01712a2639 among them, -1.44%):
  x86-32 +18-19%; the 13,715 B five (-1.27%): x86-32 +15-17%; the rest ARMv7 +3-12% or x86-32 +3-9%. **The one without:
  d180351903** (seed 91's rest; 13,883 B, -8 B: engine +48, image -56; memory the same): x86-64 -0.59% +/- 0.29% - the
  machines split, the laptop +3.40% +/- 0.09% (5 of 5 sessions), dream -4.43% +/- 0.57%, as the knee's did (636); x86-32
  -3.85% +/- 0.25% (the laptop -5.09%, dream -2.59%, both every session); ARMv7 -3.30% +/- 0.68% (2 sessions, one chain).
  Expressed, against 64a7345393: alignfn on, fbuf 2 -> 1, a different eleven folds, nocet 0, one other super, ops10 6 -> 10
  (0<?BRANCH, I, UNLOOP, FILL, CMOVE in, =I?BRANCH out) - the same mechanisms, four more primitives; its dormant rtimm=2
  and rtloopall unexpressed, so the freeze's batch leaves it (neither -loop nor lean). Its 4-byte size was not measured here.
  **The owner's call** (612's kind: smaller and faster, not a trade). Claude's view: take d180351903 if pack-designs.py
  shows it smaller at 4-byte cells too (else keep 64a7345393); 01712a2639 kept, as at 640.

## The 616 rule - no extreme gained

`followup-roles.py --gain`, the run's designs ("the check" counted with them, 641) against the best found before: every
line no - the laptop alone at 8-byte cells 38100f0280 (one of the 72) +2.69% +/- 0.56% behind 7fb40ff7ba, at 4-byte
95077030b0 (one of the 72) +1.84% +/- 0.93% behind e523a45566; x86-64 +1.26%, x86-32 +0.66%, ARMv7 +2.52%, the mean
+2.83%; binary + image f75a82e4ee the same 13,691 B as 01712a2639; memory +8 KB. Its verdict's "seed 92" does not apply
here (641): a role taken means the package and designs/ again, then the freeze. The pool's in-run fastest at both widths
were the in-run lead again (as 624 found: the fast end re-measures slower).

## The Tegra between chains

Its kernel moved from 7.3.1 to 7.3.3 between seed 90's screen (2026-11-10 10:48) and seed 91's follow-up (23:07); the
compiler stayed (GCC 16.2.1). The 45 designs read under both: median -3.38% against s6, around it an IQR of 1.56% and
5-95% of 5.24%; between two chains on one kernel IQR 0.60% (12 designs) and 2.47% (21, with this chain's loaded first
session). So a pair can swing 4-5% between chains while one chain's SE says 0.1%: a627b954c6 -6.05%, ae99617f06 -1.51%
across the kernels. This is why 629 pools every session; an ARMv7 figure resting on one chain (d180351903's -3.30%) carries
it. The loaded first session: s1 against s2 median +0.50%, 95th percentile +8.10%, but the three pairs judged above agree
between the two (a627b954c6 -3.28% / -3.14%, d180351903 -2.64% / -3.96%, 7fb40ff7ba -1.08% / -0.81%).

## The final check's predictions (641)

(1) wrong - the Tegra measured 2 of 3 sessions. (2) pending - a role changes only if the owner gives d180351903 the smallest
(then wrong). (3) right - neither of the 72's in-run fastest beat the best found before (+2.69%, +1.84%). (4) right -
none died on any line.

## The owner's decision (649)

d180351903 takes the smallest - built by pack-designs.py, smaller at both widths (13,883 / 13,627 B against 64a7345393's
13,891 / 13,675) and 9 of 9 right at both: results/handoff-relf-649.md. Small and fast on ARMv7 left to the pooled rule.
