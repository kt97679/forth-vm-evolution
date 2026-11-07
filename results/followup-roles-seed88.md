# Seed 88's follow-up chain: the portable roles re-measured, and the portable search's end (Iteration 621)

The chain at 4df9d902e4 (fury, 2026-11-06 18:14 - 2026-11-07 03:10, 8.9 hours): the 46 of results/followup-seed88.md -
seed 88's 30 best on the union's front, seed 87's follow-up pick's 13, the relf handoff's 690981ca5b, c2ef9488ff and
64a7345393 - re-measured side by side on three machines. The laptop 18 sessions (10 rounds, alone and loaded, both widths;
2 more of the 20 not started - past the remote lines' deadline, as 614 sized), dream 28 sessions at 8-byte cells and 25 at
4-byte of the 35 allowed (about 10 minutes a session), the Tegra 3. Every session measured all 46 on every line; no design
died. Pooled: results/followup-pick-seed88.md (its set as JSON, results/followup-pick-seed88.json); the readings:
results/chain-followup88/; every figure here from one command, `PRED=614 sh lab/evolve/process-followup.sh 88 621
fastest=782f3ad7ff,arm=690981ca5b,knee=c2ef9488ff,smallarm=a627b954c6,memory=fb0d57c8a2,smallest=64a7345393`
(followup-roles.py, then its --gain). The incumbents agree with seed 87's follow-up within 0.1%: 782f3ad7ff 0.3429 /
0.3384 / 0.3719, the mean 0.3507, against 611's 0.3428 / 0.3387 / 0.3715 and 0.3507.

## The roles - the rule fixed before seed 87 (results/drafts/portable-plan-602.md): speed 2%, bytes 1%, memory 4 KB

Speeds are the classes of final-pick.py step 5 (lower is faster); errors are paired by session.

| role | holder | now | the evidence |
|---|---|---|---|
| fastest portable | 782f3ad7ff | 782f3ad7ff | the run's best mean, 7055894eea, +5.47% +/- 0.40% |
| fastest on ARMv7 | 690981ca5b | 690981ca5b | the run's c7814def6d -0.70% +/- 0.53% (under 2%); 3452cb633b +0.06% - a tie the third time |
| the knee | c2ef9488ff | c2ef9488ff | none of the run's beats it by the rule |
| small, fast on ARMv7 | a627b954c6 | a627b954c6 | none of the run's beats it by the rule |
| least memory | fb0d57c8a2 | fb0d57c8a2 | 104 KB; the run's least 112 KB (640feb6013) |
| smallest | 64a7345393 | 64a7345393 | 4dd4e3e7e2 182 B smaller (1.31%) but x86-64 +4.5%, x86-32 +27.9%, ARMv7 +8.3%; 422e922f9c 40 B smaller (0.29%, under the bar) but x86-32 +3.6%, ARMv7 +5.9%, memory +4 KB |

**The smallest, judged by the owner's trade at 611**: 62abdb2c64, 136 B smaller (0.98%) for 12.5% at x86-64 and 24.0% at
x86-32, was "no small gain in one criterion for a large loss in the others". 4dd4e3e7e2 is that trade again - 182 B for
4.5%, 27.9% and 8.3% - and clears the bytes bar only against the holder, not against the smallest found before
(62abdb2c64: -0.68%); 422e922f9c is under the bar and slower in two classes. Neither takes the role - **the owner
confirmed (621)**: "performance drop is too significant and size gain is too small". Both are kept: 4dd4e3e7e2 the pooled pick's smallest (results/followup-pick-seed88.md),
422e922f9c on seed 88's recorded front.

## The rule after the follow-up (616, 618): no gain - the portable search stops

| | the run's best | found before | the run against it | gain |
|---|---|---|---|---|
| the laptop alone, 8-byte cells | c7814def6d 0.3152 | 782f3ad7ff 0.3069 | +2.70% +/- 0.36% | no |
| the laptop alone, 4-byte cells | c7814def6d 0.3205 | 9f8811f7f4 0.3141 | +2.06% +/- 0.76% | no |
| x86-64 | a8ea0ad5b7 0.3499 | 782f3ad7ff 0.3429 | +2.05% +/- 0.16% | no |
| x86-32 | 7055894eea 0.3443 | 782f3ad7ff 0.3384 | +1.74% +/- 0.23% | no |
| ARMv7 | c7814def6d 0.3267 | 690981ca5b 0.3290 | -0.70% +/- 0.53% | no |
| the mean of the three | 7055894eea 0.3699 | 782f3ad7ff 0.3507 | +5.47% +/- 0.40% | no |
| binary + image | 4dd4e3e7e2 13,709 B | 62abdb2c64 13,803 B | -0.68% | no |
| memory | 640feb6013 112 KB | fb0d57c8a2 104 KB | +8 KB | no |

No extreme gained and no role taken: by the rule the portable search stops after two runs - seed 87's gain confirmed at
611 (the mean -4.2% against 8cc7f60d6b), seed 88's none. Seed 88's one in-run gain, the fastest at 32 bits (c7814def6d
0.2803 against 0.2888, -2.9%, 614), reverses side by side: 2.1% behind 9f8811f7f4 on the laptop alone at 4-byte cells - an
in-run lead read from the run's own selection, which the follow-up exists to check. 614's compiler finding holds across the
46 (compiler 0 GCC, 1 clang): dream's time over the laptop's at 4-byte cells, by factor, GCC 1.22-1.90 and clang 1.10-1.46;
c7814def6d, a GCC build, 2.049.

## The noise against 614's sizing (2% at about 5.5 SE on the Tegra and the laptop at 4-byte cells)

A paired difference's SE: the Tegra 0.36% over 3 sessions and the laptop at 4-byte cells 0.35% - 2% at 5.6 and 5.7 SE, as
sized; the laptop at 8-byte 0.25%, loaded 0.21-0.33%; dream 0.12-0.13% (28 and 25 sessions, not 35: 2% at 15-17 SE, not
19). A design's session-to-session SD, the median over the 46: the Tegra 0.48%, dream 0.42-0.48%, the laptop 0.71-1.22%;
the laptop's sessions share a shift (range 1.1-2.3%), cancelled by pairing.

## The predictions of 614 - three right, one wrong

(1) right - the chain done, every session of every line complete (80/20). (2) wrong - no role to a seed 88 design (55/45):
the smallest's two candidates turned down by the owner's trade. (3) right - the fastest portable role stays with
782f3ad7ff, the run's best mean +5.47% (65/35). (4) right - c7814def6d on dream at 4-byte cells 2.049 times the laptop's
time (the bar 1.36; 75/25).

## Next - the last JIT run (620)

`seed 89 21h widths carryall` (results/drafts/jit-run-plan-620.md): the JIT allowed, every archived database carried, no
experiment; its remote lines screen results/screen-seed88.md (617's lines: the 375 of seed 88's union front not
re-measured here, with the six holders). Judged by confirm.py, only what it bred counted - its pool widened by --pool to
the portable runs' fronts (the default for seed 89, `confirm.py --pool-files 89`, is seeds 77-84 and 86: without seeds 87
and 88 a JIT design could pass a bar a portable design already holds). A follow-up beside the four x86 roles when it gains;
the screen's flagged join it, or a short follow-up of their own (portable-followup.py --also) - a flagged design that takes
a portable role reopens the portable search. Then the freeze (results/drafts/portable-plan-602.md, "Then the freeze").
