# The checks of seed 56's front during seed 57 - four machines (Iteration 378)

Seed 56's front (selected at 64 bits only), measured on three hosts alongside seed 57's run. Same width, other machines: dream 64-bit Spearman 0.980, the same designs at 64 bits on dream 0.949, the Tegra (ARMv7, 4-byte cells) 0.881. At 32 bits on dream: 0.713, the laptop's six fastest ranking 7-13 there - the width again, as Iteration 353 found: the skew seed 57's two-width selection is for.

## dream.lan-prebuilt

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-17 14:53 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.980** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 3 4 2 1 5 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 495ec50c15 | 1.436 | 1.352 | 0.94 |
| 4c137fcc50 | 1.425 | 1.380 | 0.97 |
| 71aca12307 | 1.484 | 1.438 | 0.97 |
| be27764d7a | 0.134 | 0.233 | 1.74 |
| 2d0c726419 | 0.125 | 0.218 | 1.74 |
| a0a0277bf2 | 0.123 | 0.217 | 1.77 |

## dream.lan-prebuilt32

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-17 14:57 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.713** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 7 13 6 9 12 10.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 71aca12307 | 1.484 | 1.358 | 0.91 |
| 495ec50c15 | 1.436 | 1.346 | 0.94 |
| af41baaf57 | 1.060 | 1.022 | 0.96 |
| 995408b295 | 0.369 | 0.699 | 1.89 |
| 0b415f2658 | 0.364 | 0.702 | 1.93 |
| 78d9b36dcd | 0.354 | 0.705 | 1.99 |

## dream.lan-prebuilt64

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-17 15:01 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.949** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 1 4 2 5 7 6.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 71aca12307 | 1.484 | 1.355 | 0.91 |
| 495ec50c15 | 1.436 | 1.362 | 0.95 |
| af41baaf57 | 1.060 | 1.023 | 0.97 |
| 4192194499 | 1.220 | 1.398 | 1.15 |
| 0b415f2658 | 0.364 | 0.417 | 1.15 |
| bb8dc4a9b9 | 0.693 | 0.826 | 1.19 |

## rage.lan-native

### rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.2.11-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-17 15:08 UTC, 2 round(s) a design.


**12 designs measured on both: Spearman 0.881** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 12): 2 4 1 5 7 3.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 6a5bb61517 | 0.882 | 0.966 | 1.10 |
| 495ec50c15 | 1.436 | 1.823 | 1.27 |
| 71aca12307 | 1.484 | 1.890 | 1.27 |
| c054a4b517 | 0.363 | 0.528 | 1.45 |
| 0b415f2658 | 0.364 | 0.533 | 1.47 |
| 78d9b36dcd | 0.354 | 0.527 | 1.49 |

