# The checks of seed 57's front during seed 58 - four machines, and seed 57's rejected designs (Iteration 384)

Seed 57's front (selected at both widths), measured on three hosts alongside seed 58's run, and - first, the new xcheck --rejected test (HANDOFF item 4d) - the designs seed 57's own selection rejected, measured elsewhere to find a blind spot. The rank agreement with the laptop: the Tegra (ARMv7, 4-byte cells) Spearman 0.973, dream 64-bit 0.959, dream default-build 64-bit 0.960, dream 32-bit 0.875 - the width's skew again (as Iteration 353 found). **The blind-spot test: of the designs the laptop rejected, none is faster on any host than the front's fastest sampled there** (Tegra 3 rejected / 0 past the fastest / 2 past the median; dream-32 6 / 0 / 2; dream-64 6 / 0 / 1) - the laptop's selection misses no design that another machine would put at the top, by this sample.

## dream.lan-prebuilt

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-18 03:19 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.960** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 3 2 1 5 7 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 7d4b2458a0 | 1.418 | 1.276 | 0.90 |
| b72b271973 | 1.423 | 1.321 | 0.93 |
| ce44174629 | 1.389 | 1.333 | 0.96 |
| a623b5ebd1 | 0.116 | 0.205 | 1.77 |
| a7f9be0a33 | 0.120 | 0.213 | 1.78 |
| 417a0a03f1 | 0.125 | 0.223 | 1.79 |

## dream.lan-prebuilt32

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-18 03:23 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.875** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 1 2 3 10 15 14.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 621a016373 (rejected) | 0.951 | 0.849 | 0.89 |
| 7d4b2458a0 | 1.418 | 1.301 | 0.92 |
| b72b271973 | 1.423 | 1.326 | 0.93 |
| 35646f5d29 | 0.352 | 0.703 | 2.00 |
| ba1dc42644 | 0.335 | 0.679 | 2.03 |
| 69bed0ce1d | 0.347 | 0.710 | 2.05 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 2 (ade7c2acb9, 16b3bec189); than its fastest: 0.

## dream.lan-prebuilt64

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-18 03:28 UTC, 3 round(s) a design.


**30 designs measured on both: Spearman 0.959** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 1 3 2 4 7 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 621a016373 (rejected) | 0.951 | 0.872 | 0.92 |
| b72b271973 | 1.423 | 1.331 | 0.94 |
| 84087712e8 | 1.452 | 1.367 | 0.94 |
| 35646f5d29 | 0.352 | 0.409 | 1.16 |
| 69bed0ce1d | 0.347 | 0.414 | 1.19 |
| 0c143496ca | 0.731 | 1.013 | 1.39 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (ade7c2acb9); than its fastest: 0.

## rage.lan-native

### rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.2.11-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-18 03:35 UTC, 2 round(s) a design.

- 5405c5b1d9 not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)
- df0c11fd98 not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)
- ade7c2acb9 not measured: failed here: died: engine did not compile (collect2: error: ld returned 1 exit status)

**13 designs measured on both: Spearman 0.973** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 13): 1 3 4 2 5 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| ded8dcc010 (rejected) | 0.734 | 0.657 | 0.90 |
| efc0c8773a (rejected) | 1.022 | 1.043 | 1.02 |
| dfd14a3b70 | 0.984 | 1.124 | 1.14 |
| ba1dc42644 | 0.335 | 0.510 | 1.52 |
| 69bed0ce1d | 0.347 | 0.532 | 1.53 |
| 35646f5d29 | 0.352 | 0.541 | 1.54 |

**Rejected by the laptop's selection, measured here: 3** - faster here than the front's median: 2 (ded8dcc010, efc0c8773a); than its fastest: 0.

