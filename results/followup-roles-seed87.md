# The follow-up chain: the relf handoff's portable roles re-measured (Iteration 611)

The chain at b74b8486cb (fury, 2026-11-05 05:04 - 18:18, 13.2 hours): the 45 of results/followup-seed87.md - seed 87's 30
best, the 282's 13 by role, the handoff's 690981ca5b and c2ef9488ff - re-measured side by side on three machines. The
laptop 28 sessions (10 rounds, alone and loaded, both widths; 2 more of the 30 not started - past the remote lines'
deadline, as planned), dream 45 sessions at 8-byte cells and 41 at 4-byte, the Tegra 5. Every session measured all 45 on
every line; no design died. Pooled: results/followup-pick-seed87.md; the readings: results/chain-followup87/; every
figure here: results/drafts/followup-roles-611.py. The incumbents agree with seed 86's chains within 1% (690981ca5b
0.416 / 0.456 / 0.330 against 601's 0.414 / 0.455 / 0.327).

## The roles - the rule fixed before seed 87 (results/drafts/portable-plan-602.md): speed 2%, bytes 1%, memory 4 KB

Speeds are the classes of final-pick.py step 5 (lower is faster); errors are paired by session.

| role at 601 | design at 601 | now | the evidence |
|---|---|---|---|
| fastest portable | 690981ca5b | **782f3ad7ff** | the mean 0.3507 against 0.3969, -11.6% +/- 0.1%: x86-64 -17.6%, x86-32 -25.7%, ARMv7 +12.7% |
| fastest on ARMv7 | 690981ca5b | 690981ca5b | 3452cb633b -0.08% +/- 0.21% (a tie again); the next, a2df4ef183, +1.6% |
| the knee: fast portable on x86, small | c2ef9488ff | c2ef9488ff | 0d66d2e102 1.4% smaller but 2.0% and 1.8% slower on x86 - a trade, not a gain |
| small, fast on ARMv7 | 22420b3b61 | **a627b954c6** | 1.7% smaller at 8-byte cells (18,607 against 18,928 B), 1.2% at 4-byte (18,135 against 18,348), ARMv7 -1.1%; memory 124 KB against 120 - the owner (611): the 4 KB traded for the gains |
| least memory | fb0d57c8a2 | fb0d57c8a2 | 104 KB; the next 108 KB |
| smallest | cea114f47e | cea114f47e | 62abdb2c64 136 B smaller (0.98%) but 12.5% slower at x86-64 and 24.0% at x86-32 - the owner (611): no small gain in one criterion for a large loss in the others |

The first role splits: 782f3ad7ff, a design of the portable run, is the fastest without the JIT and the best mean on x86 at
both widths (and the generic pick of the 45); 690981ca5b keeps the ARMv7 role. 782f3ad7ff, a627b954c6: 9 of 9 workloads
right against s6 at both widths (pack-designs.py). The four JIT roles were not re-measured (a portable chain): the
handoff's ten, results/handoff-relf-611.md.

**Open for the owner**: 64a7345393 is smaller than cea114f47e at both widths (13,891 against 13,939 B; 13,675 against
13,703), faster in every class (x86-64 -2.9% +/- 0.2%, x86-32 -3.1% +/- 0.2%, ARMv7 -7.1% +/- 0.3%), the same memory
(116 KB), 9 of 9 right at both widths: it dominates cea114f47e, by 0.34% of bytes where the rule asks 1%.

## The noise, against the chain's sizing (NEXT-RUN 610: a session moves a design 0.7-0.9%)

A design's session-to-session SD, the median over the 45, paired (each session's common shift removed): the Tegra 0.44%,
dream 0.42% and 0.44%, the laptop 0.79% at 8-byte cells and 1.08% at 4-byte. A paired difference's SE: the Tegra 0.28%
over 5 sessions - 2% at 7 SE, not the 4 the sizing aimed at; dream 0.09-0.10%; the laptop 0.21-0.29%. The laptop's
sessions share a shift (range 2.5-3.0%; its last third 0.8-1.0% below its first); pairing within a session cancels it.

## Across machines: factor and the compiler on dream at 4-byte cells

dream's speed over the laptop's at 4-byte cells, the median by (factor, compiler); 8-byte cells and the Tegra (over the
laptop at 4) beside it:

| factor, compiler | designs | dream/laptop, 4-byte | 8-byte | the Tegra/laptop |
|---|---|---|---|---|
| 0, GCC | 10 | 1.418 | 1.257 | 0.903 |
| 0, clang | 17 | 1.107 | 1.165 | 1.258 |
| 2, clang | 9 | 1.387 | 1.536 | 1.154 |
| 3, GCC | 7 | 1.949 | 1.287 | 1.053 |
| all 45 | 45 | 1.244 | 1.254 | 1.127 |

factor 3 (every word's repeated cold code in shared bodies) with GCC runs 1.95 times the laptop's time on dream at 32
bits, against 1.24 for the 45 - normal at 64 bits and on the Tegra. It is why the laptop's fastest at 32 bits
(9f8811f7f4, a2df4ef183, b35ae710e6) and 690981ca5b and 3452cb633b sit 34-36% behind the best at x86-32 across machines,
and part of why dream's 4-byte line ranks the 45 at Spearman 0.77 against the laptop (8-byte 0.94). GCC without factor 3
is slow there too (1.42 against clang's 1.11); every factor-3 design here is GCC, so the two are not separated. dream
runs the prebuilt engines: the Skylake at 32 bits, not the build - not confirmed.
