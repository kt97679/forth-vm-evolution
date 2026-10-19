# The checks of seed 59's front during seed 60 - dream at three builds and the Tegra (Iteration 406)

Seed 59's front, sampled ten a host, and seed 59's rejected designs. Spearman against the laptop's 64-bit speeds: dream 0.941
(default build, 24 designs) and 0.721 (64-bit, 10), at 32 bits 0.370 (10) - against the laptop's own 32-bit speeds
-0.257 (6 with one; `--laptop32`, Iteration 402); the Tegra 1.000 over the 4 it built. **The Tegra's six failures name
their cause at last** (Iteration 389's why()): `Error: bad immediate value for offset (5224)` from the assembler, every
one with alignhot 64 - open item 0d, results/xcheck32-402.md's lead superseded: across seeds 58-60's chains every one
of the 14 that failed there has alignhot 32 or 64, every one of the 28 that built 0 or 1. Rejected designs faster than
the front's median: dream 369ef14956 (at the 64-bit build than its fastest too); the Tegra 3, of the 4 measured.

## dream.lan-prebuilt

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-19 03:59 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.941** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 2 1 6 3 5 11.

| design | laptop | here | here / laptop |
|---|---|---|---|
| eb93048eea | 1.328 | 1.244 | 0.94 |
| 2edb0c836c | 1.402 | 1.317 | 0.94 |
| a161098f78 | 1.362 | 1.285 | 0.94 |
| f3e418a356 | 0.123 | 0.213 | 1.73 |
| 8e358090f6 | 0.123 | 0.215 | 1.75 |
| 745aaee6aa | 0.120 | 0.210 | 1.75 |

Copied there: 8.8 MB in 0m 00s (38179 KB/s); mkdir 384 ms, start 179740 ms; the connection 245 ms
12 ms
11 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 0.98 on average, 1.72 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.18, the busiest then: sshd 54.8%, sshd 9.5%, chrome 2.0%.

## dream.lan-prebuilt32

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-19 04:02 UTC, 3 round(s) a design.


**10 designs measured on both: Spearman 0.370** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 10): 4 3 2 6 5 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| a2a87060a2 | 0.541 | 0.531 | 0.98 |
| 49dd6f75b8 (rejected) | 0.541 | 0.643 | 1.19 |
| 2c53666224 (rejected) | 0.511 | 0.682 | 1.33 |
| 57e65b543e | 0.293 | 0.621 | 2.12 |
| 9de9bfb586 | 0.295 | 0.633 | 2.15 |
| cd9d470f51 | 0.289 | 0.621 | 2.15 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (369ef14956); than its fastest: 0.

Copied there: 8.6 MB in 0m 00s (83815 KB/s); mkdir 14 ms, start 135522 ms; the connection 245 ms
12 ms
11 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 2.30 on average, 2.90 at most, over 5 samples 30 s apart, on 8 CPUs; at its start 2.53, the busiest then: chrome 2.0%, chrome 1.4%, mysqld 0.8%.

## dream.lan-prebuilt64

### dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-19 04:04 UTC, 3 round(s) a design.


**10 designs measured on both: Spearman 0.721** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 10): 6 2 1 5 4 3.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 49dd6f75b8 (rejected) | 0.541 | 0.484 | 0.90 |
| a2a87060a2 | 0.541 | 0.558 | 1.03 |
| 280d3e3632 (rejected) | 0.425 | 0.448 | 1.06 |
| 3a5638f18d | 0.300 | 0.372 | 1.24 |
| 9de9bfb586 | 0.295 | 0.380 | 1.29 |
| cd9d470f51 | 0.289 | 0.389 | 1.35 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (369ef14956); than its fastest: 1 (369ef14956).

Copied there: 8.5 MB in 0m 00s (85554 KB/s); mkdir 19 ms, start 136170 ms; the connection 245 ms
12 ms
11 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.26 on average, 1.41 at most, over 5 samples 30 s apart, on 8 CPUs; at its start 1.41, the busiest then: ps 200%, chrome 2.0%, chrome 1.4%.

## rage.lan-native

### rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.2.11-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-19 04:09 UTC, 2 round(s) a design.

- cd9d470f51 not measured: failed here: died: engine did not compile (ccAF0GNS.s:1212: Error: bad immediate value for offset (5224))
- 57e65b543e not measured: failed here: died: engine did not compile (ccAnAYMZ.s:788: Error: bad immediate value for offset (5224))
- 9de9bfb586 not measured: failed here: died: engine did not compile (ccdOka1T.s:824: Error: bad immediate value for offset (5224))
- 3a5638f18d not measured: failed here: died: engine did not compile (ccTzTBkV.s:824: Error: bad immediate value for offset (5224))
- f8bc41d8c3 not measured: failed here: died: engine did not compile (ccrCRv5W.s:788: Error: bad immediate value for offset (5224))
- 369ef14956 not measured: failed here: died: engine did not compile (ccjUH2VD.s:788: Error: bad immediate value for offset (5224))

**4 designs measured on both: Spearman 1.000** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 4): 1 2 3 4.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 49dd6f75b8 (rejected) | 0.541 | 0.625 | 1.16 |
| a2a87060a2 | 0.541 | 0.636 | 1.18 |
| 9883b8ef9c (rejected) | 0.415 | 0.495 | 1.19 |
| a2a87060a2 | 0.541 | 0.636 | 1.18 |
| 9883b8ef9c (rejected) | 0.415 | 0.495 | 1.19 |
| b00dcff7b6 (rejected) | 0.476 | 0.606 | 1.27 |

**Rejected by the laptop's selection, measured here: 3** - faster here than the front's median: 3 (9883b8ef9c, b00dcff7b6, 49dd6f75b8); than its fastest: 3 (9883b8ef9c, b00dcff7b6, 49dd6f75b8).

Copied there: 8.4 MB in 0m 01s (7838 KB/s); mkdir 227 ms, start 1923585 ms; the connection 232 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.48 on average, 2.24 at most, over 65 samples 30 s apart, on 4 CPUs; at its start 0.19, the busiest then: ps 300%, sshd-session 85.8%, sh 33.3%.
