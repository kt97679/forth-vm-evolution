# Seed 91's follow-up chain: the portable run's best 30 beside the portable designs found before (Iteration 640)

The chain at e22aa0b0be (fury, 2026-11-10 22:57 - 2026-11-11 13:17 UTC, 14.3 hours; 14:57 - 05:17 Pacific): the 38 of
results/followup-seed91.md - seed 91's best 30 by select(), the six portable holders (results/relf-designs-636.md),
c2ef9488ff and the screen's 7fb40ff7ba - re-measured side by side. The laptop 35 of 39 steps (the last 4 skipped by
repeat-fits: a session of 1455 s would end 10 minutes past the remote lines' deadline), dream 40 sessions a width, the
Tegra 5; every session measured all 38 on every line; no host over 2.0 load on average; the laptop's own checks PASS
(run-tests, validate 7 of 7 IDENTICAL, the jail). Noise: a paired difference's SE the laptop 0.17% / 0.23% (8 / 4-byte),
dream 0.07% / 0.10%, the Tegra 0.31%. Pooled: results/followup-pick-seed91.md (its set as JSON,
results/followup-pick-seed91.json); the readings results/chain-followup91/; the figures from `HANDOFF=results/handoff-relf-636.md
PRED=637 sh lab/evolve/process-followup.sh 91 640 fastest=782f3ad7ff,arm=3eb59b271d,knee=11a56ff9e4,smallarm=ae99617f06,
memory=fb0d57c8a2,smallest=64a7345393`; the gain against the whole pool from results/drafts/gain-bridge-640.py.

## The roles (results/handoff-relf-636.md; speed 2% at 2 SE, binary + image 1%, memory 4 KB)

- Fastest portable: 782f3ad7ff kept - the mean 0.3448 (x86-64 0.3428, x86-32 0.3380, ARMv7 0.3537); the run's best mean,
  b311f84693, 0.3452 (+0.13% +/- 0.18%).
- Fastest on ARMv7: 3eb59b271d kept (0.3121) - 965f48c803 -1.22% +/- 0.40%, 7fb40ff7ba -0.62% +/- 0.39%, short of 2%.
- The knee (11a56ff9e4), small and fast on ARMv7 (ae99617f06), least memory (fb0d57c8a2): no candidate.
- Smallest: 64a7345393 (13,891 B) against 01712a2639 (13,691 B, -1.44%): x86-64 +4.53% +/- 0.12%, x86-32 +18.42% +/-
  0.11%, ARMv7 +6.53% +/- 0.26%, memory +4 KB. The rule's candidate; the trade the owner turned down twice (611 and 621:
  4dd4e3e7e2, 1.31% smaller, x86-32 +27.9% - "performance drop is too significant and size gain is too small"). The
  owner's call; Claude's view: keep 64a7345393 - a milder form of the same trade (1.44% for x86-32 +18.4%, against 1.31%
  for +27.9%), still 200 bytes for a loss in every class.

## The 616 rule - a gain only against the list's own found-before

`followup-roles.py --gain` (OUT/gain.txt) says GAIN twice: the laptop alone at 4-byte cells, 3060f04651 0.3086 against
782f3ad7ff 0.3262 (-5.38% +/- 0.31%), and binary + image, 01712a2639 against 64a7345393 (-1.44%). Both are against the
list's 8 found before - followup-pick-seed90.json (seed 90's 7-design knee check) and the screen's flag - not the best
found before: the pool's extremes that hold no role were not in the list. Against the whole pool, from the records:

- Binary + image (exact): the pool's smallest is 4dd4e3e7e2, 13,709 B (results/portable-front-seed90.md) - 01712a2639
  -0.13%, short of 1% (637's in-run 18 bytes).
- The laptop alone at 4-byte cells, each JIT-free design of the earlier follow-ups (87-90) carried into this chain through
  the designs both measured (paired by session within each chain): e523a45566 (seed 89's follow-up) 0.3107 over 6 bridges
  (0.3099-0.3119) - 3060f04651 -0.68% (-1.05% to -0.42%); 9f8811f7f4 0.3122 (from chain 87) and 0.3142 (from 88) -
  -1.14% and -1.78%. Short of 2% by every bridge. The bridges hold: 782f3ad7ff read 0.3264 in seed 88's chain, 0.3262 here.
- At 8-byte cells, each class and the mean of the three: no gain already against the 8 (wider, it can only stay so).

So by the rule's intent (616: "beats the best of those found before"; its first form keyed on 9f8811f7f4, the pooled
pick's fastest at 32 bits) no extreme gained - the in-run verdict (637) re-measured. **The portable search stops and the
freeze follows, unless the owner gives 01712a2639 the smallest role** (a role taken is a gain by 616 - seed 92). The
comparator's gap: portable-followup.py takes found before from the last follow-up's pick alone - if another follow-up is
set, carry each earlier pick's extremes into its list.

## Seed 91's follow-up's predictions (637; 638's sizes)

(1) right - every line complete, the Tegra's fifth included. (2) right by the pooled reading (no gain), pending the
owner's call on the smallest; the tool's literal verdict is a gain. (3) right - 7fb40ff7ba -0.62% +/- 0.39% on the Tegra,
short of 2%. (4) wrong - 3060f04651 0.69% +/- 0.20% faster than 782f3ad7ff on the laptop at 8-byte cells (0.3048 against
0.3069).
