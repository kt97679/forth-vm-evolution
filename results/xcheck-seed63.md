# The checks of seed 62's front during seed 63 - dream at three builds and the Tegra (Iteration 441)

Seed 62's front, sampled, its rejected designs, and designs asked for by id. Spearman against the laptop's 64-bit
speeds: dream 0.723 (default build, 24), 0.932 (64-bit, 30), at 32 bits 0.834 (30); the Tegra 0.912 (16). Against the
laptop's own 32-bit speeds: dream 0.894 (23), the Tegra 0.867 (12).

**The Tegra's rebuild test (Iteration 428): 7 of 7 asked for built and were measured** - ce937eca6d and 5405c5b1d9
(alignhot 32, the linker's failure in seeds 58-59's chains) and 3a5638f18d and cd9d470f51 (alignhot 64, the assembler's
in seed 60's) among them: alignhot left out of a 32-bit ARM build (Iteration 407) was the whole cause. Item 0d closed.

**The head to head across the machine classes (Iteration 430; review-checks.py generic):** 10 designs on all three.
First 5f512a3017 (seed 62's front; x86-64 0.368, x86-32 0.509, ARMv7 0.391 - mean 0.419, 25,105 bytes), then
83716d5eaf (seed 62's front, 0.437), bf439eb307 (0.467), ad56a8e0fd (0.523, vetoed at x86-64), 11e5884401 (0.560,
vetoed at both x86); the rest, small-end designs, 1.43 and slower.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-20 17:14 UTC, 3 round(s) a design.


**24 designs measured on both: Spearman 0.723** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 24): 4 9 14 12 8 10.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 6908fe3fe5 | 1.520 | 1.371 | 0.90 |
| a296e513a0 | 0.748 | 0.675 | 0.90 |
| 84e6a6813a | 1.424 | 1.318 | 0.93 |
| 890dfecc36 | 0.121 | 0.209 | 1.73 |
| ac7640e77b | 0.122 | 0.212 | 1.74 |
| f6b7cc70a1 | 0.121 | 0.215 | 1.78 |

Copied there: 9.2 MB in 0m 00s (79588 KB/s); mkdir 281 ms, start 171049 ms; the connection 353 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.42 on average, 2.09 at most, over 6 samples 30 s apart, on 8 CPUs; at its start 0.89, the busiest then: sshd 10.0%, sshd 9.3%, chrome 2.0%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 4-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-20 17:17 UTC, 3 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 3 of 3 built and measured here.

- bf439eb307 speed 0.625 here
- 11e5884401 speed 0.669 here
- ad56a8e0fd speed 0.564 here

**30 designs measured on both: Spearman 0.834** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 7 14 5 8 6 9.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 649f19592e | 1.057 | 0.914 | 0.86 |
| a598c55b80 | 0.762 | 0.671 | 0.88 |
| 708c3ae7fa (rejected) | 0.705 | 0.638 | 0.91 |
| 5f512a3017 | 0.289 | 0.509 | 1.76 |
| 83716d5eaf | 0.300 | 0.614 | 2.05 |
| d169bc4d67 (rejected) | 0.483 | 1.178 | 2.44 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (3e2ad66957); than its fastest: 0.

Copied there: 9.3 MB in 0m 00s (79014 KB/s); mkdir 10 ms, start 204125 ms; the connection 353 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.26 on average, 1.36 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 1.26, the busiest then: chrome 2.0%, chrome 1.4%, mysqld 0.8%.

---

## dream - Intel(R) Core(TM) i7-6700 CPU @ 3.40GHz

little-endian, 8-byte cells - measured on the host (Iteration 331)

x86_64, 6.8.0-146-generic; cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0; Python 3.12.3; measured 2026-10-20 17:20 UTC, 3 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 3 of 3 built and measured here.

- bf439eb307 speed 0.371 here
- 11e5884401 speed 0.551 here
- ad56a8e0fd speed 0.535 here

**30 designs measured on both: Spearman 0.932** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 30): 2 8 1 13 3 10.

| design | laptop | here | here / laptop |
|---|---|---|---|
| 649f19592e | 1.057 | 0.865 | 0.82 |
| 6908fe3fe5 | 1.520 | 1.352 | 0.89 |
| ae55f07a3a | 1.415 | 1.287 | 0.91 |
| 9d47de1d1c | 0.297 | 0.377 | 1.27 |
| 5f512a3017 | 0.289 | 0.368 | 1.27 |
| e2da92da32 | 0.295 | 0.386 | 1.31 |

**Rejected by the laptop's selection, measured here: 6** - faster here than the front's median: 1 (3e2ad66957); than its fastest: 0.

Copied there: 9.3 MB in 0m 00s (88585 KB/s); mkdir 9 ms, start 193943 ms; the connection 353 ms
16 ms
14 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 1.39 on average, 2.38 at most, over 7 samples 30 s apart, on 8 CPUs; at its start 0.95, the busiest then: ps 100%, chrome 2.0%, chrome 1.4%.

---

## rage - ARMv7 Processor rev 3 (v7l)

little-endian, 4-byte cells - measured on the host (Iteration 331)

armv7l, 7.2.11-gentoo; cc (Gentoo 16.2.1_p20260926 p1) 16.2.1 20260926; Python 3.14.8; measured 2026-10-20 17:29 UTC, 2 round(s) a design.


**Asked for by id** (--also, Iteration 428 - the rebuild test of designs that once failed here): 7 of 7 built and measured here.

- ce937eca6d speed 0.312 here
- 5405c5b1d9 speed 0.411 here
- 3a5638f18d speed 0.450 here
- cd9d470f51 speed 0.429 here
- bf439eb307 speed 0.439 here
- 11e5884401 speed 0.478 here
- ad56a8e0fd speed 0.474 here

**16 designs measured on both: Spearman 0.912** between the laptop's speeds and this host's.

The laptop's six fastest, their rank here (of 16): 2 1 3 7 6 8.

| design | laptop | here | here / laptop |
|---|---|---|---|
| af3eaa2a8c | 1.059 | 1.065 | 1.01 |
| e56c20b0c9 (rejected) | 0.910 | 1.013 | 1.11 |
| a045e2d942 | 0.378 | 0.424 | 1.12 |
| 5f512a3017 | 0.289 | 0.391 | 1.35 |
| a8cd680648 (rejected) | 1.520 | 2.243 | 1.48 |
| f7d6bf277e (rejected) | 1.156 | 2.042 | 1.77 |

**Rejected by the laptop's selection, measured here: 4** - faster here than the front's median: 1 (0ad4447114); than its fastest: 1 (0ad4447114).

Copied there: 8.9 MB in 0m 02s (3404 KB/s); mkdir 553 ms, start 3754774 ms; the connection 292 ms at the chain's start.
The host's load while the check ran: the 1-minute load average 5.72 on average, 7.79 at most, over 125 samples 30 s apart, on 4 CPUs; at its start 6.51, the busiest then: ps 166%, cc1 70.6%, cc1 68.4%.

