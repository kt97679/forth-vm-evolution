# dream.lan's checks of seed 54's front, during seed 55 (Iteration 334)

The first run checked at both widths (chain-20261016-132647): dream.lan at 64 bits (24 designs, the
laptop's binaries) and 32-bit x86 at 4-byte cells (24 interpreted designs, the laptop's static -m32
builds, each alive there first). 3 rounds each, alongside seed 55's run.

## 64-bit

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-16 13:34 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.940** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 2 5 6 7 1 10.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 2150fa05c4 | 1.410 | 1.372 | 0.97 |
| 8a62e9fba3 | 1.431 | 1.417 | 0.99 |
| 7ad1796288 | 1.374 | 1.377 | 1.00 |
| a1400458de | 0.140 | 0.240 | 1.71 |
| 07504b6807 | 0.133 | 0.231 | 1.74 |
| e12a57503b | 0.131 | 0.231 | 1.76 |

## 32-bit x86, 4-byte cells

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-16 13:38 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.694** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 8 10 9 11 13 12.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 8a62e9fba3 | 1.431 | 1.341 | 0.94 |
| 2150fa05c4 | 1.410 | 1.354 | 0.96 |
| 7ad1796288 | 1.374 | 1.426 | 1.04 |
| de90232b56 | 0.368 | 0.700 | 1.90 |
| b926dd6bc8 | 0.351 | 0.674 | 1.92 |
| d74dc16c2f | 0.354 | 0.682 | 1.93 |
